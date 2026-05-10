# Overnight Backtest Report — 30 April 2026

Generated: 2026-04-30 15:41 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 18 |
| ⚠️ REVIEW | 99 |
| ❌ ERROR/SKIP | 54 |
| **Total combos** | **173** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| dual_ema_fractal | USOIL | H4 | T1 | 100.0 | 19.64 | 0.0 | 4 | 999.00 |
| ema_ribbon_trend | XAUUSD | H4 | T1 | 100.0 | 19.72 | 0.0 | 2 | 999.00 |
| dual_ema_momentum | USTEC | H1 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| ema_ribbon_trend | ETHUSD | H4 | T1 | 80.0 | 7.16 | 0.1 | 10 | 2.84 |
| turtle_soup | GBPJPY | H1 | T2 | 80.0 | 3.94 | 0.2 | 5 | 2.10 |
| rsi_pullback | AUDUSD | H4 | T2 | 76.9 | 9.79 | 0.5 | 13 | 3.96 |
| turtle_soup | USDCAD | H4 | T2 | 75.0 | 7.23 | 0.0 | 4 | 2.94 |
| rsi_extremes_scalp | USOIL | M15 | T2 | 75.0 | 2.63 | 1.0 | 8 | 1.49 |
| range_breakout | XAUUSD | H4 | T1 | 71.1 | 7.11 | 5.5 | 45 | 4.16 |
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 70.8 | 4.66 | 6.2 | 247 | 3.16 |
| macd_trend | USDJPY | H4 | T1 | 69.2 | 3.46 | 1.7 | 26 | 1.67 |
| orb | GBPJPY | M15 | T2 | 69.2 | 1.68 | 0.4 | 13 | 1.29 |
| range_breakout | USOIL | H4 | T1 | 66.7 | 9.52 | 0.0 | 3 | 5.63 |
| dual_ema_fractal | XAUUSD | H4 | T1 | 65.6 | 4.37 | 5.2 | 64 | 2.02 |
| gold_momentum_breakout | XAUUSD | H4 | T1 | 63.9 | 4.98 | 4.7 | 72 | 2.48 |
| vwap_momentum | EURUSD | H1 | T2 | 63.2 | 8.55 | 0.4 | 19 | 3.26 |
| dual_ema_fractal | XAUUSD | D1 | T1 | 60.7 | 5.69 | 6.3 | 28 | 3.35 |
| macd_trend | GBPJPY | H1 | T1 | 60.0 | 1.93 | 0.6 | 10 | 1.32 |

---

## ⚠️ Strategies Needing Review


### rsi_bounce | XAUUSD | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### bb_mean_reversion | US500 | H1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### macd_trend | USOIL | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | XAUUSD | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### range_breakout | US500 | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### cot_sentiment | XAUUSD | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### turtle_soup | GBPJPY | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | USTEC | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### orb | XAGUSD | M15
WR=59.3%  Sharpe=1.82  MaxDD=12.9%  Trades=81

**Parameter Tweaks:**
- Win rate 59.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### turtle_soup | XAUUSD | H4
WR=57.4%  Sharpe=-0.51  MaxDD=11.0%  Trades=61

**Parameter Tweaks:**
- Win rate 57.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.51 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### bb_mean_reversion | EURUSD | H1
WR=57.1%  Sharpe=2.44  MaxDD=0.3%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_momentum | US500 | H1
WR=57.1%  Sharpe=3.19  MaxDD=0.0%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter

### rvgi_cci_confluence | USDCAD | H4
WR=57.1%  Sharpe=1.26  MaxDD=0.5%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp | GBPJPY | M15
WR=57.1%  Sharpe=-4.25  MaxDD=0.3%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.25 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_pullback | USDJPY | H4
WR=56.9%  Sharpe=1.79  MaxDD=3.3%  Trades=232

**Parameter Tweaks:**
- Win rate 56.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### bb_squeeze_scalp | USDJPY | M15
WR=56.2%  Sharpe=2.30  MaxDD=0.8%  Trades=32

**Parameter Tweaks:**
- Win rate 56.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_fractal | GBPUSD | H4
WR=55.7%  Sharpe=-0.26  MaxDD=3.9%  Trades=61

**Parameter Tweaks:**
- Win rate 55.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.26 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.96 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H4
WR=55.2%  Sharpe=0.62  MaxDD=2.5%  Trades=67

