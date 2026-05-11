# Overnight Backtest Report — 08 May 2026

Generated: 2026-05-08 19:31 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 37 |
| ⚠️ REVIEW | 541 |
| ❌ ERROR/SKIP | 280 |
| **Total combos** | **858** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| rsi_bounce | EURUSD | H12 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| rsi_bounce | EURUSD | D1 | T2 | 100.0 | 16.07 | 0.0 | 2 | 999.00 |
| rsi_bounce | GBPJPY | D1 | T2 | 100.0 | 27.08 | 0.0 | 6 | 999.00 |
| rsi_bounce | AUDUSD | D1 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| ma_crossover | AUDUSD | H4 | T1 | 100.0 | 14.88 | 0.0 | 2 | 999.00 |
| ma_crossover | GBPJPY | D1 | T1 | 100.0 | 18.07 | 0.0 | 2 | 999.00 |
| macd_trend | GBPJPY | H2 | T2 | 100.0 | 17.84 | 0.0 | 2 | 999.00 |
| macd_trend | GBPJPY | D1 | T2 | 100.0 | 23.34 | 0.0 | 4 | 999.00 |
| macd_trend | US500 | H2 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| gold_momentum_breakout | XAUUSD | D1 | T1 | 100.0 | 50.00 | 0.0 | 3 | 999.00 |
| range_breakout | USOIL | H2 | T1 | 100.0 | 10.64 | 0.0 | 5 | 999.00 |
| ema_ribbon_trend | AAPL | M15 | T2 | 100.0 | 20.17 | 0.0 | 2 | 999.00 |
| bb_squeeze_scalp | USDJPY | M5 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999.00 |
| bb_squeeze_scalp | USDJPY | M30 | T2 | 100.0 | 18.00 | 0.0 | 7 | 999.00 |
| gold_momentum_breakout | GBPUSD | D1 | T1 | 85.7 | 11.00 | 0.8 | 7 | 6.34 |
| gold_momentum_breakout | AAPL | H4 | T1 | 85.0 | 8.81 | 0.2 | 20 | 5.63 |
| gold_momentum_breakout | US500 | H2 | T1 | 83.3 | 12.11 | 0.0 | 6 | 7.18 |
| gold_momentum_breakout | USTEC | H2 | T1 | 83.3 | 10.01 | 0.0 | 6 | 5.63 |
| turtle_soup | AUDUSD | H2 | T2 | 80.0 | 2.64 | 0.4 | 5 | 1.58 |
| bb_squeeze_scalp | US500 | M15 | T2 | 80.0 | 9.89 | 0.0 | 5 | 4.88 |
| macd_trend | GBPJPY | H4 | T2 | 76.5 | 7.02 | 0.7 | 17 | 2.89 |
| rsi_bounce | GBPUSD | H12 | T2 | 75.0 | 2.17 | 0.9 | 4 | 1.41 |
| rsi_bounce | USDJPY | D1 | T2 | 75.0 | 12.03 | 0.0 | 4 | 5.79 |
| ma_crossover | GBPJPY | H4 | T1 | 75.0 | 6.91 | 0.8 | 8 | 4.12 |
| macd_trend | USDJPY | H12 | T2 | 75.0 | 5.43 | 0.0 | 4 | 2.21 |
| macd_trend | US500 | H4 | T2 | 75.0 | 7.51 | 0.0 | 4 | 4.53 |
| macd_trend | US500 | D1 | T2 | 75.0 | 6.55 | 0.1 | 4 | 2.93 |
| bb_squeeze_scalp | USDJPY | H2 | T2 | 75.0 | 3.62 | 0.3 | 4 | 1.74 |
| stat_arb_gold_silver | XAUUSD | H2 | T1 | 72.7 | 5.42 | 3.4 | 220 | 4.26 |
| orb | GBPJPY | M15 | T2 | 72.2 | 4.49 | 0.4 | 18 | 2.00 |
| macd_trend | USDJPY | H4 | T2 | 71.4 | 2.58 | 0.4 | 7 | 1.51 |
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 71.3 | 4.62 | 7.2 | 129 | 4.10 |
| rsi_bounce | EURUSD | H2 | T2 | 70.6 | 5.26 | 0.3 | 17 | 2.26 |
| rsi_bounce | GBPJPY | H4 | T2 | 70.0 | 9.06 | 0.9 | 10 | 4.16 |
| range_breakout | USTEC | D1 | T1 | 70.0 | 5.10 | 0.4 | 10 | 2.44 |
| dual_ema_momentum | XAUUSD | D1 | T2 | 70.0 | 3.47 | 8.1 | 10 | 1.77 |
| hikkake_trap | GBPUSD | D1 | T2 | 70.0 | 2.65 | 1.5 | 10 | 1.49 |

---

## ⚠️ Strategies Needing Review


### dual_ema_fractal | USDCAD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | USOIL | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | USOIL | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | GBPJPY | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ma_crossover | EURUSD | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ma_crossover | EURUSD | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ma_crossover | GBPJPY | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### macd_trend | AUDUSD | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### macd_trend | USOIL | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | USOIL | H2
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

### gold_momentum_breakout | AMD | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### range_breakout | USOIL | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | ETHUSD | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | AMD | M15
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | AMD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | MSFT | H1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### cot_sentiment | XAUUSD | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | USDCAD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | GBPUSD | D1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rvgi_cci_confluence | AUDUSD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rvgi_cci_confluence | USDCAD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | XAUUSD | H12
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | USTEC | H2
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | USTEC | H4
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_extremes_scalp | GBPUSD | H1
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_extremes_scalp | USOIL | M15
WR=100.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rvgi_cci_confluence | USDCAD | H2
WR=75.0%  Sharpe=-2.84  MaxDD=0.0%  Trades=4

**Parameter Tweaks:**
- Win rate 75.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### dual_ema_fractal | USDCAD | H4
WR=70.8%  Sharpe=1.53  MaxDD=0.7%  Trades=24

**Parameter Tweaks:**
- Win rate 70.8% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.53 < 2.0 → reduce lot size on this pair or pause strategy

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

### dual_ema_fractal | GBPUSD | D1
WR=66.7%  Sharpe=4.28  MaxDD=1.2%  Trades=9

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_bounce | USDJPY | H4
WR=66.7%  Sharpe=2.85  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | NVDA | H4
WR=66.7%  Sharpe=2.42  MaxDD=0.2%  Trades=6

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | USOIL | D1
WR=66.7%  Sharpe=6.98  MaxDD=1.0%  Trades=6

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend | ETHUSD | M5
WR=66.7%  Sharpe=2.14  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### session_momentum | GBPUSD | H12
WR=66.7%  Sharpe=2.00  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 2.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | EURUSD | D1
WR=66.7%  Sharpe=11.80  MaxDD=0.5%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | GBPUSD | D1
WR=66.7%  Sharpe=4.55  MaxDD=0.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### orb | AUDUSD | M15
WR=66.7%  Sharpe=3.84  MaxDD=0.2%  Trades=12

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter

### rvgi_cci_confluence | EURUSD | H12
WR=66.7%  Sharpe=4.67  MaxDD=1.0%  Trades=12

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp | XAUUSD | H4
WR=66.7%  Sharpe=6.98  MaxDD=1.0%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp | GBPJPY | M5
WR=66.7%  Sharpe=-6.16  MaxDD=0.2%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.24 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### bb_squeeze_scalp | GBPJPY | M30
WR=66.7%  Sharpe=-1.45  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.45 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### bb_squeeze_scalp | GBPJPY | H1
WR=66.7%  Sharpe=6.21  MaxDD=0.3%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_extremes_scalp | EURUSD | H1
WR=66.7%  Sharpe=1.03  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.03 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.19 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | US500 | H4
WR=65.3%  Sharpe=2.54  MaxDD=0.2%  Trades=49

**Parameter Tweaks:**
- Win rate 65.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 65.3% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### rvgi_cci_confluence | GBPUSD | H12
WR=64.7%  Sharpe=0.93  MaxDD=1.6%  Trades=17

**Parameter Tweaks:**
- Win rate 64.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 64.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | H1
WR=64.5%  Sharpe=3.32  MaxDD=3.7%  Trades=496

**Parameter Tweaks:**
- Win rate 64.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 64.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### range_breakout | EURUSD | D1
WR=63.6%  Sharpe=7.06  MaxDD=0.7%  Trades=11

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend | XAUUSD | M15
WR=63.6%  Sharpe=5.12  MaxDD=1.2%  Trades=11

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | USDCAD | D1
WR=63.6%  Sharpe=2.78  MaxDD=1.5%  Trades=11

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

### rsi_pullback | GBPUSD | H12
WR=63.2%  Sharpe=2.20  MaxDD=2.9%  Trades=19

**Parameter Tweaks:**
- Win rate 63.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.2% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | XAUUSD | H4
WR=62.8%  Sharpe=5.41  MaxDD=6.6%  Trades=51

**Parameter Tweaks:**
- Win rate 62.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 62.8% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### session_momentum | GBPUSD | H2
WR=62.5%  Sharpe=2.14  MaxDD=1.1%  Trades=32

**Parameter Tweaks:**
- Win rate 62.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 62.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

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

### rvgi_cci_confluence | USDCAD | H4
WR=60.5%  Sharpe=1.36  MaxDD=0.7%  Trades=38

**Parameter Tweaks:**
- Win rate 60.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 60.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Sharpe 1.36 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_pullback | EURUSD | H4
WR=60.5%  Sharpe=2.65  MaxDD=1.4%  Trades=43

**Parameter Tweaks:**
- Win rate 60.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 60.5% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### rsi_bounce | GBPUSD | H2
WR=60.0%  Sharpe=-0.13  MaxDD=0.5%  Trades=10

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ma_crossover | AUDUSD | H1
WR=60.0%  Sharpe=3.11  MaxDD=0.1%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | AUDUSD | H4
WR=60.0%  Sharpe=2.46  MaxDD=0.3%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | USTEC | H1
WR=60.0%  Sharpe=4.15  MaxDD=0.1%  Trades=25

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_momentum | EURUSD | H4
WR=60.0%  Sharpe=3.16  MaxDD=0.5%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### orb | XAUUSD | M5
WR=60.0%  Sharpe=5.12  MaxDD=1.2%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp | USTEC | M15
WR=60.0%  Sharpe=3.36  MaxDD=0.0%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

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

### range_breakout | USTEC | H4
WR=59.5%  Sharpe=3.75  MaxDD=0.6%  Trades=74

**Parameter Tweaks:**
- Win rate 59.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### rvgi_cci_confluence | EURUSD | D1
WR=59.4%  Sharpe=-0.41  MaxDD=1.6%  Trades=32

**Parameter Tweaks:**
- Win rate 59.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.94 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | GBPJPY | H1
WR=59.3%  Sharpe=1.70  MaxDD=1.3%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.70 < 2.0 → reduce lot size on this pair or pause strategy

### macd_trend | US500 | H1
WR=59.3%  Sharpe=3.18  MaxDD=0.0%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | USOIL | H4
WR=59.1%  Sharpe=0.84  MaxDD=3.7%  Trades=22

**Parameter Tweaks:**
- Win rate 59.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 22 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.14 — marginal edge, consider disabling on USOIL unless confirmed by live data

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

### rsi_bounce | USDCAD | H1
WR=58.3%  Sharpe=-2.35  MaxDD=0.3%  Trades=12

**Parameter Tweaks:**
- Win rate 58.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### ema_ribbon_trend | USTEC | M5
WR=58.3%  Sharpe=0.75  MaxDD=0.1%  Trades=12

**Parameter Tweaks:**
- Win rate 58.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.75 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.12 — marginal edge, consider disabling on USTEC unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | M30
WR=58.0%  Sharpe=1.50  MaxDD=9.1%  Trades=873

**Parameter Tweaks:**
- Win rate 58.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.50 < 2.0 → reduce lot size on this pair or pause strategy

### session_momentum | EURUSD | H2
WR=57.8%  Sharpe=0.96  MaxDD=1.1%  Trades=45

**Parameter Tweaks:**
- Win rate 57.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_pullback | USDJPY | H12
WR=57.8%  Sharpe=1.06  MaxDD=3.8%  Trades=45

**Parameter Tweaks:**
- Win rate 57.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.06 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.18 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum | XAUUSD | H4
WR=57.7%  Sharpe=3.91  MaxDD=2.7%  Trades=26

**Parameter Tweaks:**
- Win rate 57.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter

