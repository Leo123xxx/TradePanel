# Overnight Backtest Report — 26 April 2026

Generated: 2026-04-26 11:21 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 6 |
| ⚠️ REVIEW | 131 |
| ❌ ERROR/SKIP | 28 |
| **Total combos** | **165** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| moving_average_crossover | EURUSD | H4 | T1 | 71.4 | 4.00 | 0.3 | 7 | 1.87 |
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 70.8 | 4.66 | 6.2 | 247 | 3.16 |
| macd_trend | USDJPY | H4 | T1 | 68.3 | 3.95 | 1.7 | 60 | 1.79 |
| moving_average_crossover | GBPUSD | H4 | T1 | 66.7 | 4.36 | 0.8 | 15 | 2.28 |
| gold_momentum_breakout | XAUUSD | D1 | T1 | 60.9 | 2.21 | 11.3 | 46 | 1.43 |
| moving_average_crossover | USDJPY | H4 | T1 | 60.0 | 2.30 | 3.8 | 30 | 1.40 |

---

## ⚠️ Strategies Needing Review


### ema_ribbon_trend | BTCUSD | D1
WR=59.3%  Sharpe=3.71  MaxDD=5.3%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### macd_trend | EURUSD | D1
WR=59.0%  Sharpe=1.96  MaxDD=2.6%  Trades=39

**Parameter Tweaks:**
- Win rate 59.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### moving_average_crossover | EURUSD | D1
WR=58.3%  Sharpe=0.76  MaxDD=1.9%  Trades=12

**Parameter Tweaks:**
- Win rate 58.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.76 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H4
WR=58.3%  Sharpe=-0.14  MaxDD=10.6%  Trades=120

**Parameter Tweaks:**
- Win rate 58.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.14 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H4
WR=57.9%  Sharpe=-0.83  MaxDD=1.3%  Trades=121

**Parameter Tweaks:**
- Win rate 57.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.83 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.88 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | D1
WR=57.8%  Sharpe=2.94  MaxDD=22.7%  Trades=109

**Parameter Tweaks:**
- Win rate 57.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### rsi_pullback | USDJPY | H4
WR=56.9%  Sharpe=1.79  MaxDD=3.3%  Trades=232

**Parameter Tweaks:**
- Win rate 56.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### range_breakout | XAUUSD | D1
WR=56.7%  Sharpe=2.62  MaxDD=39.6%  Trades=157

**Parameter Tweaks:**
- Win rate 56.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 39.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### range_breakout | XAUUSD | H4
WR=56.6%  Sharpe=3.16  MaxDD=21.9%  Trades=355

**Parameter Tweaks:**
- Win rate 56.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### orb | XAGUSD | M15
WR=55.3%  Sharpe=0.91  MaxDD=23.1%  Trades=94

**Parameter Tweaks:**
- Win rate 55.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.91 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H4
WR=54.8%  Sharpe=1.09  MaxDD=9.6%  Trades=221

**Parameter Tweaks:**
- Win rate 54.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Profit factor 1.19 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H4
WR=54.1%  Sharpe=2.00  MaxDD=16.9%  Trades=218

**Parameter Tweaks:**
- Win rate 54.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum | XAUUSD | H4
WR=53.0%  Sharpe=1.24  MaxDD=14.3%  Trades=164

**Parameter Tweaks:**
- Win rate 53.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### orb | XAGUSD | M5
WR=52.9%  Sharpe=0.16  MaxDD=20.5%  Trades=34

**Parameter Tweaks:**
- Win rate 52.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.16 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### macd_trend | USDJPY | H1
WR=52.8%  Sharpe=-0.05  MaxDD=5.2%  Trades=142

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.05 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### turtle_soup | EURUSD | D1
WR=52.8%  Sharpe=1.21  MaxDD=6.6%  Trades=125

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### rsi_extremes_scalp | XAUUSD | M5
WR=52.6%  Sharpe=0.13  MaxDD=18.6%  Trades=519

