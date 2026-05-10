# Overnight Backtest Report — 28 April 2026

Generated: 2026-04-28 01:12 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 6 |
| ⚠️ REVIEW | 118 |
| ❌ ERROR/SKIP | 2 |
| **Total combos** | **126** |

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

### dual_ema_fractal | XAUUSD | D1
WR=58.5%  Sharpe=3.54  MaxDD=13.6%  Trades=94

**Parameter Tweaks:**
- Win rate 58.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### moving_average_crossover | EURUSD | D1
WR=58.3%  Sharpe=0.76  MaxDD=1.9%  Trades=12

**Parameter Tweaks:**
- Win rate 58.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.76 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H4
WR=58.2%  Sharpe=-0.21  MaxDD=10.6%  Trades=122

**Parameter Tweaks:**
- Win rate 58.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.21 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H4
WR=57.4%  Sharpe=-0.93  MaxDD=1.3%  Trades=122

**Parameter Tweaks:**
- Win rate 57.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.93 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### range_breakout | XAUUSD | H4
WR=56.5%  Sharpe=3.09  MaxDD=21.9%  Trades=356

**Parameter Tweaks:**
- Win rate 56.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### orb | XAGUSD | M5
WR=56.1%  Sharpe=0.51  MaxDD=19.9%  Trades=41

**Parameter Tweaks:**
- Win rate 56.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.51 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.08 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### range_breakout | XAUUSD | D1
WR=56.0%  Sharpe=2.43  MaxDD=39.6%  Trades=157

**Parameter Tweaks:**
- Win rate 56.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 39.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### dual_ema_fractal | XAUUSD | H4
WR=54.9%  Sharpe=1.49  MaxDD=10.9%  Trades=175

**Parameter Tweaks:**
- Win rate 54.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### orb | XAGUSD | M15
WR=54.5%  Sharpe=0.77  MaxDD=24.4%  Trades=101

**Parameter Tweaks:**
- Win rate 54.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.77 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.13 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H4
WR=53.9%  Sharpe=1.82  MaxDD=16.9%  Trades=219

**Parameter Tweaks:**
- Win rate 53.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum | XAUUSD | H4
WR=53.0%  Sharpe=1.24  MaxDD=14.3%  Trades=164

**Parameter Tweaks:**
- Win rate 53.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_fractal | GBPUSD | H4
WR=52.9%  Sharpe=-0.47  MaxDD=7.2%  Trades=136

**Parameter Tweaks:**
- Win rate 52.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.47 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.94 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend | USDJPY | H1
WR=52.8%  Sharpe=-0.05  MaxDD=5.2%  Trades=142

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.05 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### turtle_soup | EURUSD | D1
WR=52.8%  Sharpe=1.26  MaxDD=6.6%  Trades=125

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_fractal | EURUSD | D1
WR=52.8%  Sharpe=-0.10  MaxDD=3.3%  Trades=72

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.10 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H4
WR=52.5%  Sharpe=-1.17  MaxDD=7.2%  Trades=122

**Parameter Tweaks:**
- Win rate 52.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H4
WR=51.8%  Sharpe=0.28  MaxDD=2.8%  Trades=137

**Parameter Tweaks:**
- Win rate 51.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.04 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | EURUSD | H1
WR=51.6%  Sharpe=-1.09  MaxDD=1.8%  Trades=64

**Parameter Tweaks:**
- Win rate 51.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.09 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | GBPUSD | H4
WR=51.5%  Sharpe=-1.37  MaxDD=8.7%  Trades=173

**Parameter Tweaks:**
- Win rate 51.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H1
WR=51.2%  Sharpe=-2.10  MaxDD=17.3%  Trades=586

**Parameter Tweaks:**
- Win rate 51.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.10 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend | EURUSD | M30
WR=50.9%  Sharpe=-2.16  MaxDD=5.0%  Trades=273

**Parameter Tweaks:**
- Win rate 50.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.16 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H1
WR=50.6%  Sharpe=-0.35  MaxDD=44.9%  Trades=731

