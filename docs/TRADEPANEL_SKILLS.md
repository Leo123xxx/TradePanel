# TradePanel — Skills & Knowledge Base
> Reusable context for Cowork / Claude AI sessions on this project.
> Last updated: 2026-05-06

---

## 1. Project Overview

| Property | Value |
|---|---|
| Root folder | `F:\REPOS\leo123xxx\TradePanel` |
| Inner app folder | `F:\REPOS\leo123xxx\TradePanel\TradePanel` |
| Account currency | ZAR (South African Rand) |
| User timezone | SAST = UTC+2, no DST (South Africa) |
| Broker / data source | MetaTrader 5 (MT5) via Python API |
| Database | PostgreSQL, accessed via `data/db_client.py` (psycopg2) |
| Python environment | `.venv` in project root (Windows) |
| Primary language | Python 3.x |

---

## 2. Critical Architecture Rules — Read Before Touching Anything

### 2.1 Timestamp Gotcha (SAST vs UTC)
- All OHLCV data in the DB is stored in **SAST (UTC+2)**, NOT UTC.
- This happens because MT5 bridge uses `datetime.fromtimestamp()` on Leo's Windows machine (South Africa).
- `base_strategy.py` SESSION_WINDOWS are defined in UTC hours.
- When applied to SAST timestamps, `EURUSD [(7, 17)]` means `hour < 17 SAST` — which is UTC 5:00-15:00, NOT the intended London/NY overlap.
- **Always account for SAST offsets when diagnosing zero-signal or zero-trade bugs.**

### 2.2 Session Filter Architecture
- `BaseStrategy.filter_by_session(df, symbol)` is called by the engine **AFTER** `generate_signals()`.
- It zeros out any signal bar where `df.index.hour` falls outside the pair's SESSION_WINDOW.
- Strategies that manage their own session logic internally (e.g. ORB) MUST set `'use_session_filter': False` in params.
- If you see a strategy generating signals internally but the engine shows 0 trades — check the session filter first.

### 2.3 Entry Timing (No Lookahead)
- Engine enters at **bar[i+1] OPEN** after signal fires on **bar[i] CLOSE**.
- There is no same-bar entry. This is intentional and must not be changed.

### 2.4 TP/SL Calculation
- ATR-based: `tp_price = entry + ATR * tp_atr_mult`, `sl_price = entry - ATR * sl_atr_mult` (long).
- ATR period set by `atr_period` param (default 14).
- **Partial Take Profit**: Automated multi-stage exits based on strategy category.
- **Breakeven**: Moves SL to entry + buffer once profit reaches `breakeven_trigger_mult * ATR`.

### 2.5 Commission — No Double-Charge
- Spread and slippage are embedded in `entry_price` at bar open.
- Only `commission_per_lot` is deducted at close.
- **Do NOT add spread_cost to commission_cost in engine.py** — this was a historical bug that was fixed.

### 2.6 Volume Filter Bias (Intraday)
- A simple rolling-mean volume filter (e.g. 20-bar) at SAST 17:30 is inflated by London/NY overlap bars.
- Post-range NY-afternoon bars (~200-400 ticks) almost never clear 1.2x of an inflated average (~800-1200 ticks).
- **Fix**: Use hourly-normalised volume — compare each bar to the mean of all bars from the same clock-hour across the dataset. This eliminates session bias.

---

## 3. Strategy Registry

**v4 Strategy Upgrades (2026-05-06) — Directional biases and 0.15 lot limit enforced**

| Strategy | Version | Key Changes |
|---|---|---|
| rsi_pullback | v3 | EMA200 gate, ADX 20-45, MACD histogram turn, RSI 38-47/53-65, trend AND not OR |
| hikkake_trap | v3 | IB range ≥0.7×ATR, ADX max 22, reversal bar in top/bottom 40%, cooldown 12 |
| session_momentum | v3 | Vol 1.5×, ADX min 28, RSI 57/43, breakout distance ≥0.3×ATR |
| vwap_momentum | v3 | ADX max 22, RSI 35/65, VWAP excess ≥0.8×ATR, vol declining 3 bars |
| rvgi_cci_confluence | v2 | EMA200 macro gate added, RSI >55/<45 gate |
| macd_trend | v3 | MACD histogram slope rising 2 bars filter |
| orb | v3 | Daily direction bias (EMA20 of daily opens) |
| bb_squeeze_scalp | v3 | 5-bar sustained squeeze, vol spike 2×, EMA200 macro gate |
| dual_ema_fractal | v3 | 2 consecutive fractals in same direction required |
| dual_ema_momentum | v3 | Full ribbon EMA15>50>100>200, ADX rising gate |
| stoch_divergence | v3 | H4+H1 dual-TF overhaul; divergence confirmed on BOTH TFs; H1 added, D1 removed |
| rsi_bounce | v3 | ADX max 18, RSI 15/85, confirmation candle required |
| bb_mean_reversion | v3 | ADX max 15, BB 3σ, vol declining 2 bars, RSI 28/72 |
| cot_sentiment | v3 | COT 4-week delta filter (positioning must still be building toward extreme) |
| stat_arb | v3 | D1 disabled (MaxDD 106%), H1/M30/M15 added |