**Parameter Tweaks:**
- Win rate 55.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.62 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H4
WR=55.2%  Sharpe=0.16  MaxDD=1.9%  Trades=58

**Parameter Tweaks:**
- Win rate 55.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.16 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USTEC | H1
WR=54.5%  Sharpe=-1.22  MaxDD=0.4%  Trades=11

**Parameter Tweaks:**
- Win rate 54.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on USTEC unless confirmed by live data

### dual_ema_momentum | GBPJPY | H1
WR=54.5%  Sharpe=0.94  MaxDD=0.8%  Trades=11

**Parameter Tweaks:**
- Win rate 54.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.94 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### macd_trend | USDJPY | H1
WR=53.9%  Sharpe=0.18  MaxDD=2.1%  Trades=89

**Parameter Tweaks:**
- Win rate 53.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.18 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.03 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_pullback | USOIL | H4
WR=53.3%  Sharpe=2.86  MaxDD=5.9%  Trades=15

**Parameter Tweaks:**
- Win rate 53.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 15 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | GBPUSD | H4
WR=52.8%  Sharpe=-0.62  MaxDD=7.0%  Trades=72

**Parameter Tweaks:**
- Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.62 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | XAUUSD | D1
WR=52.2%  Sharpe=1.09  MaxDD=26.8%  Trades=134

**Parameter Tweaks:**
- Win rate 52.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### rsi_pullback | XAUUSD | H4
WR=51.2%  Sharpe=0.99  MaxDD=24.3%  Trades=281

**Parameter Tweaks:**
- Win rate 51.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.99 < 1.0 → reduce lot size on this pair or pause strategy

### macd_trend | USOIL | H1
WR=50.0%  Sharpe=-1.05  MaxDD=2.7%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.05 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on USOIL unless confirmed by live data

### macd_trend | US500 | H1
WR=50.0%  Sharpe=-3.58  MaxDD=0.1%  Trades=8

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.58 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on US500 unless confirmed by live data

### macd_trend | USTEC | H4
WR=50.0%  Sharpe=4.14  MaxDD=0.1%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | AAPL | H4
WR=50.0%  Sharpe=0.60  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.11 — marginal edge, consider disabling on AAPL unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H4
WR=50.0%  Sharpe=-3.22  MaxDD=3.4%  Trades=14

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rsi_pullback | GBPJPY | H4
WR=50.0%  Sharpe=-2.95  MaxDD=1.1%  Trades=16

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.95 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_momentum | XAUUSD | H1
WR=50.0%  Sharpe=0.03  MaxDD=10.3%  Trades=120

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.03 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.00 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | USOIL | H4
WR=50.0%  Sharpe=-1.59  MaxDD=5.2%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.59 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on USOIL unless confirmed by live data

### hikkake_trap | US500 | H4
WR=50.0%  Sharpe=5.42  MaxDD=0.1%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter

### orb | AUDUSD | M15
WR=50.0%  Sharpe=-2.65  MaxDD=0.6%  Trades=14

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.65 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H4
WR=50.0%  Sharpe=-1.37  MaxDD=7.3%  Trades=88

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | H4
WR=50.0%  Sharpe=2.92  MaxDD=0.5%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_extremes_scalp | EURUSD | M15
WR=50.0%  Sharpe=-1.72  MaxDD=0.5%  Trades=38

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.72 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | GBPJPY | M15
WR=50.0%  Sharpe=0.93  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.93 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.18 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_extremes_scalp | AUDUSD | M15
WR=50.0%  Sharpe=0.90  MaxDD=0.1%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.90 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.17 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H4
WR=48.9%  Sharpe=1.51  MaxDD=8.8%  Trades=47

**Parameter Tweaks:**
- Win rate 48.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum | GBPUSD | H1
WR=48.9%  Sharpe=-2.07  MaxDD=6.0%  Trades=188

**Parameter Tweaks:**
- Win rate 48.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.07 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H4
WR=48.9%  Sharpe=-0.66  MaxDD=4.0%  Trades=90

**Parameter Tweaks:**
- Win rate 48.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.66 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.91 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | EURUSD | H4
WR=48.0%  Sharpe=-1.49  MaxDD=2.7%  Trades=73

**Parameter Tweaks:**
- Win rate 48.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.49 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | M15
WR=47.7%  Sharpe=-0.03  MaxDD=8.5%  Trades=86