**Parameter Tweaks:**
- Win rate 50.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 44.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.35 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H1
WR=50.5%  Sharpe=-0.79  MaxDD=46.7%  Trades=669

**Parameter Tweaks:**
- Win rate 50.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 46.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.79 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | M30
WR=50.4%  Sharpe=-2.15  MaxDD=20.7%  Trades=1241

**Parameter Tweaks:**
- Win rate 50.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.15 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | GBPUSD | H1
WR=50.1%  Sharpe=-2.08  MaxDD=22.6%  Trades=889

**Parameter Tweaks:**
- Win rate 50.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.08 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend | EURUSD | H4
WR=50.0%  Sharpe=-1.90  MaxDD=4.2%  Trades=42

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.90 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | M30
WR=49.8%  Sharpe=-0.72  MaxDD=77.4%  Trades=1114

**Parameter Tweaks:**
- Win rate 49.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 77.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.72 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | GBPUSD | M30
WR=49.6%  Sharpe=-2.57  MaxDD=26.7%  Trades=1081

**Parameter Tweaks:**
- Win rate 49.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.57 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | H1
WR=49.3%  Sharpe=-2.35  MaxDD=14.1%  Trades=594

**Parameter Tweaks:**
- Win rate 49.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.35 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | GBPUSD | M30
WR=49.2%  Sharpe=-3.13  MaxDD=4.3%  Trades=130

**Parameter Tweaks:**
- Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | M15
WR=49.2%  Sharpe=-1.30  MaxDD=85.5%  Trades=1111

**Parameter Tweaks:**
- Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 85.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.30 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H1
WR=49.2%  Sharpe=-2.01  MaxDD=27.5%  Trades=1049

**Parameter Tweaks:**
- Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 27.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.01 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup | EURUSD | M30
WR=49.1%  Sharpe=-3.23  MaxDD=24.1%  Trades=1072

**Parameter Tweaks:**
- Win rate 49.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.23 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | EURUSD | H4
WR=49.0%  Sharpe=-1.10  MaxDD=12.7%  Trades=310

**Parameter Tweaks:**
- Win rate 49.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.10 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | GBPUSD | H1
WR=48.8%  Sharpe=-2.28  MaxDD=19.9%  Trades=641

**Parameter Tweaks:**
- Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M15
WR=48.7%  Sharpe=-1.29  MaxDD=90.3%  Trades=1132

**Parameter Tweaks:**
- Win rate 48.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 90.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.29 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | EURUSD | M15
WR=48.5%  Sharpe=-3.40  MaxDD=4.8%  Trades=231

**Parameter Tweaks:**
- Win rate 48.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.40 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | M15
WR=48.4%  Sharpe=-1.94  MaxDD=88.2%  Trades=956

**Parameter Tweaks:**
- Win rate 48.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 88.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.94 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H1
WR=48.2%  Sharpe=-1.11  MaxDD=81.8%  Trades=989

**Parameter Tweaks:**
- Win rate 48.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 81.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.11 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | M30
WR=48.0%  Sharpe=-2.26  MaxDD=110.0%  Trades=1122

**Parameter Tweaks:**
- Win rate 48.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 110.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.26 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### moving_average_crossover | USDJPY | D1
WR=48.0%  Sharpe=0.18  MaxDD=5.2%  Trades=25

**Parameter Tweaks:**
- Win rate 48.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.18 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.03 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### gold_momentum_breakout | GBPUSD | M30
WR=47.9%  Sharpe=-3.39  MaxDD=37.2%  Trades=1191

**Parameter Tweaks:**
- Win rate 47.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 37.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.39 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | XAUUSD | M30
WR=47.8%  Sharpe=-1.92  MaxDD=227.5%  Trades=2154

**Parameter Tweaks:**
- Win rate 47.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 227.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.92 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H1
WR=47.7%  Sharpe=-1.60  MaxDD=60.0%  Trades=541

**Parameter Tweaks:**
- Win rate 47.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 60.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | EURUSD | H4
WR=47.6%  Sharpe=-1.54  MaxDD=6.7%  Trades=164