**TIER 1 (11 strategies — target WR 70%+)**
| Strategy | File | Pairs | Timeframes | RR | Notes |
|---|---|---|---|---|---|
| Dual EMA Fractal | `strategies/dual_ema_fractal.py` | EURUSD, GBPUSD, XAUUSD | H4, D1 | 1:2 / 1:4 | v3: 2 consecutive fractals |
| COT Sentiment | `strategies/cot_sentiment.py` | XAUUSD/EURUSD/GBPUSD/USDJPY | D1, W1 | 1:4 | v3: 4-week COT delta filter |
| RSI Bounce | `strategies/rsi_bounce.py` | EURUSD, XAUUSD, GBPUSD, USDJPY | H4, D1 | 1:2 | v3: ADX≤18, RSI 15/85, confirm candle |
| Stat Arb Gold/Silver | `strategies/stat_arb_gold_silver.py` | XAUUSD | H4, H1, M30, M15 | 1:2 | v3: D1 disabled |
| MA Crossover | `strategies/ma_crossover.py` | EURUSD, GBPUSD, USDJPY | M15–W1 | 1:2 / 1:4 | ADX≥20 |
| BB Mean Reversion | `strategies/bb_mean_reversion.py` | XAUUSD, EURUSD, GBPUSD | H1, H4 | 1:2 | v3: ADX≤15, 3σ, vol exhaustion |
| Stoch Divergence | `strategies/stoch_divergence.py` | EURUSD, XAUUSD, USDJPY | H1, H4 | 1:2 | v3: dual-TF H1+H4 |
| MACD Trend | `strategies/macd_trend.py` | EURUSD, USDJPY | H1, H4 | 1:2 | v3: histogram slope 2-bar filter |
| Gold Momentum Breakout | `strategies/gold_momentum_breakout.py` | XAUUSD, GBPUSD, stocks | H1, H4, D1 | 1:2 / 1:4 | RSI≥60 + volume 1.5× |
| Range Breakout | `strategies/range_breakout.py` | XAUUSD, EURUSD | H4 | 1:2 | Volume 1.3× gate |
| EMA Ribbon Trend | `strategies/ema_ribbon_trend.py` | BTCUSD, ETHUSD, XAUUSD, stocks | H1, H4, D1 | 1:2 / 1:4 | ADX≥28 |

**TIER 2 (14 strategies — solid, WFO validated)**
| Strategy | File | Pairs | Timeframes | RR | Notes |
|---|---|---|---|---|---|
| Session Momentum | `strategies/session_momentum.py` | EURUSD, GBPUSD, XAUUSD | H1 | 1:2 | v3: vol 1.5×, ADX 28, RSI 57/43 |
| RSI Pullback | `strategies/rsi_pullback.py` | XAUUSD, USDJPY | H4, D1 | 1:2 / 1:4 | v3: EMA200+MACD+ADX 20-45 |
| Turtle Soup | `strategies/turtle_soup.py` | EURUSD, GBPUSD, XAUUSD | H1, H4 | 1:2 / 1:4 | SMC false-break |
| Dual EMA Momentum | `strategies/dual_ema_momentum.py` | XAUUSD, EURUSD, GBPUSD | H1, H4 | 1:2 / 1:4 | v3: full ribbon+ADX rising |
| VWAP Momentum | `strategies/vwap_momentum.py` | GBPUSD, EURUSD, XAUUSD | M15, H1 | 1:2 | v3: ADX≤22, RSI 35/65, vol exhaustion |
| Hikkake Trap | `strategies/hikkake_trap.py` | XAUUSD, EURUSD, GBPUSD | H4, D1 | 1:2 | v3: ADX max 22, IB quality, cooldown 12 |
| ORB | `strategies/orb.py` | GBPUSD, EURUSD, XAUUSD | M15 | 1:2 | v3: daily bias filter; use_session_filter=False |
| RVGI-CCI Confluence | `strategies/rvgi_cci_confluence.py` | GBPUSD, USDJPY | H1 | 1:2 | v2: EMA200+RSI gate |
| BB Squeeze Scalp | `strategies/bb_squeeze_scalp.py` | XAUUSD, EURUSD, GBPUSD | M15 | 1:2 | v3: 5-bar squeeze, vol spike 2× |
| RSI Extremes Scalp | `strategies/rsi_extremes_scalp.py` | XAUUSD, EURUSD, GBPUSD | M15 | 1:2 | RSI 18/82, London/NY |
| Crypto RSI Extremes | `strategies/crypto_rsi_extremes.py` | BTCUSD, ETHUSD | H4, D1 | 1:2.5 | RSI 25/75, vol spike |
| Fast MA Scalper | DISABLED | — | — | — | WR 32-46%, confirmed broken |
| MACD Zero Scalp | DISABLED | — | — | — | WR 31-40%, confirmed broken |
| EMA Ribbon Scalp | DISABLED | — | — | — | WR 50.7%, insufficient edge |