**Parameter Tweaks:**
- Win rate 47.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.03 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | EURUSD | H4
WR=47.4%  Sharpe=-2.73  MaxDD=2.4%  Trades=19

**Parameter Tweaks:**
- Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.73 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | EURUSD | H4
WR=47.2%  Sharpe=-3.21  MaxDD=3.0%  Trades=36

**Parameter Tweaks:**
- Win rate 47.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.21 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | H1
WR=47.0%  Sharpe=-2.62  MaxDD=4.7%  Trades=168

**Parameter Tweaks:**
- Win rate 47.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.62 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | XAUUSD | M15
WR=46.9%  Sharpe=-4.20  MaxDD=6.7%  Trades=32

**Parameter Tweaks:**
- Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.20 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum | GBPUSD | H1
WR=46.7%  Sharpe=2.82  MaxDD=0.5%  Trades=15

**Parameter Tweaks:**
- Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 15 trades — widen oversold/overbought thresholds or relax ADX filter

### session_momentum | GBPJPY | H1
WR=45.5%  Sharpe=2.67  MaxDD=0.3%  Trades=11

**Parameter Tweaks:**
- Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | EURUSD | H1
WR=44.3%  Sharpe=-2.51  MaxDD=5.2%  Trades=149

**Parameter Tweaks:**
- Win rate 44.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.51 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H4
WR=43.9%  Sharpe=2.30  MaxDD=3.5%  Trades=107

**Parameter Tweaks:**
- Win rate 43.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### orb | EURUSD | M15
WR=42.6%  Sharpe=-3.85  MaxDD=5.3%  Trades=122

**Parameter Tweaks:**
- Win rate 42.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.85 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | EURUSD | D1
WR=42.6%  Sharpe=-0.75  MaxDD=10.7%  Trades=101

**Parameter Tweaks:**
- Win rate 42.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.75 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum | EURUSD | M15
WR=41.1%  Sharpe=-0.91  MaxDD=1.4%  Trades=175

**Parameter Tweaks:**
- Win rate 41.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.91 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.88 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | GBPUSD | M15
WR=41.0%  Sharpe=-5.06  MaxDD=2.0%  Trades=61

**Parameter Tweaks:**
- Win rate 41.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.06 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | USDCAD | H4
WR=40.0%  Sharpe=-4.74  MaxDD=0.2%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.74 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### macd_trend | AUDUSD | H1
WR=40.0%  Sharpe=-2.55  MaxDD=0.2%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.55 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### turtle_soup | AUDUSD | H4
WR=40.0%  Sharpe=-1.90  MaxDD=0.5%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.90 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_momentum | AUDUSD | H1
WR=40.0%  Sharpe=-1.12  MaxDD=0.5%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.12 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### vwap_momentum | XAUUSD | M15
WR=38.8%  Sharpe=0.32  MaxDD=9.7%  Trades=98

**Parameter Tweaks:**
- Win rate 38.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.32 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.05 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | GBPUSD | D1
WR=38.7%  Sharpe=-1.94  MaxDD=18.8%  Trades=106

**Parameter Tweaks:**
- Win rate 38.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.94 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | D1
WR=38.5%  Sharpe=-1.13  MaxDD=106.4%  Trades=135

**Parameter Tweaks:**
- Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 106.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_extremes_scalp | GBPUSD | M15
WR=37.9%  Sharpe=-5.70  MaxDD=1.3%  Trades=29

**Parameter Tweaks:**
- Win rate 37.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.70 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum | GBPUSD | H1
WR=37.5%  Sharpe=0.15  MaxDD=4.0%  Trades=301

**Parameter Tweaks:**
- Win rate 37.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.15 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### hikkake_trap | USOIL | H4
WR=37.5%  Sharpe=1.37  MaxDD=9.3%  Trades=8

**Parameter Tweaks:**
- Win rate 37.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter

### hikkake_trap | XAUUSD | H4
WR=36.1%  Sharpe=1.21  MaxDD=17.7%  Trades=119

**Parameter Tweaks:**
- Win rate 36.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### cot_sentiment | USDJPY | D1
WR=35.7%  Sharpe=-3.59  MaxDD=36.8%  Trades=126

**Parameter Tweaks:**
- Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 36.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.59 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum | EURUSD | H1
WR=33.9%  Sharpe=-1.76  MaxDD=8.0%  Trades=292

