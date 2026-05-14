# Overnight Backtest Report — 11 May 2026

Generated: 2026-05-11 18:42 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 1 |
| ⚠️ REVIEW | 7 |
| ❌ ERROR/SKIP | 0 |
| **Total combos** | **8** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| hikkake_trap | USOIL | H4 | T2 | 73.8 | 3.83 | 2.1 | 42 | 1.89 |

---

## ⚠️ Strategies Needing Review


### hikkake_trap | GBPUSD | D1
WR=63.6%  Sharpe=3.16  MaxDD=1.4%  Trades=11

**Parameter Tweaks:**
- Win rate 63.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.6% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 11 trades — widen oversold/overbought thresholds or relax ADX filter

### hikkake_trap | US500 | H4
WR=63.3%  Sharpe=4.93  MaxDD=0.1%  Trades=30

**Parameter Tweaks:**
- Win rate 63.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Win rate 63.3% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit

### hikkake_trap | US500 | D1
WR=59.4%  Sharpe=5.11  MaxDD=0.1%  Trades=32

**Parameter Tweaks:**
- Win rate 59.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### hikkake_trap | USOIL | D1
WR=59.3%  Sharpe=3.65  MaxDD=8.0%  Trades=27

**Parameter Tweaks:**
- Win rate 59.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 27 trades — widen oversold/overbought thresholds or relax ADX filter

### hikkake_trap | GBPUSD | H4
WR=58.8%  Sharpe=3.15  MaxDD=0.6%  Trades=17

**Parameter Tweaks:**
- Win rate 58.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 17 trades — widen oversold/overbought thresholds or relax ADX filter

### hikkake_trap | XAUUSD | H4
WR=51.4%  Sharpe=0.69  MaxDD=8.9%  Trades=37

**Parameter Tweaks:**
- Win rate 51.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe 0.69 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.10 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap | XAUUSD | D1
WR=50.0%  Sharpe=-1.60  MaxDD=16.4%  Trades=20

**Parameter Tweaks:**
- Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -1.60 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

---

## ❌ Errors / Skipped