### rvgi_cci_confluence | GBPUSD | D1
WR=57.7%  Sharpe=-0.07  MaxDD=2.2%  Trades=26

**Parameter Tweaks:**
- Win rate 57.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.07 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | XAUUSD | D1
WR=57.6%  Sharpe=-1.92  MaxDD=42.2%  Trades=33

**Parameter Tweaks:**
- Win rate 57.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 42.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.92 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | GBPUSD | H1
WR=57.1%  Sharpe=1.19  MaxDD=1.1%  Trades=21

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.19 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.18 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

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

### turtle_soup | XAUUSD | H4
WR=57.1%  Sharpe=-1.23  MaxDD=16.9%  Trades=49

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### orb | GBPJPY | M5
WR=57.1%  Sharpe=-4.36  MaxDD=0.3%  Trades=7

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.36 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | D1
WR=57.1%  Sharpe=0.11  MaxDD=1.3%  Trades=21

**Parameter Tweaks:**
- Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H1
WR=56.8%  Sharpe=0.84  MaxDD=9.0%  Trades=148

**Parameter Tweaks:**
- Win rate 56.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.17 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | GBPUSD | H4
WR=56.8%  Sharpe=2.56  MaxDD=1.5%  Trades=37

**Parameter Tweaks:**
- Win rate 56.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)

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

### rsi_pullback | USDJPY | H4
WR=56.2%  Sharpe=-0.06  MaxDD=2.9%  Trades=48

**Parameter Tweaks:**
- Win rate 56.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.06 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum | GBPUSD | H4
WR=56.0%  Sharpe=2.12  MaxDD=1.4%  Trades=25

**Parameter Tweaks:**
- Win rate 56.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_fractal | GBPUSD | H1
WR=55.9%  Sharpe=0.10  MaxDD=3.3%  Trades=143

**Parameter Tweaks:**
- Win rate 55.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | M5
WR=55.9%  Sharpe=0.12  MaxDD=47.4%  Trades=1936

**Parameter Tweaks:**
- Win rate 55.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 47.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.12 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.02 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | XAUUSD | M5
WR=55.9%  Sharpe=0.05  MaxDD=13.5%  Trades=560

**Parameter Tweaks:**
- Win rate 55.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.05 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.01 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H4
WR=55.9%  Sharpe=-0.49  MaxDD=1.5%  Trades=34

**Parameter Tweaks:**
- Win rate 55.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.49 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPUSD | M30
WR=55.6%  Sharpe=0.38  MaxDD=0.5%  Trades=27

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.38 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.06 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend | US500 | M5
WR=55.6%  Sharpe=-2.54  MaxDD=0.0%  Trades=9

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on US500 unless confirmed by live data

### session_momentum | XAUUSD | H2
WR=55.6%  Sharpe=-0.21  MaxDD=2.9%  Trades=18

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 18 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.21 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H4
WR=55.6%  Sharpe=1.90  MaxDD=1.7%  Trades=18

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 18 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.90 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | XAUUSD | M15
WR=55.6%  Sharpe=1.60  MaxDD=1.2%  Trades=9

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.60 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | XAUUSD | H2
WR=55.6%  Sharpe=1.96  MaxDD=2.3%  Trades=9

**Parameter Tweaks:**
- Win rate 55.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.96 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | GBPJPY | M15
WR=55.5%  Sharpe=-0.92  MaxDD=5.3%  Trades=355

**Parameter Tweaks:**
- Win rate 55.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.92 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_fractal | GBPUSD | H4
WR=55.3%  Sharpe=0.26  MaxDD=3.3%  Trades=38

**Parameter Tweaks:**
- Win rate 55.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.26 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.04 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | AMD | M30
WR=55.1%  Sharpe=0.78  MaxDD=1.1%  Trades=118

**Parameter Tweaks:**
- Win rate 55.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.14 — marginal edge, consider disabling on AMD unless confirmed by live data

### rsi_bounce | USOIL | M30
WR=55.0%  Sharpe=-0.76  MaxDD=2.0%  Trades=40

**Parameter Tweaks:**
- Win rate 55.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_bounce | GBPJPY | M30
WR=54.8%  Sharpe=4.27  MaxDD=1.2%  Trades=31

**Parameter Tweaks:**
- Win rate 54.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### macd_trend | USOIL | M15
WR=54.8%  Sharpe=2.17  MaxDD=1.7%  Trades=62

**Parameter Tweaks:**
- Win rate 54.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### gold_momentum_breakout | GBPUSD | H4
WR=54.8%  Sharpe=0.76  MaxDD=1.3%  Trades=42

**Parameter Tweaks:**
- Win rate 54.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.12 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H2
WR=54.5%  Sharpe=-1.05  MaxDD=1.4%  Trades=33

**Parameter Tweaks:**
- Win rate 54.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.05 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | H4
WR=54.3%  Sharpe=0.35  MaxDD=1.3%  Trades=35

**Parameter Tweaks:**
- Win rate 54.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.06 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_pullback | XAGUSD | H4
WR=54.2%  Sharpe=3.09  MaxDD=9.5%  Trades=59

**Parameter Tweaks:**
- Win rate 54.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### hikkake_trap | XAUUSD | D1
WR=54.2%  Sharpe=1.73  MaxDD=12.5%  Trades=24

**Parameter Tweaks:**
- Win rate 54.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.73 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | USOIL | M5
WR=54.0%  Sharpe=-2.48  MaxDD=1.0%  Trades=37

**Parameter Tweaks:**
- Win rate 54.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.48 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on USOIL unless confirmed by live data

### cot_sentiment | EURUSD | D1
WR=54.0%  Sharpe=3.51  MaxDD=2.7%  Trades=50

**Parameter Tweaks:**
- Win rate 54.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### macd_trend | AUDUSD | H1
WR=53.9%  Sharpe=-3.83  MaxDD=0.8%  Trades=26

**Parameter Tweaks:**
- Win rate 53.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### macd_trend | US500 | M5
WR=53.9%  Sharpe=-2.82  MaxDD=0.1%  Trades=26

**Parameter Tweaks:**
- Win rate 53.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.82 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on US500 unless confirmed by live data

### ema_ribbon_trend | USTEC | M30
WR=53.9%  Sharpe=2.24  MaxDD=0.3%  Trades=13

**Parameter Tweaks:**
- Win rate 53.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_pullback | EURUSD | H12
WR=53.9%  Sharpe=1.13  MaxDD=1.4%  Trades=13

**Parameter Tweaks:**
- Win rate 53.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.18 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp | USDJPY | H1
WR=53.9%  Sharpe=-0.23  MaxDD=1.6%  Trades=13

**Parameter Tweaks:**
- Win rate 53.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### dual_ema_momentum | XAUUSD | M5
WR=53.6%  Sharpe=-1.56  MaxDD=7.8%  Trades=84

**Parameter Tweaks:**
- Win rate 53.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | GBPUSD | M15
WR=53.5%  Sharpe=-2.77  MaxDD=5.9%  Trades=232

**Parameter Tweaks:**
- Win rate 53.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.77 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ma_crossover | EURUSD | H1
WR=53.3%  Sharpe=0.64  MaxDD=0.8%  Trades=30

**Parameter Tweaks:**
- Win rate 53.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.64 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | BTCUSD | H2
WR=53.3%  Sharpe=0.90  MaxDD=5.6%  Trades=60

**Parameter Tweaks:**
- Win rate 53.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.90 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.15 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### hikkake_trap | XAUUSD | M15
WR=53.1%  Sharpe=-1.03  MaxDD=33.4%  Trades=605

**Parameter Tweaks:**
- Win rate 53.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 33.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.03 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | USDJPY | H1
WR=52.9%  Sharpe=-0.04  MaxDD=1.4%  Trades=34

**Parameter Tweaks:**
- Win rate 52.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum | XAUUSD | H1
WR=52.9%  Sharpe=-1.88  MaxDD=3.8%  Trades=34

**Parameter Tweaks:**
- Win rate 52.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.88 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H2
WR=52.8%  Sharpe=0.00  MaxDD=1.5%  Trades=89

**Parameter Tweaks:**
- Win rate 52.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.00 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | XAUUSD | H1
WR=52.8%  Sharpe=1.13  MaxDD=8.3%  Trades=36

**Parameter Tweaks:**
- Win rate 52.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.18 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | M30
WR=52.8%  Sharpe=-1.55  MaxDD=3.1%  Trades=199

**Parameter Tweaks:**
- Win rate 52.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | USOIL | H4
WR=52.7%  Sharpe=3.02  MaxDD=4.6%  Trades=55

**Parameter Tweaks:**
- Win rate 52.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum | EURUSD | H2
WR=52.6%  Sharpe=-2.42  MaxDD=1.1%  Trades=19

**Parameter Tweaks:**
- Win rate 52.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | AUDUSD | M30
WR=52.6%  Sharpe=-7.14  MaxDD=1.3%  Trades=19

**Parameter Tweaks:**
- Win rate 52.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.14 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### turtle_soup | AUDUSD | H1
WR=52.5%  Sharpe=-1.09  MaxDD=3.1%  Trades=120

**Parameter Tweaks:**
- Win rate 52.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.09 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_pullback | USDJPY | M30
WR=52.4%  Sharpe=-1.35  MaxDD=5.2%  Trades=225

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### turtle_soup | XAUUSD | M30
WR=52.4%  Sharpe=0.86  MaxDD=13.1%  Trades=225

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.17 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover | GBPJPY | M30
WR=52.4%  Sharpe=0.39  MaxDD=1.6%  Trades=42

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_momentum | EURUSD | M30
WR=51.9%  Sharpe=-1.27  MaxDD=1.9%  Trades=52

**Parameter Tweaks:**
- Win rate 51.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.27 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H4
WR=51.9%  Sharpe=-1.76  MaxDD=2.4%  Trades=27

**Parameter Tweaks:**
- Win rate 51.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H2
WR=51.7%  Sharpe=-0.37  MaxDD=9.3%  Trades=29

**Parameter Tweaks:**
- Win rate 51.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.37 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.94 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | XAUUSD | H1
WR=51.6%  Sharpe=0.64  MaxDD=15.1%  Trades=153

**Parameter Tweaks:**
- Win rate 51.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.64 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.13 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | ETHUSD | H2
WR=51.6%  Sharpe=-1.96  MaxDD=0.7%  Trades=62

**Parameter Tweaks:**
- Win rate 51.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H2
WR=51.6%  Sharpe=-1.08  MaxDD=4.8%  Trades=95

**Parameter Tweaks:**
- Win rate 51.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.08 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | GBPUSD | D1
WR=51.4%  Sharpe=0.90  MaxDD=3.0%  Trades=35

**Parameter Tweaks:**
- Win rate 51.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.90 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.14 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | M30
WR=51.3%  Sharpe=-1.15  MaxDD=4.9%  Trades=234

**Parameter Tweaks:**
- Win rate 51.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.15 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | MSFT | M30
WR=51.1%  Sharpe=-0.74  MaxDD=2.2%  Trades=135

**Parameter Tweaks:**
- Win rate 51.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on MSFT unless confirmed by live data

### rsi_pullback | USDJPY | M15
WR=51.1%  Sharpe=-1.42  MaxDD=5.7%  Trades=368

**Parameter Tweaks:**
- Win rate 51.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_pullback | XAGUSD | M5
WR=50.9%  Sharpe=-0.83  MaxDD=46.6%  Trades=585

**Parameter Tweaks:**
- Win rate 50.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 46.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### gold_momentum_breakout | MSFT | H1
WR=50.9%  Sharpe=-3.87  MaxDD=3.2%  Trades=57

**Parameter Tweaks:**
- Win rate 50.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.87 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on MSFT unless confirmed by live data

### range_breakout | US500 | H4
WR=50.8%  Sharpe=0.51  MaxDD=0.3%  Trades=67

**Parameter Tweaks:**
- Win rate 50.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on US500 unless confirmed by live data

### turtle_soup | XAUUSD | M5
WR=50.7%  Sharpe=-1.15  MaxDD=13.1%  Trades=138

**Parameter Tweaks:**
- Win rate 50.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.15 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | XAGUSD | M30
WR=50.7%  Sharpe=0.32  MaxDD=24.3%  Trades=379

**Parameter Tweaks:**
- Win rate 50.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H2
WR=50.5%  Sharpe=-0.20  MaxDD=12.1%  Trades=97

