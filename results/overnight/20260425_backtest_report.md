# Overnight Backtest Report — 25 April 2026

Generated: 2026-04-25 08:39 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 5 |
| ⚠️ REVIEW | 33 |
| ❌ ERROR/SKIP | 0 |
| **Total combos** | **38** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 70.8 | 4.66 | 6.2 | 247 | 3.16 |
| range_breakout | XAUUSD | H4 | T1 | 56.6 | 3.16 | 21.9 | 355 | 2.04 |
| rsi_pullback | USDJPY | H4 | T2 | 56.4 | 2.16 | 3.3 | 225 | 1.39 |
| orb | XAGUSD | M15 | T2 | 55.3 | 0.91 | 23.1 | 94 | 1.15 |
| rsi_pullback | XAUUSD | H4 | T2 | 50.2 | 1.28 | 20.6 | 277 | 1.31 |

---

## ⚠️ Strategies Needing Review


### ema_ribbon_trend | BTCUSD | H4
WR=58.3%  Sharpe=0.65  MaxDD=9.3%  Trades=120

**Parameter Tweaks:**
- Sharpe 0.65 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 1.11 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H4
WR=57.0%  Sharpe=-0.96  MaxDD=1.3%  Trades=121

**Parameter Tweaks:**
- Sharpe -0.96 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### macd_trend | USDJPY | H1
WR=52.8%  Sharpe=-0.21  MaxDD=5.0%  Trades=142

**Parameter Tweaks:**
- Sharpe -0.21 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### moving_average_crossover | EURUSD | H1
WR=51.6%  Sharpe=-1.09  MaxDD=1.8%  Trades=64

**Parameter Tweaks:**
- Sharpe -1.09 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H1
WR=51.1%  Sharpe=-1.53  MaxDD=16.4%  Trades=697

**Parameter Tweaks:**
- Sharpe -1.53 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H1
WR=50.9%  Sharpe=-0.52  MaxDD=54.8%  Trades=796

**Parameter Tweaks:**
- Max drawdown 54.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.52 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.90 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H1
WR=49.8%  Sharpe=-0.23  MaxDD=28.7%  Trades=490

**Parameter Tweaks:**
- Max drawdown 28.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.23 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.95 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H1
WR=48.4%  Sharpe=-0.68  MaxDD=74.4%  Trades=980

**Parameter Tweaks:**
- Max drawdown 74.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.68 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.88 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H4
WR=48.0%  Sharpe=0.36  MaxDD=21.5%  Trades=100

**Parameter Tweaks:**
- Max drawdown 21.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.36 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 1.07 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | EURUSD | H4
WR=47.6%  Sharpe=-1.73  MaxDD=6.2%  Trades=164

**Parameter Tweaks:**
- Win rate 47.6% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.73 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | GBPUSD | D1
WR=46.9%  Sharpe=-0.35  MaxDD=14.6%  Trades=98

**Parameter Tweaks:**
- Win rate 46.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.35 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.95 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend | EURUSD | H1
WR=46.5%  Sharpe=-1.85  MaxDD=6.2%  Trades=226

**Parameter Tweaks:**
- Win rate 46.5% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.85 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | EURUSD | D1
WR=45.4%  Sharpe=-0.82  MaxDD=11.6%  Trades=97

**Parameter Tweaks:**
- Win rate 45.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.82 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H1
WR=45.3%  Sharpe=-2.24  MaxDD=16.3%  Trades=611

**Parameter Tweaks:**
- Win rate 45.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.24 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### moving_average_crossover | USDJPY | H1
WR=44.8%  Sharpe=-1.45  MaxDD=4.5%  Trades=67

**Parameter Tweaks:**
- Win rate 44.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.45 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### dual_ema_fractal | EURUSD | H1
WR=44.3%  Sharpe=-2.58  MaxDD=20.5%  Trades=709

**Parameter Tweaks:**
- Win rate 44.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.58 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | EURUSD | M15
WR=43.4%  Sharpe=-4.02  MaxDD=5.9%  Trades=136

**Parameter Tweaks:**
- Win rate 43.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.02 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H1
WR=42.3%  Sharpe=-3.23  MaxDD=16.5%  Trades=572

**Parameter Tweaks:**
- Win rate 42.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.23 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum | EURUSD | M15
WR=40.7%  Sharpe=-3.08  MaxDD=9.8%  Trades=523

**Parameter Tweaks:**
- Win rate 40.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.08 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | GBPUSD | H1
WR=40.0%  Sharpe=-5.68  MaxDD=5.4%  Trades=75

**Parameter Tweaks:**
- Win rate 40.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.68 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H1
WR=40.0%  Sharpe=0.66  MaxDD=3.4%  Trades=30

**Parameter Tweaks:**
- Win rate 40.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.66 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 1.11 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | H1
WR=38.9%  Sharpe=0.30  MaxDD=3.1%  Trades=149

**Parameter Tweaks:**
- Win rate 38.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.30 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 1.04 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H1
WR=38.8%  Sharpe=1.53  MaxDD=8.6%  Trades=103

**Parameter Tweaks:**
- Win rate 38.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)

### session_momentum | XAUUSD | H1
WR=37.6%  Sharpe=1.72  MaxDD=6.4%  Trades=234

**Parameter Tweaks:**
- Win rate 37.6% < 48.0% → tighten entry filter (increase ADX min or add regime check)

### vwap_momentum | GBPUSD | M15
WR=37.6%  Sharpe=-4.32  MaxDD=17.2%  Trades=543

**Parameter Tweaks:**
- Win rate 37.6% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.32 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | EURUSD | H1
WR=37.5%  Sharpe=-0.57  MaxDD=1.8%  Trades=112

**Parameter Tweaks:**
- Win rate 37.5% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.57 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | GBPUSD | H1
WR=37.0%  Sharpe=1.70  MaxDD=1.6%  Trades=208

**Parameter Tweaks:**
- Win rate 37.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)

### stoch_divergence | USDJPY | H4
WR=37.0%  Sharpe=0.62  MaxDD=4.7%  Trades=100

**Parameter Tweaks:**
- Win rate 37.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.62 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### cot_sentiment | USDJPY | D1
WR=36.3%  Sharpe=-4.12  MaxDD=44.3%  Trades=102

**Parameter Tweaks:**
- Win rate 36.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 44.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.12 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### hikkake_trap | XAUUSD | H4
WR=35.7%  Sharpe=1.34  MaxDD=37.1%  Trades=291

**Parameter Tweaks:**
- Win rate 35.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 37.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### stoch_divergence | EURUSD | H4
WR=34.5%  Sharpe=-0.63  MaxDD=3.8%  Trades=58

**Parameter Tweaks:**
- Win rate 34.5% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.63 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | XAUUSD | D1
WR=33.3%  Sharpe=-1.56  MaxDD=14.6%  Trades=15

**Parameter Tweaks:**
- Win rate 33.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.56 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | GBPUSD | H1
WR=30.8%  Sharpe=-2.17  MaxDD=6.0%  Trades=104

**Parameter Tweaks:**
- Win rate 30.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 0.8 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

---

## ❌ Errors / Skipped
