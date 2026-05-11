# Overnight Backtest Report — 08 May 2026

Generated: 2026-05-08 22:03 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 25 |
| ⚠️ REVIEW | 68 |
| ❌ ERROR/SKIP | 5 |
| **Total combos** | **98** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| rsi_bounce | GBPJPY | D1 | T2 | 100.0 | 27.08 | 0.0 | 6 | 999.00 |
| rsi_bounce | EURUSD | D1 | T2 | 100.0 | 16.07 | 0.0 | 2 | 999.00 |
| rsi_bounce | EURUSD | H12 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| rsi_bounce | AUDUSD | D1 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| ma_crossover | GBPJPY | D1 | T1 | 100.0 | 26.19 | 0.0 | 3 | 999.00 |
| ma_crossover | AUDUSD | H4 | T1 | 100.0 | 15.45 | 0.0 | 3 | 999.00 |
| macd_trend | GBPJPY | H2 | T2 | 100.0 | 17.84 | 0.0 | 2 | 999.00 |
| macd_trend | US500 | H2 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| gold_momentum_breakout | XAUUSD | D1 | T1 | 100.0 | 50.00 | 0.0 | 3 | 999.00 |
| range_breakout | USOIL | H2 | T1 | 100.0 | 10.64 | 0.0 | 5 | 999.00 |
| bb_squeeze_scalp | US500 | M15 | T2 | 100.0 | 17.10 | 0.0 | 5 | 999.00 |
| gold_momentum_breakout | GBPUSD | D1 | T1 | 85.7 | 11.00 | 0.8 | 7 | 6.34 |
| gold_momentum_breakout | US500 | H2 | T1 | 83.3 | 12.11 | 0.0 | 6 | 7.18 |
| gold_momentum_breakout | USTEC | H2 | T1 | 83.3 | 10.01 | 0.0 | 6 | 5.63 |
| range_breakout | USTEC | D1 | T1 | 78.6 | 8.05 | 0.2 | 14 | 4.07 |
| macd_trend | GBPJPY | H4 | T2 | 76.5 | 7.02 | 0.7 | 17 | 2.89 |
| rsi_bounce | USDJPY | D1 | T2 | 75.0 | 12.03 | 0.0 | 4 | 5.79 |
| macd_trend | US500 | H4 | T2 | 75.0 | 7.51 | 0.0 | 4 | 4.53 |
| macd_trend | US500 | D1 | T2 | 75.0 | 6.55 | 0.1 | 4 | 2.93 |
| stat_arb_gold_silver | XAUUSD | H2 | T1 | 72.7 | 5.42 | 3.4 | 220 | 4.26 |
| orb | GBPJPY | M15 | T2 | 72.2 | 4.49 | 0.4 | 18 | 2.00 |
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 71.3 | 4.62 | 7.2 | 129 | 4.10 |
| gold_momentum_breakout | AAPL | H4 | T1 | 70.8 | 6.43 | 0.5 | 24 | 2.59 |
| rsi_bounce | EURUSD | H2 | T2 | 70.6 | 5.26 | 0.3 | 17 | 2.26 |
| rsi_bounce | GBPJPY | H4 | T2 | 70.0 | 9.06 | 0.9 | 10 | 4.16 |

---

## ⚠️ Strategies Needing Review


### rsi_bounce | GBPJPY | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | USTEC | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | USDJPY | M5
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | XAUUSD | H4
WR=69.2%  Sharpe=6.16  MaxDD=2.9%  Trades=52

**Parameter Tweaks:**
- Win rate 69.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 69.2% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### gold_momentum_breakout | XAUUSD | H4
WR=68.0%  Sharpe=6.24  MaxDD=3.2%  Trades=50

**Parameter Tweaks:**
- Win rate 68.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 68.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### session_momentum | EURUSD | H4
WR=68.0%  Sharpe=5.69  MaxDD=1.0%  Trades=25

**Parameter Tweaks:**
- Win rate 68.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 68.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_bounce | USDJPY | H4
WR=66.7%  Sharpe=2.85  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | GBPJPY | D1
WR=66.7%  Sharpe=3.23  MaxDD=1.4%  Trades=6

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | USTEC | H2
WR=66.7%  Sharpe=5.30  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | EURUSD | D1
WR=66.7%  Sharpe=11.80  MaxDD=0.5%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### rvgi_cci_confluence | EURUSD | H12
WR=66.7%  Sharpe=4.67  MaxDD=1.0%  Trades=12

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | US500 | H4
WR=65.3%  Sharpe=2.54  MaxDD=0.2%  Trades=49

**Parameter Tweaks:**
- Win rate 65.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 65.3% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### stat_arb_gold_silver | XAUUSD | H1
WR=64.5%  Sharpe=3.32  MaxDD=3.7%  Trades=496