Pass criteria (aligned 2026-05-07 — single source of truth across all files):
- Win Rate: >= 70% (PASS gate in run_overnight_backtest.py + recommendations.py)
- Sharpe: >= 2.0 (PASS gate — enforced in both engines)
- Risk Reward: >= 1:2 minimum (tp_atr_mult=2.0, sl_atr_mult=1.0)
- Max Drawdown: <= 12% | Lot Size: max 0.15 | All P&L in ZAR (R18.50/USD)
- Near-PASS threshold (priority tuning): Sharpe >= 1.2

---

## 4. Known Bugs — Fixed, Do Not Reintroduce

### Bug 5: PIP_SIZES missing for new pairs (2026-04-30)
- **Symptom**: US500, USTEC, USOIL, NVDA, AMD, MSFT, AAPL showed 100-571% MaxDD in backtest. XAUUSD SL/TP in Telegram displayed at entry price ±$0.003.
- **Root cause**: All 11 new pairs defaulted to `DEFAULT_PIP_SIZE=0.0001`, inflating P&L by 100–10,000×.
- **Fix**: Centralised pip sizes into `utils/pip_sizes.py` (`get_pip_size(symbol)` function). `backtesting/engine.py` and `notifications/router.py` both import from this single source. **Never hardcode pip sizes — always use `get_pip_size()`.**

### Bug 6: `_check_strategy_active` reading wrong config (2026-04-30)
- **Symptom**: No trades ever placed by live engine despite signals being detected.
- **Root cause**: `risk/manager.py._check_strategy_active()` read `config.yaml`'s `strategies:` key (which doesn't exist) instead of `strategies.yaml`. Always returned `False`, blocking every trade at risk check #1.
- **Fix**: Now reads from `self.strategies_meta` (loaded from `strategies.yaml` at init).

### Bug 7: Duplicate signal logging in detect mode (2026-04-30)
- **Symptom**: `/signals` showed same signal repeated 5× (one per minute).
- **Root cause**: `paper_engine._track_processed_signal()` was never called in detect mode, so the dedup cache was always empty and the same signal was re-logged every 1-minute scan.
- **Fix**: `_track_processed_signal()` now called immediately after `_log_signal()`. Dedup window extended 5→60 min.

### Bug 8: CronTrigger timezone mismatch (2026-04-30)
- **Symptom**: Signal outcome checker was scheduled for 01:00 UTC (03:00 SAST) not 01:00 SAST.
- **Root cause**: `CronTrigger(hour=1)` in Docker (UTC environment) fires at 01:00 UTC.
- **Fix**: Changed to `CronTrigger(hour=23, minute=0, timezone='UTC')` = 01:00 SAST. Always specify `timezone='UTC'` explicitly on CronTriggers in docker_jobs.py.

### Bug 1: ORB Session Filter (root cause of EURUSD 0 trades)
- **Symptom**: ORB generates signals internally (confirmed via diagnostic print), but engine shows 0 trades.
- **Root cause**: `filter_by_session` for EURUSD `[(7, 17)]` applied to SAST timestamps blocks all bars at SAST hour >= 17. ORB post-range runs SAST 17:30-21:30, so every signal was zeroed.
- **Fix**: Set `'use_session_filter': False` in ORB params. ORB manages its own windows via `is_range` / `is_post_range`.
- **Why XAGUSD was unaffected**: Its window is `[(7, 20)]`, so SAST 17:30-20:00 passed the `hour < 20` check.

### Bug 2: ORB Volume Filter Session Bias
- **Symptom**: EURUSD ORB 0 signals even when breakout conditions met.
- **Root cause**: 20-bar rolling volume average dominated by London/NY overlap. NY afternoon bars fail the 1.2x threshold.
- **Fix**: Hourly-normalised volume (`df.groupby('_hr')['tick_volume'].transform('mean')`). Apply filter at **range bars** (not post-range breakout bars) — the day is either good-volume or not.

