# System Architecture & Configuration Reference

Deep dive into system design, configuration options, and API reference.

---

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    TRADE PANEL BOT                       │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐          ┌──────────────────┐
│  MetaTrader 5    │◄────────►│  MT5 Bridge      │
│   (Broker)       │          │ (Connector)      │
└──────────────────┘          └──────────────────┘
                                     ▲
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼───────┐  ┌────▼────────┐  ┌───▼──────────┐
            │  Paper Engine │  │Risk Manager │  │ Strategies   │
            │(signal detect)│  │ (validates) │  │ (23+)        │
            └───────┬───────┘  └────┬────────┘  └───┬──────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │       PostgreSQL Database       │
                    │(trades, signals, metrics)       │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                │                │
            ┌───────▼────────┐  ┌────▼────────┐  ┌──▼──────────┐
            │  FastAPI       │  │  Telegram   │  │  Scheduler  │
            │  Dashboard     │  │  Bot        │  │  (APSched)  │
            │  (http:5000)   │  │ (Alerts)    │  │  (Jobs)     │
            └────────────────┘  └─────────────┘  └─────────────┘
```

---

## Directory Structure

```
TradePanel/
├── trade.bat                    # Unified Management CLI (Entry Point)
├── docs/                        # Consolidated Documentation
│   ├── ARCHITECTURE.md          # This file
│   ├── STRATEGIES.md            # Strategy catalog
│   ├── GETTING_STARTED.md       # Installation guide
│   └── extras/                  # PDF/Docx/Cheat Sheets
├── scripts/                     # Operational scripts (.bat, .py, .ps1)
├── config/                      # YAML configurations
├── data/                        # DB clients & ingestion
├── mt5_bridge/                  # MT5 integration
├── strategies/                  # 23+ strategy files
├── backtesting/                 # Backtest & WFO engines
├── forward_test/                # Paper/Live engines
├── webapp/                      # Dashboard & API
├── scheduler/                   # APScheduler jobs
├── risk/                        # Risk & Regime managers
├── logs/                        # Runtime log files
├── archive/                     # Historical/Obsolete files
└── main.py                      # Core entry point
```

---

## Configuration Reference

### config/config.yaml

**System Settings**
```yaml
system:
  mode: paper              # paper | live
  log_level: INFO          # DEBUG | INFO | WARNING | ERROR
  heartbeat_interval: 60   # seconds between health checks
```

**Trading Pairs**
```yaml
pairs:
  XAUUSD:
    enabled: true
    spread_pips: 5.0       # Typical spread
    slippage_pips: 2.0     # Order slippage assumption
    commission_per_lot: 7.0
    min_lot: 0.01
    max_lot: 1.0
    pip_value_per_lot: 10.0
```

**Risk Management**
```yaml
risk_management:
  risk_per_trade_pct: 2.0        # % of account per trade
  max_lot_size: 1.0              # Hard ceiling
  max_concurrent_positions: 5    # Max open trades
  max_spread_pips: 5.0           # Skip if wider
  max_drawdown_warning_pct: 12.0 # Telegram alert
  max_drawdown_hard_pct: 15.0    # Auto-pause
  strategy_correlation_threshold: 0.7
  use_macro_regime_filter: false # Currently disabled
  use_multi_tf_confirmation: false # Currently disabled
  signal_validity_bars: 2        # Bars signal stays active
  trading_hours:
    start: "00:30"
    end: "23:59"
    days: [0, 1, 2, 3, 4]        # Mon-Fri
  crypto_trading_hours:
    start: "00:10"
    end: "23:59"
    days: [0, 1, 2, 3, 4, 5, 6]  # 24/7
    pairs: [BTCUSD, ETHUSD]
```

**Backtesting**
```yaml
backtesting:
  slippage_model: per_pair
  data_split:
    in_sample_pct: 0.70
    out_of_sample_pct: 0.20
    forward_test_pct: 0.10
```

**Notifications**
```yaml
notifications:
  telegram_enabled: true
  min_alert_interval: 300  # seconds between alerts
  daily_summary_time: "18:00"
```

**Scheduler**
```yaml
scheduler:
  heartbeat_interval_sec: 60
  signal_check_interval_sec: 900  # 15 minutes
  pnl_rollup_interval_sec: 3600   # 1 hour
