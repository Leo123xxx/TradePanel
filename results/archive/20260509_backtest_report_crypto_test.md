# Overnight Backtest Report — 09 May 2026

Generated: 2026-05-09 03:12 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 0 |
| ⚠️ REVIEW | 8 |
| ❌ ERROR/SKIP | 0 |
| **Total combos** | **8** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|

---

## ⚠️ Strategies Needing Review


### crypto_rsi_extremes | BTCUSD | H1
WR=42.9%  Sharpe=-3.46  MaxDD=35.1%  Trades=210

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 35.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | M15
WR=42.3%  Sharpe=-4.11  MaxDD=54.1%  Trades=537

**Parameter Tweaks:**
- Win rate 42.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 54.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | H1
WR=39.2%  Sharpe=-4.83  MaxDD=3.0%  Trades=227

**Parameter Tweaks:**
- Win rate 39.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | D1
WR=37.5%  Sharpe=-7.86  MaxDD=0.6%  Trades=8

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | H4
WR=31.2%  Sharpe=-4.95  MaxDD=30.2%  Trades=64

**Parameter Tweaks:**
- Win rate 31.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 30.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | H4
WR=31.2%  Sharpe=-6.10  MaxDD=2.0%  Trades=64

**Parameter Tweaks:**
- Win rate 31.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | M15
WR=28.4%  Sharpe=-6.40  MaxDD=6.1%  Trades=697

**Parameter Tweaks:**
- Win rate 28.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.40 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | D1
WR=14.3%  Sharpe=-6.22  MaxDD=8.2%  Trades=7

**Parameter Tweaks:**
- Win rate 14.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.39 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

---

## ❌ Errors / Skipped