**Parameter Tweaks:**
- Win rate 47.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.54 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USDJPY | D1
WR=47.5%  Sharpe=-1.22  MaxDD=11.7%  Trades=40

**Parameter Tweaks:**
- Win rate 47.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### bb_mean_reversion | EURUSD | H1
WR=47.4%  Sharpe=-2.02  MaxDD=12.3%  Trades=580

**Parameter Tweaks:**
- Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.02 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | EURUSD | H1
WR=47.4%  Sharpe=-2.28  MaxDD=30.9%  Trades=1331

**Parameter Tweaks:**
- Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 30.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H1
WR=47.3%  Sharpe=-2.31  MaxDD=18.4%  Trades=613

**Parameter Tweaks:**
- Win rate 47.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | XAUUSD | H1
WR=47.1%  Sharpe=-1.33  MaxDD=130.9%  Trades=1345

**Parameter Tweaks:**
- Win rate 47.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 130.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.33 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | M30
WR=47.0%  Sharpe=-3.23  MaxDD=19.6%  Trades=797

**Parameter Tweaks:**
- Win rate 47.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.23 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M30
WR=46.9%  Sharpe=-2.78  MaxDD=18.8%  Trades=895

**Parameter Tweaks:**
- Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.78 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | EURUSD | M30
WR=46.9%  Sharpe=-3.93  MaxDD=4.3%  Trades=128

**Parameter Tweaks:**
- Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.93 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | M30
WR=46.7%  Sharpe=-3.84  MaxDD=31.9%  Trades=890

**Parameter Tweaks:**
- Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 31.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.84 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### moving_average_crossover | EURUSD | M15
WR=46.6%  Sharpe=-4.17  MaxDD=3.1%  Trades=118

**Parameter Tweaks:**
- Win rate 46.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M30
WR=46.6%  Sharpe=-2.52  MaxDD=154.1%  Trades=1294

**Parameter Tweaks:**
- Win rate 46.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 154.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.52 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H4
WR=46.5%  Sharpe=-2.66  MaxDD=39.0%  Trades=174

**Parameter Tweaks:**
- Win rate 46.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 39.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.66 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | H4
WR=46.4%  Sharpe=-1.40  MaxDD=5.5%  Trades=153

**Parameter Tweaks:**
- Win rate 46.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.40 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | EURUSD | H1
WR=46.3%  Sharpe=-2.22  MaxDD=6.4%  Trades=227

**Parameter Tweaks:**
- Win rate 46.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H1
WR=45.5%  Sharpe=-2.68  MaxDD=16.8%  Trades=602

**Parameter Tweaks:**
- Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.68 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | EURUSD | H1
WR=45.5%  Sharpe=-3.33  MaxDD=28.9%  Trades=908

**Parameter Tweaks:**
- Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 28.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.33 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | M15
WR=45.4%  Sharpe=-4.43  MaxDD=16.3%  Trades=681

**Parameter Tweaks:**
- Win rate 45.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.43 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M15
WR=45.0%  Sharpe=-4.09  MaxDD=17.2%  Trades=849

**Parameter Tweaks:**
- Win rate 45.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.09 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover | USDJPY | H1
WR=44.8%  Sharpe=-1.45  MaxDD=4.5%  Trades=67

**Parameter Tweaks:**
- Win rate 44.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.45 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### turtle_soup | EURUSD | M15
WR=44.6%  Sharpe=-4.43  MaxDD=21.1%  Trades=963

**Parameter Tweaks:**
- Win rate 44.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.43 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H1
WR=44.4%  Sharpe=-3.34  MaxDD=55.2%  Trades=423

**Parameter Tweaks:**
- Win rate 44.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 55.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.34 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H1
WR=44.3%  Sharpe=-3.47  MaxDD=19.5%  Trades=576

**Parameter Tweaks:**
- Win rate 44.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.47 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | EURUSD | H4
WR=42.9%  Sharpe=5.65  MaxDD=0.9%  Trades=14