**Parameter Tweaks:**
- Win rate 64.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 64.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### ma_crossover | GBPJPY | H4
WR=63.6%  Sharpe=4.58  MaxDD=0.8%  Trades=11

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | EURUSD | D1
WR=63.6%  Sharpe=7.06  MaxDD=0.7%  Trades=11

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### orb | GBPJPY | M30
WR=63.6%  Sharpe=3.44  MaxDD=0.4%  Trades=22

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 22 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_bounce | GBPJPY | H1
WR=63.2%  Sharpe=6.14  MaxDD=0.7%  Trades=19

**Parameter Tweaks:**
- Win rate 63.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.2% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | XAUUSD | H4
WR=62.8%  Sharpe=5.41  MaxDD=6.6%  Trades=51

**Parameter Tweaks:**
- Win rate 62.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 62.8% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### range_breakout | USOIL | D1
WR=62.5%  Sharpe=5.70  MaxDD=1.1%  Trades=8

**Parameter Tweaks:**
- Win rate 62.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 62.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter

### rvgi_cci_confluence | EURUSD | H4
WR=62.5%  Sharpe=3.19  MaxDD=0.9%  Trades=40

**Parameter Tweaks:**
- Win rate 62.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 62.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### dual_ema_fractal | XAUUSD | D1
WR=61.5%  Sharpe=5.09  MaxDD=7.5%  Trades=13

**Parameter Tweaks:**
- Win rate 61.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 61.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_pullback | XAUUSD | H4
WR=60.7%  Sharpe=3.28  MaxDD=8.2%  Trades=56

**Parameter Tweaks:**
- Win rate 60.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 60.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### rsi_pullback | EURUSD | H4
WR=60.5%  Sharpe=2.65  MaxDD=1.4%  Trades=43

**Parameter Tweaks:**
- Win rate 60.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 60.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### macd_trend | USTEC | H1
WR=60.0%  Sharpe=4.15  MaxDD=0.1%  Trades=25

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | EURUSD | H2
WR=59.7%  Sharpe=0.01  MaxDD=1.2%  Trades=72

**Parameter Tweaks:**
- Win rate 59.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.01 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.00 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H4
WR=59.5%  Sharpe=3.83  MaxDD=5.9%  Trades=42

**Parameter Tweaks:**
- Win rate 59.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### macd_trend | US500 | H1
WR=59.3%  Sharpe=3.18  MaxDD=0.0%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter

### cot_sentiment | EURUSD | H12
WR=59.0%  Sharpe=2.63  MaxDD=4.2%  Trades=83

**Parameter Tweaks:**
- Win rate 59.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### gold_momentum_breakout | USTEC | H4
WR=58.8%  Sharpe=1.55  MaxDD=0.7%  Trades=51

**Parameter Tweaks:**
- Win rate 58.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.55 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | AUDUSD | M30
WR=58.3%  Sharpe=-1.02  MaxDD=0.5%  Trades=24

**Parameter Tweaks:**
- Win rate 58.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.02 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### range_breakout | USTEC | H4
WR=58.2%  Sharpe=3.56  MaxDD=0.6%  Trades=79

**Parameter Tweaks:**
- Win rate 58.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### stat_arb_gold_silver | XAUUSD | M30
WR=58.0%  Sharpe=1.50  MaxDD=9.1%  Trades=873

**Parameter Tweaks:**
- Win rate 58.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.50 < 2.0 → reduce lot size on this pair or pause strategy

### session_momentum | XAUUSD | H4
WR=57.7%  Sharpe=3.91  MaxDD=2.7%  Trades=26

**Parameter Tweaks:**
- Win rate 57.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_bounce | USDJPY | M30
WR=57.1%  Sharpe=2.97  MaxDD=0.4%  Trades=21

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | US500 | D1
WR=57.1%  Sharpe=7.15  MaxDD=0.1%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_fractal | XAUUSD | H2
WR=56.3%  Sharpe=2.71  MaxDD=7.1%  Trades=103

**Parameter Tweaks:**
- Win rate 56.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### rsi_bounce | AUDUSD | H1
WR=56.2%  Sharpe=1.44  MaxDD=0.5%  Trades=16

**Parameter Tweaks:**
- Win rate 56.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.44 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | AAPL | M15
WR=55.4%  Sharpe=1.40  MaxDD=0.5%  Trades=65

**Parameter Tweaks:**
- Win rate 55.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.40 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | GBPJPY | M30
WR=54.8%  Sharpe=4.27  MaxDD=1.2%  Trades=31

**Parameter Tweaks:**
- Win rate 54.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### gold_momentum_breakout | GBPUSD | H4
WR=54.8%  Sharpe=0.76  MaxDD=1.3%  Trades=42