**Parameter Tweaks:**
- Win rate 33.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.76 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | AUDUSD | H4
WR=33.3%  Sharpe=-11.41  MaxDD=0.2%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -11.41 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.16 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### bb_mean_reversion | XAUUSD | H1
WR=33.3%  Sharpe=-10.22  MaxDD=2.4%  Trades=9

**Parameter Tweaks:**
- Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -10.22 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.24 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum | USOIL | H1
WR=33.3%  Sharpe=-3.34  MaxDD=2.4%  Trades=9

**Parameter Tweaks:**
- Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.34 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on USOIL unless confirmed by live data

### hikkake_trap | EURUSD | H4
WR=32.7%  Sharpe=-2.15  MaxDD=9.4%  Trades=107

**Parameter Tweaks:**
- Win rate 32.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.15 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum | GBPUSD | M15
WR=32.4%  Sharpe=-2.94  MaxDD=3.6%  Trades=142

**Parameter Tweaks:**
- Win rate 32.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.94 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp | EURUSD | M15
WR=32.2%  Sharpe=-8.56  MaxDD=2.5%  Trades=59

**Parameter Tweaks:**
- Win rate 32.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.56 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | AUDUSD | H1
WR=30.0%  Sharpe=-2.60  MaxDD=0.8%  Trades=10

**Parameter Tweaks:**
- Win rate 30.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.60 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### vwap_momentum | US500 | M15
WR=28.6%  Sharpe=-5.61  MaxDD=0.0%  Trades=7

**Parameter Tweaks:**
- Win rate 28.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.61 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on US500 unless confirmed by live data

### vwap_momentum | USTEC | M15
WR=28.6%  Sharpe=-1.69  MaxDD=0.2%  Trades=7

**Parameter Tweaks:**
- Win rate 28.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.69 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on USTEC unless confirmed by live data

### stoch_divergence | USDJPY | H4
WR=25.0%  Sharpe=-2.96  MaxDD=1.6%  Trades=8

**Parameter Tweaks:**
- Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.96 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### bb_squeeze_scalp | USTEC | M15
WR=25.0%  Sharpe=-12.38  MaxDD=0.1%  Trades=4

**Parameter Tweaks:**
- Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.38 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.13 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_extremes_scalp | USDJPY | M15
WR=23.8%  Sharpe=-6.77  MaxDD=1.4%  Trades=21

**Parameter Tweaks:**
- Win rate 23.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.77 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.38 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### hikkake_trap | GBPJPY | H4
WR=22.2%  Sharpe=-5.29  MaxDD=1.5%  Trades=9

**Parameter Tweaks:**
- Win rate 22.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.29 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### stoch_divergence | EURUSD | H4
WR=14.3%  Sharpe=-7.28  MaxDD=1.6%  Trades=7

**Parameter Tweaks:**
- Win rate 14.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.28 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | AUDUSD | M15
WR=14.3%  Sharpe=-20.35  MaxDD=0.4%  Trades=7

**Parameter Tweaks:**
- Win rate 14.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -20.35 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.08 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### stoch_divergence | EURUSD | D1
WR=12.5%  Sharpe=-7.33  MaxDD=4.0%  Trades=8

**Parameter Tweaks:**
- Win rate 12.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.33 < 1.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | H4
WR=0.0%  Sharpe=-50.00  MaxDD=0.5%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 1.0 → reduce lot size on this pair or pause strategy

### bb_mean_reversion | XAUUSD | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### macd_trend | US500 | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | US500 | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | MSFT | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### range_breakout | USTEC | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | MSFT | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | GBPJPY | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | GBPJPY | M15
WR=0.0%  Sharpe=-50.00  MaxDD=0.8%  Trades=10

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 1.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | GBPJPY | H1
WR=0.0%  Sharpe=-48.83  MaxDD=0.3%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -48.83 < 1.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | US500 | H1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | US500 | M15
WR=0.0%  Sharpe=-36.12  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -36.12 < 1.0 → reduce lot size on this pair or pause strategy

---

## ❌ Errors / Skipped

