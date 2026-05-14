# Apache Kafka Integration Plan
## Near-Real-Time Live Stream Data for Paper Trading

**Document:** `docs/guides/KAFKA_INTEGRATION_PLAN.md`  
**Created:** 2026-05-12  
**Phase:** 3B-1 (Infrastructure Hardening)  
**Status:** Design — not yet implemented

---

## Why Kafka?

### The Problem with the Current Architecture

Right now, TradePanel's data flow is entirely poll-based:

```
MT5 Terminal
    ↓  (every 60 seconds — scheduler heartbeat)
data/ingestion.py → pull_latest_bars()
    ↓
PostgreSQL (market_data table)
    ↓  (strategy loop reads DB on each cycle)
forward_test/paper_engine.py → signal_checker.py
    ↓
orders → MT5
```

**The consequences:**
- A signal that triggers at bar open could take up to 60 seconds to be detected
- During high-volatility events (NFP, FOMC, gold spikes), a 60-second delay means the entry price has already moved
- All data consumers (paper engine, dashboard, analytics) independently query the same DB table, creating redundant load
- There is no publish/subscribe — if you add a new consumer (e.g., Prometheus exporter), it has to poll the DB again

### What Kafka Gives You

Kafka is a distributed message broker. Instead of each component polling PostgreSQL for new data, MT5 publishes every new tick and closed candle to a Kafka topic. All consumers (signal checker, DB sync, dashboard, analytics) subscribe and react the moment data arrives.

```
MT5 Terminal
    ↓  (tick by tick — every price update)
kafka/producer.py  →  Kafka Topic: tradepanel.ticks
                   →  Kafka Topic: tradepanel.ohlcv.M1 (closed candles)
                   →  Kafka Topic: tradepanel.ohlcv.H1
                   →  Kafka Topic: tradepanel.ohlcv.H4
                   ...
    ↓  (consumers react within milliseconds)
    ├── kafka/signal_consumer.py   → strategy signals → orders
    ├── kafka/db_sink.py           → PostgreSQL (replaces ingestion.py in live mode)
    ├── kafka/analytics_consumer.py → real-time P&L, Sharpe rolling calculation
    └── kafka/dashboard_consumer.py → WebSocket push to React frontend
```

**Latency improvement:** 60 seconds → under 5 seconds for M1 candle close detection. For tick-level strategies, under 100ms.

---

## Where Kafka Fits in the Current Stack

Here is the precise insertion point in each module:

### 1. MT5 Bridge (`mt5_bridge/`) — Where Data Is Born

**Current:** `data_feed.py::pull_latest_bars()` is called by the scheduler on a timer.  
**With Kafka:** Add `mt5_bridge/tick_producer.py` that subscribes to the MT5 tick stream and publishes to Kafka continuously.

```
mt5_bridge/
  connector.py         ← no change
  order_manager.py     ← no change
  data_feed.py         ← keep for backfill/historical ingest only
  tick_producer.py     ← NEW: continuous tick publisher to Kafka
```