### Bug 3: Commission Double-Charge
- **Symptom**: PnL appeared lower than expected.
- **Root cause**: Engine was adding both spread_cost and commission_cost at trade close. Spread is already in entry_price.
- **Fix**: Only deduct commission_per_lot at close.

### Bug 4: COT Sentiment 0 SELL Signals
- **Symptom**: COT strategy generated BUY signals but zero SELL signals for all FX pairs.
- **Root cause 1**: `anti_threshold = 100 - 80 = 20` was too extreme; FX COT index rarely hits 20.
- **Root cause 2**: `in_bear = close < ema200` almost never True for XAUUSD (multi-year bull) or FX pairs during consolidation (EMA200 too slow).
- **Fix**: Separate `sell_threshold=30` param. Pair-aware gate: EMA200 for XAUUSD/XAGUSD (hard gate), EMA50 direction for EURUSD/GBPUSD/USDJPY.
- **Trade-off**: EURUSD COT sell signals are currently losing (Sharpe -0.82). Monitor whether sells should be disabled for FX.

### Bug 9: Lot size limit bypass in backtests (2026-05-06)
- **Symptom**: Backtest results for high-ATR strategies showed excessive drawdowns.
- **Root cause**: `BacktestEngine` used a fixed lot size (0.1) but some scripts might have requested higher, and there was no hard cap in the engine.
- **Fix**: Enforced `min(lot_size, 0.15)` hard cap in `BacktestEngine.__init__`.

### Bug 10: Lack of directional filtering (2026-05-06)
- **Symptom**: Strategies were forced to trade both directions even when one side was clearly unprofitable (e.g. trading long in a structural bear market).
- **Root cause**: `BaseStrategy` lacked `allow_long`/`allow_short` flags.
- **Fix**: Added `allow_long` and `allow_short` (default: True) to `BaseStrategy` and implemented `filter_by_direction()` in engines.

---

## 5. Data Pipeline

| Component | File | Schedule |
|---|---|---|
| MT5 bridge | `mt5_bridge/data_feed.py` | Continuous (auto-reconnect) |
| OHLCV ingestion | `data/ingestion.py` | Every 6h via APScheduler |
| COT data | `data/cot_feed.py` | Fridays 21:00 UTC auto + manual `--history` |
| Data cleaner | `data/cleaner.py` | Daily |
| Overnight backtest | `scripts/run_overnight_backtest.py` | Nightly |

DB tables: `market_data` (raw), `market_data_resampled` (higher TFs), `cot_data`

Initial COT load: `python data/cot_feed.py --history`

---

## 6. Backtest Runner

```
python scripts/run_overnight_backtest.py --no-telegram
```

Reports: `results/overnight/YYYYMMDD_backtest_report.{json,md}`

---

## 7. Config Files

| File | Purpose |
|---|---|
| `config/config.yaml` | Pair spreads, slippage, commission, pip values, ZAR rates |
| `config/strategies.yaml` | Enable/disable strategies, pairs, timeframes, parameters per strategy |
| `utils/pip_sizes.py` | **Master source of truth for pip sizes** — import `get_pip_size(symbol)` |

Key config values:
- `backtesting_usdzar_rate: 18.50` — update quarterly
- `backtesting_jpyzar_rate: 0.1233` — update quarterly
- Spread values — verify against broker monthly

---

## 8. Bash Environment Notes (Cowork Sessions)

- Bash sandbox path mapping: `F:\REPOS\leo123xxx\TradePanel` -> `/sessions/.../mnt/leo123xxx--TradePanel/`
- Inner folder: `F:\REPOS\leo123xxx\TradePanel\TradePanel` -> `/sessions/.../mnt/TradePanel/`
- Cannot connect to PostgreSQL from bash sandbox (psycopg2 not installed in sandbox)
- Cannot run full backtest from sandbox — must run on Leo's Windows machine
- **File writing tip**: For Python files with f-strings, Unicode, or special characters, use bash `cat > file << 'PYEOF'` heredoc. The Write tool may corrupt files at special characters.
- After writing via bash, verify with Read tool that the file content is intact

---

## 9. COT Sentiment — Pair-Specific Logic

```
_COMMODITY_PAIRS = {"XAUUSD", "XAGUSD"}

For commodities: EMA200 gate (hard)
  - in_bull = close > ema200
  - in_bear = close < ema200
  - Rationale: prevents shorting gold in multi-year structural bull

For forex (EURUSD, GBPUSD, USDJPY): EMA50 direction gate only
  - in_bull = close > ema50
  - in_bear = close < ema50
  - Rationale: EMA200 too slow for daily swing; blocks all sell signals
    during valid downtrend periods on FX pairs
```

