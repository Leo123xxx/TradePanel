# TradePanel Recommendations — 20260428

Generated: 2026-04-29 08:58 UTC  
Report: `results/overnight/20260428_backtest_report.json`

---

## Summary

| Metric | Value |
|--------|-------|
| Total results | 126 |
| ✅ PASS | 6 (5%) |
| 🔄 REVIEW | 118 (94%) |
| ⏭ SKIP | 2 |

## 🗑️ Removal / Escalation Queue

- 🟡 WATCH **orb** EURUSD M5 — 1 consecutive fails, deadline in 33d (Sharpe -6.44)
- 🟡 WATCH **orb** EURUSD M15 — 1 consecutive fails, deadline in 33d (Sharpe -4.20)

## 🎯 Near-PASS Candidates (prioritise these)

| Strategy | Pair | TF | Sharpe | WR% | DD% | Gap to PASS |
|----------|------|----|--------|-----|-----|-------------|
| rsi_bounce | EURUSD | H4 | 5.653 | 42.9 | 0.9 | -4.653 |
| ema_ribbon_trend | BTCUSD | D1 | 3.709 | 59.3 | 5.3 | -2.709 |
| dual_ema_fractal | XAUUSD | D1 | 3.541 | 58.5 | 13.6 | -2.541 |
| range_breakout | XAUUSD | H4 | 3.085 | 56.5 | 21.9 | -2.085 |
| range_breakout | XAUUSD | D1 | 2.429 | 56.0 | 39.6 | -1.429 |

## 🔧 Priority Tuning Hints (P1 + P2)

_P1 = immediate action required / P2 = high value next test_