```

---

### config/strategies.yaml

**Strategy Definition**
```yaml
dual_ema_fractal:
  name: "Dual EMA Fractal Breaker"
  category: Trend Following
  status: implemented
  regime: [TRENDING]
  enabled: true
  tier: TIER_3
  pairs: [EURUSD]
  timeframes: [H1]
  parameters:
    ema_period: 200
    tp_atr_mult: 2.0
    sl_atr_mult: 1.5
    atr_period: 14
  pair_overrides:
    XAUUSD:
      ema_period: 180      # Custom for gold
      tp_atr_mult: 2.5
  mode: trade              # trade | monitor_only
```

**Active Strategies List**
```yaml
active:
  - dual_ema_fractal       # Loaded first
  - rsi_bounce
  - bb_mean_reversion
  - triple_macd_scalping
  - stat_arb_gold_silver
  # ... more as needed
```

---

## Trade Execution Flow

### 1. Signal Detection (Every 1 minute)

**Code**: `forward_test/paper_engine.py::_run_loop(mode='detect')`

```python
# For each active strategy & pair/timeframe:
signal = strategy.generate_signals(data)  # Returns 1, -1, or 0
if signal != 0:
    log_signal_to_db(strategy, pair, signal)  # Store in database
```

**Return**: Signals logged, NO trades placed

---

### 2. Trade Execution (Every 5 minutes)

**Code**: `forward_test/paper_engine.py::_process_symbol()`

**Step 1**: Check for existing positions
```python
positions = mt5.positions_get(symbol=symbol)
if positions:
    # Check for reversal signals → close position
```

**Step 2**: Get signal & validate
```python
signal, signal_time, is_stale = signal_checker.get_signal(...)
if is_stale:
    connector.connect(force=True)  # Reconnect if stale
```

**Step 3**: Deduplication
```python
if signal_key already processed:
    return  # Skip duplicate signals
```

**Step 4**: Market regime filter (DISABLED)
```python
if use_regime_filter and "XAU" in symbol:
    bias = regime_classifier.get_pair_bias(symbol)
    if bias == 0:  # NEUTRAL
        return  # Trade skipped
```

**Step 5**: Multi-TF confirmation (DISABLED)
```python
if use_confirm_tf and confirm_tf:
    trend = _get_confirmation_trend(symbol, confirm_tf)
    if signal != trend_direction:
        return  # Trade skipped
```

**Step 6**: Risk checks
```python
passed, reason = risk_manager.check_all(strategy, pair, lot, direction)
if not passed:
    return f"RISK BLOCKED: {reason}"