**Parameter Tweaks:**
- Win rate 54.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.12 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | XAGUSD | H4
WR=54.2%  Sharpe=3.09  MaxDD=9.5%  Trades=59

**Parameter Tweaks:**
- Win rate 54.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### cot_sentiment | EURUSD | D1
WR=54.0%  Sharpe=3.51  MaxDD=2.7%  Trades=50

**Parameter Tweaks:**
- Win rate 54.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### range_breakout | USOIL | H4
WR=50.8%  Sharpe=2.07  MaxDD=7.0%  Trades=61

**Parameter Tweaks:**
- Win rate 50.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### range_breakout | US500 | H4
WR=50.8%  Sharpe=0.51  MaxDD=0.3%  Trades=67

**Parameter Tweaks:**
- Win rate 50.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on US500 unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H2
WR=50.5%  Sharpe=-0.20  MaxDD=12.1%  Trades=97

**Parameter Tweaks:**
- Win rate 50.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.20 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | AUDUSD | H4
WR=50.0%  Sharpe=-3.27  MaxDD=0.5%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.27 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### macd_trend | USTEC | D1
WR=50.0%  Sharpe=5.24  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | AAPL | H2
WR=50.0%  Sharpe=1.96  MaxDD=0.2%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.96 < 2.0 → reduce lot size on this pair or pause strategy

### range_breakout | EURUSD | H4
WR=50.0%  Sharpe=-1.58  MaxDD=2.2%  Trades=40

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.58 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | USDJPY | M30
WR=50.0%  Sharpe=-0.21  MaxDD=0.5%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.21 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### bb_squeeze_scalp | US500 | M5
WR=50.0%  Sharpe=2.06  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend | XAUUSD | M15
WR=48.4%  Sharpe=0.53  MaxDD=3.5%  Trades=64

**Parameter Tweaks:**
- Win rate 48.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.11 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H2
WR=45.5%  Sharpe=-1.75  MaxDD=5.8%  Trades=101

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.75 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | USDJPY | H2
WR=45.5%  Sharpe=-1.82  MaxDD=1.6%  Trades=11

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.82 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### range_breakout | XAUUSD | H2
WR=44.0%  Sharpe=-1.85  MaxDD=11.4%  Trades=75

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.85 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | GBPJPY | H1
WR=43.3%  Sharpe=-2.08  MaxDD=5.4%  Trades=67

**Parameter Tweaks:**
- Win rate 43.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.08 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### macd_trend | USTEC | H4
WR=42.9%  Sharpe=-0.00  MaxDD=0.2%  Trades=7

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.00 — marginal edge, consider disabling on USTEC unless confirmed by live data

### range_breakout | US500 | H2
WR=40.0%  Sharpe=-1.57  MaxDD=0.0%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.57 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on US500 unless confirmed by live data

### rsi_bounce | EURUSD | M30
WR=35.7%  Sharpe=-13.93  MaxDD=1.8%  Trades=28

**Parameter Tweaks:**
- Win rate 35.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 28 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -13.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | EURUSD | H1
WR=35.3%  Sharpe=-5.88  MaxDD=1.1%  Trades=17

**Parameter Tweaks:**
- Win rate 35.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.88 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | EURUSD | H4
WR=33.3%  Sharpe=-9.32  MaxDD=1.2%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.28 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | USDJPY | H12
WR=33.3%  Sharpe=-4.96  MaxDD=0.9%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### ma_crossover | AUDUSD | D1
WR=33.3%  Sharpe=-9.17  MaxDD=0.3%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.17 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.22 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### range_breakout | USTEC | H2
WR=33.3%  Sharpe=-12.61  MaxDD=0.3%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.61 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.16 — marginal edge, consider disabling on USTEC unless confirmed by live data

### bb_squeeze_scalp | USDJPY | M15
WR=33.3%  Sharpe=-9.41  MaxDD=0.7%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.26 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_bounce | USDJPY | H1
WR=30.0%  Sharpe=-3.28  MaxDD=0.9%  Trades=10

**Parameter Tweaks:**
- Win rate 30.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### range_breakout | XAUUSD | D1
WR=30.0%  Sharpe=-4.66  MaxDD=16.7%  Trades=10

**Parameter Tweaks:**
- Win rate 30.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | US500 | D1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

---

## ❌ Errors / Skipped

- rsi_bounce | GBPJPY | H12 → NO_TRADES: zero_signals
- rsi_bounce | AUDUSD | H2 → NO_TRADES: zero_signals
- rsi_bounce | AUDUSD | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | AAPL | D1 → NO_TRADES: zero_signals
- bb_squeeze_scalp | US500 | M30 → NO_TRADES: zero_signals