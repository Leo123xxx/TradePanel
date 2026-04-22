# MT5 Algorithmic Trading Platform — Phase 1 Execution Plan
> Based on: `MT5_Trading_Platform_Master_Plan.docx` v1.0 | April 2026  
> Status: **In Progress — Step 12B ✅ Done | Next: Step 14 (Regime Detector)** | Last updated: 2026-04-18

---

## Before Writing Any Code — Prerequisites Checklist

These must be resolved **before Step 01** begins. They are the Known Gaps from Section 18 of the master plan.

| # | Item | Action Required | Done? |
|---|------|----------------|-------|
| P1 | **Git repository** | Create a private GitHub repo (or local Git repo). Add `.gitignore` that excludes `.env` and any secrets. | ✅ |
| P2 | **MT5 broker account** | Sign up for an MT5 broker demo account. Note your account number, password, and server name (e.g. `BrokerName-Demo`). | ✅ |
| P3 | **MT5 terminal installed** | Install MetaTrader 5 on your Windows PC. Log into your demo account. Leave the terminal running. | ✅ |
| P4 | **PostgreSQL installed** | Install PostgreSQL locally. Create a database named `trading_platform`. Note your DB username and password. | ✅ |
| P5 | **Telegram bot created** | Message `@BotFather` → `/newbot` → follow prompts → save the **Bot Token**. Then message your new bot and retrieve your **Chat ID** via the Telegram API. | ✅ |
| P6 | **Python 3.11+ installed** | Confirm `python --version` returns 3.11 or higher. Install if needed. | ✅ |
| P7 | **Confirm M1 data depth** | After connecting to MT5, check how many years of M1 history your broker provides for EURUSD. Target: 5–10 years. | ✅ |

---

## Phase 1 Build — 20 Steps

Each step has a **goal**, **files to create**, **how to verify it's done**, and **what to tell Claude** when you're ready to implement it.

---

### STEP 01 — Project Setup
**Goal:** Create the full folder structure, config template, `.env` file, and `requirements.txt`.

**Files to create:**
```
trading_platform/
├── config/config.yaml (template — no real secrets)
├── config/strategies.yaml (empty for now)
├── requirements.txt
├── .env (real secrets — never committed)
├── .gitignore
└── README.md (stub)
```

**requirements.txt contents:**
```
MetaTrader5
vectorbt
backtrader
psycopg2-binary
pandas
numpy
pandas-ta
apscheduler
python-telegram-bot>=20.0
pyyaml
python-dotenv
pytest
fastapi
uvicorn
```

**Verify:** Run `pip install -r requirements.txt` with no errors.

**Tell Claude:** *"Let's implement Step 01 — create the full folder structure, requirements.txt, config.yaml template, .env file, and .gitignore for the MT5 trading platform."*

---

### STEP 02 — Database Schema
**Goal:** Create all 10 PostgreSQL tables via a `setup_db.py` script.

**Tables to create:** `strategies`, `backtest_runs`, `signals`, `trades`, `positions`, `bot_health`, `daily_summary`, `commands`, `market_data`, `regime_log`

**Files to create:**
```
scripts/setup_db.py
data/db_client.py
```

**Verify:** Run `python scripts/setup_db.py` → connect to PostgreSQL → confirm all 10 tables exist with `\dt`.

**Tell Claude:** *"Let's implement Step 02 — write setup_db.py to create all 10 database tables from the schema in the master plan, and write db_client.py with PostgreSQL connection helpers."*

---

### STEP 03 — MT5 Bridge: Connection
**Goal:** Connect to the running MT5 terminal and confirm the connection works.

**Files to create:**
```
mt5_bridge/connector.py
tests/test_mt5_bridge.py
```

**Verify:** Run the connector script → it logs in → prints account info → disconnects cleanly. Unit test passes.

**Tell Claude:** *"Let's implement Step 03 — write connector.py to log into MT5 using credentials from the .env file, test the connection, and write a unit test for it."*

---

### STEP 04 — MT5 Bridge: Data Feed
**Goal:** Pull historical OHLCV for EURUSD M1 from MT5 and store it in the `market_data` table.

