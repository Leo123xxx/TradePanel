# TradePanel — Skills & Knowledge Base
> Reusable context for Cowork / Claude AI sessions on this project.
> Last updated: 2026-04-25

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

| Strategy | File | Key Pairs / TFs | Status | Notes |
|---|---|---|---|---|
| Stat Arb Gold/Silver | `strategies/stat_arb_gold_silver.py` | XAUUSD H4 | PASS | Best performer: Sharpe=4.66, WR=70.8%, DD=6.2% |
| Range Breakout | `strategies/range_breakout.py` | XAUUSD H4 | PASS | Sharpe=3.16, DD=21.9% — watch DD |
| RSI Pullback | `strategies/rsi_pullback.py` | XAUUSD H4, USDJPY H4 | PASS | Sharpe 1.28-2.16 |
| ORB | `strategies/orb.py` | XAGUSD M15, EURUSD M15 | REVIEW | XAGUSD works; EURUSD trading (136 trades) but Sharpe=-4.02 |
| COT Sentiment | `strategies/cot_sentiment.py` | XAUUSD/EURUSD/GBPUSD/USDJPY D1 | REVIEW | Weekly COT data; EMA200 gate for commodities |
| Session Momentum | `strategies/session_momentum.py` | XAUUSD H1, GBPUSD H1 | REVIEW | Near-pass: Sharpe ~1.7 but WR <40% |

Pass criteria (approx): WR >= 50%, Sharpe >= 1.0, DD <= 25%

---

## 4. Known Bugs — Fixed, Do Not Reintroduce

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
| `strategies.yaml` | Enable/disable strategies per tier |

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

*End of TRADEPANEL_SKILLS.md*