Thresholds: `sentiment_threshold=80` (BUY), `sell_threshold=30` (SELL)
Exit: when COT index crosses back through 50 (neutral zone)

---

## 10. ORB — Key Parameters

```python
params = {
    'ny_offset_hours':     7,      # SAST - 7 = NY-equivalent hour
    'range_start_ny':      9.5,    # 9:30 AM NY = SAST 16:30
    'range_duration_mins': 60,     # Range window: SAST 16:30-17:30
    'vol_filter':          1.2,    # Min relative volume for range bars
    'tp_atr_mult':         2.0,
    'sl_atr_mult':         1.0,
    'use_session_filter':  False,  # CRITICAL - do not set to True
}
```

Post-range window: SAST 17:30-21:30 (NY 10:30-14:30)
Signal: first close crossing above range_high (long) or below range_low (short) in post-range, on a day where range bars had above-average volume.

---

## 11. Diagnostic Pattern — Zero Trades Debugging

When a strategy shows 0 trades in backtest output:
1. Add diagnostic print inside `generate_signals()` — count raw signals before return
2. If signals > 0 internally but 0 in engine: **check `use_session_filter`**
3. If signals = 0 internally: check each filter condition separately (vol_ok, session window, trend gate)
4. Check `df.index.hour` values — are they SAST or UTC? Does the session window match?
5. Check non-zero tick_volume percentage — if < 50%, volume filter is bypassed automatically

---

## 12. Live Readiness & Production Safety (2026-05-03)

### 12.1 Circuit Breaker (Hard Drawdown)
- **Trigger**: Fires when daily drawdown exceeds `max_drawdown_hard_pct` (default: 20.0%).
- **Action**: Immediately closes all bot-managed positions (Magic != 0) and sets `bot_health.CIRCUIT_BREAKER` status to `PAUSED`.
- **Reset**: Clears automatically at midnight SAST, or manually via `/resume` Telegram command.
- **Gating**: `RiskManager.check_all()` returns `False` if a circuit breaker event is active for today.

### 12.2 Magic Number Isolation
- **Bot Magic**: `zlib.adler32(strat_name.encode()) % 1000000`.
- **Manual Magic**: Always `0`.
- **Isolation**: The bot strictly ignores positions with `magic=0` during trade management, signal processing, and drawdown calculations. Manual trades are safe from bot intervention.

### 12.3 1% ATR-Based Risk Sizing
- **Formula**: `lots = (balance * 0.01) / (sl_points * tick_value_per_lot)`.
- **Implementation**: Calculated in `RiskManager.calculate_lot_size(symbol, sl_points)`.
- **Consistency**: Lot size is dynamically anchored to account balance and current MT5 tick values, ensuring a fixed 1% risk regardless of volatility.

### 12.4 Manual Trade Mirroring
- **Command**: `/trade <SYM> <DIR> <LOTS> [ENTRY]` mirrors a manual MT5 trade into the DB.
- **Mirror Mode**: Trades are stored with `mode='MANUAL'` and `magic=0`.
- **Dashboard**: Manual trades appear in the "Trade Journal" and contribute to total performance metrics, but are ignored by bot risk-management logic.

### 12.5 News Blackout
- **Command**: `/news_blackout <minutes>` sets a block window.
- **Expiry**: Stored as a `resume_at` timestamp in `bot_health`. Risk manager auto-blocks entries until the time passes.

### 12.6 Breakeven Management
- **Trigger**: Moves SL to entry price once the trade profit reaches `breakeven_trigger_mult * ATR` (default 1.5x).
- **Persistence**: Verified on every engine scan cycle. Prevents winners from turning into losers.

---

---

## 13. File Writing Rules — CRITICAL (2026-05-04 Session, Reconfirmed 2026-05-06)

### 13.1 Never use the Edit tool on .py files
The Edit tool silently introduces UTF-16 null bytes mid-file. The file appears to write successfully, but Windows Python exits silently with zero output and Linux Python says "source code cannot contain null bytes".

Use bash Python inline instead:
```
python3 << 'PYEOF'
path = "/sessions/.../mnt/TradePanel/forward_test/paper_engine.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
src = src.replace("old string here", "new string here")
with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("Done")
PYEOF
```

Null byte check: `python3 -c "print(open(path,'rb').read().count(b'\x00'))"`

### 13.2 Never use Write tool for long Python files with f-strings
The Write tool may truncate at Unicode characters (em-dashes, smart quotes).
Use bash heredoc instead: `cat > file << 'PYEOF' ... PYEOF`