The tick producer runs in its own thread alongside the existing connector. It calls `mt5.copy_ticks_from()` in a tight loop (or uses MT5's callback if available) and publishes every new tick to `tradepanel.ticks`.

### 2. Data Pipeline (`data/`) — Where Candles Are Built

**Current:** `ingestion.py` pulls bars from MT5 on demand.  
**With Kafka:** Add `kafka/aggregator.py` that consumes `tradepanel.ticks` and builds OHLCV candles, publishing completed bars to `tradepanel.ohlcv.<TF>` topics.

This is the OHLCV aggregation layer — it converts a stream of raw ticks into the M1, M5, M15, H1, H4 candles that strategies need.

```
kafka/
  producer.py          ← wraps kafka-python producer, reused by all publishers
  aggregator.py        ← NEW: tick → OHLCV candle builder, publishes per-TF topics
  signal_consumer.py   ← NEW: subscribes to OHLCV topics, triggers strategy eval
  db_sink.py           ← NEW: subscribes to OHLCV topics, writes to PostgreSQL
  analytics_consumer.py ← NEW: real-time metrics (rolling Sharpe, daily P&L)
  dashboard_consumer.py ← NEW: pushes updates to React frontend via WebSocket
```

### 3. Forward Test Engine (`forward_test/`) — Where Signals Fire

**Current:** `paper_engine.py` loops every 60 seconds, calls `signal_checker.py`, which reads from PostgreSQL.  
**With Kafka:** `kafka/signal_consumer.py` replaces the scheduler-driven loop. When a new candle arrives on `tradepanel.ohlcv.H1` (for example), it immediately calls the signal checker. This is event-driven rather than time-driven.

`signal_checker.py` itself does not need to change — it still reads from PostgreSQL (which is now kept current by `db_sink.py`). The change is *what triggers* the signal check — Kafka message arrival instead of a 60-second timer.

### 4. Dashboard (`webapp/`) — Where Results Are Displayed

**Current:** React frontend polls the FastAPI backend on a timer for updated data.  
**With Kafka:** `dashboard_consumer.py` pushes updates via WebSocket the moment a new candle or trade is recorded. The frontend switches from polling to `useWebSocket()` for live updates.

---

## Topic Design

| Topic | Key | Value | Retention | Purpose |
|-------|-----|-------|-----------|---------|
| `tradepanel.ticks` | `{symbol}` | tick JSON | 1 hour | Raw price stream from MT5 |
| `tradepanel.ohlcv.M1` | `{symbol}` | OHLCV JSON | 24 hours | Completed M1 candles |
| `tradepanel.ohlcv.M5` | `{symbol}` | OHLCV JSON | 24 hours | Completed M5 candles |
| `tradepanel.ohlcv.M15` | `{symbol}` | OHLCV JSON | 48 hours | Completed M15 candles |
| `tradepanel.ohlcv.H1` | `{symbol}` | OHLCV JSON | 7 days | Completed H1 candles |
| `tradepanel.ohlcv.H4` | `{symbol}` | OHLCV JSON | 7 days | Completed H4 candles |
| `tradepanel.ohlcv.D1` | `{symbol}` | OHLCV JSON | 30 days | Completed D1 candles |
| `tradepanel.signals` | `{strategy}_{symbol}_{tf}` | signal JSON | 7 days | Generated trade signals |
| `tradepanel.orders` | `{order_id}` | order JSON | 30 days | Placed / closed orders |
| `tradepanel.metrics` | `{strategy}_{symbol}` | metrics JSON | 30 days | Rolling P&L, Sharpe, DD |

---

## OHLCV Message Schema

```json
{
  "symbol": "XAUUSD",
  "timeframe": "H1",
  "timestamp": "2026-05-12T10:00:00Z",
  "open": 3218.45,
  "high": 3224.10,
  "low": 3215.30,
  "close": 3221.80,
  "volume": 1847,
  "spread": 3,
  "is_closed": true
}
```

`is_closed: true` means the candle is complete and can be used for signal generation. `is_closed: false` means it is the current forming candle (useful for dashboard display only — strategies should wait for `is_closed: true`).

---

## Signal Message Schema

```json
{
  "strategy": "stat_arb_gold_silver",
  "symbol": "XAUUSD",
  "timeframe": "H1",
  "direction": 1,
  "confidence": 0.82,
  "bar_time": "2026-05-12T10:00:00Z",
  "generated_at": "2026-05-12T10:00:02.341Z",
  "latency_ms": 2341
}
```

---

## Implementation Plan (4 Sprints)

### Sprint 1 — Kafka Infrastructure (1–2 days)

**Goal:** Get Kafka running locally alongside the existing Docker stack.

1. Add Kafka + Zookeeper to `docker/docker-compose.yml`:
```yaml
zookeeper:
  image: confluentinc/cp-zookeeper:7.6.0
  environment:
    ZOOKEEPER_CLIENT_PORT: 2181

kafka:
  image: confluentinc/cp-kafka:7.6.0
  depends_on: [zookeeper]
  ports:
    - "9092:9092"
  environment:
    KAFKA_BROKER_ID: 1
    KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

kafdrop:  # Web UI for topic inspection
  image: obsidiandynamics/kafdrop:latest
  ports:
    - "9000:9000"
  environment:
    KAFKA_BROKERCONNECT: kafka:29092
```

2. Install `kafka-python` in requirements:
```
kafka-python==2.0.2
```

3. Create `kafka/producer.py` — shared producer wrapper with retry logic and serialisation.

4. Create topic admin script `scripts/setup_kafka_topics.py` to pre-create all topics with correct retention policies.

**Test:** Kafdrop UI at `http://localhost:9000` shows topics and messages flowing.

---

### Sprint 2 — MT5 Tick Producer + OHLCV Aggregator (2–3 days)

**Goal:** MT5 ticks flowing through Kafka into per-timeframe OHLCV topics.

1. Create `mt5_bridge/tick_producer.py`:
```python
class MT5TickProducer:
    """
    Continuously polls MT5 for new ticks and publishes to Kafka.
    Runs in a background thread alongside the paper engine.
    """
    def __init__(self, symbols, kafka_bootstrap="localhost:9092"):
        self.symbols = symbols
        self.producer = KafkaProducer(bootstrap_servers=kafka_bootstrap, ...)
        self._last_tick = {}  # {symbol: last_tick_time}

    def start(self):
        """Start the tick polling loop in a daemon thread."""
        thread = threading.Thread(target=self._poll_loop, daemon=True)
        thread.start()

    def _poll_loop(self):
        while True:
            for symbol in self.symbols:
                ticks = mt5.copy_ticks_from(symbol, self._last_tick.get(symbol, ...), 1000, mt5.COPY_TICKS_ALL)
                if ticks is not None and len(ticks) > 0:
                    for tick in ticks:
                        self.producer.send("tradepanel.ticks", key=symbol, value=tick)
                    self._last_tick[symbol] = ticks[-1]['time']
            time.sleep(0.1)  # 100ms polling — much faster than 60s scheduler
```

2. Create `kafka/aggregator.py` — consumes `tradepanel.ticks`, maintains per-symbol OHLCV state machines, publishes closed candles to `tradepanel.ohlcv.<TF>` topics.

**Test:** With MT5 connected, verify that `tradepanel.ohlcv.M1` in Kafdrop shows new messages every ~60 seconds (one per closed M1 bar).

---

### Sprint 3 — Signal Consumer + DB Sink (2 days)

**Goal:** Strategy signals fire within seconds of a candle closing, not 60 seconds later.

1. Create `kafka/signal_consumer.py`:
```python
class SignalConsumer:
    """
    Subscribes to OHLCV topics. When a candle closes, immediately
    evaluates all strategies registered for that symbol/TF.
    Replaces the 60-second scheduler loop in paper_engine.py for live mode.
    """
    def __init__(self, paper_engine, kafka_bootstrap="localhost:9092"):
        self.paper_engine = paper_engine
        self.consumer = KafkaConsumer(
            "tradepanel.ohlcv.M1",
            "tradepanel.ohlcv.M15",
            "tradepanel.ohlcv.H1",
            "tradepanel.ohlcv.H4",
            bootstrap_servers=kafka_bootstrap,
            group_id="signal-consumer",
            auto_offset_reset="latest"
        )

    def start(self):
        for message in self.consumer:
            candle = json.loads(message.value)
            if candle["is_closed"]:
                self.paper_engine.evaluate_signal(
                    symbol=candle["symbol"],
                    timeframe=candle["timeframe"],
                    bar_time=candle["timestamp"]
                )
```

2. Create `kafka/db_sink.py` — consumes OHLCV topics and writes to PostgreSQL using the existing `DBClient.insert_market_data()`. This keeps the DB current in real-time, so the existing `signal_checker.py` (which reads from DB) continues to work without change.

**Integration point in `forward_test/paper_engine.py`:**
```python
# Add to __init__:
if self.config.get("kafka", {}).get("enabled", False):
    from kafka.signal_consumer import SignalConsumer
    self.kafka_consumer = SignalConsumer(self, kafka_bootstrap=...)
    self.kafka_consumer.start()
    # The old 60-second loop becomes a fallback health check only
```

**Test:** After a M1 candle closes in MT5, a signal evaluation log entry appears in the paper engine within 3 seconds.

---

### Sprint 4 — Analytics Consumer + Dashboard WebSocket (1–2 days)

**Goal:** Real-time dashboard without polling.

1. Create `kafka/analytics_consumer.py` — subscribes to `tradepanel.orders` and `tradepanel.ohlcv.D1`, publishes rolling Sharpe, daily P&L, and drawdown to `tradepanel.metrics`.

2. Update `webapp/api/` to expose a WebSocket endpoint:
```python
# webapp/api/ws.py
@app.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    await websocket.accept()
    consumer = KafkaConsumer("tradepanel.metrics", ...)
    for message in consumer:
        await websocket.send_json(json.loads(message.value))
```

3. Update React frontend to use WebSocket instead of polling:
```jsx
// App.jsx — replace setInterval polling with:
const { lastMessage } = useWebSocket("ws://localhost:8000/ws/metrics");
```

**Test:** Open dashboard, verify equity curve updates within 5 seconds of a simulated trade.

---

## Configuration

Add a `kafka` block to `config/config.yaml`:

```yaml
kafka:
  enabled: false          # Set true to activate streaming mode
  bootstrap_servers: "localhost:9092"
  tick_poll_interval_ms: 100   # How often to poll MT5 for new ticks
  consumer_group: "tradepanel"
  topics:
    ticks: "tradepanel.ticks"
    ohlcv_prefix: "tradepanel.ohlcv"
    signals: "tradepanel.signals"
    orders: "tradepanel.orders"
    metrics: "tradepanel.metrics"
```

The `enabled: false` default means the existing scheduler-based system continues to work unchanged. Setting `enabled: true` activates Kafka streaming mode. This allows a clean rollback if issues arise.

---

## What Does NOT Change

This is important. The Kafka layer is additive, not a rewrite:

- `strategies/*.py` — no changes. Strategies still receive a DataFrame and return a signal.
- `backtesting/engine.py` — no changes. Backtesting remains offline/historical.
- `risk/manager.py` — no changes. Risk checks still happen before order placement.
- `mt5_bridge/order_manager.py` — no changes. Orders still go through the same validation.
- `data/db_client.py` — no changes. DB writes are still done via DBClient.
- `config/strategies.yaml` — no changes. Strategy parameters are unaffected.

The Kafka layer sits between MT5 data arrival and paper engine evaluation. Everything downstream of the signal check is identical.

---

## Effort Estimate

| Sprint | Work | Estimated Time |
|--------|------|----------------|
| 1 | Kafka + Docker setup, topic creation | 1–2 days |
| 2 | Tick producer + OHLCV aggregator | 2–3 days |
| 3 | Signal consumer + DB sink | 2 days |
| 4 | Analytics consumer + WebSocket dashboard | 1–2 days |
| **Total** | | **6–9 days** |

This assumes Python + Kafka familiarity. The kafka-python library is straightforward, and the existing code is clean enough that integration points are well-defined.

---

## Prerequisite Before Starting

1. Confirm Docker has enough memory allocated (Kafka + Zookeeper need ~1.5GB combined)
2. Confirm MT5 terminal is running persistently (tick producer needs constant MT5 connection)
3. Consider running Kafka on WSL2 for better performance on Windows (or keep it in Docker — either works)
4. The existing overnight backtest pipeline does NOT use Kafka — it runs independently against historical DB data. No changes needed there.

---

## Decision: When to Start This

Kafka integration is not required for the current paper trading phase. The 60-second latency is acceptable for H1 and H4 strategies. Recommend starting Sprint 1 (Docker setup) in Week 2 of the current sprint plan, so it is ready when paper testing validates the strategy set. For M1/M5 scalping strategies (once those are tuned), Kafka becomes essential.

**Start Kafka work after:** ESCALATE strategies are disabled and Phase 3A strategy quality sprint is complete.

---

*See also: `docs/core/MASTER_PROJECT_STATUS.md` Phase 3B-1 | `docs/v3/ORCHESTRATION_V3.md`*