**Parameter Tweaks:**
- Win rate 50.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.20 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | H1
WR=50.3%  Sharpe=-0.13  MaxDD=14.3%  Trades=195

**Parameter Tweaks:**
- Win rate 50.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | D1
WR=50.0%  Sharpe=1.98  MaxDD=2.9%  Trades=8

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.98 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | AUDUSD | M30
WR=50.0%  Sharpe=-3.78  MaxDD=1.8%  Trades=72

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal | AUDUSD | H4
WR=50.0%  Sharpe=-3.91  MaxDD=0.6%  Trades=10

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.91 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H4
WR=50.0%  Sharpe=-3.63  MaxDD=3.8%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H12
WR=50.0%  Sharpe=-5.44  MaxDD=1.8%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.44 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | USDJPY | M5
WR=50.0%  Sharpe=-6.66  MaxDD=0.5%  Trades=24

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_bounce | AUDUSD | H4
WR=50.0%  Sharpe=-3.27  MaxDD=0.5%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.27 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_bounce | USDCAD | M30
WR=50.0%  Sharpe=-2.85  MaxDD=0.4%  Trades=16

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.85 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### ma_crossover | EURUSD | H2
WR=50.0%  Sharpe=-6.73  MaxDD=0.6%  Trades=10

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | GBPJPY | M15
WR=50.0%  Sharpe=-0.16  MaxDD=0.8%  Trades=58

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### macd_trend | USDJPY | M15
WR=50.0%  Sharpe=-2.16  MaxDD=2.8%  Trades=94

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend | USDJPY | D1
WR=50.0%  Sharpe=-4.53  MaxDD=2.2%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend | USOIL | H4
WR=50.0%  Sharpe=-5.08  MaxDD=3.0%  Trades=8

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.08 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on USOIL unless confirmed by live data

### macd_trend | USTEC | H2
WR=50.0%  Sharpe=2.65  MaxDD=0.1%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend | USTEC | D1
WR=50.0%  Sharpe=5.24  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | AMD | M15
WR=50.0%  Sharpe=-0.22  MaxDD=1.2%  Trades=284

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.97 — marginal edge, consider disabling on AMD unless confirmed by live data

### gold_momentum_breakout | AMD | H4
WR=50.0%  Sharpe=4.08  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | MSFT | H4
WR=50.0%  Sharpe=3.08  MaxDD=1.4%  Trades=10

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout | AAPL | H2
WR=50.0%  Sharpe=4.29  MaxDD=0.2%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### range_breakout | EURUSD | H4
WR=50.0%  Sharpe=-1.58  MaxDD=2.2%  Trades=40

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.58 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | M15
WR=50.0%  Sharpe=5.69  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend | NVDA | M15
WR=50.0%  Sharpe=-4.30  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.30 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on NVDA unless confirmed by live data

### cot_sentiment | XAUUSD | H12
WR=50.0%  Sharpe=1.64  MaxDD=1.8%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.64 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | EURUSD | H12
WR=50.0%  Sharpe=5.23  MaxDD=0.5%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | GBPUSD | H12
WR=50.0%  Sharpe=6.04  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | XAUUSD | H2
WR=50.0%  Sharpe=-0.23  MaxDD=9.5%  Trades=76

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.96 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | XAUUSD | H12
WR=50.0%  Sharpe=6.01  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### turtle_soup | BTCUSD | H1
WR=50.0%  Sharpe=-0.74  MaxDD=9.6%  Trades=100

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.90 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### turtle_soup | BTCUSD | H12
WR=50.0%  Sharpe=-4.00  MaxDD=6.1%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### turtle_soup | BTCUSD | D1
WR=50.0%  Sharpe=-1.13  MaxDD=4.9%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### turtle_soup | ETHUSD | H12
WR=50.0%  Sharpe=0.29  MaxDD=0.3%  Trades=6

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.29 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.04 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H12
WR=50.0%  Sharpe=-2.55  MaxDD=12.9%  Trades=12

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | H2
WR=50.0%  Sharpe=-0.45  MaxDD=0.4%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.45 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | M5
WR=50.0%  Sharpe=4.92  MaxDD=0.9%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp | USDJPY | M15
WR=50.0%  Sharpe=-2.63  MaxDD=0.7%  Trades=10

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### bb_squeeze_scalp | US500 | M5
WR=50.0%  Sharpe=1.70  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.70 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | US500 | H4
WR=50.0%  Sharpe=-7.24  MaxDD=0.0%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.24 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.22 — marginal edge, consider disabling on US500 unless confirmed by live data

### rsi_extremes_scalp | EURUSD | H2
WR=50.0%  Sharpe=3.15  MaxDD=0.2%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_extremes_scalp | EURUSD | H4
WR=50.0%  Sharpe=-6.72  MaxDD=0.6%  Trades=4

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | USOIL | M30
WR=50.0%  Sharpe=0.86  MaxDD=0.3%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.17 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_extremes_scalp | USOIL | H1
WR=50.0%  Sharpe=-7.40  MaxDD=0.5%  Trades=2

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.40 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.21 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_pullback | XAUUSD | M15
WR=49.9%  Sharpe=-1.53  MaxDD=30.5%  Trades=479

**Parameter Tweaks:**
- Win rate 49.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 30.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | XAUUSD | M15
WR=49.7%  Sharpe=-1.10  MaxDD=15.8%  Trades=181

**Parameter Tweaks:**
- Win rate 49.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | AAPL | M30
WR=49.7%  Sharpe=-0.38  MaxDD=1.5%  Trades=165

**Parameter Tweaks:**
- Win rate 49.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.38 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.94 — marginal edge, consider disabling on AAPL unless confirmed by live data

### turtle_soup | EURUSD | H1
WR=49.7%  Sharpe=-2.04  MaxDD=4.0%  Trades=169

**Parameter Tweaks:**
- Win rate 49.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | GBPJPY | M15
WR=49.6%  Sharpe=-2.46  MaxDD=3.1%  Trades=133

**Parameter Tweaks:**
- Win rate 49.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### gold_momentum_breakout | US500 | H1
WR=49.2%  Sharpe=0.45  MaxDD=0.2%  Trades=266

**Parameter Tweaks:**
- Win rate 49.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.45 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.07 — marginal edge, consider disabling on US500 unless confirmed by live data

### ema_ribbon_trend | AAPL | M5
WR=49.1%  Sharpe=-1.22  MaxDD=0.8%  Trades=53

**Parameter Tweaks:**
- Win rate 49.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on AAPL unless confirmed by live data

### hikkake_trap | GBPUSD | H1
WR=48.8%  Sharpe=-1.78  MaxDD=4.2%  Trades=80

**Parameter Tweaks:**
- Win rate 48.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M30
WR=48.7%  Sharpe=-1.40  MaxDD=21.7%  Trades=349

**Parameter Tweaks:**
- Win rate 48.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.40 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | USDCAD | H1
WR=48.7%  Sharpe=-2.62  MaxDD=5.5%  Trades=187

**Parameter Tweaks:**
- Win rate 48.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.62 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### gold_momentum_breakout | MSFT | M15
WR=48.6%  Sharpe=-2.38  MaxDD=5.8%  Trades=296

**Parameter Tweaks:**
- Win rate 48.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.38 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on MSFT unless confirmed by live data

### macd_trend | USTEC | M30
WR=48.6%  Sharpe=-0.50  MaxDD=0.2%  Trades=35

**Parameter Tweaks:**
- Win rate 48.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.50 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_pullback | XAUUSD | M5
WR=48.5%  Sharpe=-1.00  MaxDD=33.5%  Trades=555

**Parameter Tweaks:**
- Win rate 48.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 33.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### session_momentum | GBPUSD | M30
WR=48.4%  Sharpe=-2.27  MaxDD=2.9%  Trades=126

**Parameter Tweaks:**
- Win rate 48.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.27 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | USTEC | M15
WR=48.4%  Sharpe=0.35  MaxDD=0.5%  Trades=403

**Parameter Tweaks:**
- Win rate 48.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.05 — marginal edge, consider disabling on USTEC unless confirmed by live data

### turtle_soup | ETHUSD | H4
WR=48.4%  Sharpe=-0.62  MaxDD=0.5%  Trades=31

**Parameter Tweaks:**
- Win rate 48.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.62 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.91 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H1
WR=48.4%  Sharpe=-2.19  MaxDD=7.2%  Trades=242

**Parameter Tweaks:**
- Win rate 48.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.19 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | AMD | H1
WR=48.3%  Sharpe=0.54  MaxDD=0.9%  Trades=29

**Parameter Tweaks:**
- Win rate 48.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on AMD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M30
WR=48.2%  Sharpe=-1.80  MaxDD=3.1%  Trades=255

**Parameter Tweaks:**
- Win rate 48.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.80 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | GBPJPY | M30
WR=48.1%  Sharpe=-1.48  MaxDD=4.3%  Trades=104

**Parameter Tweaks:**
- Win rate 48.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.48 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### hikkake_trap | XAUUSD | M30
WR=48.1%  Sharpe=-1.82  MaxDD=29.0%  Trades=337

**Parameter Tweaks:**
- Win rate 48.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 29.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.82 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | XAGUSD | M15
WR=48.0%  Sharpe=-0.03  MaxDD=32.9%  Trades=527

**Parameter Tweaks:**
- Win rate 48.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 32.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.03 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.99 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### ema_ribbon_trend | US500 | M15
WR=48.0%  Sharpe=-0.91  MaxDD=0.1%  Trades=25

**Parameter Tweaks:**
- Win rate 48.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.91 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on US500 unless confirmed by live data

### session_momentum | GBPUSD | H1
WR=48.0%  Sharpe=-1.82  MaxDD=2.5%  Trades=73

**Parameter Tweaks:**
- Win rate 48.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.82 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | USOIL | M30
WR=47.9%  Sharpe=-1.69  MaxDD=21.5%  Trades=430

**Parameter Tweaks:**
- Win rate 47.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 21.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.69 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on USOIL unless confirmed by live data

### gold_momentum_breakout | US500 | M30
WR=47.9%  Sharpe=-1.38  MaxDD=0.4%  Trades=311

**Parameter Tweaks:**
- Win rate 47.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.38 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on US500 unless confirmed by live data

### session_momentum | GBPUSD | M15
WR=47.9%  Sharpe=-1.01  MaxDD=2.5%  Trades=140

**Parameter Tweaks:**
- Win rate 47.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.01 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | H1
WR=47.8%  Sharpe=-0.33  MaxDD=3.3%  Trades=138

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.33 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.95 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### gold_momentum_breakout | USTEC | H1
WR=47.8%  Sharpe=1.15  MaxDD=0.7%  Trades=299

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 1.15 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.19 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_pullback | XAGUSD | H1
WR=47.8%  Sharpe=-1.04  MaxDD=31.1%  Trades=253

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 31.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### gold_momentum_breakout | USOIL | H1
WR=47.8%  Sharpe=-1.95  MaxDD=14.4%  Trades=226

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on USOIL unless confirmed by live data

### session_momentum | EURUSD | H1
WR=47.8%  Sharpe=-2.96  MaxDD=2.1%  Trades=67

**Parameter Tweaks:**
- Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | AUDUSD | M30
WR=47.6%  Sharpe=-6.78  MaxDD=0.9%  Trades=21

**Parameter Tweaks:**
- Win rate 47.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### macd_trend | US500 | M15
WR=47.6%  Sharpe=-3.47  MaxDD=0.0%  Trades=21

**Parameter Tweaks:**
- Win rate 47.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.47 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on US500 unless confirmed by live data

### bb_squeeze_scalp | USTEC | H1
WR=47.6%  Sharpe=-0.87  MaxDD=0.4%  Trades=21

**Parameter Tweaks:**
- Win rate 47.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.87 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_pullback | GBPUSD | M15
WR=47.6%  Sharpe=-3.35  MaxDD=10.6%  Trades=353

**Parameter Tweaks:**
- Win rate 47.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend | MSFT | M5
WR=47.5%  Sharpe=-0.51  MaxDD=0.5%  Trades=40

**Parameter Tweaks:**
- Win rate 47.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.93 — marginal edge, consider disabling on MSFT unless confirmed by live data

### hikkake_trap | XAUUSD | H1
WR=47.5%  Sharpe=-1.17  MaxDD=13.5%  Trades=137

**Parameter Tweaks:**
- Win rate 47.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.17 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | M30
WR=47.4%  Sharpe=-2.17  MaxDD=10.8%  Trades=306

