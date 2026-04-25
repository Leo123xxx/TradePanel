# TradePanel — System Recommendations & Action Plan
**Date:** 24 April 2026  
**Author:** System Audit (AI-assisted)  
**Status:** Applied + Outstanding

---

## What Was Applied Today

All of the following changes have been made directly to the codebase in this session.

### 1. Tier 1 & 2 Only — Strategy Tiers Locked Down

`dual_ema_fractal` was incorrectly labelled TIER_3 despite being the **#1 performer** (55.62% WR). It has been promoted to TIER_1.

**Now active (19 strategies):**

| Tier | Strategy | Pair(s) | TF | Win Rate |
|------|----------|---------|-----|---------|
| T1 | dual_ema_fractal ⭐ | EURUSD, GBPUSD, XAUUSD | H1 | 55.62% |
| T1 | rsi_bounce | EURUSD, XAUUSD, GBPUSD | H1 | 52.16% |
| T1 | cot_sentiment* | XAUUSD, EURUSD, GBPUSD | D1 | 52.55% |
| T1 | stat_arb_gold_silver | XAUUSD | H4 | — |
| T1 | moving_average_crossover | EURUSD, GBPUSD, USDJPY | H1 | 50.38% |
| T1 | bb_mean_reversion | XAUUSD, EURUSD | H1 | — |
| T1 | stoch_divergence | EURUSD, USDJPY | H4 | — |
| T1 | macd_trend | EURUSD, USDJPY | H1 | — |
| T1 | gold_momentum_breakout | XAUUSD, GBPUSD | H1 | — |
| T1 | range_breakout | XAUUSD | H4 | — |
| T1 | ema_ribbon_trend | BTCUSD, ETHUSD | H4 | — |
| T2 | session_momentum | XAUUSD, GBPUSD | H1 | 50.70% |
| T2 | rsi_pullback | XAUUSD, USDJPY | H4 | — |
| T2 | turtle_soup | EURUSD, GBPUSD | H1/H4 | 49.25% |
| T2 | dual_ema_momentum | XAUUSD | H1/H4 | — |
| T2 | vwap_momentum | GBPUSD, EURUSD | M15/M30 | 51.05% |
| T2 | hikkake_trap | XAUUSD | H4 | — |
| T2 | orb | XAGUSD, EURUSD | M15/H1 | 49.22% |
| T2 | rvgi_cci_confluence | EURUSD, GBPUSD | H1 | — |

> *cot_sentiment disabled: requires CFTC data feed integration.

**Disabled (all Tier 3 & 4):** triple_macd_scalping, dual_ema_fractal (old T3 label), rsi_2, crypto_rsi_extremes, volatility_squeeze_breakout, institutional_silver_bullet, naked_price_action, ict_judas_swing + all 6 M1/M5 scalpers.

---

### 2. Database Updates Every 6 Hours

`scheduler/jobs.py` and `config/config.yaml` updated. Data ingest now runs at **00:05, 06:05, 12:05, 18:05 UTC** daily (was once at 00:05 only). This means backtests always have data that is at most 6 hours old.

### 3. Overnight Backtest — Automated Nightly at 02:00 UTC

New script: `scripts/run_overnight_backtest.py`  
New APScheduler job: `overnight_backtest` (Mon–Fri 02:00 UTC)

The overnight runner:
- Runs all 18 active Tier 1 & 2 strategies across their canonical pair/timeframe combos (≈45 total combos)
- Calculates Win Rate, Sharpe Ratio, Max Drawdown, Profit Factor per combo
- Generates concrete parameter tweak suggestions when metrics fall below thresholds
- Saves a full JSON + Markdown report to `results/overnight/YYYYMMDD_backtest_report.{json,md}`
- Sends a Telegram summary with top performers and attention items

**Trigger manually anytime:**
```bash
python scripts/run_overnight_backtest.py              # All Tier 1 & 2
python scripts/run_overnight_backtest.py --tier 1    # Tier 1 only
python scripts/run_overnight_backtest.py --strategy rsi_bounce --no-telegram
```