**Parameter Tweaks:**
- Win rate 42.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter

### orb | EURUSD | M5
WR=42.9%  Sharpe=-6.44  MaxDD=1.5%  Trades=42

**Parameter Tweaks:**
- Win rate 42.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.44 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | EURUSD | M15
WR=42.8%  Sharpe=-4.20  MaxDD=6.2%  Trades=138

**Parameter Tweaks:**
- Win rate 42.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.20 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | M15
WR=42.7%  Sharpe=-5.13  MaxDD=22.9%  Trades=715

**Parameter Tweaks:**
- Win rate 42.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -5.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H1
WR=42.6%  Sharpe=-4.01  MaxDD=4.7%  Trades=437

**Parameter Tweaks:**
- Win rate 42.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.01 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.53 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H4
WR=42.3%  Sharpe=-2.13  MaxDD=7.2%  Trades=123

**Parameter Tweaks:**
- Win rate 42.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | XAUUSD | M30
WR=41.6%  Sharpe=1.57  MaxDD=7.0%  Trades=214

**Parameter Tweaks:**
- Win rate 41.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum | XAUUSD | D1
WR=41.2%  Sharpe=-0.86  MaxDD=54.2%  Trades=85

**Parameter Tweaks:**
- Win rate 41.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 54.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.86 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

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

### rsi_bounce | XAUUSD | H1
WR=39.4%  Sharpe=1.74  MaxDD=8.6%  Trades=104

**Parameter Tweaks:**
- Win rate 39.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### session_momentum | GBPUSD | H1
WR=39.4%  Sharpe=0.98  MaxDD=2.6%  Trades=208

**Parameter Tweaks:**
- Win rate 39.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.98 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum | GBPUSD | M15
WR=39.3%  Sharpe=-1.60  MaxDD=3.3%  Trades=122

**Parameter Tweaks:**
- Win rate 39.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | XAUUSD | M30
WR=39.2%  Sharpe=0.64  MaxDD=14.9%  Trades=158

**Parameter Tweaks:**
- Win rate 39.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.64 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | GBPUSD | D1
WR=38.9%  Sharpe=-1.54  MaxDD=18.3%  Trades=131

**Parameter Tweaks:**
- Win rate 38.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.54 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | D1
WR=38.5%  Sharpe=-1.13  MaxDD=106.4%  Trades=135

**Parameter Tweaks:**
- Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 106.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum | XAUUSD | M15
WR=38.4%  Sharpe=0.57  MaxDD=23.5%  Trades=510

**Parameter Tweaks:**
- Win rate 38.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.57 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.12 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | M30
WR=37.9%  Sharpe=-4.01  MaxDD=66.3%  Trades=651

**Parameter Tweaks:**
- Win rate 37.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 66.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.01 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### stoch_divergence | EURUSD | M30
WR=37.7%  Sharpe=-0.77  MaxDD=5.9%  Trades=586

**Parameter Tweaks:**
- Win rate 37.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.77 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.90 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | GBPUSD | M30
WR=37.7%  Sharpe=-0.31  MaxDD=7.5%  Trades=236

**Parameter Tweaks:**
- Win rate 37.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.96 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | XAUUSD | M30
WR=37.6%  Sharpe=0.74  MaxDD=16.6%  Trades=415

**Parameter Tweaks:**
- Win rate 37.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.74 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | EURUSD | H1
WR=37.2%  Sharpe=-0.65  MaxDD=1.8%  Trades=113

**Parameter Tweaks:**
- Win rate 37.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.65 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### stoch_divergence | USDJPY | H4
WR=37.0%  Sharpe=0.62  MaxDD=4.7%  Trades=100

**Parameter Tweaks:**
- Win rate 37.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.62 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum | XAUUSD | M15
WR=36.3%  Sharpe=0.37  MaxDD=11.9%  Trades=179

**Parameter Tweaks:**
- Win rate 36.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.37 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.06 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum | GBPUSD | H1
WR=36.0%  Sharpe=0.22  MaxDD=2.4%  Trades=75