**Parameter Tweaks:**
- Win rate 47.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_momentum | GBPUSD | H2
WR=47.4%  Sharpe=-0.79  MaxDD=0.7%  Trades=19

**Parameter Tweaks:**
- Win rate 47.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.79 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | USDJPY | H1
WR=47.2%  Sharpe=-1.97  MaxDD=5.9%  Trades=127

**Parameter Tweaks:**
- Win rate 47.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H1
WR=47.2%  Sharpe=-2.96  MaxDD=4.3%  Trades=144

**Parameter Tweaks:**
- Win rate 47.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup | AUDUSD | M15
WR=47.1%  Sharpe=-4.10  MaxDD=4.1%  Trades=174

**Parameter Tweaks:**
- Win rate 47.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_pullback | XAUUSD | M30
WR=47.1%  Sharpe=-1.78  MaxDD=38.2%  Trades=359

**Parameter Tweaks:**
- Win rate 47.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 38.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### session_momentum | XAUUSD | M5
WR=47.1%  Sharpe=-1.74  MaxDD=4.6%  Trades=51

**Parameter Tweaks:**
- Win rate 47.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | XAUUSD | H2
WR=47.0%  Sharpe=-0.44  MaxDD=13.8%  Trades=100

**Parameter Tweaks:**
- Win rate 47.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.44 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | BTCUSD | M5
WR=46.9%  Sharpe=-3.00  MaxDD=12.6%  Trades=209

**Parameter Tweaks:**
- Win rate 46.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | H4
WR=46.9%  Sharpe=-7.67  MaxDD=2.9%  Trades=32

**Parameter Tweaks:**
- Win rate 46.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | M30
WR=46.6%  Sharpe=-2.74  MaxDD=16.9%  Trades=118

**Parameter Tweaks:**
- Win rate 46.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### macd_trend | USDJPY | M5
WR=46.6%  Sharpe=-2.88  MaxDD=1.1%  Trades=73

**Parameter Tweaks:**
- Win rate 46.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.88 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### gold_momentum_breakout | USTEC | M5
WR=46.6%  Sharpe=-1.47  MaxDD=0.7%  Trades=262

**Parameter Tweaks:**
- Win rate 46.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.47 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on USTEC unless confirmed by live data

### dual_ema_fractal | XAUUSD | M30
WR=46.5%  Sharpe=-2.54  MaxDD=28.7%  Trades=301

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 28.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | USDCAD | M15
WR=46.5%  Sharpe=-2.93  MaxDD=2.6%  Trades=129

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### cot_sentiment | EURUSD | H4
WR=46.5%  Sharpe=-0.70  MaxDD=6.9%  Trades=314

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.70 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.90 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | GBPJPY | H1
WR=46.5%  Sharpe=-3.50  MaxDD=5.7%  Trades=99

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.50 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_bounce | XAUUSD | M30
WR=46.3%  Sharpe=-6.85  MaxDD=7.3%  Trades=41

**Parameter Tweaks:**
- Win rate 46.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.85 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | GBPUSD | H4
WR=46.3%  Sharpe=-3.43  MaxDD=4.1%  Trades=41

**Parameter Tweaks:**
- Win rate 46.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.43 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | M15
WR=46.3%  Sharpe=-2.57  MaxDD=12.6%  Trades=134

**Parameter Tweaks:**
- Win rate 46.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.57 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H4
WR=46.1%  Sharpe=3.13  MaxDD=8.6%  Trades=13

**Parameter Tweaks:**
- Win rate 46.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_momentum | XAUUSD | M30
WR=46.1%  Sharpe=-1.45  MaxDD=16.3%  Trades=102

**Parameter Tweaks:**
- Win rate 46.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.45 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | AAPL | H1
WR=46.0%  Sharpe=-2.57  MaxDD=1.7%  Trades=76

**Parameter Tweaks:**
- Win rate 46.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.57 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on AAPL unless confirmed by live data

### rsi_bounce | XAUUSD | M5
WR=46.0%  Sharpe=-1.32  MaxDD=4.5%  Trades=50

**Parameter Tweaks:**
- Win rate 46.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | XAUUSD | H2
WR=46.0%  Sharpe=-1.52  MaxDD=20.0%  Trades=74

**Parameter Tweaks:**
- Win rate 46.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.52 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | EURUSD | M30
WR=45.9%  Sharpe=-4.78  MaxDD=9.3%  Trades=316

**Parameter Tweaks:**
- Win rate 45.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | H1
WR=45.8%  Sharpe=-0.12  MaxDD=5.7%  Trades=48

**Parameter Tweaks:**
- Win rate 45.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.12 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.98 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | AAPL | M15
WR=45.8%  Sharpe=-0.76  MaxDD=3.0%  Trades=330

**Parameter Tweaks:**
- Win rate 45.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.89 — marginal edge, consider disabling on AAPL unless confirmed by live data

### turtle_soup | GBPJPY | M30
WR=45.7%  Sharpe=-3.54  MaxDD=8.9%  Trades=210

**Parameter Tweaks:**
- Win rate 45.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### ema_ribbon_trend | AMD | M5
WR=45.6%  Sharpe=-2.83  MaxDD=1.1%  Trades=57

**Parameter Tweaks:**
- Win rate 45.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on AMD unless confirmed by live data

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

### rsi_bounce | USOIL | H1
WR=45.5%  Sharpe=-4.54  MaxDD=3.1%  Trades=22

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 22 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on USOIL unless confirmed by live data

### session_momentum | XAUUSD | M30
WR=45.5%  Sharpe=-3.61  MaxDD=5.5%  Trades=55

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.61 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | BTCUSD | M15
WR=45.5%  Sharpe=-3.13  MaxDD=19.8%  Trades=198

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | H1
WR=45.5%  Sharpe=-2.41  MaxDD=1.1%  Trades=22

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 22 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | GBPUSD | M15
WR=45.5%  Sharpe=-4.91  MaxDD=3.8%  Trades=77

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.91 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### hikkake_trap | GBPUSD | M30
WR=45.5%  Sharpe=-3.25  MaxDD=7.7%  Trades=154

**Parameter Tweaks:**
- Win rate 45.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.25 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | M15
WR=45.4%  Sharpe=-3.41  MaxDD=7.6%  Trades=249

**Parameter Tweaks:**
- Win rate 45.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | H1
WR=45.4%  Sharpe=-3.79  MaxDD=4.0%  Trades=130

**Parameter Tweaks:**
- Win rate 45.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.79 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | H12
WR=45.3%  Sharpe=-2.74  MaxDD=46.3%  Trades=64

**Parameter Tweaks:**
- Win rate 45.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 46.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | USTEC | M30
WR=45.2%  Sharpe=-0.71  MaxDD=1.1%  Trades=323

**Parameter Tweaks:**
- Win rate 45.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.71 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.90 — marginal edge, consider disabling on USTEC unless confirmed by live data

### dual_ema_fractal | EURUSD | H2
WR=45.2%  Sharpe=-2.73  MaxDD=5.5%  Trades=124

**Parameter Tweaks:**
- Win rate 45.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | BTCUSD | H4
WR=45.2%  Sharpe=-1.05  MaxDD=6.7%  Trades=31

**Parameter Tweaks:**
- Win rate 45.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.05 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.86 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### range_breakout | XAUUSD | H1
WR=45.1%  Sharpe=0.06  MaxDD=14.4%  Trades=184

**Parameter Tweaks:**
- Win rate 45.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.06 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.01 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | M15
WR=45.0%  Sharpe=-1.28  MaxDD=23.9%  Trades=331

**Parameter Tweaks:**
- Win rate 45.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover | EURUSD | M30
WR=45.0%  Sharpe=-1.89  MaxDD=1.0%  Trades=40

**Parameter Tweaks:**
- Win rate 45.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | H2
WR=45.0%  Sharpe=-0.30  MaxDD=3.9%  Trades=60

**Parameter Tweaks:**
- Win rate 45.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.30 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.95 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup | AUDUSD | M30
WR=44.9%  Sharpe=-3.73  MaxDD=6.4%  Trades=187

**Parameter Tweaks:**
- Win rate 44.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_pullback | USDJPY | D1
WR=44.8%  Sharpe=-0.87  MaxDD=5.8%  Trades=29

**Parameter Tweaks:**
- Win rate 44.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.87 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.88 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_pullback | USDJPY | M5
WR=44.8%  Sharpe=-3.35  MaxDD=5.2%  Trades=297

**Parameter Tweaks:**
- Win rate 44.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend | USOIL | M30
WR=44.7%  Sharpe=-3.23  MaxDD=9.3%  Trades=76

**Parameter Tweaks:**
- Win rate 44.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | H4
WR=44.7%  Sharpe=-2.33  MaxDD=5.7%  Trades=47

**Parameter Tweaks:**
- Win rate 44.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.33 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M5
WR=44.6%  Sharpe=-1.55  MaxDD=27.0%  Trades=314

**Parameter Tweaks:**
- Win rate 44.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 27.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | GBPUSD | M30
WR=44.5%  Sharpe=-3.14  MaxDD=8.3%  Trades=247

**Parameter Tweaks:**
- Win rate 44.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.14 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H1
WR=44.5%  Sharpe=-1.71  MaxDD=3.9%  Trades=182

**Parameter Tweaks:**
- Win rate 44.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.71 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USTEC | M5
WR=44.4%  Sharpe=-3.48  MaxDD=0.2%  Trades=27

**Parameter Tweaks:**
- Win rate 44.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.48 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on USTEC unless confirmed by live data

### gold_momentum_breakout | NVDA | H1
WR=44.4%  Sharpe=2.80  MaxDD=0.3%  Trades=36

**Parameter Tweaks:**
- Win rate 44.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### session_momentum | XAUUSD | H12
WR=44.4%  Sharpe=0.30  MaxDD=7.5%  Trades=9

**Parameter Tweaks:**
- Win rate 44.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.30 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.06 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | XAGUSD | H2
WR=44.3%  Sharpe=-1.10  MaxDD=28.5%  Trades=88

**Parameter Tweaks:**
- Win rate 44.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 28.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | M15
WR=44.3%  Sharpe=-2.11  MaxDD=6.3%  Trades=332

**Parameter Tweaks:**
- Win rate 44.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_pullback | EURUSD | H2
WR=44.2%  Sharpe=-3.08  MaxDD=5.2%  Trades=95

**Parameter Tweaks:**
- Win rate 44.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.08 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | XAUUSD | M15
WR=44.2%  Sharpe=-1.78  MaxDD=33.1%  Trades=428

**Parameter Tweaks:**
- Win rate 44.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 33.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### range_breakout | EURUSD | H1
WR=44.2%  Sharpe=-3.89  MaxDD=6.2%  Trades=231

**Parameter Tweaks:**
- Win rate 44.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | US500 | M15
WR=44.1%  Sharpe=-2.09  MaxDD=0.6%  Trades=410

**Parameter Tweaks:**
- Win rate 44.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.09 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on US500 unless confirmed by live data

### range_breakout | USTEC | M15
WR=44.1%  Sharpe=-1.18  MaxDD=0.8%  Trades=256

**Parameter Tweaks:**
- Win rate 44.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.18 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.83 — marginal edge, consider disabling on USTEC unless confirmed by live data

### ema_ribbon_trend | BTCUSD | M5
WR=44.0%  Sharpe=-5.97  MaxDD=11.1%  Trades=84

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### range_breakout | USTEC | M5
WR=44.0%  Sharpe=-2.54  MaxDD=0.7%  Trades=193

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.54 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on USTEC unless confirmed by live data

### range_breakout | XAUUSD | H2
WR=44.0%  Sharpe=-1.85  MaxDD=11.4%  Trades=75

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.85 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | GBPJPY | H4
WR=44.0%  Sharpe=-5.25  MaxDD=4.6%  Trades=25

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.25 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_fractal | EURUSD | M15
WR=44.0%  Sharpe=-3.24  MaxDD=6.6%  Trades=291

**Parameter Tweaks:**
- Win rate 44.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.24 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_pullback | EURUSD | M30
WR=43.9%  Sharpe=-4.53  MaxDD=9.5%  Trades=294

**Parameter Tweaks:**
- Win rate 43.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPUSD | M15
WR=43.6%  Sharpe=-1.20  MaxDD=0.7%  Trades=39

**Parameter Tweaks:**
- Win rate 43.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.20 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | USTEC | M30
WR=43.5%  Sharpe=-1.21  MaxDD=0.9%  Trades=230