### 4. Telegram Bot — 5 New Commands

| Command | Purpose |
|---------|---------|
| `/backtest_report` | Full summary of last overnight backtest |
| `/best_pairs` | Pairs ranked by average win rate |
| `/top_strategies` | Top 5 by Sharpe ratio |
| `/backtest_status` | When did last backtest run? Pass/fail counts |
| `/params` | Parameter tweak suggestions for underperformers |

### 5. Bug Fix — `win_rate` NameError in `_send_daily_summary`

`scheduler/jobs.py` referenced `win_rate` before it was defined. Fixed: win rate is now computed before building the stats dict.

---

## Robustness Fixes Still Recommended

These are **not yet applied** — implement in priority order.

### CRITICAL

**R1. Add retry logic to MT5 connection in `connector.py`**  
The connector calls `mt5.initialize()` once and returns. In production, MT5 terminals disconnect briefly during news events or restarts. Add exponential backoff (3 retries, 5s/15s/30s delays) with Telegram alert on persistent failure.

**R2. Backtest engine data validation guard**  
`backtesting/engine.py` has no minimum-bar guard. If fewer than 100 bars are loaded (e.g. a new pair was added but data hasn't been ingested yet), the backtest runs on noise. Add a check:
```python
if len(data_df) < 200:
    raise ValueError(f"Insufficient data: {len(data_df)} bars (need ≥ 200)")
```

**R3. DB connection pool exhaustion**  
`DBClient` uses `SimpleConnectionPool(1, 10)`. Under load (scheduler + paper engine + backtest all running simultaneously), connections can be exhausted and raise `PoolError`. Switch to `ThreadedConnectionPool` and add a timeout + retry wrapper on `getconn()`.

**R4. Fix `_send_daily_summary` — missing `win_rate` (now fixed), but also verify `exit_price - entry_price` P&L logic**  
Currently PnL is calculated as `exit_price - entry_price` in raw price units, not in account currency. For USDJPY (pip value ≈ $9) and XAGUSD (pip value $5/lot) this gives incorrect dollar P&L in the daily summary. The PnL should be multiplied by `pip_value_per_lot × lot_size`. Add a `trades.pnl_usd` column populated at close time.

### HIGH PRIORITY

**R5. Walk-forward validation before strategy promotion**  
Currently strategies are placed in Tier 1/2 based on in-sample win rate. Every tier promotion should require passing at least 2 of 3 WFO windows (Sharpe > 0 out-of-sample). Automate this gate in the overnight backtest runner: if a strategy drops below 50% WR for 5 consecutive days → auto-demote to Tier 2 and send Telegram alert.

**R6. Strategy correlation cap enforcement**  
`risk_management.strategy_correlation_threshold` is set to 0.7 but is only checked monthly. The `_strategy_correlation_check` job runs on the 1st of the month. Change to **weekly** (every Monday at 09:00 UTC). High correlation between `dual_ema_fractal` and `moving_average_crossover` on EURUSD H1 is expected — document this explicitly in config.

**R7. Graceful shutdown — open positions on KeyboardInterrupt**  
`main.py` exits cleanly on `^C`, but doesn't close open paper positions. Add a shutdown hook that marks all OPENED paper trades as CLOSED with `close_reason='SYSTEM_SHUTDOWN'` and notifies Telegram.

**R8. `cot_sentiment` data dependency**  
This is the #2 ranked strategy (52.55% WR) but is disabled because it needs CFTC COT data. Integrate the free CFTC API (`https://publicreporting.cftc.gov/`) or use `pandas-datareader` for weekly COT data. This is a high-value unlock.

### MEDIUM PRIORITY

**R9. Add `results/overnight/` to `.gitignore`**  
The overnight backtest generates thousands of timestamped files. These don't belong in git. Add to `.gitignore`:
```
results/overnight/
results/daily_validation/
logs/
```

**R10. Spread check in backtesting engine**  
The engine applies spread costs from `config.yaml` but doesn't reject signals when the spread exceeds `max_spread_pips`. In live/paper mode, `risk/manager.py` does this check. The backtest should mirror it: skip entry if `spread_pips > config.pairs[pair].max_spread_pips`.

**R11. Log rotation**  
`telegram_bot.log` is already 5.3 MB and growing. Add Python `logging.handlers.RotatingFileHandler` (max 10 MB, 5 backups) to prevent disk fill. Currently `logging_/event_logger.py` writes to flat files with no rotation.

**R12. `macro_feed.py` and `use_macro_regime_filter`**  
Both `use_macro_regime_filter` and `use_multi_tf_confirmation` are hardcoded `false` ("PATH B: DISABLED FOR TESTING"). These have been disabled for testing since initial deployment. Schedule a review: enable `use_multi_tf_confirmation` first (no external dependency) and run a 2-week forward test. Expected improvement: −15% false signals.

---

## Testing Plan — E2E + Full Backtest

### Phase 1: Unit Tests (run now, < 5 minutes)
```bash
pytest tests/ -v --tb=short
```
Expected: `test_mt5_bridge`, `test_strategy_engine`, `test_risk_manager`, `test_phase_0` all pass.

### Phase 2: DB & Data Integrity (run now)
```bash
python scripts/check_env.py          # MT5 + DB connectivity
python data/ingestion.py             # Verify data coverage per pair/timeframe
```
Check: all 7 pairs have H1, H4, D1 data from 2022-01-01 to present.

### Phase 3: Single-Strategy Backtest Smoke Tests
Run the top 3 strategies manually to verify engine output:
```bash
python scripts/run_backtest.py --strategy dual_ema_fractal  --pair EURUSD --timeframe H1
python scripts/run_backtest.py --strategy rsi_bounce        --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy stat_arb_gold_silver --pair XAUUSD --timeframe H4
```
Expected: ≥ 50 trades, Win Rate > 48%, Sharpe > 0.8.

### Phase 4: Full Overnight Backtest (trigger manually, ~30 min)
```bash
python scripts/run_overnight_backtest.py
```
Expected output in `results/overnight/` with ≥ 60% of combos PASS.

### Phase 5: Paper Trading Forward Test (ongoing, 2 weeks minimum)
Run in scheduler mode and check Telegram daily summaries. The acceptance criterion for any strategy moving to TIER_1 is:
- Forward test Win Rate ≥ 90% of backtest Win Rate
- Forward test Sharpe ≥ 0.8
- No more than 3 consecutive losing days

### Phase 6: Walk-Forward Re-Optimisation (after Phase 5)
```bash
python scripts/run_walk_forward.py --strategy dual_ema_fractal --pair EURUSD
```
WFO pass criterion: Sharpe > 0 in at least 2 of 3 windows.

---

## Pairs with Highest Win Rate — Recommendations

Based on strategy definitions and WFO results in `results/wfo_master_summary.md`:

| Rank | Pair | Best Strategy | Observed WR | Notes |
|------|------|---------------|-------------|-------|
| 1 | XAUUSD | dual_ema_fractal + stat_arb | 55.6% | Primary — highest liquidity, widest ATR |
| 2 | EURUSD | dual_ema_fractal | 55.6% | Best spread (1 pip), calibration pair |
| 3 | GBPUSD | session_momentum + dual_ema | ~50–52% | London session bias — strong H1 |
| 4 | USDJPY | macd_trend + stoch_divergence | ~49–50% | Persistent trend, BoJ risk |
| 5 | BTCUSD | ema_ribbon_trend | 24/7, wider ATR multiples needed |
| 6 | XAGUSD | orb + stat_arb | Correlated to gold — avoid overexposure |
| 7 | ETHUSD | ema_ribbon_trend | Lowest priority — ETH/BTC correlation > 0.9 |

**Recommendation:** Concentrate capital on XAUUSD + EURUSD + GBPUSD. These three pairs cover trending, range, and session strategies cleanly. Limit BTCUSD/ETHUSD to ≤ 1 strategy each to avoid correlation breach.

---

## Telegram Bot — Additional Recommendations

Beyond the 5 commands added today, consider the following enhancements:

**High Value**
- `/promote <strategy>` — Manually promote a strategy to a higher tier (with PIN confirmation)
- `/pause <strategy>` — Immediately disable a strategy and close its open positions
- `/ingest` — Trigger an on-demand 6-hour data ingest cycle outside scheduled times
- Inline keyboard buttons on signal alerts (Accept / Reject / Snooze) for manual review mode

**Monitoring Improvements**
- Daily drawdown bar (progress bar graphic) showing current drawdown vs 12%/20% thresholds
- Regime change alerts: when a pair transitions from TRENDING → RANGING, notify and suggest which strategies to pause
- Weekly P&L chart (simple ASCII bar chart per day) in the Monday report

**Reliability**
- Add a `/ping` command that responds instantly (< 100ms) as a liveness check — distinct from `/health` which queries the DB
- Rate-limit `send_sync_message` with a Redis-backed or in-memory deduplication set (min 5 min between identical messages) to avoid Telegram flood limits
- Wrap all `send_sync_message` calls in a try/except that logs to file on failure rather than crashing the scheduler

**Security**
- Add `ALLOWED_CHAT_IDS` whitelist check at the top of every command handler — currently anyone who finds the bot token can query live account data
- Consider adding a `/lock` command that disables all trading commands until `/unlock <PIN>` is sent

---

## Parameter Auto-Optimisation Pipeline

The overnight backtest now generates tweak suggestions. The next logical step is to close the loop:

1. **Overnight backtest** runs at 02:00 UTC → generates `parameter_tweaks` per strategy/pair
2. **Auto-optimizer** (`scripts/auto_optimize.py` — already exists) reads those suggestions and runs a constrained grid search
3. **Walk-forward validation** confirms the new params don't overfit
4. **Telegram approval gate** sends the proposed param change to you. Only applies if you reply `/approve` within 24h
5. **Config update** — auto-optimizer writes updated params back to `strategies.yaml`

This creates a closed-loop system where strategies self-tune weekly without manual intervention, but always with human approval before going live.

---

## Summary Checklist

| # | Item | Status |
|---|------|--------|
| 1 | Promote `dual_ema_fractal` → TIER_1 | ✅ Done |
| 2 | Disable all Tier 3 & 4 strategies | ✅ Done |
| 3 | Enable 18 Tier 1/2 strategies in config.yaml | ✅ Done |
| 4 | DB ingest every 6 hours | ✅ Done |
| 5 | Overnight backtest script | ✅ Done |
| 6 | Overnight backtest APScheduler job | ✅ Done |
| 7 | 5 new Telegram commands | ✅ Done |
| 8 | Fix `win_rate` NameError in daily summary | ✅ Done |
| 9 | MT5 connection retry logic | ✅ Done |
| 10 | Backtest data minimum-bar guard | ✅ Done |
| 11 | DB pool → ThreadedConnectionPool | ⏳ Recommended |
| 12 | PnL → ZAR account currency conversion (daily/weekly summaries + win-rate query fix) | ✅ Done |
| 13 | CFTC COT data integration (`data/cot_feed.py` + `cot_sentiment` strategy) | ✅ Done |
| 14 | WFO auto-demotion gate | ⏳ Recommended |
| 15 | Weekly correlation check (vs monthly) | ⏳ Recommended |
| 16 | Log rotation | ⏳ Recommended |
| 17 | Enable `use_multi_tf_confirmation` forward test | ⏳ Recommended |
| 18 | Security: ALLOWED_CHAT_IDS whitelist | ⏳ Recommended |
| 19 | Telegram `/pause`, `/promote`, `/ingest` commands | ⏳ Recommended |
| 20 | Auto-optimisation approval loop | ⏳ Recommended |
