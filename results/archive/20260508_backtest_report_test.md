# Overnight Backtest Report — 08 May 2026

Generated: 2026-05-08 15:27 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 3 |
| ⚠️ REVIEW | 16 |
| ❌ ERROR/SKIP | 5 |
| **Total combos** | **24** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| ma_crossover | AUDUSD | H4 | T1 | 100.0 | 14.88 | 0.0 | 2 | 999.00 |
| ma_crossover | GBPJPY | D1 | T1 | 100.0 | 18.07 | 0.0 | 2 | 999.00 |
| ma_crossover | GBPJPY | H4 | T1 | 75.0 | 6.91 | 0.8 | 8 | 4.12 |

---

## ⚠️ Strategies Needing Review


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

### ma_crossover | AUDUSD | H1
WR=60.0%  Sharpe=3.11  MaxDD=0.1%  Trades=5

**Parameter Tweaks:**
- Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### ma_crossover | GBPJPY | H1
WR=59.3%  Sharpe=1.70  MaxDD=1.3%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe 1.70 < 2.0 → reduce lot size on this pair or pause strategy

### ma_crossover | EURUSD | H1
WR=53.3%  Sharpe=0.64  MaxDD=0.8%  Trades=30

**Parameter Tweaks:**
- Win rate 53.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.64 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | GBPJPY | M30
WR=52.4%  Sharpe=0.39  MaxDD=1.6%  Trades=42

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.39 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

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

### ma_crossover | AUDUSD | M30
WR=47.6%  Sharpe=-6.78  MaxDD=0.9%  Trades=21

**Parameter Tweaks:**
- Win rate 47.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.78 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.35 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### ma_crossover | EURUSD | M30
WR=45.0%  Sharpe=-1.89  MaxDD=1.0%  Trades=40

**Parameter Tweaks:**
- Win rate 45.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | GBPJPY | M5
WR=37.9%  Sharpe=-2.89  MaxDD=0.6%  Trades=29

**Parameter Tweaks:**
- Win rate 37.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -2.89 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### ma_crossover | AUDUSD | M5
WR=35.7%  Sharpe=-4.72  MaxDD=0.3%  Trades=14

**Parameter Tweaks:**
- Win rate 35.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -4.72 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### ma_crossover | EURUSD | M15
WR=34.4%  Sharpe=-5.30  MaxDD=2.1%  Trades=61

**Parameter Tweaks:**
- Win rate 34.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.30 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover | AUDUSD | M15
WR=32.4%  Sharpe=-1.97  MaxDD=0.9%  Trades=34

**Parameter Tweaks:**
- Win rate 32.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.73 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### ma_crossover | EURUSD | M5
WR=20.0%  Sharpe=-12.04  MaxDD=0.8%  Trades=20

**Parameter Tweaks:**
- Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -12.04 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.17 — marginal edge, consider disabling on EURUSD unless confirmed by live data

---

## ❌ Errors / Skipped

- ma_crossover | EURUSD | H12 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | H2 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | H12 → NO_TRADES: zero_signals
- ma_crossover | AUDUSD | D1 → NO_TRADES: zero_signals
- ma_crossover | GBPJPY | H2 → NO_TRADES: zero_signals