**Parameter Tweaks:**
- Win rate 43.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.21 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_pullback | XAUUSD | H1
WR=43.5%  Sharpe=-0.72  MaxDD=43.3%  Trades=253

**Parameter Tweaks:**
- Win rate 43.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 43.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.87 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | M15
WR=43.5%  Sharpe=-3.38  MaxDD=11.2%  Trades=451

**Parameter Tweaks:**
- Win rate 43.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.38 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | M15
WR=43.3%  Sharpe=-1.34  MaxDD=200.8%  Trades=1816

**Parameter Tweaks:**
- Win rate 43.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 200.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.34 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### cot_sentiment | EURUSD | H2
WR=43.3%  Sharpe=-2.28  MaxDD=24.0%  Trades=676

**Parameter Tweaks:**
- Win rate 43.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_pullback | XAGUSD | D1
WR=43.3%  Sharpe=-1.13  MaxDD=27.5%  Trades=30

**Parameter Tweaks:**
- Win rate 43.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 27.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### rsi_pullback | EURUSD | D1
WR=43.2%  Sharpe=-2.68  MaxDD=8.3%  Trades=37

**Parameter Tweaks:**
- Win rate 43.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.68 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.68 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb | XAUUSD | M30
WR=43.2%  Sharpe=-2.69  MaxDD=19.7%  Trades=37

**Parameter Tweaks:**
- Win rate 43.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.69 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | USOIL | M30
WR=43.2%  Sharpe=-2.76  MaxDD=12.5%  Trades=199

**Parameter Tweaks:**
- Win rate 43.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on USOIL unless confirmed by live data

### turtle_soup | GBPUSD | H2
WR=43.1%  Sharpe=-2.17  MaxDD=6.1%  Trades=102

**Parameter Tweaks:**
- Win rate 43.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.17 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | EURUSD | M15
WR=43.0%  Sharpe=-4.02  MaxDD=9.3%  Trades=367

**Parameter Tweaks:**
- Win rate 43.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.02 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | M15
WR=43.0%  Sharpe=-2.18  MaxDD=2.4%  Trades=79

**Parameter Tweaks:**
- Win rate 43.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.18 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | AUDUSD | H1
WR=42.9%  Sharpe=-5.39  MaxDD=2.3%  Trades=49

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### macd_trend | USTEC | H4
WR=42.9%  Sharpe=-0.00  MaxDD=0.2%  Trades=7

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.00 — marginal edge, consider disabling on USTEC unless confirmed by live data

### gold_momentum_breakout | GBPUSD | H12
WR=42.9%  Sharpe=-9.73  MaxDD=2.0%  Trades=7

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.23 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | M30
WR=42.8%  Sharpe=-3.84  MaxDD=12.7%  Trades=360

**Parameter Tweaks:**
- Win rate 42.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | USOIL | H1
WR=42.7%  Sharpe=-2.93  MaxDD=10.2%  Trades=82

**Parameter Tweaks:**
- Win rate 42.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_bounce | USOIL | M15
WR=42.6%  Sharpe=-4.92  MaxDD=5.5%  Trades=54

**Parameter Tweaks:**
- Win rate 42.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.92 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on USOIL unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H1
WR=42.6%  Sharpe=-3.84  MaxDD=12.6%  Trades=54

**Parameter Tweaks:**
- Win rate 42.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### macd_trend | USOIL | H1
WR=42.5%  Sharpe=-4.41  MaxDD=9.1%  Trades=47

**Parameter Tweaks:**
- Win rate 42.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on USOIL unless confirmed by live data

### turtle_soup | USDCAD | H4
WR=42.5%  Sharpe=-4.14  MaxDD=3.2%  Trades=47

**Parameter Tweaks:**
- Win rate 42.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.14 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### orb | XAUUSD | M15
WR=42.5%  Sharpe=-4.02  MaxDD=18.8%  Trades=40

**Parameter Tweaks:**
- Win rate 42.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.02 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | USDJPY | M30
WR=42.5%  Sharpe=-1.49  MaxDD=2.6%  Trades=73

**Parameter Tweaks:**
- Win rate 42.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.49 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### dual_ema_fractal | EURUSD | M30
WR=42.4%  Sharpe=-3.64  MaxDD=8.5%  Trades=262

**Parameter Tweaks:**
- Win rate 42.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.64 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | US500 | M30
WR=42.3%  Sharpe=-2.93  MaxDD=0.4%  Trades=227

**Parameter Tweaks:**
- Win rate 42.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on US500 unless confirmed by live data

### range_breakout | US500 | H1
WR=42.1%  Sharpe=-1.28  MaxDD=0.2%  Trades=209

**Parameter Tweaks:**
- Win rate 42.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.82 — marginal edge, consider disabling on US500 unless confirmed by live data

### turtle_soup | ETHUSD | M30
WR=42.0%  Sharpe=-5.18  MaxDD=2.6%  Trades=207

**Parameter Tweaks:**
- Win rate 42.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.18 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### turtle_soup | GBPUSD | M30
WR=42.0%  Sharpe=-3.94  MaxDD=11.6%  Trades=319

**Parameter Tweaks:**
- Win rate 42.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.94 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | USOIL | H1
WR=42.0%  Sharpe=-3.29  MaxDD=26.5%  Trades=267

**Parameter Tweaks:**
- Win rate 42.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.29 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on USOIL unless confirmed by live data

### turtle_soup | EURUSD | H4
WR=41.9%  Sharpe=-4.93  MaxDD=3.8%  Trades=43

**Parameter Tweaks:**
- Win rate 41.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | BTCUSD | M30
WR=41.7%  Sharpe=-3.35  MaxDD=29.7%  Trades=199

**Parameter Tweaks:**
- Win rate 41.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 29.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rsi_bounce | USDCAD | M15
WR=41.7%  Sharpe=-7.00  MaxDD=0.7%  Trades=24

**Parameter Tweaks:**
- Win rate 41.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### macd_trend | GBPJPY | H1
WR=41.5%  Sharpe=-2.23  MaxDD=5.5%  Trades=65

**Parameter Tweaks:**
- Win rate 41.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.69 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### gold_momentum_breakout | USOIL | M15
WR=41.4%  Sharpe=-2.75  MaxDD=26.1%  Trades=548

**Parameter Tweaks:**
- Win rate 41.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 26.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.75 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_bounce | USDJPY | M15
WR=41.4%  Sharpe=-3.28  MaxDD=1.1%  Trades=29

**Parameter Tweaks:**
- Win rate 41.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | H1
WR=41.4%  Sharpe=-2.63  MaxDD=10.1%  Trades=174

**Parameter Tweaks:**
- Win rate 41.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_bounce | EURUSD | M15
WR=41.3%  Sharpe=-4.42  MaxDD=0.7%  Trades=46

**Parameter Tweaks:**
- Win rate 41.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_pullback | USDJPY | H2
WR=41.3%  Sharpe=-5.49  MaxDD=11.8%  Trades=92

**Parameter Tweaks:**
- Win rate 41.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.49 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### turtle_soup | EURUSD | H2
WR=41.3%  Sharpe=-3.02  MaxDD=4.8%  Trades=92

**Parameter Tweaks:**
- Win rate 41.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.02 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USDJPY | H2
WR=41.2%  Sharpe=-3.13  MaxDD=2.3%  Trades=17

**Parameter Tweaks:**
- Win rate 41.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_pullback | XAGUSD | H12
WR=41.2%  Sharpe=-3.59  MaxDD=14.6%  Trades=17

**Parameter Tweaks:**
- Win rate 41.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.59 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### rsi_pullback | GBPUSD | H1
WR=41.1%  Sharpe=-3.86  MaxDD=12.0%  Trades=209

**Parameter Tweaks:**
- Win rate 41.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup | GBPUSD | H1
WR=41.1%  Sharpe=-3.97  MaxDD=9.5%  Trades=175

**Parameter Tweaks:**
- Win rate 41.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### cot_sentiment | EURUSD | H1
WR=41.0%  Sharpe=-3.28  MaxDD=45.8%  Trades=1346

**Parameter Tweaks:**
- Win rate 41.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 45.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.28 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | GBPJPY | M15
WR=40.9%  Sharpe=-5.39  MaxDD=1.7%  Trades=44

**Parameter Tweaks:**
- Win rate 40.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### session_momentum | EURUSD | M30
WR=40.7%  Sharpe=-3.31  MaxDD=3.3%  Trades=135

**Parameter Tweaks:**
- Win rate 40.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.31 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### stat_arb_gold_silver | XAUUSD | D1
WR=40.6%  Sharpe=-2.53  MaxDD=74.5%  Trades=138

**Parameter Tweaks:**
- Win rate 40.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 74.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | USDCAD | M30
WR=40.5%  Sharpe=-4.84  MaxDD=6.3%  Trades=148

**Parameter Tweaks:**
- Win rate 40.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_pullback | GBPUSD | H2
WR=40.5%  Sharpe=-2.92  MaxDD=7.5%  Trades=84

**Parameter Tweaks:**
- Win rate 40.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.92 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | XAUUSD | M15
WR=40.2%  Sharpe=-4.16  MaxDD=20.7%  Trades=102

**Parameter Tweaks:**
- Win rate 40.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 20.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | M15
WR=40.2%  Sharpe=-4.80  MaxDD=12.9%  Trades=413

**Parameter Tweaks:**
- Win rate 40.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.80 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | EURUSD | H1
WR=40.1%  Sharpe=-4.23  MaxDD=8.1%  Trades=192

**Parameter Tweaks:**
- Win rate 40.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | M5
WR=40.1%  Sharpe=-1.44  MaxDD=18.7%  Trades=222

**Parameter Tweaks:**
- Win rate 40.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.44 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | XAUUSD | H1
WR=40.0%  Sharpe=-5.26  MaxDD=4.1%  Trades=15

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.26 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend | US500 | M30
WR=40.0%  Sharpe=-3.24  MaxDD=0.1%  Trades=25

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -3.24 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.64 — marginal edge, consider disabling on US500 unless confirmed by live data

### range_breakout | XAUUSD | H12
WR=40.0%  Sharpe=-9.87  MaxDD=1.6%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.87 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.23 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### range_breakout | US500 | H2
WR=40.0%  Sharpe=-1.57  MaxDD=0.0%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.57 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on US500 unless confirmed by live data

### range_breakout | USTEC | H2
WR=40.0%  Sharpe=-9.72  MaxDD=0.2%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.23 — marginal edge, consider disabling on USTEC unless confirmed by live data

### ema_ribbon_trend | XAUUSD | M30
WR=40.0%  Sharpe=-6.96  MaxDD=1.2%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup | AUDUSD | H4
WR=40.0%  Sharpe=-1.94  MaxDD=2.7%  Trades=40

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.94 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### turtle_soup | AUDUSD | D1
WR=40.0%  Sharpe=-2.01  MaxDD=2.0%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.01 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_momentum | GBPUSD | H1
WR=40.0%  Sharpe=-6.41  MaxDD=3.2%  Trades=35

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.40 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum | GBPUSD | H4
WR=40.0%  Sharpe=-10.09  MaxDD=0.8%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -10.09 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.22 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### orb | AUDUSD | M5
WR=40.0%  Sharpe=-15.45  MaxDD=0.2%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -15.45 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.05 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | M30
WR=40.0%  Sharpe=-4.15  MaxDD=1.9%  Trades=5

**Parameter Tweaks:**
- Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.15 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | USDCAD | H1
WR=39.7%  Sharpe=-4.98  MaxDD=2.6%  Trades=68

**Parameter Tweaks:**
- Win rate 39.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.98 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### macd_trend | AUDUSD | M15
WR=39.7%  Sharpe=-6.95  MaxDD=2.0%  Trades=63

**Parameter Tweaks:**
- Win rate 39.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | H1
WR=39.5%  Sharpe=-3.73  MaxDD=5.5%  Trades=167

**Parameter Tweaks:**
- Win rate 39.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | XAUUSD | M15
WR=39.5%  Sharpe=-4.47  MaxDD=8.3%  Trades=76

**Parameter Tweaks:**
- Win rate 39.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.47 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout | US500 | M5
WR=39.4%  Sharpe=-1.95  MaxDD=0.2%  Trades=249

**Parameter Tweaks:**
- Win rate 39.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on US500 unless confirmed by live data

### dual_ema_fractal | USOIL | M15
WR=39.2%  Sharpe=-1.55  MaxDD=7.5%  Trades=158

