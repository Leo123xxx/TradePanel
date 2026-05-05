# TradePanel — Skills & Knowledge Base
> Reusable context for Cowork / Claude AI sessions on this project.
> Last updated: 2026-05-01

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
- Partial TP at 1:1 then breakeven is controlled by `use_partial_tp` param.

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

**v3 Strategy Upgrades (2026-05-01) — All strategies upgraded for 70%+ WR target**

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

Pass criteria (2026-05-01):
- Win Rate: >= 70% minimum (all strategies overhauled to this target)
- Risk Reward: >= 1:2 on M15/M30/H1/H4 (tp_atr_mult=2.0, sl_atr_mult=1.0)
- Risk Reward: >= 1:4 on D1/W1 swing trades (tp_atr_mult=4.0, sl_atr_mult=1.0)
- Sharpe: >= 1.0 | Max Drawdown: <= 20% | All P&L in ZAR (R18.50/USD)

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

*End of TRADEPANEL_SKILLS.md*