**Files to create:**
```
mt5_bridge/data_feed.py
mt5_bridge/account.py
```

**Verify:** After running, query `SELECT COUNT(*) FROM market_data WHERE pair = 'EURUSD' AND timeframe = 'M1'` — should return thousands of rows.

**Tell Claude:** *"Let's implement Step 04 — write data_feed.py to pull historical EURUSD M1 OHLCV data from MT5 and store it in the market_data PostgreSQL table. Also write account.py for balance/equity queries."*

---

### STEP 05 — Data Resampler
**Goal:** Derive M5, M15, H1, H4, D1 bars from the M1 data already in the database.

**Files to create:**
```
data/resampler.py
data/cleaner.py
data/ingestion.py
```

**Verify:** After running, query `market_data` for timeframe = 'H1' — should contain valid OHLCV bars derived from M1.

**Tell Claude:** *"Let's implement Step 05 — write resampler.py to aggregate M1 data in the market_data table into M5, M15, H1, H4, and D1 timeframes. Also write cleaner.py for gap detection and data validation."*

---

### STEP 06 — Telegram: Outbound Messages
**Goal:** Send a test message from Python to your phone via the Telegram bot.

**Files to create:**
```
notifications/telegram_bot.py
notifications/templates.py
```

**Verify:** Run the script → message arrives on your phone within 5 seconds.

**Tell Claude:** *"Let's implement Step 06 — write telegram_bot.py to send outbound messages using the bot token and chat ID from .env. Also write templates.py with all message format templates from the master plan. Send a test message to confirm it works."*

---

### STEP 07 — Telegram: Inbound Commands
**Goal:** Bot responds to `/status`, `/health`, and `/help` commands sent from your phone.

**Files to create:**
```
notifications/router.py
(update telegram_bot.py with command handlers)
```

**Verify:** Send `/help` from your phone → bot replies with the full command list.

**Tell Claude:** *"Let's implement Step 07 — add inbound command handling to telegram_bot.py. Implement /status, /health, /balance, /help, and /mode commands. The bot should poll or use webhooks to receive commands."*

---

### STEP 08 — Logging & Health Monitor
**Goal:** Write heartbeat events to `bot_health` every 60 seconds. Trigger a Telegram alert if the heartbeat stops.

**Files to create:**
```
logging_/event_logger.py
logging_/health_monitor.py
```

**Verify:** Run the health monitor for 3 minutes → query `bot_health` table → should see 3 heartbeat rows. Manually kill the process → Telegram alert arrives within 10 minutes.

**Tell Claude:** *"Let's implement Step 08 — write event_logger.py to write structured events to the bot_health table, and health_monitor.py to send a heartbeat every 60 seconds and fire a Telegram alert if heartbeat is missed."*

---

### STEP 09 — Strategy Base Class
**Goal:** Define the abstract interface that all strategies must implement.

**Files to create:**
```
strategies/base_strategy.py
strategies/registry.py
tests/test_strategy_engine.py
```

**Verify:** Unit tests pass. Any attempt to instantiate a strategy without implementing all 5 required methods raises a `NotImplementedError`.

**Tell Claude:** *"Let's implement Step 09 — write base_strategy.py as an abstract base class with the 5 required methods: __init__, generate_signals, get_parameters, get_metadata, validate_params. Write registry.py to load and register strategies. Add unit tests."*

---

### STEP 10 — Strategy 1: MA Crossover
**Goal:** First real strategy — Moving Average Crossover — generating buy/sell signals on historical data.

**Files to create:**
```
strategies/ma_crossover.py
config/strategies.yaml (add MA Crossover params)
```

**Verify:** Instantiate the strategy with test data → `generate_signals()` returns a DataFrame with a `signal` column containing values of 1, -1, or 0.

**Tell Claude:** *"Let's implement Step 10 — write ma_crossover.py as a Moving Average Crossover strategy inheriting from base_strategy.py. It should use fast/slow MA parameters from strategies.yaml and generate buy/sell signals using pandas-ta. Add it to the registry."*

---