**Parameter Tweaks:**
- Win rate 39.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.75 — marginal edge, consider disabling on USOIL unless confirmed by live data

### turtle_soup | ETHUSD | H1
WR=39.1%  Sharpe=-5.63  MaxDD=2.5%  Trades=138

**Parameter Tweaks:**
- Win rate 39.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### cot_sentiment | EURUSD | M30
WR=39.1%  Sharpe=-4.42  MaxDD=83.6%  Trades=2638

**Parameter Tweaks:**
- Win rate 39.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 83.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | AUDUSD | M30
WR=39.0%  Sharpe=-6.93  MaxDD=1.8%  Trades=41

**Parameter Tweaks:**
- Win rate 39.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.38 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### range_breakout | US500 | M15
WR=38.8%  Sharpe=-3.21  MaxDD=0.4%  Trades=281

**Parameter Tweaks:**
- Win rate 38.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.21 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.61 — marginal edge, consider disabling on US500 unless confirmed by live data

### dual_ema_momentum | GBPUSD | M30
WR=38.8%  Sharpe=-6.80  MaxDD=3.8%  Trades=49

**Parameter Tweaks:**
- Win rate 38.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.80 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | USOIL | M30
WR=38.7%  Sharpe=-3.43  MaxDD=25.6%  Trades=408

**Parameter Tweaks:**
- Win rate 38.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 25.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.43 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on USOIL unless confirmed by live data

### macd_trend | GBPJPY | M5
WR=38.7%  Sharpe=-6.71  MaxDD=3.6%  Trades=119

**Parameter Tweaks:**
- Win rate 38.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.71 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### cot_sentiment | XAUUSD | H4
WR=38.6%  Sharpe=-2.56  MaxDD=114.1%  Trades=342

**Parameter Tweaks:**
- Win rate 38.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 114.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### session_momentum | EURUSD | M5
WR=38.4%  Sharpe=-4.07  MaxDD=1.4%  Trades=99

**Parameter Tweaks:**
- Win rate 38.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.07 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | M30
WR=38.1%  Sharpe=-4.65  MaxDD=12.6%  Trades=270

**Parameter Tweaks:**
- Win rate 38.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.65 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### ma_crossover | GBPJPY | M5
WR=37.9%  Sharpe=-2.89  MaxDD=0.6%  Trades=29

**Parameter Tweaks:**
- Win rate 37.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### range_breakout | XAUUSD | M15
WR=37.8%  Sharpe=-1.85  MaxDD=28.2%  Trades=399

**Parameter Tweaks:**
- Win rate 37.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 28.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.85 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### range_breakout | USOIL | M15
WR=37.8%  Sharpe=-3.41  MaxDD=24.8%  Trades=479

**Parameter Tweaks:**
- Win rate 37.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 24.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.57 — marginal edge, consider disabling on USOIL unless confirmed by live data

### gold_momentum_breakout | NVDA | M15
WR=37.7%  Sharpe=-1.50  MaxDD=1.9%  Trades=265

**Parameter Tweaks:**
- Win rate 37.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.50 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.77 — marginal edge, consider disabling on NVDA unless confirmed by live data

### range_breakout | EURUSD | M30
WR=37.7%  Sharpe=-3.96  MaxDD=6.4%  Trades=289

**Parameter Tweaks:**
- Win rate 37.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.55 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | XAUUSD | M30
WR=37.6%  Sharpe=-3.65  MaxDD=46.0%  Trades=314

**Parameter Tweaks:**
- Win rate 37.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 46.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.65 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | H12
WR=37.5%  Sharpe=-4.94  MaxDD=1.1%  Trades=8

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.94 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | NVDA | M30
WR=37.5%  Sharpe=-2.40  MaxDD=1.3%  Trades=104

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.40 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on NVDA unless confirmed by live data

### bb_squeeze_scalp | US500 | H1
WR=37.5%  Sharpe=-0.90  MaxDD=0.1%  Trades=24

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -0.90 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.88 — marginal edge, consider disabling on US500 unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M15
WR=37.4%  Sharpe=-4.22  MaxDD=9.6%  Trades=471

**Parameter Tweaks:**
- Win rate 37.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | USDCAD | M30
WR=37.4%  Sharpe=-6.04  MaxDD=6.1%  Trades=190

**Parameter Tweaks:**
- Win rate 37.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.40 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### turtle_soup | GBPUSD | M15
WR=37.2%  Sharpe=-6.36  MaxDD=9.3%  Trades=239

**Parameter Tweaks:**
- Win rate 37.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.36 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.38 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | M30
WR=37.2%  Sharpe=-5.39  MaxDD=6.4%  Trades=223

**Parameter Tweaks:**
- Win rate 37.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### gold_momentum_breakout | MSFT | M5
WR=37.1%  Sharpe=-3.97  MaxDD=9.6%  Trades=525

**Parameter Tweaks:**
- Win rate 37.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on MSFT unless confirmed by live data

### cot_sentiment | XAUUSD | H1
WR=36.7%  Sharpe=-4.41  MaxDD=360.8%  Trades=1559

**Parameter Tweaks:**
- Win rate 36.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 360.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | USOIL | H4
WR=36.7%  Sharpe=-5.89  MaxDD=9.6%  Trades=30

**Parameter Tweaks:**
- Win rate 36.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rvgi_cci_confluence | USDCAD | H1
WR=36.5%  Sharpe=-4.01  MaxDD=3.3%  Trades=104

**Parameter Tweaks:**
- Win rate 36.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.01 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.56 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### cot_sentiment | XAUUSD | H2
WR=36.5%  Sharpe=-4.32  MaxDD=242.9%  Trades=782

**Parameter Tweaks:**
- Win rate 36.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 242.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | EURUSD | M5
WR=36.4%  Sharpe=-4.63  MaxDD=3.1%  Trades=162

**Parameter Tweaks:**
- Win rate 36.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | XAUUSD | M30
WR=36.4%  Sharpe=-4.51  MaxDD=508.2%  Trades=2963

**Parameter Tweaks:**
- Win rate 36.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 508.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | GBPJPY | M5
WR=36.4%  Sharpe=-5.73  MaxDD=0.9%  Trades=44

**Parameter Tweaks:**
- Win rate 36.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### orb | AUDUSD | H1
WR=36.4%  Sharpe=-9.56  MaxDD=1.4%  Trades=11

**Parameter Tweaks:**
- Win rate 36.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.24 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### gold_momentum_breakout | AAPL | M5
WR=36.1%  Sharpe=-2.47  MaxDD=3.8%  Trades=549

**Parameter Tweaks:**
- Win rate 36.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.47 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on AAPL unless confirmed by live data

### ema_ribbon_trend | USTEC | M15
WR=36.0%  Sharpe=-4.25  MaxDD=0.6%  Trades=25

**Parameter Tweaks:**
- Win rate 36.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 25 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.25 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_bounce | EURUSD | M30
WR=35.7%  Sharpe=-13.93  MaxDD=1.8%  Trades=28

**Parameter Tweaks:**
- Win rate 35.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 28 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -13.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | AUDUSD | M5
WR=35.7%  Sharpe=-4.72  MaxDD=0.3%  Trades=14

**Parameter Tweaks:**
- Win rate 35.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | M5
WR=35.6%  Sharpe=-5.22  MaxDD=2.8%  Trades=115

**Parameter Tweaks:**
- Win rate 35.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | XAUUSD | M5
WR=35.5%  Sharpe=-4.41  MaxDD=34.1%  Trades=282

**Parameter Tweaks:**
- Win rate 35.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 34.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | EURUSD | H1
WR=35.3%  Sharpe=-5.88  MaxDD=1.1%  Trades=17

**Parameter Tweaks:**
- Win rate 35.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.88 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H2
WR=35.3%  Sharpe=-6.90  MaxDD=9.1%  Trades=17

**Parameter Tweaks:**
- Win rate 35.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.90 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | NVDA | M5
WR=35.3%  Sharpe=-5.50  MaxDD=0.9%  Trades=51

**Parameter Tweaks:**
- Win rate 35.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.50 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on NVDA unless confirmed by live data

### turtle_soup | EURUSD | M15
WR=35.3%  Sharpe=-5.79  MaxDD=7.4%  Trades=272

**Parameter Tweaks:**
- Win rate 35.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.79 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | USTEC | H1
WR=35.2%  Sharpe=-2.14  MaxDD=1.6%  Trades=199

**Parameter Tweaks:**
- Win rate 35.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.14 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on USTEC unless confirmed by live data

### session_momentum | EURUSD | M15
WR=35.1%  Sharpe=-5.53  MaxDD=5.3%  Trades=171

**Parameter Tweaks:**
- Win rate 35.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | GBPJPY | M5
WR=35.0%  Sharpe=-5.06  MaxDD=4.1%  Trades=163

**Parameter Tweaks:**
- Win rate 35.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.06 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### macd_trend | USOIL | M5
WR=34.9%  Sharpe=-5.77  MaxDD=5.9%  Trades=86

**Parameter Tweaks:**
- Win rate 34.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.77 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on USOIL unless confirmed by live data

### dual_ema_fractal | USDCAD | M30
WR=34.4%  Sharpe=-4.64  MaxDD=1.9%  Trades=61

**Parameter Tweaks:**
- Win rate 34.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.64 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### ma_crossover | EURUSD | M15
WR=34.4%  Sharpe=-5.30  MaxDD=2.1%  Trades=61

**Parameter Tweaks:**
- Win rate 34.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.30 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend | USTEC | M15
WR=34.4%  Sharpe=-9.67  MaxDD=0.4%  Trades=32

**Parameter Tweaks:**
- Win rate 34.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -9.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.27 — marginal edge, consider disabling on USTEC unless confirmed by live data

### turtle_soup | ETHUSD | M15
WR=34.0%  Sharpe=-7.14  MaxDD=3.5%  Trades=297

**Parameter Tweaks:**
- Win rate 34.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.14 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### dual_ema_momentum | EURUSD | M5
WR=34.0%  Sharpe=-7.66  MaxDD=1.9%  Trades=50

**Parameter Tweaks:**
- Win rate 34.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | XAUUSD | M15
WR=33.9%  Sharpe=-5.46  MaxDD=826.6%  Trades=5615

**Parameter Tweaks:**
- Win rate 33.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 826.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -5.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | M15
WR=33.4%  Sharpe=-5.61  MaxDD=13.7%  Trades=395

**Parameter Tweaks:**
- Win rate 33.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.61 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### cot_sentiment | XAUUSD | M5
WR=33.4%  Sharpe=-6.15  MaxDD=423.3%  Trades=2936

**Parameter Tweaks:**
- Win rate 33.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 423.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -6.15 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal | XAUUSD | H12
WR=33.3%  Sharpe=2.08  MaxDD=8.0%  Trades=12

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter

### dual_ema_fractal | GBPJPY | D1
WR=33.3%  Sharpe=-2.72  MaxDD=1.7%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_fractal | USDCAD | H2
WR=33.3%  Sharpe=-1.76  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.76 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_bounce | EURUSD | H4
WR=33.3%  Sharpe=-9.32  MaxDD=1.2%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.28 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce | XAUUSD | M15
WR=33.3%  Sharpe=-6.42  MaxDD=9.7%  Trades=42

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce | GBPUSD | H4
WR=33.3%  Sharpe=-10.77  MaxDD=0.7%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -10.77 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.19 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | GBPUSD | D1
WR=33.3%  Sharpe=-8.55  MaxDD=0.8%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -8.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.27 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | USDJPY | H12
WR=33.3%  Sharpe=-4.96  MaxDD=0.9%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_bounce | USDCAD | D1
WR=33.3%  Sharpe=-1.11  MaxDD=1.0%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### macd_trend | AUDUSD | D1
WR=33.3%  Sharpe=-1.32  MaxDD=1.5%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.81 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### gold_momentum_breakout | NVDA | H2
WR=33.3%  Sharpe=-12.29  MaxDD=0.2%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.29 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.14 — marginal edge, consider disabling on NVDA unless confirmed by live data

### gold_momentum_breakout | MSFT | H2
WR=33.3%  Sharpe=-11.00  MaxDD=0.6%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -11.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.18 — marginal edge, consider disabling on MSFT unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H4
WR=33.3%  Sharpe=-5.55  MaxDD=6.5%  Trades=12

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H12
WR=33.3%  Sharpe=0.89  MaxDD=1.1%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.16 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | M30
WR=33.3%  Sharpe=-5.95  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.27 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### ema_ribbon_trend | MSFT | M30
WR=33.3%  Sharpe=-12.18  MaxDD=0.8%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.18 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.14 — marginal edge, consider disabling on MSFT unless confirmed by live data