**Parameter Tweaks:**
- Win rate 52.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H4
WR=52.5%  Sharpe=-1.17  MaxDD=7.2%  Trades=122

**Parameter Tweaks:**
- Win rate 52.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | D1
WR=52.1%  Sharpe=-0.04  MaxDD=6.4%  Trades=94

**Parameter Tweaks:**
- Win rate 52.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | EURUSD | H1
WR=51.6%  Sharpe=-1.09  MaxDD=1.8%  Trades=64

**Parameter Tweaks:**
- Win rate 51.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.09 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_pullback | XAUUSD | D1
WR=51.5%  Sharpe=0.78  MaxDD=26.8%  Trades=134

**Parameter Tweaks:**
- Win rate 51.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.78 < 1.0 → reduce lot size on this pair or pause strategy

### turtle_soup | GBPUSD | H4
WR=51.5%  Sharpe=-1.37  MaxDD=8.7%  Trades=173

**Parameter Tweaks:**
- Win rate 51.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H1
WR=51.2%  Sharpe=-1.84  MaxDD=18.1%  Trades=719

**Parameter Tweaks:**
- Win rate 51.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.84 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | XAUUSD | H4
WR=50.9%  Sharpe=0.86  MaxDD=24.3%  Trades=281

**Parameter Tweaks:**
- Win rate 50.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.86 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.19 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H4
WR=50.9%  Sharpe=-0.10  MaxDD=4.4%  Trades=175

**Parameter Tweaks:**
- Win rate 50.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.10 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H1
WR=50.7%  Sharpe=-1.02  MaxDD=77.2%  Trades=813

**Parameter Tweaks:**
- Win rate 50.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 77.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.02 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H1
WR=50.4%  Sharpe=-0.41  MaxDD=44.9%  Trades=726

**Parameter Tweaks:**
- Win rate 50.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 44.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.41 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | GBPUSD | H1
WR=50.2%  Sharpe=-2.05  MaxDD=22.2%  Trades=887

**Parameter Tweaks:**
- Win rate 50.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.05 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_scalp | XAUUSD | M5
WR=50.1%  Sharpe=-0.42  MaxDD=21.3%  Trades=347

**Parameter Tweaks:**
- Win rate 50.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.42 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### moving_average_crossover | USDJPY | D1
WR=50.0%  Sharpe=0.20  MaxDD=5.2%  Trades=24

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.20 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.03 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend | EURUSD | H4
WR=50.0%  Sharpe=-1.90  MaxDD=4.2%  Trades=42

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.90 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H4
WR=49.4%  Sharpe=-1.53  MaxDD=10.1%  Trades=166

**Parameter Tweaks:**
- Win rate 49.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.53 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | H1
WR=49.3%  Sharpe=-2.36  MaxDD=14.1%  Trades=592

**Parameter Tweaks:**
- Win rate 49.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.36 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H1
WR=49.2%  Sharpe=-2.00  MaxDD=27.5%  Trades=1047

**Parameter Tweaks:**
- Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 27.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.00 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | M15
WR=49.2%  Sharpe=-1.31  MaxDD=84.8%  Trades=1098

**Parameter Tweaks:**
- Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 84.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | USDJPY | H1
WR=49.0%  Sharpe=-0.89  MaxDD=20.4%  Trades=680

**Parameter Tweaks:**
- Win rate 49.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.89 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### range_breakout | EURUSD | H4
WR=48.9%  Sharpe=-1.11  MaxDD=12.7%  Trades=309

**Parameter Tweaks:**
- Win rate 48.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.11 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | XAUUSD | M1
WR=48.8%  Sharpe=-1.91  MaxDD=168.8%  Trades=2637

**Parameter Tweaks:**
- Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 168.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.91 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | GBPUSD | H1
WR=48.8%  Sharpe=-2.27  MaxDD=19.9%  Trades=639

**Parameter Tweaks:**
- Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.27 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M15
WR=48.8%  Sharpe=-1.24  MaxDD=90.3%  Trades=1121