### STEP 11 — Backtesting Engine
**Goal:** Run the MA Crossover strategy against historical data bar-by-bar and output a full metrics scorecard.

**Files to create:**
```
backtesting/engine.py
backtesting/metrics.py
backtesting/report.py
scripts/run_backtest.py
tests/test_backtesting.py
```

**Key rules:** No look-ahead bias. Realistic costs (spread + slippage + swap + commission) on every trade. Output all 20+ metrics from Section 8.3 of the master plan.

**Verify:** Run `python scripts/run_backtest.py --strategy ma_crossover --pair EURUSD --timeframe H1` → scorecard prints to console and saves to `backtest_runs` table.

**Tell Claude:** *"Let's implement Step 11 — write the backtesting engine in engine.py using bar-by-bar simulation with no look-ahead bias. Apply spread, slippage (1–3 pip model), swap, and commission costs. Use metrics.py to compute all 20+ metrics from the master plan. Save results to backtest_runs table via report.py."*

---

### STEP 11B — Strategy Suite: Build All 8 Testable Strategies
**Goal:** Build and backtest all 8 strategies from `validation/strategies_structured.md` before walk-forward optimisation. This gives a meaningful comparison baseline and surfaces which strategies are worth optimising.

**Strategy status:**

| # | Name | File | Action |
|---|------|------|--------|
| 1 | MA Crossover | `ma_crossover.py` | ✅ Done + baseline backtest run |
| 2 | Range Breakout | `range_breakout.py` | Build |
| 3 | RSI Pullback (trend+reversion) | `rsi_pullback.py` | Build (replaces simple rsi_bounce) |
| 4 | BB Mean Reversion | `bb_mean_reversion.py` | Build (replaces gold_momentum_breakout) |
| 5 | Swing Pullback | `swing_pullback.py` | Build |
| 6 | News Event Breakout | — | 🔴 Deferred — needs economic calendar feed |
| 7 | Session Momentum (London/NY) | `session_momentum.py` | Build |
| 8 | Regime-Aware Filter | — | 🔴 Deferred — needs DXY/VIX/yields (Step 14) |
| 9 | Stochastic Divergence | `stoch_divergence.py` | Build |
| 10 | ML Classifier | — | 🔴 Deferred — own major build step |

**Files to create:**
```
strategies/range_breakout.py
strategies/rsi_pullback.py
strategies/bb_mean_reversion.py
strategies/swing_pullback.py
strategies/session_momentum.py
strategies/stoch_divergence.py
ta_compat.py (update — add stochastic oscillator)
```

**After building all strategies — run full backtest sweep:**
```bash
python scripts/run_backtest.py --strategy ma_crossover       --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy range_breakout     --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy rsi_pullback       --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy bb_mean_reversion  --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy swing_pullback     --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy session_momentum   --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy stoch_divergence   --pair XAUUSD --timeframe H4
```

**Verify:** All 7 backtests complete and save to `backtest_runs` table. Review scorecard for each.

**Gate to Step 12:** All strategies must run without errors. At least 3 must show Profit Factor > 1.0 in the raw baseline (before optimisation) — this confirms the strategy logic is directionally sound before walk-forward.

**Deferred strategies note:**
- **Strategy 6 (News Breakout):** Requires an economic calendar integration (CPI, NFP dates). Deferred until external data feed is available.
- **Strategy 8 (Regime-Aware):** Requires DXY, VIX, and real yields data feeds — connects naturally to Step 14 (Regime Detector).
- **Strategy 10 (ML Classifier):** Requires scikit-learn/LightGBM, feature engineering pipeline, and retraining infrastructure. Own dedicated build step after Phase 1.

**Tell Claude:** *"Let's implement Step 11B — build all 6 remaining strategies from validation/strategies_structured.md (range_breakout, rsi_pullback, bb_mean_reversion, swing_pullback, session_momentum, stoch_divergence). Then run the full backtest sweep across all 7 testable strategies on XAUUSD and produce a comparison scorecard."*

---

### STEP 12 — Walk-Forward Optimisation
**Goal:** Run **all 8 testable strategies** through rolling training/test windows to validate they aren't overfitted. Strategies that pass the OOS threshold proceed to paper trading.