### turtle_soup | GBPJPY | H2
WR=33.3%  Sharpe=-9.62  MaxDD=0.7%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.62 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.25 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### turtle_soup | GBPJPY | D1
WR=33.3%  Sharpe=-6.79  MaxDD=0.8%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.79 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### dual_ema_momentum | GBPUSD | M5
WR=33.3%  Sharpe=-10.31  MaxDD=1.8%  Trades=33

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -10.31 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.18 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | USDCAD | D1
WR=33.3%  Sharpe=-5.56  MaxDD=3.0%  Trades=21

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_extremes_scalp | EURUSD | M5
WR=33.3%  Sharpe=-10.93  MaxDD=0.1%  Trades=3

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -10.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.11 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | EURUSD | M15
WR=33.3%  Sharpe=-9.16  MaxDD=0.1%  Trades=6

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -9.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.25 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | EURUSD | M15
WR=33.2%  Sharpe=-5.65  MaxDD=7.8%  Trades=340

**Parameter Tweaks:**
- Win rate 33.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.65 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.42 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | AMD | M5
WR=33.1%  Sharpe=-4.83  MaxDD=8.9%  Trades=583

**Parameter Tweaks:**
- Win rate 33.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.46 — marginal edge, consider disabling on AMD unless confirmed by live data

### range_breakout | US500 | M5
WR=32.5%  Sharpe=-4.80  MaxDD=0.3%  Trades=197

**Parameter Tweaks:**
- Win rate 32.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.80 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on US500 unless confirmed by live data

### ma_crossover | AUDUSD | M15
WR=32.4%  Sharpe=-1.97  MaxDD=0.9%  Trades=34

**Parameter Tweaks:**
- Win rate 32.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### hikkake_trap | GBPUSD | M5
WR=31.7%  Sharpe=-8.16  MaxDD=7.6%  Trades=199

**Parameter Tweaks:**
- Win rate 31.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.16 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp | XAUUSD | H1
WR=31.6%  Sharpe=-8.86  MaxDD=5.8%  Trades=19

**Parameter Tweaks:**
- Win rate 31.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -8.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence | USDCAD | M15
WR=31.6%  Sharpe=-4.57  MaxDD=6.2%  Trades=301

**Parameter Tweaks:**
- Win rate 31.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.57 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.48 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### cot_sentiment | EURUSD | M15
WR=31.5%  Sharpe=-5.97  MaxDD=152.6%  Trades=4912

**Parameter Tweaks:**
- Win rate 31.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 152.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -5.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.39 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | USDCAD | M5
WR=31.5%  Sharpe=-1.67  MaxDD=0.7%  Trades=54

**Parameter Tweaks:**
- Win rate 31.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### dual_ema_fractal | USDCAD | M15
WR=30.9%  Sharpe=-7.51  MaxDD=1.3%  Trades=42

**Parameter Tweaks:**
- Win rate 30.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_pullback | XAUUSD | H12
WR=30.8%  Sharpe=-1.81  MaxDD=27.2%  Trades=13

**Parameter Tweaks:**
- Win rate 30.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 27.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.81 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.70 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_pullback | EURUSD | M5
WR=30.7%  Sharpe=-6.67  MaxDD=10.5%  Trades=411

**Parameter Tweaks:**
- Win rate 30.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | AUDUSD | M15
WR=30.5%  Sharpe=-6.42  MaxDD=1.7%  Trades=59

**Parameter Tweaks:**
- Win rate 30.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### orb | GBPJPY | H1
WR=30.4%  Sharpe=-7.82  MaxDD=3.6%  Trades=23

**Parameter Tweaks:**
- Win rate 30.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 23 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.82 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

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

### rvgi_cci_confluence | GBPJPY | D1
WR=30.0%  Sharpe=-1.12  MaxDD=6.1%  Trades=20

**Parameter Tweaks:**
- Win rate 30.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.12 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.84 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_bounce | GBPUSD | M5
WR=29.4%  Sharpe=-7.63  MaxDD=0.9%  Trades=34

**Parameter Tweaks:**
- Win rate 29.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout | EURUSD | H12
WR=28.6%  Sharpe=-5.72  MaxDD=1.3%  Trades=7

**Parameter Tweaks:**
- Win rate 28.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup | GBPUSD | M5
WR=28.0%  Sharpe=-4.24  MaxDD=2.0%  Trades=93

**Parameter Tweaks:**
- Win rate 28.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.24 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_pullback | GBPUSD | M5
WR=27.4%  Sharpe=-7.76  MaxDD=13.0%  Trades=372

**Parameter Tweaks:**
- Win rate 27.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.76 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal | USOIL | M5
WR=27.4%  Sharpe=-3.66  MaxDD=5.3%  Trades=95

**Parameter Tweaks:**
- Win rate 27.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.51 — marginal edge, consider disabling on USOIL unless confirmed by live data

### gold_momentum_breakout | USOIL | M5
WR=26.9%  Sharpe=-5.46  MaxDD=23.4%  Trades=353

**Parameter Tweaks:**
- Win rate 26.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 23.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -5.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.37 — marginal edge, consider disabling on USOIL unless confirmed by live data

### turtle_soup | AUDUSD | M5
WR=26.9%  Sharpe=-6.06  MaxDD=2.0%  Trades=93

**Parameter Tweaks:**
- Win rate 26.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.06 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.38 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### range_breakout | EURUSD | M5
WR=26.7%  Sharpe=-6.27  MaxDD=2.9%  Trades=172

**Parameter Tweaks:**
- Win rate 26.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.27 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.39 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | GBPJPY | M5
WR=26.5%  Sharpe=-6.75  MaxDD=4.8%  Trades=170

**Parameter Tweaks:**
- Win rate 26.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.75 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_bounce | AUDUSD | M15
WR=26.3%  Sharpe=-12.97  MaxDD=1.7%  Trades=38

**Parameter Tweaks:**
- Win rate 26.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -12.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.15 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### gold_momentum_breakout | NVDA | M5
WR=25.8%  Sharpe=-7.20  MaxDD=9.5%  Trades=596

**Parameter Tweaks:**
- Win rate 25.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.20 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on NVDA unless confirmed by live data

### turtle_soup | EURUSD | M5
WR=25.5%  Sharpe=-7.22  MaxDD=2.6%  Trades=106

**Parameter Tweaks:**
- Win rate 25.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.29 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment | EURUSD | M5
WR=25.2%  Sharpe=-6.67  MaxDD=82.4%  Trades=2863

**Parameter Tweaks:**
- Win rate 25.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 82.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -6.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.34 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout | GBPUSD | M5
WR=25.1%  Sharpe=-7.66  MaxDD=6.8%  Trades=211

**Parameter Tweaks:**
- Win rate 25.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend | US500 | M30
WR=25.0%  Sharpe=-7.11  MaxDD=0.1%  Trades=8

**Parameter Tweaks:**
- Win rate 25.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on US500 unless confirmed by live data

### dual_ema_momentum | EURUSD | D1
WR=25.0%  Sharpe=-2.84  MaxDD=2.8%  Trades=4

**Parameter Tweaks:**
- Win rate 25.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum | GBPUSD | M5
WR=24.5%  Sharpe=-7.93  MaxDD=3.2%  Trades=98

**Parameter Tweaks:**
- Win rate 24.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.93 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | GBPJPY | M5
WR=24.3%  Sharpe=-7.35  MaxDD=11.4%  Trades=415

**Parameter Tweaks:**
- Win rate 24.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.35 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_bounce | EURUSD | M5
WR=24.2%  Sharpe=-8.90  MaxDD=0.9%  Trades=33

**Parameter Tweaks:**
- Win rate 24.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.90 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.28 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | M15
WR=24.2%  Sharpe=-7.00  MaxDD=10.3%  Trades=376

**Parameter Tweaks:**
- Win rate 24.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.00 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.34 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### macd_trend | AUDUSD | M5
WR=23.3%  Sharpe=-9.88  MaxDD=1.0%  Trades=43

**Parameter Tweaks:**
- Win rate 23.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -9.88 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.22 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### turtle_soup | ETHUSD | M5
WR=22.6%  Sharpe=-10.26  MaxDD=3.4%  Trades=358

**Parameter Tweaks:**
- Win rate 22.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -10.26 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.20 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### rvgi_cci_confluence | EURUSD | M5
WR=22.5%  Sharpe=-7.58  MaxDD=9.6%  Trades=445

**Parameter Tweaks:**
- Win rate 22.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.58 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.31 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### range_breakout | USOIL | M5
WR=22.4%  Sharpe=-6.95  MaxDD=17.4%  Trades=272

**Parameter Tweaks:**
- Win rate 22.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.31 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_bounce | USOIL | H4
WR=22.2%  Sharpe=-4.36  MaxDD=4.3%  Trades=9

**Parameter Tweaks:**
- Win rate 22.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.36 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rvgi_cci_confluence | USDCAD | M5
WR=21.2%  Sharpe=-7.32  MaxDD=4.4%  Trades=245

**Parameter Tweaks:**
- Win rate 21.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.34 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### dual_ema_fractal | USDCAD | M5
WR=20.0%  Sharpe=-11.50  MaxDD=0.5%  Trades=20

**Parameter Tweaks:**
- Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -11.50 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.14 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_bounce | XAUUSD | H2
WR=20.0%  Sharpe=-14.53  MaxDD=3.0%  Trades=5

**Parameter Tweaks:**
- Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -14.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.09 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover | EURUSD | M5
WR=20.0%  Sharpe=-12.04  MaxDD=0.8%  Trades=20

**Parameter Tweaks:**
- Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.17 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp | EURUSD | M30
WR=20.0%  Sharpe=-17.73  MaxDD=1.3%  Trades=15

**Parameter Tweaks:**
- Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -17.73 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.09 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal | AUDUSD | M5
WR=17.1%  Sharpe=-8.42  MaxDD=1.1%  Trades=41

**Parameter Tweaks:**
- Win rate 17.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.42 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.28 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rvgi_cci_confluence | AUDUSD | M5
WR=17.1%  Sharpe=-11.70  MaxDD=7.4%  Trades=328

**Parameter Tweaks:**
- Win rate 17.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -11.70 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.19 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### session_momentum | EURUSD | H12
WR=16.7%  Sharpe=-21.46  MaxDD=1.8%  Trades=6

**Parameter Tweaks:**
- Win rate 16.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -21.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.05 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap | GBPUSD | H12
WR=16.7%  Sharpe=-20.13  MaxDD=2.8%  Trades=6

**Parameter Tweaks:**
- Win rate 16.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -20.13 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.08 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence | GBPUSD | M5
WR=15.6%  Sharpe=-12.19  MaxDD=13.2%  Trades=365

**Parameter Tweaks:**
- Win rate 15.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -12.19 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.16 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce | USDCAD | M5
WR=15.4%  Sharpe=-11.96  MaxDD=0.8%  Trades=26

**Parameter Tweaks:**
- Win rate 15.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 26 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -11.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.16 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_bounce | AUDUSD | M5
WR=14.3%  Sharpe=-12.39  MaxDD=0.7%  Trades=28

**Parameter Tweaks:**
- Win rate 14.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 28 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.15 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal | GBPUSD | H12
WR=0.0%  Sharpe=-50.00  MaxDD=1.0%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | GBPJPY | H2
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_fractal | USDCAD | D1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | XAUUSD | D1
WR=0.0%  Sharpe=-50.00  MaxDD=1.4%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_bounce | USDCAD | H4
WR=0.0%  Sharpe=-50.00  MaxDD=0.5%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout | US500 | D1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | BTCUSD | D1
WR=0.0%  Sharpe=-15.50  MaxDD=6.5%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -15.50 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | XAUUSD | M5
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | XAUUSD | H1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | USTEC | H1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | AMD | M30
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend | MSFT | M15
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | XAUUSD | D1
WR=0.0%  Sharpe=-50.00  MaxDD=3.7%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | AUDUSD | H12
WR=0.0%  Sharpe=-50.00  MaxDD=0.8%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | USDCAD | H2
WR=0.0%  Sharpe=-50.00  MaxDD=0.3%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### turtle_soup | ETHUSD | D1
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | XAUUSD | H12
WR=0.0%  Sharpe=-50.00  MaxDD=2.9%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | EURUSD | H12
WR=0.0%  Sharpe=-50.00  MaxDD=0.8%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### dual_ema_momentum | GBPUSD | H12
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | GBPUSD | M5
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | BTCUSD | M5
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### vwap_momentum | BTCUSD | M15
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### rvgi_cci_confluence | AUDUSD | H2
WR=0.0%  Sharpe=-50.00  MaxDD=0.3%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | USDJPY | H4
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp | GBPJPY | M15
WR=0.0%  Sharpe=-47.38  MaxDD=0.3%  Trades=2

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -47.38 < 2.0 → reduce lot size on this pair or pause strategy