**Parameter Tweaks:**
- Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 90.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.24 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | M15
WR=48.6%  Sharpe=-1.90  MaxDD=88.2%  Trades=949

**Parameter Tweaks:**
- Win rate 48.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 88.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.90 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H1
WR=48.3%  Sharpe=-1.13  MaxDD=81.8%  Trades=986

**Parameter Tweaks:**
- Win rate 48.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 81.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | EURUSD | M15
WR=48.2%  Sharpe=-3.44  MaxDD=4.8%  Trades=228

**Parameter Tweaks:**
- Win rate 48.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.44 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | M5
WR=48.2%  Sharpe=-2.23  MaxDD=50.8%  Trades=313

**Parameter Tweaks:**
- Win rate 48.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 50.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.23 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### fast_ma_scalper | XAUUSD | M1
WR=47.9%  Sharpe=-2.35  MaxDD=188.0%  Trades=2414

**Parameter Tweaks:**
- Win rate 47.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 188.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.35 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H1
WR=47.8%  Sharpe=-1.55  MaxDD=60.0%  Trades=540

**Parameter Tweaks:**
- Win rate 47.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 60.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.55 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### fast_ma_scalper | XAUUSD | M5
WR=47.6%  Sharpe=-0.94  MaxDD=46.9%  Trades=473

**Parameter Tweaks:**
- Win rate 47.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 46.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.94 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | EURUSD | H4
WR=47.6%  Sharpe=-1.54  MaxDD=6.7%  Trades=164

**Parameter Tweaks:**
- Win rate 47.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.54 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | H1
WR=47.5%  Sharpe=-2.00  MaxDD=12.3%  Trades=579

**Parameter Tweaks:**
- Win rate 47.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.00 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USDJPY | D1
WR=47.5%  Sharpe=-1.22  MaxDD=11.7%  Trades=40

**Parameter Tweaks:**
- Win rate 47.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H1
WR=47.4%  Sharpe=-2.29  MaxDD=18.4%  Trades=612

**Parameter Tweaks:**
- Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.29 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | EURUSD | H1
WR=47.3%  Sharpe=-2.30  MaxDD=30.9%  Trades=1327

**Parameter Tweaks:**
- Win rate 47.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 30.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.30 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | XAUUSD | H1
WR=47.1%  Sharpe=-1.36  MaxDD=130.9%  Trades=1342

**Parameter Tweaks:**
- Win rate 47.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 130.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.36 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### volatility_breakout_scalp | XAUUSD | M5
WR=46.9%  Sharpe=-0.82  MaxDD=78.1%  Trades=1208

**Parameter Tweaks:**
- Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 78.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.82 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | H4
WR=46.7%  Sharpe=-1.31  MaxDD=5.3%  Trades=152

**Parameter Tweaks:**
- Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | EURUSD | M15
WR=46.6%  Sharpe=-4.17  MaxDD=3.1%  Trades=118

**Parameter Tweaks:**
- Win rate 46.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H4
WR=46.5%  Sharpe=-2.66  MaxDD=39.0%  Trades=174

**Parameter Tweaks:**
- Win rate 46.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 39.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.66 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | EURUSD | H1
WR=46.5%  Sharpe=-2.17  MaxDD=6.4%  Trades=226

**Parameter Tweaks:**
- Win rate 46.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | EURUSD | H1
WR=45.5%  Sharpe=-3.32  MaxDD=28.7%  Trades=904

**Parameter Tweaks:**
- Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 28.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.32 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M15
WR=45.2%  Sharpe=-4.03  MaxDD=17.0%  Trades=840

**Parameter Tweaks:**
- Win rate 45.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.03 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### volatility_breakout_scalp | XAUUSD | M1
WR=45.1%  Sharpe=-2.50  MaxDD=402.0%  Trades=4533

**Parameter Tweaks:**
- Win rate 45.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 402.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.50 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H1
WR=44.9%  Sharpe=-3.04  MaxDD=22.7%  Trades=724