**Files to create:**
```
backtesting/walk_forward.py
```

**Verify:** Run walk-forward with minimum 4 windows → results table shows per-window Sharpe and P&L → strategy passes if profitable in >70% of windows.

**Tell Claude:** *"Let's implement Step 12 — write walk_forward.py to run rolling walk-forward optimisation over the MA Crossover strategy. Use configurable training and test window sizes. Minimum 4 windows. Log all window results to backtest_runs table and print a summary."*

---

### STEP 13 — Risk Manager
**Goal:** Pre-trade check module that runs 7 checks before any order is placed.

**Files to create:**
```
risk/manager.py
```

**The 7 checks (all must pass before an order fires):**
1. Strategy is active and not paused
2. Market regime matches strategy category
3. Lot size ≤ `max_lot_size` in config
4. Total positions < `max_concurrent_positions`
5. Margin available in MT5 account
6. Current spread ≤ `max_spread_pips`
7. Within permitted trading hours

**Verify:** Unit tests cover all 7 checks — including edge cases where each check fails and blocks the order.

**Tell Claude:** *"Let's implement Step 13 — write risk/manager.py with the 7 pre-trade checks from Section 10 of the master plan. All parameters must come from config.yaml. Write comprehensive unit tests covering every failure case."*

---

### STEP 14 — Regime Detector
**Goal:** Classify market as Trending / Ranging / High Volatility / Low Volatility per pair per hour using ADX and ATR.

**Files to create:**
```
risk/regime_detector.py
```

**Verify:** Run against H1 EURUSD data → `regime_log` table populated with hourly regime classification.

**Tell Claude:** *"Let's implement Step 14 — write regime_detector.py to classify market regime per pair per hour using ADX (>25 = trending, <20 = ranging) and ATR (>1.5x 20-period avg = high vol, <0.5x = low vol) using pandas-ta. Log results to regime_log table."*

---

### STEP 15 — Paper Trading Engine (Demo MT5)
**Goal:** MA Crossover strategy running live on MT5 demo account — placing real demo trades automatically.

**Files to create:**
```
mt5_bridge/order_manager.py
forward_test/paper_engine.py
forward_test/signal_checker.py
scripts/run_paper.py
```

**Verify:** Run `python scripts/run_paper.py` → strategy checks signals every 15 minutes → when a signal fires, a trade appears in MT5 terminal and in the `trades` table with mode = 'PAPER'.

**Tell Claude:** *"Let's implement Step 15 — write paper_engine.py to run the MA Crossover strategy on MT5 demo account. Write order_manager.py to send, modify, and close orders. Write signal_checker.py to run every 15 minutes. All trades logged to the trades table with mode='PAPER'."*

---

### STEP 16 — Notification Router
**Goal:** Telegram messages firing automatically for every trade open, trade close, and drawdown event.

**Files to create:**
```
(update notifications/router.py — wire it into paper_engine.py)
```

**Verify:** Open a paper trade manually → Telegram message arrives on your phone within 30 seconds. Close the trade → close notification arrives with P&L and close reason.

**Tell Claude:** *"Let's implement Step 16 — wire the notification router into the paper trading engine so trade open, trade close, drawdown warning, and drawdown hard limit events all send Telegram messages using the templates from templates.py."*

---

### STEP 17 — Scheduler: All Jobs
**Goal:** Full automation — all 11 scheduled jobs running continuously without manual intervention.

**Files to create:**
```
scheduler/jobs.py
(update scripts/run_paper.py to start scheduler)
```

**The 11 jobs:**
| Job | Frequency |
|-----|-----------|
| Heartbeat check | Every 60s |
| MT5 connection check | Every 60s |
| Position sync | Every 5 min |
| Signal check | Every 15 min |
| P&L roll-up | Every 1 hour |
| Regime detection | Every 1 hour |
| Data ingest | Daily midnight |
| Daily summary (Telegram) | 6:00 PM daily |
| Weekly report (Telegram) | Mon 8:00 AM |
| DB cleanup / archive | Sunday midnight |
| Strategy correlation check | Monthly |

