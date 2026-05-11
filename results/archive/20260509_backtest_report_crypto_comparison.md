# Overnight Backtest Report — 09 May 2026

Generated: 2026-05-09 09:34 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 0 |
| ⚠️ REVIEW | 6 |
| ❌ ERROR/SKIP | 6 |
| **Total combos** | **12** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|

---

## ⚠️ Strategies Needing Review


### donchian_trend | BTCUSD | D1
WR=58.9%  Sharpe=2.92  MaxDD=12.4%  Trades=73

**Parameter Tweaks:**
- Win rate 58.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### donchian_trend | BTCUSD | H4
WR=56.4%  Sharpe=0.56  MaxDD=25.8%  Trades=307

**Parameter Tweaks:**
- Win rate 56.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 25.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### donchian_trend | ETHUSD | H4
WR=52.4%  Sharpe=-0.56  MaxDD=2.8%  Trades=340

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### donchian_trend | ETHUSD | H1
WR=48.7%  Sharpe=-2.62  MaxDD=10.7%  Trades=1152

**Parameter Tweaks:**
- Win rate 48.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.62 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### donchian_trend | BTCUSD | H1
WR=47.9%  Sharpe=-1.41  MaxDD=93.1%  Trades=1105

**Parameter Tweaks:**
- Win rate 47.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 93.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### donchian_trend | ETHUSD | D1
WR=46.5%  Sharpe=-0.97  MaxDD=2.9%  Trades=86

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

---

## ❌ Errors / Skipped

- supertrend | BTCUSD | H1 → ERROR: 1
- supertrend | BTCUSD | H4 → ERROR: 1
- supertrend | BTCUSD | D1 → ERROR: 1
- supertrend | ETHUSD | H1 → ERROR: 1
- supertrend | ETHUSD | H4 → ERROR: 1
- supertrend | ETHUSD | D1 → ERROR: 1