**Parameter Tweaks:**
- Win rate 44.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | M15
WR=44.9%  Sharpe=-4.79  MaxDD=22.4%  Trades=867

**Parameter Tweaks:**
- Win rate 44.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.79 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | USDJPY | H1
WR=44.8%  Sharpe=-1.45  MaxDD=4.5%  Trades=67

**Parameter Tweaks:**
- Win rate 44.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.45 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H1
WR=44.8%  Sharpe=-3.27  MaxDD=55.2%  Trades=420

**Parameter Tweaks:**
- Win rate 44.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 55.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.27 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rsi_extremes_scalp | USDJPY | M5
WR=44.7%  Sharpe=-4.01  MaxDD=6.2%  Trades=338

**Parameter Tweaks:**
- Win rate 44.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.01 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_pullback | XAUUSD | H1
WR=44.4%  Sharpe=-2.14  MaxDD=180.7%  Trades=1143

**Parameter Tweaks:**
- Win rate 44.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 180.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.14 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | EURUSD | M15
WR=44.3%  Sharpe=-4.47  MaxDD=21.0%  Trades=953

**Parameter Tweaks:**
- Win rate 44.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.47 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H1
WR=44.2%  Sharpe=-3.46  MaxDD=19.4%  Trades=574

**Parameter Tweaks:**
- Win rate 44.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.46 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | EURUSD | M15
WR=43.4%  Sharpe=-4.02  MaxDD=5.9%  Trades=136

**Parameter Tweaks:**
- Win rate 43.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.02 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | M1
WR=43.1%  Sharpe=-4.03  MaxDD=172.3%  Trades=1448

**Parameter Tweaks:**
- Win rate 43.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 172.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.03 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.53 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H1
WR=42.5%  Sharpe=-4.04  MaxDD=4.7%  Trades=435

**Parameter Tweaks:**
- Win rate 42.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.53 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### orb | EURUSD | M5
WR=42.5%  Sharpe=-6.23  MaxDD=1.4%  Trades=40

**Parameter Tweaks:**
- Win rate 42.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.23 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | M15
WR=42.4%  Sharpe=-5.54  MaxDD=31.4%  Trades=910

**Parameter Tweaks:**
- Win rate 42.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 31.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -5.54 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H4
WR=41.8%  Sharpe=-2.28  MaxDD=7.2%  Trades=122

**Parameter Tweaks:**
- Win rate 41.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_zero_scalp | USDJPY | M5
WR=41.0%  Sharpe=-5.86  MaxDD=5.5%  Trades=251

**Parameter Tweaks:**
- Win rate 41.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.86 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### dual_ema_momentum | XAUUSD | D1
WR=41.0%  Sharpe=-0.53  MaxDD=54.2%  Trades=83

**Parameter Tweaks:**
- Win rate 41.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 54.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.53 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | EURUSD | D1
WR=40.6%  Sharpe=-1.39  MaxDD=10.9%  Trades=123

**Parameter Tweaks:**
- Win rate 40.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.39 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | XAUUSD | H1
WR=40.3%  Sharpe=1.21  MaxDD=8.8%  Trades=233

**Parameter Tweaks:**
- Win rate 40.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### moving_average_crossover | GBPUSD | H1
WR=40.0%  Sharpe=-5.68  MaxDD=5.4%  Trades=75

**Parameter Tweaks:**
- Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.68 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum | GBPUSD | M15
WR=39.7%  Sharpe=-1.53  MaxDD=3.3%  Trades=121

**Parameter Tweaks:**
- Win rate 39.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.53 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum | GBPUSD | H1
WR=39.4%  Sharpe=0.98  MaxDD=2.6%  Trades=208

**Parameter Tweaks:**
- Win rate 39.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.98 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### cot_sentiment | GBPUSD | D1
WR=38.9%  Sharpe=-1.57  MaxDD=18.3%  Trades=131