### 13.3 YAML files from bash mount may have null bytes
Copy to outputs folder then strip before parsing:
```
raw = open(path, 'rb').read().replace(b'\x00', b'')
yaml.safe_load(raw.decode('utf-8'))
```

### 13.4 Bash mount truncates long Python lines (false SyntaxError)
The Linux mount of the Windows filesystem truncates very long lines, causing py_compile to report SyntaxError on valid code.
Fix: Use the Read tool to verify Python syntax — never bash py_compile for validation.

---

## 14. Database — Patterns & Tools (2026-05-06)

### 14.1 Adminer (preferred DB GUI)
- URL: http://localhost:8080
- Server: `host.docker.internal:5433` — NOT `db` (hostname does not resolve inside Docker on Windows Docker Desktop)
- DB: `trading_platform` | User: `trader` | Password: `traderpass`
- Collation warning on login is non-blocking — run `ALTER DATABASE trading_platform REFRESH COLLATION VERSION;` to dismiss

### 14.2 net_pnl write pattern (trade close)
Always fetch real P&L from MT5 deal history when closing a trade — not a tick approximation:

```python
deals = mt5.history_deals_get(
    datetime.now() - timedelta(days=1),
    datetime.now() + timedelta(hours=1),
    position=ticket
)
real_pnl = sum(d.profit for d in deals) if deals else fallback_calc
self.db.execute_query(
    "UPDATE trades SET exit_price=%s, close_time=%s, status=%s, close_reason=%s, net_pnl=%s WHERE mt5_ticket=%s",
    (exit_price, close_time, 'CLOSED', reason, real_pnl, ticket)
)
```

### 14.3 triggered_trade_id linking pattern (signal to trade)
After inserting a new trade, link it back to the most recent unlinked signal:

```python
if strategy_id:
    self.db.execute_query("""
        UPDATE signals
        SET triggered_trade_id = %s
        WHERE signal_id = (
            SELECT signal_id FROM signals
            WHERE strategy_id = %s
              AND pair = %s
              AND triggered_trade_id IS NULL
            ORDER BY timestamp DESC
            LIMIT 1
        )
    """, (trade_id, strategy_id, symbol))
```

### 14.4 COALESCE for backward-compatible P&L queries
Old rows have net_pnl = NULL. Use COALESCE so historical data still renders:
`COALESCE(t.net_pnl, t.exit_price - t.entry_price) AS pnl`
Note: exit_price - entry_price is NOT real account-currency P&L — it is a price diff fallback for pre-fix rows only.

---

## 15. Health and Connectivity Endpoint Pattern (2026-05-06)

`webapp/api/router_health.py` provides real connectivity checks (not hardcoded strings):

| Service | Check | ONLINE threshold |
|---|---|---|
| PostgreSQL | `SELECT 1` live query | Succeeds |
| MT5 Bridge | Last HEARTBEAT in `bot_health` table | < 5 minutes ago |
| Event Bus | `bus._running` attribute | True |

Frontend: `useConnectivity()` hook polls `/api/health` every 15 seconds and feeds `ConnStatus` component coloured by real status value.

---

## 16. signal_taken Dashboard Pattern (2026-05-06)

The full chain from trade execution to dashboard display:

1. DB: `signals.triggered_trade_id UUID` set by `paper_engine._log_trade_open()` after inserting into `trades`
2. API (`/api/papertrades/signals`): `(sig.triggered_trade_id IS NOT NULL) AS signal_taken` in SELECT
3. Response: `"signal_taken": bool(r[8])` in the JSON dict
4. Dashboard (`App.jsx`): checkmark if signal_taken, dash if not
5. Telegram (`/signals` command): "TAKEN" or "Not taken" badge per signal

When debugging "all signals show Not taken": check whether `_log_trade_open()` is actually executing the UPDATE. If `strategy_id` is None the UPDATE is skipped — ensure strategy_id is passed through from the signal record.

---


## 17. Signals Tab & Account-Aware Signals (2026-05-07)

### 17.1 Signals Dashboard Tab
A dedicated "Signals" tab (with LIVE badge) was added to `webapp/frontend/src/App.jsx`.
Component: `SignalsTab` (line ~1756). Features:
- Auto-refreshes every 30 seconds via `usePolling`
- Time window selector: 6h / 24h / 48h / 7d
- Account filter pills — one pill per `account_profiles` entry; amber pill for pending/untaken signals
- Stats strip: total signals, taken count, take rate %
- Signal table: Time | Account | Strategy | Pair | TF | Direction | Price | Validity | Status