### rsi_extremes_scalp | GBPUSD | M30
WR=0.0%  Sharpe=0.00  MaxDD=0.0%  Trades=1

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

---

## ❌ Errors / Skipped

- dual_ema_fractal | GBPJPY | H12 → NO_TRADES: zero_signals
- dual_ema_fractal | AUDUSD | H2 → NO_TRADES: zero_signals
- dual_ema_fractal | AUDUSD | H12 → NO_TRADES: zero_signals
- dual_ema_fractal | AUDUSD | D1 → NO_TRADES: zero_signals
- dual_ema_fractal | USOIL | H2 → NO_TRADES: zero_signals
- rsi_bounce | GBPJPY | H12 → NO_TRADES: zero_signals
- rsi_bounce | AUDUSD | H2 → NO_TRADES: zero_signals
- rsi_bounce | AUDUSD | H12 → NO_TRADES: zero_signals
- rsi_bounce | USDCAD | H2 → NO_TRADES: zero_signals
- rsi_bounce | USDCAD | H12 → NO_TRADES: zero_signals
- rsi_bounce | USOIL | H2 → NO_TRADES: zero_signals
- rsi_bounce | USOIL | H12 → NO_TRADES: zero_signals
- rsi_bounce | USOIL | D1 → NO_TRADES: zero_signals
- ma_crossover | EURUSD | H12 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | H2 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | H12 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | D1 → NO_TRADES: zero_signals
- ma_crossover | GBPJPY | H2 → NO_TRADES: zero_signals
- macd_trend | GBPJPY | H12 → NO_TRADES: zero_signals
- macd_trend | AUDUSD | H12 → NO_TRADES: zero_signals
- macd_trend | USOIL | H2 → NO_TRADES: zero_signals
- macd_trend | USOIL | H12 → NO_TRADES: zero_signals
- macd_trend | US500 | H12 → NO_TRADES: zero_signals
- macd_trend | USTEC | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | XAUUSD | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | USOIL | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | USOIL | D1 → NO_TRADES: zero_signals
- gold_momentum_breakout | US500 | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | USTEC | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | NVDA | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | NVDA | D1 → NO_TRADES: zero_signals
- gold_momentum_breakout | AMD | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | AMD | D1 → NO_TRADES: zero_signals
- gold_momentum_breakout | MSFT | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | MSFT | D1 → NO_TRADES: zero_signals
- gold_momentum_breakout | AAPL | H12 → NO_TRADES: zero_signals
- gold_momentum_breakout | AAPL | D1 → NO_TRADES: zero_signals
- range_breakout | US500 | H12 → NO_TRADES: zero_signals
- range_breakout | USTEC | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | ETHUSD | H1 → NO_TRADES: zero_signals
- ema_ribbon_trend | ETHUSD | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | ETHUSD | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | ETHUSD | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | XAUUSD | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | XAUUSD | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | XAUUSD | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | XAUUSD | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | H1 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | US500 | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | USTEC | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | USTEC | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | USTEC | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | USTEC | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | M30 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | H1 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | NVDA | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | AMD | H1 → NO_TRADES: zero_signals
- ema_ribbon_trend | AMD | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | AMD | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | AMD | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | MSFT | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | MSFT | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | MSFT | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | MSFT | D1 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | M30 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | H1 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | H2 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | H4 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | H12 → NO_TRADES: zero_signals
- ema_ribbon_trend | AAPL | D1 → NO_TRADES: zero_signals
- cot_sentiment | XAUUSD | W1 → SKIP: insufficient_data
- cot_sentiment | EURUSD | W1 → SKIP: insufficient_data
- session_momentum | EURUSD | D1 → NO_TRADES: zero_signals
- session_momentum | GBPUSD | D1 → NO_TRADES: zero_signals
- session_momentum | XAUUSD | D1 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | M5 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | M15 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | M30 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | H1 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | H2 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | H4 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | H12 → NO_TRADES: zero_signals
- session_momentum | GBPJPY | D1 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | M5 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | M15 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | M30 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | H1 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | H2 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | H4 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | H12 → NO_TRADES: zero_signals
- session_momentum | AUDUSD | D1 → NO_TRADES: zero_signals
- session_momentum | USOIL | M5 → NO_TRADES: zero_signals
- session_momentum | USOIL | M15 → NO_TRADES: zero_signals
- session_momentum | USOIL | M30 → NO_TRADES: zero_signals
- session_momentum | USOIL | H1 → NO_TRADES: zero_signals
- session_momentum | USOIL | H2 → NO_TRADES: zero_signals
- session_momentum | USOIL | H4 → NO_TRADES: zero_signals
- session_momentum | USOIL | H12 → NO_TRADES: zero_signals
- session_momentum | USOIL | D1 → NO_TRADES: zero_signals
- session_momentum | US500 | M5 → NO_TRADES: zero_signals
- session_momentum | US500 | M15 → NO_TRADES: zero_signals
- session_momentum | US500 | M30 → NO_TRADES: zero_signals
- session_momentum | US500 | H1 → NO_TRADES: zero_signals
- session_momentum | US500 | H2 → NO_TRADES: zero_signals
- session_momentum | US500 | H4 → NO_TRADES: zero_signals
- session_momentum | US500 | H12 → NO_TRADES: zero_signals
- session_momentum | US500 | D1 → NO_TRADES: zero_signals
- session_momentum | USTEC | M5 → NO_TRADES: zero_signals
- session_momentum | USTEC | M15 → NO_TRADES: zero_signals
- session_momentum | USTEC | M30 → NO_TRADES: zero_signals
- session_momentum | USTEC | H1 → NO_TRADES: zero_signals
- session_momentum | USTEC | H2 → NO_TRADES: zero_signals
- session_momentum | USTEC | H4 → NO_TRADES: zero_signals
- session_momentum | USTEC | H12 → NO_TRADES: zero_signals
- session_momentum | USTEC | D1 → NO_TRADES: zero_signals
- turtle_soup | GBPJPY | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | M5 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | M15 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | M30 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | H1 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | H2 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | GBPJPY | D1 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | M5 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | M15 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | M30 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | H1 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | H2 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | AUDUSD | D1 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | M5 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | M15 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | M30 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | H1 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | H2 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | USOIL | D1 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | M5 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | M15 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | M30 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | H1 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | H2 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | US500 | D1 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | M5 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | M15 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | M30 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | H1 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | H2 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | H4 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | H12 → NO_TRADES: zero_signals
- dual_ema_momentum | USTEC | D1 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | M15 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | M30 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | H1 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | H2 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | H4 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | H12 → NO_TRADES: zero_signals
- vwap_momentum | GBPUSD | D1 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | M5 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | M15 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | M30 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | H1 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | H2 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | H4 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | H12 → NO_TRADES: zero_signals
- vwap_momentum | EURUSD | D1 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | M5 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | M15 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | M30 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | H1 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | H2 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | H4 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | H12 → NO_TRADES: zero_signals
- vwap_momentum | XAUUSD | D1 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | M5 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | M15 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | M30 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | H1 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | H2 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | H4 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | H12 → NO_TRADES: zero_signals
- vwap_momentum | GBPJPY | D1 → NO_TRADES: zero_signals
- vwap_momentum | US500 | M5 → NO_TRADES: zero_signals
- vwap_momentum | US500 | M15 → NO_TRADES: zero_signals
- vwap_momentum | US500 | M30 → NO_TRADES: zero_signals
- vwap_momentum | US500 | H1 → NO_TRADES: zero_signals
- vwap_momentum | US500 | H2 → NO_TRADES: zero_signals
- vwap_momentum | US500 | H4 → NO_TRADES: zero_signals
- vwap_momentum | US500 | H12 → NO_TRADES: zero_signals
- vwap_momentum | US500 | D1 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | M5 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | M15 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | M30 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | H1 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | H2 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | H4 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | H12 → NO_TRADES: zero_signals
- vwap_momentum | USTEC | D1 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | M30 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | H1 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | H2 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | H4 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | H12 → NO_TRADES: zero_signals
- vwap_momentum | BTCUSD | D1 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | M5 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | M15 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | M30 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | H1 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | H2 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | H4 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | H12 → NO_TRADES: zero_signals
- vwap_momentum | ETHUSD | D1 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | M5 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | M15 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | M30 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | H1 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | H2 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | H4 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | H12 → NO_TRADES: zero_signals
- hikkake_trap | USOIL | D1 → NO_TRADES: zero_signals
- hikkake_trap | US500 | M5 → NO_TRADES: zero_signals
- hikkake_trap | US500 | M15 → NO_TRADES: zero_signals
- hikkake_trap | US500 | M30 → NO_TRADES: zero_signals
- hikkake_trap | US500 | H1 → NO_TRADES: zero_signals
- hikkake_trap | US500 | H2 → NO_TRADES: zero_signals
- hikkake_trap | US500 | H4 → NO_TRADES: zero_signals
- hikkake_trap | US500 | H12 → NO_TRADES: zero_signals
- hikkake_trap | US500 | D1 → NO_TRADES: zero_signals
- orb | XAUUSD | H2 → NO_TRADES: zero_signals
- orb | XAUUSD | H4 → NO_TRADES: zero_signals
- orb | XAUUSD | H12 → NO_TRADES: zero_signals
- orb | XAUUSD | D1 → NO_TRADES: zero_signals
- orb | GBPJPY | H2 → NO_TRADES: zero_signals
- orb | GBPJPY | H4 → NO_TRADES: zero_signals
- orb | GBPJPY | H12 → NO_TRADES: zero_signals
- orb | GBPJPY | D1 → NO_TRADES: zero_signals
- orb | AUDUSD | H2 → NO_TRADES: zero_signals
- orb | AUDUSD | H4 → NO_TRADES: zero_signals
- orb | AUDUSD | H12 → NO_TRADES: zero_signals
- orb | AUDUSD | D1 → NO_TRADES: zero_signals
- rvgi_cci_confluence | GBPJPY | H12 → NO_TRADES: zero_signals
- bb_squeeze_scalp | XAUUSD | D1 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USDJPY | H12 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USDJPY | D1 → NO_TRADES: zero_signals
- bb_squeeze_scalp | GBPJPY | H2 → NO_TRADES: zero_signals
- bb_squeeze_scalp | GBPJPY | H4 → NO_TRADES: zero_signals
- bb_squeeze_scalp | GBPJPY | H12 → NO_TRADES: zero_signals
- bb_squeeze_scalp | GBPJPY | D1 → NO_TRADES: zero_signals
- bb_squeeze_scalp | US500 | M30 → NO_TRADES: zero_signals
- bb_squeeze_scalp | US500 | H2 → NO_TRADES: zero_signals
- bb_squeeze_scalp | US500 | H12 → NO_TRADES: zero_signals
- bb_squeeze_scalp | US500 | D1 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USTEC | M5 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USTEC | M30 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USTEC | H12 → NO_TRADES: zero_signals
- bb_squeeze_scalp | USTEC | D1 → NO_TRADES: zero_signals
- rsi_extremes_scalp | EURUSD | H12 → NO_TRADES: zero_signals
- rsi_extremes_scalp | EURUSD | D1 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | M5 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | M15 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | H2 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | H4 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | H12 → NO_TRADES: zero_signals
- rsi_extremes_scalp | GBPUSD | D1 → NO_TRADES: zero_signals
- rsi_extremes_scalp | USOIL | M5 → NO_TRADES: zero_signals
- rsi_extremes_scalp | USOIL | H2 → NO_TRADES: zero_signals
- rsi_extremes_scalp | USOIL | H4 → NO_TRADES: zero_signals
- rsi_extremes_scalp | USOIL | H12 → NO_TRADES: zero_signals
- rsi_extremes_scalp | USOIL | D1 → NO_TRADES: zero_signals