**Parameter Tweaks:**
- Win rate 38.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.57 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H1
WR=38.8%  Sharpe=1.53  MaxDD=8.6%  Trades=103

**Parameter Tweaks:**
- Win rate 38.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### bb_squeeze_scalp | GBPUSD | M5
WR=38.8%  Sharpe=-6.60  MaxDD=5.5%  Trades=188

**Parameter Tweaks:**
- Win rate 38.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | XAUUSD | M15
WR=38.6%  Sharpe=0.65  MaxDD=23.5%  Trades=508

**Parameter Tweaks:**
- Win rate 38.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.65 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.13 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### fast_ma_scalper | USDJPY | M5
WR=38.5%  Sharpe=-5.73  MaxDD=7.5%  Trades=314

**Parameter Tweaks:**
- Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.73 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | D1
WR=38.5%  Sharpe=-1.13  MaxDD=106.4%  Trades=135

**Parameter Tweaks:**
- Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 106.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | EURUSD | H4
WR=38.5%  Sharpe=4.84  MaxDD=0.9%  Trades=13

**Parameter Tweaks:**
- Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter

### fast_ma_scalper | GBPUSD | M5
WR=38.0%  Sharpe=-5.41  MaxDD=9.8%  Trades=392

**Parameter Tweaks:**
- Win rate 38.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.41 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | EURUSD | H1
WR=37.5%  Sharpe=-0.57  MaxDD=1.8%  Trades=112

**Parameter Tweaks:**
- Win rate 37.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.57 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | XAUUSD | M15
WR=36.5%  Sharpe=0.45  MaxDD=11.9%  Trades=178

**Parameter Tweaks:**
- Win rate 36.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.45 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.08 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum | GBPUSD | H1
WR=36.0%  Sharpe=0.22  MaxDD=2.4%  Trades=75

**Parameter Tweaks:**
- Win rate 36.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.03 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### hikkake_trap | EURUSD | H1
WR=35.9%  Sharpe=-1.00  MaxDD=13.9%  Trades=986

**Parameter Tweaks:**
- Win rate 35.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.00 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H4
WR=35.7%  Sharpe=1.34  MaxDD=37.1%  Trades=291

**Parameter Tweaks:**
- Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 37.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### cot_sentiment | XAUUSD | D1
WR=35.7%  Sharpe=0.59  MaxDD=12.0%  Trades=14

**Parameter Tweaks:**
- Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.59 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### stoch_divergence | USDJPY | H4
WR=35.2%  Sharpe=0.33  MaxDD=4.7%  Trades=91

**Parameter Tweaks:**
- Win rate 35.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.33 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.05 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### vwap_momentum | EURUSD | M15
WR=35.1%  Sharpe=-2.31  MaxDD=9.1%  Trades=516

**Parameter Tweaks:**
- Win rate 35.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H1
WR=35.0%  Sharpe=-1.04  MaxDD=112.9%  Trades=1203

**Parameter Tweaks:**
- Win rate 35.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 112.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | USDJPY | D1
WR=34.5%  Sharpe=-4.04  MaxDD=45.0%  Trades=139

**Parameter Tweaks:**
- Win rate 34.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 45.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### vwap_momentum | GBPUSD | M5
WR=34.4%  Sharpe=-4.53  MaxDD=6.6%  Trades=244

**Parameter Tweaks:**
- Win rate 34.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.53 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### volatility_breakout_scalp | BTCUSD | M5
WR=34.3%  Sharpe=-6.53  MaxDD=117.3%  Trades=1485

**Parameter Tweaks:**
- Win rate 34.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 117.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -6.53 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.38 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### macd_zero_scalp | BTCUSD | M5
WR=34.3%  Sharpe=-6.55  MaxDD=37.2%  Trades=542

**Parameter Tweaks:**
- Win rate 34.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 37.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -6.55 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### stoch_divergence | EURUSD | H4
WR=34.0%  Sharpe=-0.60  MaxDD=4.1%  Trades=47