**Verify:** Start the system → let it run for 1 hour → query `bot_health` for heartbeat rows, query `regime_log` for regime rows, confirm daily summary Telegram message arrives at configured time.

**Tell Claude:** *"Let's implement Step 17 — write scheduler/jobs.py using APScheduler with all 11 jobs from Section 12 of the master plan. Integrate with paper_engine.py, health_monitor.py, regime_detector.py, and the notification router. Add graceful shutdown on SIGTERM."*

---

### STEP 18 — Deploy All Validated Strategies to Paper Trading
**Goal:** All strategies that passed walk-forward thresholds (Step 12) run live on MT5 demo alongside MA Crossover. Each strategy activates according to its regime conditions.

**Verify:** All validated strategies appear in `/strategies` Telegram command response. Each generates live signals on the demo account. Trades logged to `trades` table with correct `strategy_id`.

**Tell Claude:** *"Let's implement Step 18 — deploy all walk-forward validated strategies to the paper trading engine. Each strategy should only activate when its regime conditions are met (as defined in strategies_structured.md). Confirm all strategies appear in the /strategies Telegram response."*

---

### STEP 19 — Full System Test
**Goal:** End-to-end validation that every piece works together.

**Test checklist:**
- [x] Both strategies generating signals on demo
- [x] All trades appearing in MT5 terminal and `trades` table
- [x] `/status` command returns live positions
- [x] `/closeall` command closes all open positions
- [x] Daily summary Telegram message arrives on schedule
- [x] Drawdown simulation: manually inject a large loss → confirm Telegram warning fires → confirm hard limit pauses the strategy
- [x] Health monitor: kill MT5 terminal → confirm heartbeat lost alert fires within 10 minutes
- [x] DB cleanup job runs without errors
- [x] All pytest unit tests pass: `pytest tests/ -v`

**Tell Claude:** *"Let's run the full system test from Step 19. Walk through each checklist item, fix any failures, and confirm everything works end-to-end on the demo account."*
**Status:** `☐ Pending — requires Steps 14–18 to be complete first`

> ⚠️ **Note (Step 19 checklist above):** The checkboxes shown in the test checklist are targets, not completed items. Do not mark them done until actually tested on the live demo account.

---

### STEP 20 — Phase 1 Complete
**Goal:** README written, all tests passing, system running stably on demo.

**Deliverables:**
- `README.md` with setup instructions (how to install, configure, and run)
- All unit tests passing: `pytest tests/ -v`
- System running on demo account for a minimum of **2–4 weeks**
- Weekly reassessment report reviewed at least once

**Extended demo criteria before any live promotion:**
- [ ] Running continuously for 2–4 weeks with no critical failures
- [ ] Drawdown has not exceeded 50% of the backtest max drawdown
- [ ] Live behaviour (win rate, P&L, trade frequency) is within 30% of backtest expectations
- [ ] All Telegram notifications tested and confirmed working
- [ ] Weekly report reviewed and any anomalies addressed
**Status:** `☐ Pending — minimum 2–4 weeks of live demo run required`

---

## Strategy Promotion Thresholds (Reference)

Before any strategy moves from backtest → paper → live, it must pass **all** of these:

| Metric | Minimum |
|--------|---------|
| Sharpe Ratio (annualised) | > 1.0 |
| Profit Factor | > 1.4 |
| Max Drawdown | < 20% |
| Win Rate | > 45% |
| Minimum Trades | > 100 |
| OOS Sharpe vs IS Sharpe | Within 30% |
| Walk-Forward windows profitable | > 70% |

---

## How to Work Through This Plan With Claude

Each step is self-contained. When you're ready to implement a step:

1. Open a Cowork session
2. Copy the **"Tell Claude"** prompt for that step
3. Paste it and let Claude build it
4. Run the verification check yourself
5. Tick the step off and move to the next

If a step produces an error, paste the error into the chat and Claude will debug it before moving on.

---

## Current Status