**Parameter Tweaks:**
- Win rate 36.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.03 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H4
WR=36.0%  Sharpe=1.36  MaxDD=37.1%  Trades=292

**Parameter Tweaks:**
- Win rate 36.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 37.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### hikkake_trap | EURUSD | H1
WR=35.8%  Sharpe=-1.03  MaxDD=13.9%  Trades=988

**Parameter Tweaks:**
- Win rate 35.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.03 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | XAUUSD | D1
WR=35.7%  Sharpe=0.59  MaxDD=12.0%  Trades=14

**Parameter Tweaks:**
- Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.59 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum | EURUSD | M30
WR=35.6%  Sharpe=-1.50  MaxDD=5.7%  Trades=331

**Parameter Tweaks:**
- Win rate 35.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.50 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum | GBPUSD | M5
WR=35.6%  Sharpe=-4.20  MaxDD=6.6%  Trades=261

**Parameter Tweaks:**
- Win rate 35.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.20 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | GBPUSD | M30
WR=35.5%  Sharpe=-1.72  MaxDD=9.0%  Trades=344

**Parameter Tweaks:**
- Win rate 35.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.72 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | EURUSD | M15
WR=35.1%  Sharpe=-2.31  MaxDD=9.1%  Trades=518

**Parameter Tweaks:**
- Win rate 35.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.31 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H1
WR=35.1%  Sharpe=-0.98  MaxDD=112.9%  Trades=1209

**Parameter Tweaks:**
- Win rate 35.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 112.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.98 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | USDJPY | D1
WR=34.5%  Sharpe=-4.04  MaxDD=45.0%  Trades=139

**Parameter Tweaks:**
- Win rate 34.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 45.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.04 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### stoch_divergence | EURUSD | H4
WR=34.5%  Sharpe=-0.63  MaxDD=3.8%  Trades=58

**Parameter Tweaks:**
- Win rate 34.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.63 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | XAUUSD | M30
WR=34.0%  Sharpe=-1.17  MaxDD=143.9%  Trades=1768

**Parameter Tweaks:**
- Win rate 34.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 143.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H1
WR=33.9%  Sharpe=-1.52  MaxDD=26.5%  Trades=1012

**Parameter Tweaks:**
- Win rate 33.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.52 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stoch_divergence | EURUSD | H1
WR=33.6%  Sharpe=-1.91  MaxDD=8.3%  Trades=286

**Parameter Tweaks:**
- Win rate 33.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.91 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### stoch_divergence | USDJPY | H1
WR=33.1%  Sharpe=-0.58  MaxDD=9.8%  Trades=257

**Parameter Tweaks:**
- Win rate 33.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.58 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.91 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### vwap_momentum | GBPUSD | M15
WR=32.8%  Sharpe=-3.08  MaxDD=15.0%  Trades=542

**Parameter Tweaks:**
- Win rate 32.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.08 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### vwap_momentum | EURUSD | M5
WR=31.5%  Sharpe=-5.52  MaxDD=5.5%  Trades=219

**Parameter Tweaks:**
- Win rate 31.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.52 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPUSD | H1
WR=30.8%  Sharpe=-2.17  MaxDD=6.0%  Trades=104

**Parameter Tweaks:**
- Win rate 30.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | EURUSD | M30
WR=30.7%  Sharpe=-4.32  MaxDD=5.3%  Trades=137

**Parameter Tweaks:**
- Win rate 30.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.32 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPUSD | M30
WR=28.0%  Sharpe=-4.38  MaxDD=6.4%  Trades=125

**Parameter Tweaks:**
- Win rate 28.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.38 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

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
WR=25.6%  Sharpe=0.69  MaxDD=38.6%  Trades=176

**Parameter Tweaks:**
- Win rate 25.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 38.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.69 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

---

## ❌ Errors / Skipped

- cot_sentiment | XAUUSD | W1 → SKIP: insufficient_data
- cot_sentiment | EURUSD | W1 → SKIP: insufficient_data