# TradePanel Recommendations — 20260501

Generated: 2026-05-01 02:01 UTC  
Report: `results/overnight/20260501_backtest_report.json`

---

## Summary

| Metric | Value |
|--------|-------|
| Total results | 60 |
| ✅ PASS | 17 (28%) |
| 🔄 REVIEW | 30 (50%) |
| ⏭ SKIP | 0 |

## 🎉 New PASSes Since Last Run

- **ma_crossover** AUDUSD H1 — Sharpe 48.07, WR 100%

## 🎯 Near-PASS Candidates (prioritise these)

| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker |
|----------|------|----|--------|-----|-----|---------|
| gold_momentum_breakout | GBPUSD | H4 | 0.719 | 55.2 | 0.0 | Sharpe 0.72 (+0.28 needed), WR 55.2% (+4.8pp needed) |
| ma_crossover | USDJPY | D1 | 0.604 | 50.0 | 0.0 | Sharpe 0.60 (+0.40 needed), WR 50.0% (+10.0pp needed) |

## 🔧 Priority Tuning Hints (P1 + P2)

_P1 = immediate action required / P2 = high value next test_

### bb_squeeze_scalp — NVDA M15
**Action:** 🚫 Sharpe -3.90 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Only 12 trades — widen entry conditions
  - Sharpe -3.90 < 0.8 → reduce lot size
  - Profit factor 0.57 — marginal edge

### rsi_extremes_scalp — XAUUSD M15
**Action:** 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.9% < 48.0% → tighten entry filter
  - Sharpe -4.20 < 0.8 → reduce lot size
  - Profit factor 0.51 — marginal edge

### rsi_pullback — GBPJPY H4
**Action:** 🚫 Sharpe -4.96 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Only 16 trades — widen entry conditions
  - Sharpe -4.96 < 0.8 → reduce lot size
  - Profit factor 0.48 — marginal edge

### bb_squeeze_scalp — AAPL M15
**Action:** 🚫 Sharpe -10.21 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 21.4% < 48.0% → tighten entry filter
  - Only 14 trades — widen entry conditions
  - Sharpe -10.21 < 0.8 → reduce lot size
  - Profit factor 0.26 — marginal edge

### ma_crossover — GBPJPY H1
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Only 5 trades — widen entry conditions
  - Sharpe 0.46 < 0.8 → reduce lot size
  - Profit factor 1.07 — marginal edge

### gold_momentum_breakout — AAPL H1
**Action:** 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 44.4% < 48.0% → tighten entry filter
  - Only 9 trades — widen entry conditions
  - Sharpe 0.38 < 0.8 → reduce lot size
  - Profit factor 1.06 — marginal edge

### ma_crossover — GBPJPY H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### ma_crossover — USDCAD H1
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### ma_crossover — USDCAD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### gold_momentum_breakout — XAUUSD D1
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### gold_momentum_breakout — US500 H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### gold_momentum_breakout — MSFT H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### rsi_bounce — XAUUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult
  - Only 1 trades — widen entry conditions
  - Sharpe 0.00 < 0.8 → reduce lot size

### rsi_bounce — XAUUSD H1
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Only 6 trades — widen entry conditions
  - Sharpe -0.27 < 0.8 → reduce lot size
  - Profit factor 0.96 — marginal edge

### gold_momentum_breakout — NVDA H1
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 40.0% < 48.0% → tighten entry filter
  - Only 5 trades — widen entry conditions
  - Sharpe -4.10 < 0.8 → reduce lot size
  - Profit factor 0.54 — marginal edge

### bb_squeeze_scalp — GBPJPY M15
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Only 7 trades — widen entry conditions
  - Sharpe -4.25 < 0.8 → reduce lot size
  - Profit factor 0.52 — marginal edge

### gold_momentum_breakout — AMD H1
**Action:** 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Only 2 trades — widen entry conditions
  - Sharpe -5.19 < 0.8 → reduce lot size
  - Profit factor 0.37 — marginal edge

### bb_squeeze_scalp — AUDUSD M15
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 48.0% → tighten entry filter
  - Only 8 trades — widen entry conditions
  - Sharpe -9.47 < 0.8 → reduce lot size
  - Profit factor 0.28 — marginal edge

### ma_crossover — EURUSD H4
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 48.0% → tighten entry filter
  - Only 3 trades — widen entry conditions
  - Sharpe -10.52 < 0.8 → reduce lot size
  - Profit factor 0.20 — marginal edge

### bb_squeeze_scalp — USTEC M15
**Action:** 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 48.0% → tighten entry filter
  - Only 4 trades — widen entry conditions
  - Sharpe -12.38 < 0.8 → reduce lot size
  - Profit factor 0.13 — marginal edge

### bb_squeeze_scalp — US500 M15
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 3 trades — widen entry conditions
  - Sharpe -36.12 < 0.8 → reduce lot size

### rsi_bounce — GBPUSD H1
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 5 trades — widen entry conditions
  - Sharpe -50.00 < 0.8 → reduce lot size

### rsi_bounce — USDJPY H1
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter
  - Only 3 trades — widen entry conditions
  - Sharpe -50.00 < 0.8 → reduce lot size

---

## Appendix — Full REVIEW Strategy Tuning List

| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |
|----------|----------|------|----|--------|-----|--------|
| P1 | bb_squeeze_scalp | NVDA | M15 | -3.905 | 50.0 | 🚫 Sharpe -3.90 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | XAUUSD | M15 | -4.203 | 46.9 | 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_pullback | GBPJPY | H4 | -4.958 | 50.0 | 🚫 Sharpe -4.96 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | AAPL | M15 | -10.213 | 21.4 | 🚫 Sharpe -10.21 — strategy is actively losing money. Do not tune parameters yet.… |
| P2 | ma_crossover | GBPJPY | H1 | 0.456 | 60.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | AAPL | H1 | 0.378 | 44.4 | 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | GBPJPY | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | USDCAD | H1 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | USDCAD | H4 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | XAUUSD | D1 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | US500 | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | MSFT | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | XAUUSD | H4 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | XAUUSD | H1 | -0.272 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | NVDA | H1 | -4.097 | 40.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | GBPJPY | M15 | -4.252 | 57.1 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | AMD | H1 | -5.19 | 50.0 | 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | AUDUSD | M15 | -9.475 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | EURUSD | H4 | -10.518 | 33.3 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | USTEC | M15 | -12.381 | 25.0 | 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | US500 | M15 | -36.123 | 0.0 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | GBPUSD | H1 | -50.0 | 0.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | USDJPY | H1 | -50.0 | 0.0 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P4 | gold_momentum_breakout | GBPUSD | H4 | 0.719 | 55.2 | 📋 WR 55%, Sharpe 0.72. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | ma_crossover | USDJPY | D1 | 0.604 | 50.0 | 📋 WR 50%, Sharpe 0.60. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rsi_pullback | XAUUSD | D1 | 0.568 | 51.8 | 📋 WR 52%, Sharpe 0.57. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | bb_squeeze_scalp | XAUUSD | M15 | -0.028 | 47.7 | 📋 WR 48%, Sharpe -0.03. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | gold_momentum_breakout | USTEC | H1 | -0.144 | 44.4 | 📋 WR 44%, Sharpe -0.14. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ma_crossover | USDJPY | H1 | -0.262 | 47.4 | 📋 WR 47%, Sharpe -0.26. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ma_crossover | EURUSD | H1 | -0.445 | 55.6 | 📋 WR 56%, Sharpe -0.45. Investigate avg_trade_duration — if trades close in < 1h… |