### 17.2 Account-Aware Signals Endpoint (2026-05-07)
`GET /api/papertrades/signals` (in `webapp/api/router_papertrades.py`) now JOINs:
```sql
LEFT JOIN trades t ON sig.triggered_trade_id = t.trade_id
LEFT JOIN account_profiles ap ON t.account_id = ap.account_id
```
Each signal in the response now includes:
- `account_id` — NULL if signal not yet taken
- `account_name` — human-readable name (e.g. "Exness DEMO"), "—" if untaken
- `account_type` — "DEMO" | "LIVE" | "PAPER"

This means taken signals show which account executed the trade; pending signals show "—".

### 17.3 Debugging Signal-to-Account Linkage
If all signals show `account_name: "—"` even after trades are placed:
1. Check `signals.triggered_trade_id` is being SET — see Section 16 for the UPDATE pattern
2. Check `trades.account_id` is non-NULL — verify `paper_engine` is passing `account_id` at trade insert
3. The JOIN is a LEFT JOIN chain, so any NULL in the chain silently returns NULL for account fields

---

## 18. Walk-Forward Optimisation (WFO) — Commands, Schedule & Interpretation (2026-05-07)

WFO validates that a strategy's parameters generalise to **unseen out-of-sample data**,
making it the strongest confirmation beyond a regular overnight backtest.
A strategy that passes both the overnight backtest AND WFO is market-ready.

---

### 18.1 Commands

**Full suite — all enabled strategies (preferred, run this):**
```powershell
# Inside Docker (preferred — has all deps):
docker exec tradepanel-backend python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20

# Native (outside Docker — requires psycopg2, yaml in host env):
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
```

**Single strategy (faster iteration / debugging):**
```powershell
docker exec tradepanel-backend python scripts/run_wfo_all.py --strategy stat_arb_gold_silver
docker exec tradepanel-backend python scripts/run_wfo_all.py --strategy range_breakout
```

**Expected runtime:** 30–90 minutes for the full suite (~22 strategies x 2–4 combos = ~60 WFO runs).

**Output:** `results/wfo_master_summary.md` — updated in place after every run.

---

### 18.2 Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `--n_windows` | 3 | Number of rolling IS/OOS windows |
| `--is_pct` | 0.70 | In-sample fraction of each window (70%) |
| `--oos_pct` | 0.20 | Out-of-sample fraction (20%), gap = remaining 10% |
| `--strategy` | (all) | Run a single strategy by its yaml name |

**Recommended defaults:** `--n_windows 3 --is_pct 0.70 --oos_pct 0.20`
Use `--n_windows 5` for strategies with > 500 trades to get richer OOS validation.

---

### 18.3 Pass Thresholds

WFO uses slightly looser thresholds than the full overnight backtest because OOS windows
are smaller and inherently noisier. These are calibrated for OOS realism:

| Gate | WFO OOS per-window | Overnight backtest |
|------|-------------------|-------------------|
| Win Rate | >= 65% | >= 70% |
| Sharpe | >= 1.5 | >= 2.0 |
| Trades | >= 10 | >= 20 |
| **Strategy verdict** | >= 70% of windows pass | — |

A strategy is **WFO VALIDATED** when >= 70% of its OOS windows meet all three gates.

---

### 18.4 Schedule

WFO runs automatically **twice a week** via the APScheduler job added to `docker_jobs.py`:
- **Wednesday 03:00 UTC** (Thu 05:00 SAST)
- **Sunday 03:00 UTC** (Sun 05:00 SAST)

Job ID: `wfo_biweekly` | Method: `_run_wfo_suite` → `_wfo_worker`

Telegram alerts are sent on start and completion with a PASS/FAIL/ERROR count digest.

**Why twice a week?** Market regime can shift materially in 48–72h (e.g. FOMC, NFP).
Wednesday catches mid-week regime state; Sunday catches the weekly close and reset.

---

### 18.5 How Recommendations Cross-Reference WFO

`scheduler/recommendations.py` reads `results/wfo_master_summary.md` on every run via
`_load_wfo_results()`. The generated recommendations report now includes a
**WFO Validation Status** section that annotates each combo with its WFO verdict:

- **WFO PASS** — OOS validated; safe to increase lot size or promote to live
- **WFO FAIL** — Fails OOS gate — do not promote, even if overnight backtest says PASS
- **WFO ERROR** — Run error (usually missing data or yaml dep) — re-run manually

**Key rule:** a strategy that passes the overnight backtest but **fails WFO** should be
treated as REVIEW, not PASS. WFO is the final gate before live promotion.

---

### 18.6 Interpreting Results

```
results/wfo_master_summary.md   — overview table + per-window detail
results/wfo/                    — individual strategy log files
```