```

**Step 7**: Calculate SL/TP
```python
df = signal_checker.get_latest_data(symbol, mt5_tf, count=50)
atr = ta.atr(df['high'], df['low'], df['close'], length=14)
sl_points = (atr * sl_mult) / symbol_info.point
tp_points = (atr * tp_mult) / symbol_info.point
```

**Step 8**: Execute trade
```python
res = order_manager.open_position(
    symbol, direction, lot_size,
    sl_points=sl_points, tp_points=tp_points,
    comment=f"PAPER_{strategy_name}",
    magic=magic_number
)
```

**Step 9**: Log trade
```python
_log_trade_open(strategy_name, symbol, direction, lot, res)
```

---

## Risk Management Checks

**All Checked in `risk/manager.py::check_all()`**

```python
1. Strategy is active & not paused
2. Market regime suitable for strategy
3. Lot size ≤ max_lot_size
4. Total positions < max_concurrent_positions
5. Free margin available (150% buffer)
6. Current spread ≤ max_spread_pips
7. Within trading hours for asset
8. No high correlation with existing positions
```

If ANY check fails:
```
RISK BLOCKED: [Specific reason]
```

---

## API Reference

### REST Endpoints

**Get Account Info**
```
GET /api/account
Response: {
  "balance": 2947.14,
  "equity": 2947.14,
  "margin_used": 0,
  "margin_free": 2947.14
}
```

**Get Open Positions**
```
GET /api/positions
Response: [
  {
    "ticket": 123456789,
    "symbol": "EURUSD",
    "type": "BUY",
    "volume": 0.1,
    "entry_price": 1.0850,
    "current_price": 1.0865,
    "sl": 1.0800,
    "tp": 1.0950
  }
]
```

**Get Trade History**
```
GET /api/trades?limit=50&offset=0
Response: [
  {
    "trade_id": "uuid",
    "strategy": "dual_ema_fractal",
    "pair": "EURUSD",
    "direction": "BUY",
    "entry_price": 1.0850,
    "exit_price": 1.0920,
    "pnl": 70.00,
    "entry_time": "2026-04-24T10:30:00Z",
    "exit_time": "2026-04-24T11:45:00Z"
  }
]
```

**Get Strategy Performance**
```
GET /api/strategies/performance?since=2026-04-01
Response: {
  "dual_ema_fractal": {
    "trades": 12,
    "win_rate": 0.5833,
    "sharpe": 1.25,
    "max_drawdown": 0.08,
    "pnl": 1250.00
  }
}
```

---

## Database Schema

**trades**
```sql
CREATE TABLE trades (
  trade_id UUID PRIMARY KEY,
  strategy_id INT REFERENCES strategies(id),
  mode VARCHAR(10),        -- PAPER, LIVE
  pair VARCHAR(20),        -- EURUSD
  direction VARCHAR(10),   -- BUY, SELL
  lot_size DECIMAL,
  entry_price DECIMAL,
  entry_time TIMESTAMP,
  exit_price DECIMAL,
  exit_time TIMESTAMP,
  pnl DECIMAL,
  status VARCHAR(20),      -- OPEN, CLOSED
  mt5_ticket BIGINT
);
```

**signals**
```sql
CREATE TABLE signals (
  signal_id SERIAL PRIMARY KEY,
  strategy_id INT REFERENCES strategies(id),
  pair VARCHAR(20),
  timeframe VARCHAR(10),   -- H1, M5, etc
  signal INT,              -- 1, -1, 0
  signal_time TIMESTAMP,
  strength DECIMAL
);
```

**strategies**
```sql
CREATE TABLE strategies (
  strategy_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  category VARCHAR(50),
  tier VARCHAR(20),
  enabled BOOLEAN,
  mode VARCHAR(20)         -- trade, monitor_only
);
```

---

## Execution Modes

### Paper Trading
```bash
python main.py paper-trade
```

- Simulates trades without risking money
- Uses real price data
- Logs all execution to database
- Good for testing & learning

### Live Trading
```bash
python main.py live-trade
```

⚠️ **Only after**:
- Testing paper mode for 1+ weeks
- Verifying all risk controls work
- Confirming performance in your market

### Backtest
```bash
python -m scripts.run_backtest \
  --strategy dual_ema_fractal \
  --pair EURUSD \
  --timeframe H1 \
  --start 2024-01-01 \
  --end 2025-12-31
```

---

## Scheduler Jobs

**All Registered in `scheduler/jobs.py`**

| Job | Interval | What It Does |
|-----|----------|-------------|
| Heartbeat | 60s | Health check, log status |
| MT5 Check | 60s | Verify connection |
| Signal Detect | 1m | Generate signals (logs only) |
| Trade Execute | 5m | Execute trades if signal |
| Position Sync | 5m | Sync DB with actual positions |
| PnL Rollup | 1h | Calculate hourly P&L |
| Regime Detect | 1h | Update macro regime |
| Daily Data | 00:05 | Ingest new market data |
| Daily Summary | 18:00 | Send daily report |
| Weekly Report | Mon 08:00 | Send weekly metrics |

---

## Performance Metrics

**Calculated in `backtesting/metrics.py`**

- **Win Rate**: # Winning Trades / Total Trades
- **Sharpe Ratio**: (Return - Risk-Free Rate) / Volatility
- **Max Drawdown**: (Trough - Peak) / Peak
- **Profit Factor**: Gross Profit / Gross Loss
- **Average Trade**: Total PnL / # Trades
- **Trade Duration**: Avg time in trade

---

## Key Files to Modify

| Need | Edit This |
|------|-----------|
| Add strategy | `config/strategies.yaml` |
| Enable strategy | `config/config.yaml` |
| Change risk | `config/config.yaml` (risk_management) |
| Change pairs | `config/config.yaml` (pairs) |
| Trading hours | `config/config.yaml` (trading_hours) |
| Telegram alerts | `config/config.yaml` (notifications) |

---

## Environment Variables (Optional)

```bash
export MT5_LOGIN=12345
export MT5_PASSWORD=your_password
export MT5_SERVER=BrokerName
export TELEGRAM_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_id
export DATABASE_URL=postgresql://user:pass@localhost/db
```

---

## Monitoring & Logging

**Log Locations**:
```
logs/
├── paper_engine.log        # Trade execution
├── api.log                 # Dashboard API
├── scheduler.log           # Scheduled jobs
├── strategies.log          # Strategy errors
└── mt5_connector.log       # MT5 connection
```

**Real-time Monitoring**:
```bash
# Paper engine trades
tail -f logs/paper_engine.log | grep "EXECUTING\|Trade opened"