### gold_momentum_breakout — GBPUSD H1
**Action:** 🚫 Sharpe -2.01 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 27.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.01 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_mean_reversion — EURUSD H1
**Action:** 🚫 Sharpe -2.02 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.02 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — GBPUSD H1
**Action:** 🚫 Sharpe -2.08 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 22.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.08 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — GBPUSD H1
**Action:** 🚫 Sharpe -2.10 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 51.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.10 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD H4
**Action:** 🚫 Sharpe -2.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.13 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion — EURUSD M30
**Action:** 🚫 Sharpe -2.15 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 20.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.15 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend — EURUSD M30
**Action:** 🚫 Sharpe -2.16 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.16 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — GBPUSD H1
**Action:** 🚫 Sharpe -2.17 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 30.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.17 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend — EURUSD H1
**Action:** 🚫 Sharpe -2.22 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.22 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion — XAUUSD M30
**Action:** 🚫 Sharpe -2.26 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 110.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.26 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum — GBPUSD H1
**Action:** 🚫 Sharpe -2.28 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.28 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout — EURUSD H1
**Action:** 🚫 Sharpe -2.28 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 30.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.28 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — EURUSD M15
**Action:** 🚫 Sharpe -2.31 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.31 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H1
**Action:** 🚫 Sharpe -2.31 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.31 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum — EURUSD H1
**Action:** 🚫 Sharpe -2.35 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.35 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout — XAUUSD M30
**Action:** 🚫 Sharpe -2.52 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 154.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.52 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.65 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup — GBPUSD M30
**Action:** 🚫 Sharpe -2.57 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 26.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.57 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_mean_reversion — XAUUSD H4
**Action:** 🚫 Sharpe -2.66 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (53%) >> SHORT (40%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 46.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 39.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.66 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal — EURUSD H1
**Action:** 🚫 Sharpe -2.68 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.68 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD M30
**Action:** 🚫 Sharpe -2.78 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.78 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — GBPUSD M15
**Action:** 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 32.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.08 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.66 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### moving_average_crossover — GBPUSD M30
**Action:** 🚫 Sharpe -3.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.13 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — EURUSD M30
**Action:** 🚫 Sharpe -3.23 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.23 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — EURUSD M30
**Action:** 🚫 Sharpe -3.23 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 24.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.23 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — EURUSD H1
**Action:** 🚫 Sharpe -3.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 28.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.33 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD H1
**Action:** 🚫 Sharpe -3.34 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 55.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.34 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### gold_momentum_breakout — GBPUSD M30
**Action:** 🚫 Sharpe -3.39 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 37.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.39 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend — EURUSD M15
**Action:** 🚫 Sharpe -3.40 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.40 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.60 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD H1
**Action:** 🚫 Sharpe -3.47 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.47 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD M30
**Action:** 🚫 Sharpe -3.84 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 31.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.84 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### moving_average_crossover — EURUSD M30
**Action:** 🚫 Sharpe -3.93 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.93 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend — ETHUSD H1
**Action:** 🚫 Sharpe -4.01 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.01 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.53 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD M30
**Action:** 🚫 Sharpe -4.01 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 37.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 66.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -4.01 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.52 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### cot_sentiment — USDJPY D1
**Action:** 🚫 Sharpe -4.04 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 34.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 45.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -4.04 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.55 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rvgi_cci_confluence — EURUSD M15
**Action:** 🚫 Sharpe -4.09 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.09 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.55 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover — EURUSD M15
**Action:** 🚫 Sharpe -4.17 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.17 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.52 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — GBPUSD M5
**Action:** 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.20 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### orb — EURUSD M15
**Action:** 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.20 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — EURUSD M30
**Action:** 🚫 Sharpe -4.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 30.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.32 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — GBPUSD M30
**Action:** 🚫 Sharpe -4.38 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 28.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.38 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — EURUSD M15
**Action:** 🚫 Sharpe -4.43 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.43 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — EURUSD M15
**Action:** 🚫 Sharpe -4.43 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 21.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -4.43 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — GBPUSD M15
**Action:** 🚫 Sharpe -5.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 22.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -5.13 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_bounce — EURUSD M15
**Action:** 🚫 Sharpe -5.34 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 27.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.34 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.48 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — EURUSD M5
**Action:** 🚫 Sharpe -5.52 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 31.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.52 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.48 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### moving_average_crossover — GBPUSD H1
**Action:** 🚫 Sharpe -5.68 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 40.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.68 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.47 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### orb — EURUSD M5
**Action:** 🚫 Sharpe -6.44 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -6.44 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.41 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment — XAGUSD D1
**Action:** 🚫 Sharpe -7.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 26.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 241.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -7.32 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.34 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD D1
**Action:** 🎯 Near-PASS (Sharpe 3.71, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Direction:** Directional bias: LONG (69%) >> SHORT (50%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 59.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_fractal — XAUUSD D1
**Action:** 🎯 Near-PASS (Sharpe 3.54, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Backtest suggestions:**
  - Win rate 58.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### range_breakout — XAUUSD H4
**Action:** 💡 WR 56% but max DD 22%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 56.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 21.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### range_breakout — XAUUSD D1
**Action:** 💡 WR 56% but max DD 40%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 56.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 39.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop

### macd_trend — EURUSD D1
**Action:** 🎯 Near-PASS (Sharpe 1.96, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Direction:** Directional bias: SHORT (67%) >> LONG (54%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 59.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### gold_momentum_breakout — XAUUSD H4
**Action:** 🎯 Near-PASS (Sharpe 1.82, WR 54%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Backtest suggestions:**
  - Win rate 53.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_fractal — XAUUSD H4
**Action:** 🎯 Near-PASS (Sharpe 1.49, WR 55%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Direction:** Directional bias: LONG (59%) >> SHORT (45%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 54.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### turtle_soup — EURUSD D1
**Action:** 🎯 Near-PASS (Sharpe 1.26, WR 53%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Direction:** Directional bias: SHORT (62%) >> LONG (45%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 52.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### dual_ema_momentum — XAUUSD H4
**Action:** 🎯 Near-PASS (Sharpe 1.24, WR 53%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Backtest suggestions:**
  - Win rate 53.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### orb — XAGUSD M15
**Action:** 💡 WR 54% but max DD 24%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 54.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 24.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe 0.77 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 1.13 — marginal edge, consider disabling on XAGUSD unless confirmed by live data

### moving_average_crossover — EURUSD D1
**Action:** 🎯 Near-PASS (Sharpe 0.76, WR 58%). Try increasing TP: tp_atr_mult +0.5. WR is strong enough to absorb the extra room.
**Backtest suggestions:**
  - Win rate 58.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.76 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 1.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum — XAUUSD H1
**Action:** 💡 WR 51% but max DD 45%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 50.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 44.9% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -0.35 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.93 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal — XAUUSD H1
**Action:** 💡 WR 51% but max DD 47%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 50.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 46.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -0.79 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.87 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

---

## Appendix — Full REVIEW Strategy Tuning List

| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |
|----------|----------|------|----|--------|-----|--------|
| P1 | gold_momentum_breakout | GBPUSD | H1 | -2.007 | 49.2 | 🚫 Sharpe -2.01 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | EURUSD | H1 | -2.023 | 47.4 | 🚫 Sharpe -2.02 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPUSD | H1 | -2.081 | 50.1 | 🚫 Sharpe -2.08 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPUSD | H1 | -2.102 | 51.2 | 🚫 Sharpe -2.10 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | H4 | -2.133 | 42.3 | 🚫 Sharpe -2.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | EURUSD | M30 | -2.155 | 50.4 | 🚫 Sharpe -2.15 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | M30 | -2.164 | 50.9 | 🚫 Sharpe -2.16 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | GBPUSD | H1 | -2.168 | 30.8 | 🚫 Sharpe -2.17 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H1 | -2.216 | 46.3 | 🚫 Sharpe -2.22 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | XAUUSD | M30 | -2.26 | 48.0 | 🚫 Sharpe -2.26 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | GBPUSD | H1 | -2.283 | 48.8 | 🚫 Sharpe -2.28 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | EURUSD | H1 | -2.285 | 47.4 | 🚫 Sharpe -2.28 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | EURUSD | M15 | -2.306 | 35.1 | 🚫 Sharpe -2.31 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H1 | -2.306 | 47.3 | 🚫 Sharpe -2.31 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | EURUSD | H1 | -2.351 | 49.3 | 🚫 Sharpe -2.35 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | XAUUSD | M30 | -2.523 | 46.6 | 🚫 Sharpe -2.52 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPUSD | M30 | -2.565 | 49.6 | 🚫 Sharpe -2.57 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | XAUUSD | H4 | -2.657 | 46.5 | 🚫 Sharpe -2.66 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | H1 | -2.683 | 45.5 | 🚫 Sharpe -2.68 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | M30 | -2.783 | 46.9 | 🚫 Sharpe -2.78 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | GBPUSD | M15 | -3.079 | 32.8 | 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | moving_average_crossover | GBPUSD | M30 | -3.134 | 49.2 | 🚫 Sharpe -3.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | M30 | -3.225 | 47.0 | 🚫 Sharpe -3.23 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | M30 | -3.232 | 49.1 | 🚫 Sharpe -3.23 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | H1 | -3.328 | 45.5 | 🚫 Sharpe -3.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | H1 | -3.34 | 44.4 | 🚫 Sharpe -3.34 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | GBPUSD | M30 | -3.394 | 47.9 | 🚫 Sharpe -3.39 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | M15 | -3.395 | 48.5 | 🚫 Sharpe -3.40 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | H1 | -3.471 | 44.3 | 🚫 Sharpe -3.47 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | M30 | -3.841 | 46.7 | 🚫 Sharpe -3.84 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | moving_average_crossover | EURUSD | M30 | -3.926 | 46.9 | 🚫 Sharpe -3.93 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | ETHUSD | H1 | -4.012 | 42.6 | 🚫 Sharpe -4.01 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | M30 | -4.014 | 37.9 | 🚫 Sharpe -4.01 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | USDJPY | D1 | -4.037 | 34.5 | 🚫 Sharpe -4.04 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | M15 | -4.087 | 45.0 | 🚫 Sharpe -4.09 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | moving_average_crossover | EURUSD | M15 | -4.175 | 46.6 | 🚫 Sharpe -4.17 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | GBPUSD | M5 | -4.199 | 35.6 | 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | EURUSD | M15 | -4.201 | 42.8 | 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | EURUSD | M30 | -4.316 | 30.7 | 🚫 Sharpe -4.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | GBPUSD | M30 | -4.383 | 28.0 | 🚫 Sharpe -4.38 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | M15 | -4.429 | 45.4 | 🚫 Sharpe -4.43 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | M15 | -4.433 | 44.6 | 🚫 Sharpe -4.43 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPUSD | M15 | -5.135 | 42.7 | 🚫 Sharpe -5.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | EURUSD | M15 | -5.337 | 27.8 | 🚫 Sharpe -5.34 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | EURUSD | M5 | -5.523 | 31.5 | 🚫 Sharpe -5.52 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | moving_average_crossover | GBPUSD | H1 | -5.68 | 40.0 | 🚫 Sharpe -5.68 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | EURUSD | M5 | -6.442 | 42.9 | 🚫 Sharpe -6.44 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | XAGUSD | D1 | -7.319 | 26.2 | 🚫 Sharpe -7.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P2 | ema_ribbon_trend | BTCUSD | D1 | 3.709 | 59.3 | 🎯 Near-PASS (Sharpe 3.71, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | dual_ema_fractal | XAUUSD | D1 | 3.541 | 58.5 | 🎯 Near-PASS (Sharpe 3.54, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | range_breakout | XAUUSD | H4 | 3.085 | 56.5 | 💡 WR 56% but max DD 22%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P2 | range_breakout | XAUUSD | D1 | 2.429 | 56.0 | 💡 WR 56% but max DD 40%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P2 | macd_trend | EURUSD | D1 | 1.957 | 59.0 | 🎯 Near-PASS (Sharpe 1.96, WR 59%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | gold_momentum_breakout | XAUUSD | H4 | 1.816 | 53.9 | 🎯 Near-PASS (Sharpe 1.82, WR 54%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | dual_ema_fractal | XAUUSD | H4 | 1.492 | 54.9 | 🎯 Near-PASS (Sharpe 1.49, WR 55%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | turtle_soup | EURUSD | D1 | 1.258 | 52.8 | 🎯 Near-PASS (Sharpe 1.26, WR 53%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | dual_ema_momentum | XAUUSD | H4 | 1.238 | 53.0 | 🎯 Near-PASS (Sharpe 1.24, WR 53%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | orb | XAGUSD | M15 | 0.774 | 54.5 | 💡 WR 54% but max DD 24%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P2 | moving_average_crossover | EURUSD | D1 | 0.764 | 58.3 | 🎯 Near-PASS (Sharpe 0.76, WR 58%). Try increasing TP: tp_atr_mult +0.5. WR is st… |
| P2 | dual_ema_momentum | XAUUSD | H1 | -0.345 | 50.6 | 💡 WR 51% but max DD 45%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P2 | dual_ema_fractal | XAUUSD | H1 | -0.788 | 50.5 | 💡 WR 51% but max DD 47%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P3 | rsi_bounce | EURUSD | H4 | 5.653 | 42.9 | 🎯 Near-PASS (Sharpe 5.65, PF 2.38). Entry timing is the gap — add ADX > 20 gate … |
| P3 | rsi_bounce | XAUUSD | H1 | 1.745 | 39.4 | 🎯 Near-PASS (Sharpe 1.74, PF 1.51). Entry timing is the gap — add ADX > 20 gate … |
| P3 | session_momentum | XAUUSD | M30 | 1.569 | 41.6 | 🎯 Near-PASS (Sharpe 1.57, PF 1.31). Entry timing is the gap — add ADX > 20 gate … |
| P3 | hikkake_trap | XAUUSD | H4 | 1.361 | 36.0 | 🎯 Near-PASS (Sharpe 1.36, PF 1.35). Entry timing is the gap — add ADX > 20 gate … |
| P3 | session_momentum | XAUUSD | H1 | 1.205 | 40.3 | 🎯 Near-PASS (Sharpe 1.21, PF 1.24). Entry timing is the gap — add ADX > 20 gate … |
| P3 | session_momentum | GBPUSD | H1 | 0.982 | 39.4 | 🎯 Near-PASS (Sharpe 0.98, PF 1.15). Entry timing is the gap — add ADX > 20 gate … |
| P3 | vwap_momentum | XAUUSD | M30 | 0.743 | 37.6 | 🎯 Near-PASS (Sharpe 0.74, PF 1.16). Entry timing is the gap — add ADX > 20 gate … |
| P3 | hikkake_trap | XAUUSD | D1 | 0.692 | 25.6 | 🎯 Near-PASS (Sharpe 0.69, PF 1.15). Entry timing is the gap — add ADX > 20 gate … |
| P3 | rsi_bounce | XAUUSD | M30 | 0.645 | 39.2 | 🎯 Near-PASS (Sharpe 0.64, PF 1.16). Entry timing is the gap — add ADX > 20 gate … |
| P3 | stoch_divergence | USDJPY | H4 | 0.62 | 37.0 | 🎯 Near-PASS (Sharpe 0.62, PF 1.09). Entry timing is the gap — add ADX > 20 gate … |
| P3 | cot_sentiment | XAUUSD | D1 | 0.592 | 35.7 | 🔧 Low WR (36%) but PF 1.10 — system captures large wins rarely. Typical of trend… |
| P3 | vwap_momentum | XAUUSD | M15 | 0.572 | 38.4 | 🔧 Low WR (38%) but PF 1.12 — system captures large wins rarely. Typical of trend… |
| P3 | session_momentum | XAUUSD | M15 | 0.365 | 36.3 | 🔧 Low WR (36%) but PF 1.06 — system captures large wins rarely. Typical of trend… |
| P3 | vwap_momentum | GBPUSD | H1 | 0.217 | 36.0 | 🔧 Low WR (36%) but PF 1.03 — system captures large wins rarely. Typical of trend… |
| P3 | moving_average_crossover | USDJPY | D1 | 0.185 | 48.0 | 🔧 Marginal edge (WR 48%, PF 1.03). Check long_win_rate vs short_win_rate — if on… |
| P4 | orb | XAGUSD | M5 | 0.514 | 56.1 | 📋 WR 56%, Sharpe 0.51. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_fractal | EURUSD | H4 | 0.278 | 51.8 | 📋 WR 52%, Sharpe 0.28. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | macd_trend | USDJPY | H1 | -0.047 | 52.8 | 📋 WR 53%, Sharpe -0.05. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_fractal | EURUSD | D1 | -0.102 | 52.8 | 📋 WR 53%, Sharpe -0.10. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ema_ribbon_trend | BTCUSD | H4 | -0.209 | 58.2 | 📋 WR 58%, Sharpe -0.21. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | session_momentum | GBPUSD | M30 | -0.312 | 37.7 | ❌ WR 38%, PF 0.96 — no edge detected. Entry signal does not predict direction be… |
| P4 | dual_ema_fractal | GBPUSD | H4 | -0.47 | 52.9 | 📋 WR 53%, Sharpe -0.47. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | stoch_divergence | USDJPY | H1 | -0.577 | 33.1 | ❌ WR 33%, PF 0.91 — no edge detected. Entry signal does not predict direction be… |
| P4 | stoch_divergence | EURUSD | H4 | -0.634 | 34.5 | ❌ WR 34%, PF 0.92 — no edge detected. Entry signal does not predict direction be… |
| P4 | rsi_bounce | EURUSD | H1 | -0.648 | 37.2 | ❌ WR 37%, PF 0.92 — no edge detected. Entry signal does not predict direction be… |
| P4 | dual_ema_momentum | XAUUSD | M30 | -0.718 | 49.8 | 📋 WR 50%, Sharpe -0.72. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | stoch_divergence | EURUSD | M30 | -0.772 | 37.7 | ❌ WR 38%, PF 0.90 — no edge detected. Entry signal does not predict direction be… |
| P4 | dual_ema_momentum | XAUUSD | D1 | -0.859 | 41.2 | 📋 WR 41%, Sharpe -0.86. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ema_ribbon_trend | ETHUSD | H4 | -0.932 | 57.4 | 📋 WR 57%, Sharpe -0.93. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | hikkake_trap | XAUUSD | H1 | -0.984 | 35.1 | ❌ WR 35%, PF 0.84 — no edge detected. Entry signal does not predict direction be… |
| P4 | hikkake_trap | EURUSD | H1 | -1.026 | 35.8 | ❌ WR 36%, PF 0.87 — no edge detected. Entry signal does not predict direction be… |
| P4 | moving_average_crossover | EURUSD | H1 | -1.093 | 51.6 | 📋 WR 52%, Sharpe -1.09. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | range_breakout | EURUSD | H4 | -1.097 | 49.0 | 📋 WR 49%, Sharpe -1.10. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | gold_momentum_breakout | XAUUSD | H1 | -1.113 | 48.2 | 📋 WR 48%, Sharpe -1.11. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | stat_arb_gold_silver | XAUUSD | D1 | -1.133 | 38.5 | ❌ WR 39%, PF 0.80 — no edge detected. Entry signal does not predict direction be… |
| P4 | rvgi_cci_confluence | GBPUSD | H4 | -1.171 | 52.5 | 📋 WR 52%, Sharpe -1.17. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | hikkake_trap | XAUUSD | M30 | -1.172 | 34.0 | ❌ WR 34%, PF 0.81 — no edge detected. Entry signal does not predict direction be… |
| P4 | macd_trend | USDJPY | D1 | -1.217 | 47.5 | 📋 WR 48%, Sharpe -1.22. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | gold_momentum_breakout | XAUUSD | M15 | -1.293 | 48.7 | 📋 WR 49%, Sharpe -1.29. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_momentum | XAUUSD | M15 | -1.297 | 49.2 | 📋 WR 49%, Sharpe -1.30. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | range_breakout | XAUUSD | H1 | -1.329 | 47.1 | 📋 WR 47%, Sharpe -1.33. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | GBPUSD | H4 | -1.373 | 51.5 | 📋 WR 51%, Sharpe -1.37. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | cot_sentiment | EURUSD | D1 | -1.393 | 40.6 | 📋 WR 41%, Sharpe -1.39. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | bb_mean_reversion | EURUSD | H4 | -1.397 | 46.4 | 📋 WR 46%, Sharpe -1.40. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | moving_average_crossover | USDJPY | H1 | -1.452 | 44.8 | 📋 WR 45%, Sharpe -1.45. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | vwap_momentum | EURUSD | M30 | -1.498 | 35.6 | ❌ WR 36%, PF 0.81 — no edge detected. Entry signal does not predict direction be… |
| P4 | hikkake_trap | GBPUSD | H1 | -1.524 | 33.9 | ❌ WR 34%, PF 0.81 — no edge detected. Entry signal does not predict direction be… |
| P4 | cot_sentiment | GBPUSD | D1 | -1.539 | 38.9 | ❌ WR 39%, PF 0.80 — no edge detected. Entry signal does not predict direction be… |
| P4 | turtle_soup | EURUSD | H4 | -1.541 | 47.6 | 📋 WR 48%, Sharpe -1.54. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | bb_mean_reversion | XAUUSD | H1 | -1.601 | 47.7 | 📋 WR 48%, Sharpe -1.60. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | session_momentum | GBPUSD | M15 | -1.602 | 39.3 | ❌ WR 39%, PF 0.81 — no edge detected. Entry signal does not predict direction be… |
| P4 | vwap_momentum | GBPUSD | M30 | -1.717 | 35.5 | ❌ WR 35%, PF 0.79 — no edge detected. Entry signal does not predict direction be… |
| P4 | macd_trend | EURUSD | H4 | -1.899 | 50.0 | 📋 WR 50%, Sharpe -1.90. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | stoch_divergence | EURUSD | H1 | -1.91 | 33.6 | ❌ WR 34%, PF 0.77 — no edge detected. Entry signal does not predict direction be… |
| P4 | rsi_bounce | XAUUSD | H4 | -1.915 | 27.6 | ❌ WR 28%, PF 0.69 — no edge detected. Entry signal does not predict direction be… |
| P4 | range_breakout | XAUUSD | M30 | -1.916 | 47.8 | 📋 WR 48%, Sharpe -1.92. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | bb_mean_reversion | XAUUSD | M15 | -1.936 | 48.4 | 📋 WR 48%, Sharpe -1.94. Investigate avg_trade_duration — if trades close in < 1h… |
