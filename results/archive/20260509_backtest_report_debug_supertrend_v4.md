# Overnight Backtest Report — 09 May 2026

Generated: 2026-05-09 09:53 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 0 |
| ⚠️ REVIEW | 6 |
| ❌ ERROR/SKIP | 0 |
| **Total combos** | **6** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|

---

## ⚠️ Strategies Needing Review


### supertrend | BTCUSD | H4
WR=51.9%  Sharpe=-1.99  MaxDD=32.4%  Trades=108

**Parameter Tweaks:**
- Win rate 51.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 32.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.99 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### supertrend | BTCUSD | D1
WR=47.8%  Sharpe=-1.62  MaxDD=29.1%  Trades=23

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 29.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Only 23 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.62 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### supertrend | ETHUSD | D1
WR=45.8%  Sharpe=-6.13  MaxDD=2.6%  Trades=24

**Parameter Tweaks:**
- Win rate 45.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.31 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### supertrend | ETHUSD | H4
WR=45.7%  Sharpe=-4.05  MaxDD=3.3%  Trades=105

**Parameter Tweaks:**
- Win rate 45.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.05 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.53 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### supertrend | ETHUSD | H1
WR=45.1%  Sharpe=-4.10  MaxDD=5.8%  Trades=386

**Parameter Tweaks:**
- Win rate 45.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### supertrend | BTCUSD | H1
WR=44.2%  Sharpe=-2.78  MaxDD=72.3%  Trades=351

**Parameter Tweaks:**
- Win rate 44.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 72.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

---

## ❌ Errors / Skipped