**Red flags in WFO results:**
- OOS Sharpe < 0 on any window → strategy may be overfit; diagnose before enabling
- OOS win rate trending down window by window → regime sensitivity; add regime filter
- 0 OOS trades on any window → data gap or strategy too restrictive; check pair data freshness
- All windows ERROR → usually missing Python deps (`yaml`, `psycopg2`) or no DB data for that pair/TF

**Good signs:**
- OOS Sharpe > IS Sharpe on any window → strategy is genuinely predictive, not overfit
- Consistent win rate across all windows (low variance) → robust to regime changes
- Pass rate >= 70% → promote to live consideration

---

### 18.7 Adding a New Strategy to WFO

Add an entry to `WFO_CONFIGS` in `scripts/run_wfo_all.py`:
```python
"your_strategy_name": [("XAUUSD", "H4"), ("EURUSD", "H1")],
```
Choose 2 primary pairs that are representative of the strategy's intended market.
The strategy class must already be in `STRATEGY_MAP` in `scripts/run_walk_forward.py`.

---

---

## 19. Trade Management: Partial Take Profits (2026-05-11)

The system now implements a category-aware **Partial Take Profit (PTP)** system in the live/paper engine. This ensures that profit is secured early while allowing "runners" to capture large trends.

### 19.1 PTP Logic by Category
| Category | Trigger | Close Size | SL Action |
|----------|---------|------------|-----------|
| **Trend Following** | 1.2x ATR | 25% | Move to Breakeven |
| **Breakouts** | 1.5x ATR | 33% | Move to Breakeven |
| **Mean Reversion** | 1.0x ATR | 60% | Move to Breakeven |
| **Scalping** | 1.0x ATR | 75% | Move to Breakeven |

### 19.2 Implementation Details
- **Sync**: The `lot_size` is automatically synchronized in the database when a partial close occurs.
- **Security**: Stat Arb strategies are excluded from PTP logic to preserve Z-score exit integrity.
- **Control**: Enable/Disable via `use_partial_tp: true/false` in `strategies.yaml`.
- **Alerts**: Telegram alerts are sent with the `💰 PARTIAL TP HIT` badge.

---

*End of TRADEPANEL_SKILLS.md*

---

## Section 20: Canonical Job Schedule (as of 2026-05-10)

All jobs live in `scheduler/docker_jobs.py`. Config overrides via `config/config.yaml` scheduler section.
Times below in UTC with SAST equivalent (UTC+2, no DST).

| Job ID | Trigger | UTC | SAST | Days | Config key |
|--------|---------|-----|------|------|------------|
| heartbeat | interval 60s | — | — | always | heartbeat_interval_sec |
| mt5_conn | interval 60s | — | — | always | — |
| signal_detect | interval 1m | — | — | always | — |
| trade_execute | interval 5m | — | — | always | — |
| position_sync | interval 5m | — | — | always | — |
| pnl_rollup | interval 1h | — | — | always | — |
| regime_detect | interval 1h | — | — | always | — |
| mt5_history_sync | interval 4h | — | — | always | — |
| data_ingest_6h | cron | 00:05,06:05,12:05,18:05 | 02:05,08:05,14:05,20:05 | daily | data_ingest_hours / data_ingest_minute |
| signal_outcome_check | cron | 23:00 | 01:00+1 | daily | timezone='UTC' hardcoded |
| overnight_backtest | cron | 02:00 | 04:00 | Mon–Fri | overnight_backtest_hour / overnight_backtest_minute |
| wfo_biweekly | cron | 03:00 | 05:00 | Wed+Sun | — |
| yahoo_history_fill | cron | 01:30 | 03:30 | Sunday | — |
| db_cleanup | cron | 00:30 | 02:30 | Sunday | db_cleanup_day / db_cleanup_time |
| daily_summary | cron | 18:00 | 20:00 | daily | notifications.daily_summary_time |
| weekly_report | cron | 08:00 | 10:00 | Monday | — |
| correlation_check | cron | 09:00 | 11:00 | Monday | — |
| cot_refresh | cron | 21:00 | 23:00 | Friday | — |
| weekly_archive | cron | 23:59 | 01:59+1 | Thursday | — |
| **daily-tradepanel-automation** (Cowork) | cron | **04:04** | **06:04** | daily | Cowork task cron: `4 6 * * *` SAST |

**Critical alignment rules:**
- All `CronTrigger` calls in docker_jobs.py run in Docker's UTC timezone. Always specify `timezone='UTC'` explicitly.
- The Cowork automation runs at 06:04 SAST (04:04 UTC), AFTER the overnight backtest (starting 04:00 SAST, ~60–90 min).
- Active results window: last 3 days in `results/overnight/`.
- Disabled strategies live in `strategies/strategies_archive.py` and `strategies/archive/` — not loaded by registry.