**Parameter Tweaks:**
- Win rate 34.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H1
WR=34.0%  Sharpe=-1.49  MaxDD=26.3%  Trades=1008

**Parameter Tweaks:**
- Win rate 34.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.49 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stoch_divergence | EURUSD | H1
WR=33.6%  Sharpe=-1.89  MaxDD=7.5%  Trades=256

**Parameter Tweaks:**
- Win rate 33.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.89 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_zero_scalp | EURUSD | M5
WR=33.3%  Sharpe=-7.79  MaxDD=6.1%  Trades=261

**Parameter Tweaks:**
- Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.79 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### stoch_divergence | USDJPY | H1
WR=33.0%  Sharpe=-0.30  MaxDD=8.4%  Trades=227

**Parameter Tweaks:**
- Win rate 33.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.30 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.95 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### vwap_momentum | GBPUSD | M15
WR=32.9%  Sharpe=-3.06  MaxDD=15.0%  Trades=538

**Parameter Tweaks:**
- Win rate 32.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.06 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### fast_ma_scalper | EURUSD | M5
WR=32.7%  Sharpe=-7.21  MaxDD=9.2%  Trades=382

**Parameter Tweaks:**
- Win rate 32.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.21 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | GBPUSD | M5
WR=32.2%  Sharpe=-7.86  MaxDD=11.8%  Trades=351

**Parameter Tweaks:**
- Win rate 32.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.86 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp | EURUSD | M5
WR=31.6%  Sharpe=-9.10  MaxDD=5.5%  Trades=187

**Parameter Tweaks:**
- Win rate 31.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -9.10 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.25 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPUSD | H1
WR=30.8%  Sharpe=-2.17  MaxDD=6.0%  Trades=104

**Parameter Tweaks:**
- Win rate 30.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | EURUSD | M5
WR=30.7%  Sharpe=-5.76  MaxDD=5.3%  Trades=202

**Parameter Tweaks:**
- Win rate 30.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.76 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_zero_scalp | GBPUSD | M5
WR=30.6%  Sharpe=-9.55  MaxDD=9.5%  Trades=265

**Parameter Tweaks:**
- Win rate 30.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -9.55 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.25 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_extremes_scalp | EURUSD | M5
WR=29.7%  Sharpe=-8.72  MaxDD=10.6%  Trades=380

**Parameter Tweaks:**
- Win rate 29.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.72 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.27 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_scalp | EURUSD | M5
WR=29.1%  Sharpe=-8.06  MaxDD=6.5%  Trades=261

**Parameter Tweaks:**
- Win rate 29.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.06 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_scalp | GBPUSD | M5
WR=28.7%  Sharpe=-8.89  MaxDD=11.1%  Trades=293

**Parameter Tweaks:**
- Win rate 28.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.89 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.27 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | EURUSD | M15
WR=27.8%  Sharpe=-5.34  MaxDD=3.4%  Trades=108

**Parameter Tweaks:**
- Win rate 27.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.34 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H4
WR=27.6%  Sharpe=-1.92  MaxDD=11.2%  Trades=29

**Parameter Tweaks:**
- Win rate 27.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.92 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | XAGUSD | D1
WR=26.2%  Sharpe=-7.32  MaxDD=241.7%  Trades=122

**Parameter Tweaks:**
- Win rate 26.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 241.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -7.32 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.34 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### hikkake_trap | XAUUSD | D1
WR=25.7%  Sharpe=0.74  MaxDD=38.6%  Trades=175

**Parameter Tweaks:**
- Win rate 25.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 38.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.74 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### fast_ma_scalper | GBPUSD | M1
WR=18.8%  Sharpe=-14.82  MaxDD=51.9%  Trades=1745

**Parameter Tweaks:**
- Win rate 18.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 51.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -14.82 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.10 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_scalp | GBPUSD | M1
WR=17.9%  Sharpe=-15.57  MaxDD=40.5%  Trades=1320