# All activity
tail -f logs/*.log

# Errors only
grep -i error logs/*.log
```

---

## Troubleshooting Architecture

**Data Flow Debugging**:
```
1. Check if signal is generated
   → Look for [Strategy name] in logs
2. Check if risk checks pass
   → Look for RISK BLOCKED messages
3. Check if trade executes
   → Look for EXECUTING and Trade opened
4. Check if position shows up
   → Verify mt5.positions_get() returns position
```

---

---

## End-to-End Workflow

### Phase 1: Research & Optimization (WFO)
The **Walk-Forward Optimizer** is the "Scientific Core" of the platform. Instead of simple backtesting, it uses a rolling window approach:
1. **In-Sample (IS):** Grid search finds the best parameters for a 3-month window.
2. **Out-of-Sample (OOS):** These parameters are tested on the *following* month of data (which the optimizer has never seen).
3. **Pass/Fail:** A strategy only moves to production if it passes **70%+** of its OOS windows with a positive Sharpe Ratio.

### Phase 2: Market Intelligence (Regime Detection)
The system does not trade blindly. The `RegimeDetector` classifies every instrument every hour:
- **Trending:** High ADX, EMA alignment. (Targeted by Trend strategies).
- **Ranging:** Low ADX, Bollinger Band containment. (Targeted by Mean-Reversion).
- **Volatile:** ATR expansion. (Used for risk-off signals).

### Phase 3: The "Decision Gate" (Risk Management)
When a strategy generates a signal, it must pass a "Gauntlet" of checks:
1. **Regime Match:** Ensure the strategy category matches the current market state.
2. **Meta-Labeling:** Secondary momentum/volume validation (RSI > 55 for longs, 1.2x Vol).
3. **Correlation Check:** Ensure the portfolio isn't over-exposed to a single currency (e.g., USD).
4. **Account Safety:** Margin check + Max Concurrent positions check.

### Phase 4: Execution & Monitoring
Trades are executed as **Limit or Market Orders** with ATR-based Stop Losses. The system then enters a persistent monitoring loop:
- **Telegram:** Instant alerts for Entry, Partial TP, Break-Even (BE) adjustments, and Exit.
- **Dashboard:** Real-time equity curve and performance metrics (Sharpe, Profit Factor, Recovery Factor).

---

## Design Philosophy
- **Glassmorphism:** The UI and notifications follow a premium, translucent design language for high visual impact.
- **Fail-Safe Operation:** Decoupled heartbeat systems ensure that if the MT5 terminal crashes, the Telegram bot immediately alerts the operator.
- **Data Integrity:** No "look-ahead bias." All backtests and WFO runs strictly execute on the `bar[i+1]` Open after a signal fires on the `bar[i]` Close.

---

## Maintenance Schedule (Automated)
| Time (UTC) | Task | Purpose |
|------------|------|---------|
| 00:05 | Daily Data Sync | Update DB with yesterday's close |
| 02:00 | Overnight WFO | Re-optimize parameters for the new day |
| 06:00 | Strategy Tiering | Promote/Demote strategies based on WFO |
| 08:00 | Heartbeat | System health status report to Telegram |

---

**For more help, see TROUBLESHOOTING.md or STRATEGIES.md**