| Step | Module | Status |
|------|--------|--------|
| P1–P7 | Prerequisites | ✅ Done |
| 01 | Project Setup | ✅ Done |
| 02 | Database Schema | ✅ Done |
| 03 | MT5 Bridge — Connection | ✅ Done |
| 04 | MT5 Bridge — Data Feed | ✅ Done (+ audit fix: date-range pull) |
| 05 | Data Resampler | ✅ Done |
| 06 | Telegram — Outbound | ✅ Done |
| 07 | Telegram — Inbound | ✅ Done |
| 08 | Logging & Health Monitor | ✅ Done |
| 09 | Strategy Base Class | ✅ Done (+ audit fix: metadata) |
| 10 | MA Crossover Strategy | ✅ Done (+ audit fix: 5 pairs, EMA/SMA, ADX) |
| 11 | Backtesting Engine | ✅ Done — 28 metrics, config costs, no look-ahead |
| 11B | Strategy Suite (7 strategies) | ✅ Done — baseline backtests complete |
| 12 | Walk-Forward Optimisation | ✅ Done — 3 strategies passed WF initially |
| 12B | Re-test Fixed Strategies | ✅ Done — 3 Tier-1, 3 Tier-2 strategies confirmed |
| 13 | Risk Manager | ✅ Done — stub exists, verify 7 checks in agent run |
| 14 | Regime Detector | ⚠️ Stub exists — pandas_ta crash fixed (2026-04-18) |
| 15 | Paper Trading Engine | ⚠️ Stub exists — old strategies replaced (2026-04-18) |
| 16 | Notification Router | ⚠️ Stub exists — format_daily_summary added (2026-04-18) |
| 17 | Scheduler — All Jobs | ⚠️ Stub exists — all 11 jobs implemented (2026-04-18) |
| 18 | Deploy Validated Strategies | ☐ Pending — requires Steps 14–17 verified |
| 19 | Full System Test | ☐ Pending — requires Step 18 complete |
| 20 | Phase 1 Complete | ☐ Pending — requires 2–4 weeks demo run |

---

---

## Checkpoint Audit — Changes Made (2026-04-17)

### Bug Fixes Applied

| File | Issue | Fix |
|------|-------|-----|
| `data/db_client.py` | Connection leak — never closed | `SimpleConnectionPool`, get/release in `finally` |
| `strategies/base_strategy.py` | `get_metadata()` missing regime/timeframes/pairs | Added all three to constructor + return |
| `mt5_bridge/data_feed.py` | `count=5000` bars = ~3.5 days only | `copy_rates_range()` from 2020-01-01 |

### New File: `data/ingestion.py`
Run this BEFORE Step 11. Pulls M1 history for all 5 pairs (2020→now), resamples to M5/M15/H1/H4/D1, runs gap checks, prints coverage summary.

```bash
python -m data.ingestion
```

### 5-Pair Configuration (config.yaml + strategies.yaml)

| Pair | Spread | Slippage | Notes |
|------|--------|----------|-------|
| XAUUSD | 4.0 pips | 2.0 | Primary. High spread — must be in cost model. |
| EURUSD | 1.0 pip | 0.5 | Benchmark / engine calibration pair. |
| GBPUSD | 1.5 pips | 0.8 | Volatility + London session test. |
| USDJPY | 1.0 pip | 0.5 | Trend persistence + regime proxy. |
| XAGUSD | 6.0 pips | 3.0 | Gold correlation / cost stress test. |

**Rule:** Backtesting engine loads `spread_pips`/`slippage_pips` per pair from `config.yaml → pairs[symbol]`. Global `default_spread` is fallback only.

### Validation Folder
`validation/` added by Leo. Contains 10 XAUUSD strategies and 6-phase framework. **`validation_report.json` has placeholder metrics only** — all strategies show identical numbers. Connect to real backtest engine at Step 11.

---

## Step 11 — Pre-Flight Checklist

Before writing engine code:

```bash
# 1. MT5 terminal running and logged into demo account
# 2. Pull all historical data
python -m data.ingestion

# 3. Confirm data range (should show 2020–2026)
python mt5_bridge/data_feed.py
```

Then build `backtesting/engine.py` per the step detail above.

---

*Plan generated from MT5_Trading_Platform_Master_Plan.docx v1.0 — April 2026*