**Parameter Tweaks:**
- Win rate 17.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 40.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -15.57 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.09 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp | EURUSD | M1
WR=17.7%  Sharpe=-14.77  MaxDD=23.0%  Trades=1028

**Parameter Tweaks:**
- Win rate 17.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -14.77 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.11 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### fast_ma_scalper | EURUSD | M1
WR=17.4%  Sharpe=-13.91  MaxDD=36.9%  Trades=1687

**Parameter Tweaks:**
- Win rate 17.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 36.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -13.91 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.11 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | EURUSD | M1
WR=16.8%  Sharpe=-14.48  MaxDD=40.9%  Trades=1865

**Parameter Tweaks:**
- Win rate 16.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 40.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -14.48 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.10 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_zero_scalp | GBPUSD | M1
WR=16.8%  Sharpe=-16.28  MaxDD=36.3%  Trades=1159

**Parameter Tweaks:**
- Win rate 16.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 36.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -16.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.08 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_scalp | EURUSD | M1
WR=16.3%  Sharpe=-15.76  MaxDD=31.6%  Trades=1378

**Parameter Tweaks:**
- Win rate 16.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 31.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -15.76 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.09 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_zero_scalp | EURUSD | M1
WR=15.4%  Sharpe=-16.66  MaxDD=29.6%  Trades=1256

**Parameter Tweaks:**
- Win rate 15.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 29.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -16.66 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.08 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### volatility_breakout_scalp | ETHUSD | M5
WR=11.8%  Sharpe=-20.08  MaxDD=14.6%  Trades=1581

**Parameter Tweaks:**
- Win rate 11.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -20.08 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.05 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

---

## ❌ Errors / Skipped

- dual_ema_fractal | EURUSD | M30 → SKIP: insufficient_data
- rsi_bounce | EURUSD | M30 → SKIP: insufficient_data
- rsi_bounce | XAUUSD | M30 → SKIP: insufficient_data
- rsi_bounce | GBPUSD | M30 → SKIP: insufficient_data
- moving_average_crossover | EURUSD | M30 → SKIP: insufficient_data
- moving_average_crossover | GBPUSD | M30 → SKIP: insufficient_data
- bb_mean_reversion | XAUUSD | M30 → SKIP: insufficient_data
- bb_mean_reversion | EURUSD | M30 → SKIP: insufficient_data
- stoch_divergence | EURUSD | M30 → SKIP: insufficient_data
- macd_trend | EURUSD | M30 → SKIP: insufficient_data
- gold_momentum_breakout | XAUUSD | M30 → SKIP: insufficient_data
- gold_momentum_breakout | GBPUSD | M30 → SKIP: insufficient_data
- range_breakout | XAUUSD | M30 → SKIP: insufficient_data
- ema_ribbon_trend | BTCUSD | M30 → SKIP: insufficient_data
- cot_sentiment | XAUUSD | W1 → SKIP: insufficient_data
- cot_sentiment | EURUSD | W1 → SKIP: insufficient_data
- session_momentum | XAUUSD | M30 → SKIP: insufficient_data
- session_momentum | GBPUSD | M30 → SKIP: insufficient_data
- rsi_pullback | XAUUSD | M30 → SKIP: insufficient_data
- turtle_soup | EURUSD | M30 → SKIP: insufficient_data
- turtle_soup | GBPUSD | M30 → SKIP: insufficient_data
- dual_ema_momentum | XAUUSD | M30 → SKIP: insufficient_data
- vwap_momentum | GBPUSD | M30 → SKIP: insufficient_data
- vwap_momentum | EURUSD | M30 → SKIP: insufficient_data
- vwap_momentum | XAUUSD | M30 → SKIP: insufficient_data
- hikkake_trap | XAUUSD | M30 → SKIP: insufficient_data
- rvgi_cci_confluence | EURUSD | M30 → SKIP: insufficient_data
- rvgi_cci_confluence | GBPUSD | M30 → SKIP: insufficient_data