- dual_ema_fractal | GBPJPY | D1 → SKIP: insufficient_data
- dual_ema_fractal | AUDUSD | D1 → SKIP: insufficient_data
- dual_ema_fractal | USOIL | D1 → SKIP: insufficient_data
- rsi_bounce | EURUSD | H4 → NO_TRADES: zero_signals
- rsi_bounce | EURUSD | D1 → NO_TRADES: zero_signals
- rsi_bounce | XAUUSD | D1 → NO_TRADES: zero_signals
- rsi_bounce | GBPUSD | H4 → NO_TRADES: zero_signals
- rsi_bounce | GBPJPY | H4 → NO_TRADES: zero_signals
- rsi_bounce | GBPJPY | D1 → SKIP: insufficient_data
- rsi_bounce | AUDUSD | H4 → NO_TRADES: zero_signals
- rsi_bounce | USDCAD | H4 → NO_TRADES: zero_signals
- rsi_bounce | USOIL | H4 → NO_TRADES: zero_signals
- rsi_bounce | USOIL | D1 → SKIP: insufficient_data
- bb_mean_reversion | EURUSD | H4 → NO_TRADES: zero_signals
- bb_mean_reversion | GBPJPY | H1 → NO_TRADES: zero_signals
- bb_mean_reversion | GBPJPY | H4 → NO_TRADES: zero_signals
- bb_mean_reversion | USOIL | H1 → NO_TRADES: zero_signals
- bb_mean_reversion | USOIL | H4 → NO_TRADES: zero_signals
- bb_mean_reversion | US500 | H4 → NO_TRADES: zero_signals
- stoch_divergence | GBPJPY | H4 → NO_TRADES: zero_signals
- stoch_divergence | GBPJPY | D1 → SKIP: insufficient_data
- stoch_divergence | AUDUSD | H4 → NO_TRADES: zero_signals
- stoch_divergence | USDCAD | H4 → NO_TRADES: zero_signals
- macd_trend | GBPJPY | H4 → NO_TRADES: zero_signals
- macd_trend | AUDUSD | H4 → NO_TRADES: zero_signals
- gold_momentum_breakout | USOIL | H4 → NO_TRADES: zero_signals
- gold_momentum_breakout | USOIL | D1 → SKIP: insufficient_data
- gold_momentum_breakout | US500 | D1 → SKIP: insufficient_data
- gold_momentum_breakout | USTEC | H4 → NO_TRADES: zero_signals
- gold_momentum_breakout | USTEC | D1 → SKIP: insufficient_data
- gold_momentum_breakout | NVDA | H4 → NO_TRADES: zero_signals
- gold_momentum_breakout | NVDA | D1 → ERROR: Insufficient data for NVDA D1: 172 bars (need >= 200). Run data ingest first.
- gold_momentum_breakout | AMD | H4 → NO_TRADES: zero_signals
- gold_momentum_breakout | AMD | D1 → ERROR: Insufficient data for AMD D1: 173 bars (need >= 200). Run data ingest first.
- gold_momentum_breakout | MSFT | D1 → ERROR: Insufficient data for MSFT D1: 180 bars (need >= 200). Run data ingest first.
- gold_momentum_breakout | AAPL | D1 → ERROR: Insufficient data for AAPL D1: 177 bars (need >= 200). Run data ingest first.
- ema_ribbon_trend | US500 | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | D1 → SKIP: insufficient_data
- ema_ribbon_trend | USTEC | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | USTEC | D1 → SKIP: insufficient_data
- ema_ribbon_trend | NVDA | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | D1 → ERROR: Insufficient data for NVDA D1: 172 bars (need >= 200). Run data ingest first.
- ema_ribbon_trend | AMD | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | AMD | D1 → ERROR: Insufficient data for AMD D1: 173 bars (need >= 200). Run data ingest first.
- ema_ribbon_trend | MSFT | D1 → ERROR: Insufficient data for MSFT D1: 180 bars (need >= 200). Run data ingest first.
- ema_ribbon_trend | AAPL | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | D1 → ERROR: Insufficient data for AAPL D1: 177 bars (need >= 200). Run data ingest first.
- cot_sentiment | XAUUSD | W1 → SKIP: insufficient_data
- cot_sentiment | EURUSD | W1 → SKIP: insufficient_data
- cot_sentiment | XAGUSD | D1 → NO_TRADES: zero_signals
- rsi_pullback | USOIL | D1 → SKIP: insufficient_data
- dual_ema_momentum | AUDUSD | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | H4 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | H1 → NO_TRADES: zero_signals