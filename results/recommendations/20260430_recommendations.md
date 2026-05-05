# TradePanel Recommendations — 20260430

Generated: 2026-04-30 03:40 UTC  
Report: `results/overnight/20260430_backtest_report.json`

---

## Summary

| Metric | Value |
|--------|-------|
| Total results | 126 |
| ✅ PASS | 11 (9%) |
| 🔄 REVIEW | 110 (87%) |
| ⏭ SKIP | 2 |

## 🎉 New PASSes Since Last Run

- **dual_ema_fractal** XAUUSD H4 — Sharpe 4.89, WR 66%
- **dual_ema_fractal** XAUUSD D1 — Sharpe 5.69, WR 61%
- **rsi_bounce** EURUSD H1 — Sharpe 2.67, WR 67%
- **macd_trend** EURUSD D1 — Sharpe 6.27, WR 74%
- **gold_momentum_breakout** XAUUSD H4 — Sharpe 4.98, WR 64%
- **range_breakout** XAUUSD H4 — Sharpe 7.11, WR 71%
- **ema_ribbon_trend** ETHUSD H4 — Sharpe 7.16, WR 80%
- **turtle_soup** EURUSD D1 — Sharpe 5.57, WR 61%

## ⚠️ Regressions (PASS → REVIEW)

- **gold_momentum_breakout** XAUUSD D1 — Sharpe now 0.00, WR 100% — **Investigate immediately**

## 🗑️ Removal / Escalation Queue

- 🟡 WATCH **orb** EURUSD M5 — 2 consecutive fails, deadline in 32d (Sharpe -4.75)
- 🟡 WATCH **orb** EURUSD M15 — 2 consecutive fails, deadline in 32d (Sharpe -3.85)

## 🎯 Near-PASS Candidates (prioritise these)

| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker |
|----------|------|----|--------|-----|-----|---------|
| dual_ema_momentum | XAUUSD | D1 | 4.172 | 53.9 | 7.9 | WR 53.9% needs +6.1pp |
| vwap_momentum | GBPUSD | H1 | 2.82 | 46.7 | 0.5 | WR 46.7% needs +13.3pp |
| bb_mean_reversion | EURUSD | H1 | 2.442 | 57.1 | 0.3 | WR 57.1% needs +2.9pp |
| hikkake_trap | XAUUSD | D1 | 2.03 | 29.4 | 26.0 | WR 29.4% needs +30.6pp |
| orb | XAGUSD | M15 | 1.823 | 59.3 | 12.9 | WR 59.3% needs +0.7pp |

## 🔧 Priority Tuning Hints (P1 + P2)

_P1 = immediate action required / P2 = high value next test_

### hikkake_trap — EURUSD H1
**Action:** 🚫 Sharpe -1.04 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.04 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.87 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — EURUSD D1
**Action:** 🚫 Sharpe -1.07 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 18 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.07 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.85 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — GBPUSD H1
**Action:** 🚫 Sharpe -1.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 52.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.85 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stat_arb_gold_silver — XAUUSD D1
**Action:** 🚫 Sharpe -1.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 38.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 106.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.13 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### stoch_divergence — EURUSD M30
**Action:** 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.24 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.84 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap — XAUUSD M30
**Action:** 🚫 Sharpe -1.30 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 70.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.30 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### hikkake_trap — GBPUSD H1
**Action:** 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 34.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum — GBPUSD M30
**Action:** 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout — XAUUSD M15
**Action:** 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 29.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.79 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H4
**Action:** 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.37 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.82 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout — XAUUSD D1
**Action:** 🚫 Sharpe -1.41 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 58.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 23.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.41 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_momentum — XAUUSD M15
**Action:** 🚫 Sharpe -1.42 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 20.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.42 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup — EURUSD H4
**Action:** 🚫 Sharpe -1.49 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.49 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — GBPUSD M5
**Action:** 🚫 Sharpe -1.65 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.65 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout — XAUUSD H1
**Action:** 🚫 Sharpe -1.84 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (54%) >> SHORT (33%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 45.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 23.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.84 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### vwap_momentum — EURUSD M30
**Action:** 🚫 Sharpe -1.85 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.85 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.78 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment — GBPUSD D1
**Action:** 🚫 Sharpe -1.94 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 38.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.94 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum — GBPUSD H1
**Action:** 🚫 Sharpe -2.07 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.07 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### gold_momentum_breakout — GBPUSD H1
**Action:** 🚫 Sharpe -2.10 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (55%) >> SHORT (41%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 47.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.10 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stoch_divergence — USDJPY H1
**Action:** 🚫 Sharpe -2.12 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 34.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.12 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend — EURUSD M30
**Action:** 🚫 Sharpe -2.15 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 53.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.15 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.73 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### session_momentum — GBPUSD M15
**Action:** 🚫 Sharpe -2.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.20 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — EURUSD H1
**Action:** 🚫 Sharpe -2.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.32 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap — XAUUSD H1
**Action:** 🚫 Sharpe -2.50 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 30.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 88.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.50 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend — EURUSD H1
**Action:** 🚫 Sharpe -2.51 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.51 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum — EURUSD H1
**Action:** 🚫 Sharpe -2.62 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.62 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout — XAUUSD M30
**Action:** 🚫 Sharpe -2.64 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 55.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.64 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### macd_trend — EURUSD H4
**Action:** 🚫 Sharpe -2.73 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.73 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.68 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD M30
**Action:** 🚫 Sharpe -2.76 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.76 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD M30
**Action:** 🚫 Sharpe -2.77 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.77 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — EURUSD M30
**Action:** 🚫 Sharpe -2.78 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.78 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD M30
**Action:** 🚫 Sharpe -2.80 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 49.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.80 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — GBPUSD M15
**Action:** 🚫 Sharpe -2.94 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 32.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.94 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — GBPUSD H1
**Action:** 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.08 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.65 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_mean_reversion — XAUUSD M15
**Action:** 🚫 Sharpe -3.15 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 11 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.15 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### range_breakout — EURUSD H4
**Action:** 🚫 Sharpe -3.21 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.21 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD H4
**Action:** 🚫 Sharpe -3.22 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.22 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD H1
**Action:** 🚫 Sharpe -3.25 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.25 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — GBPUSD M30
**Action:** 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.30 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp — XAUUSD M1
**Action:** 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.30 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal — EURUSD M15
**Action:** 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.30 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.60 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — EURUSD H1
**Action:** 🚫 Sharpe -3.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.33 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H1
**Action:** 🚫 Sharpe -3.36 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.36 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### cot_sentiment — USDJPY D1
**Action:** 🚫 Sharpe -3.59 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 35.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 36.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.59 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend — EURUSD M15
**Action:** 🚫 Sharpe -3.64 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.5% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.64 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — EURUSD M30
**Action:** 🚫 Sharpe -3.72 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.72 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb — EURUSD M15
**Action:** 🚫 Sharpe -3.85 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (50%) >> SHORT (37%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 42.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.85 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD M15
**Action:** 🚫 Sharpe -3.86 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.86 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### gold_momentum_breakout — GBPUSD M30
**Action:** 🚫 Sharpe -3.88 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.88 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### range_breakout — XAUUSD M30
**Action:** 🚫 Sharpe -3.99 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 72.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.99 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.40 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### range_breakout — EURUSD H1
**Action:** 🚫 Sharpe -4.38 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.38 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.55 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp — XAUUSD M1
**Action:** 🚫 Sharpe -4.51 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.51 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.50 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD H1
**Action:** 🚫 Sharpe -4.67 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.67 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.49 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### orb — EURUSD M5
**Action:** 🚫 Sharpe -4.75 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.75 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.52 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ema_ribbon_trend — ETHUSD H1
**Action:** 🚫 Sharpe -5.73 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.73 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.41 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### rsi_bounce — EURUSD M30
**Action:** 🚫 Sharpe -5.86 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -5.86 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.45 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — EURUSD M15
**Action:** 🚫 Sharpe -6.07 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 30.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.07 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.43 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — GBPUSD M15
**Action:** 🚫 Sharpe -6.28 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 40.8% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -6.28 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.41 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### rsi_extremes_scalp — XAUUSD M5
**Action:** 🚫 Sharpe -6.59 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.59 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.32 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup — EURUSD M15
**Action:** 🚫 Sharpe -7.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.6% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -7.83 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.32 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### vwap_momentum — EURUSD M5
**Action:** 🚫 Sharpe -9.19 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -9.19 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.30 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp — GBPUSD M5
**Action:** 🚫 Sharpe -9.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 21.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -9.83 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.19 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp — EURUSD M5
**Action:** 🚫 Sharpe -11.55 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -11.55 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp — EURUSD M1
**Action:** 🚫 Sharpe -12.12 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 26.9% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -12.12 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.18 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp — EURUSD M1
**Action:** 🚫 Sharpe -13.25 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 28.4% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -13.25 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.13 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion — EURUSD H1
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 57.1% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 7 trades — widen oversold/overbought thresholds or relax ADX filter

### orb — XAGUSD M15
**Action:** 🎯 Near-PASS (Sharpe 1.82, WR 59% — needs +0.7pp). Add a regime filter (ADX > 20 or EMA200 gate) to prune losing trades and close the WR gap.
**Backtest suggestions:**
  - Win rate 59.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)

### rsi_bounce — XAUUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### bb_mean_reversion — XAUUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout — XAUUSD D1
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### cot_sentiment — XAUUSD D1
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 1.0 → reduce lot size on this pair or pause strategy

### rsi_bounce — XAUUSD H1
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -0.27 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.96 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### gold_momentum_breakout — XAUUSD H1
**Action:** 💡 WR 50% but max DD 27%. Position sizing too aggressive or SL too wide. Try sl_atr_mult - 0.2, or cap lot size at 50% current level and re-test.
**Backtest suggestions:**
  - Win rate 50.2% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 27.3% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -0.89 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.86 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### stoch_divergence — USDJPY H4
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.96 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.65 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### rsi_bounce — XAUUSD M30
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.93 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.48 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce — GBPUSD M30
**Action:** 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.99 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### stoch_divergence — EURUSD H4
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 14.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -7.28 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.35 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_extremes_scalp — EURUSD M5
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -8.84 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.22 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion — XAUUSD H1
**Action:** 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -10.22 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.24 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_extremes_scalp — GBPUSD M5
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -14.82 < 1.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.11 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend — BTCUSD D1
**Action:** 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -15.04 < 1.0 → reduce lot size on this pair or pause strategy

### rsi_extremes_scalp — USDJPY M5
**Action:** 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -22.69 < 1.0 → reduce lot size on this pair or pause strategy

### rsi_bounce — GBPUSD H1
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 60.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -50.00 < 1.0 → reduce lot size on this pair or pause strategy

---

## Appendix — Full REVIEW Strategy Tuning List

| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |
|----------|----------|------|----|--------|-----|--------|
| P1 | hikkake_trap | EURUSD | H1 | -1.043 | 36.1 | 🚫 Sharpe -1.04 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | D1 | -1.072 | 44.4 | 🚫 Sharpe -1.07 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPUSD | H1 | -1.127 | 52.7 | 🚫 Sharpe -1.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stat_arb_gold_silver | XAUUSD | D1 | -1.133 | 38.5 | 🚫 Sharpe -1.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stoch_divergence | EURUSD | M30 | -1.243 | 35.4 | 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | XAUUSD | M30 | -1.3 | 33.3 | 🚫 Sharpe -1.30 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | GBPUSD | H1 | -1.368 | 34.9 | 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | GBPUSD | M30 | -1.369 | 35.7 | 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | XAUUSD | M15 | -1.37 | 46.5 | 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H4 | -1.371 | 50.0 | 🚫 Sharpe -1.37 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | XAUUSD | D1 | -1.406 | 58.3 | 🚫 Sharpe -1.41 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | XAUUSD | M15 | -1.419 | 45.2 | 🚫 Sharpe -1.42 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | H4 | -1.488 | 48.0 | 🚫 Sharpe -1.49 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | GBPUSD | M5 | -1.655 | 44.8 | 🚫 Sharpe -1.65 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | XAUUSD | H1 | -1.839 | 45.3 | 🚫 Sharpe -1.84 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | EURUSD | M30 | -1.849 | 35.7 | 🚫 Sharpe -1.85 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | GBPUSD | D1 | -1.942 | 38.7 | 🚫 Sharpe -1.94 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | GBPUSD | H1 | -2.069 | 48.9 | 🚫 Sharpe -2.07 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | GBPUSD | H1 | -2.099 | 47.1 | 🚫 Sharpe -2.10 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stoch_divergence | USDJPY | H1 | -2.124 | 34.8 | 🚫 Sharpe -2.12 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | M30 | -2.153 | 53.3 | 🚫 Sharpe -2.15 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | GBPUSD | M15 | -2.198 | 36.6 | 🚫 Sharpe -2.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | H1 | -2.323 | 45.9 | 🚫 Sharpe -2.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | XAUUSD | H1 | -2.503 | 30.4 | 🚫 Sharpe -2.50 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H1 | -2.513 | 44.3 | 🚫 Sharpe -2.51 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | EURUSD | H1 | -2.618 | 47.0 | 🚫 Sharpe -2.62 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | XAUUSD | M30 | -2.639 | 43.8 | 🚫 Sharpe -2.64 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H4 | -2.726 | 47.4 | 🚫 Sharpe -2.73 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | M30 | -2.76 | 47.6 | 🚫 Sharpe -2.76 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | M30 | -2.765 | 48.8 | 🚫 Sharpe -2.77 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | M30 | -2.784 | 47.7 | 🚫 Sharpe -2.78 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | M30 | -2.802 | 49.9 | 🚫 Sharpe -2.80 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | GBPUSD | M15 | -2.937 | 32.4 | 🚫 Sharpe -2.94 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPUSD | H1 | -3.081 | 45.9 | 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | XAUUSD | M15 | -3.152 | 45.5 | 🚫 Sharpe -3.15 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | EURUSD | H4 | -3.213 | 47.2 | 🚫 Sharpe -3.21 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | H4 | -3.217 | 50.0 | 🚫 Sharpe -3.22 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | H1 | -3.249 | 43.8 | 🚫 Sharpe -3.25 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPUSD | M30 | -3.295 | 48.2 | 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | XAUUSD | M1 | -3.297 | 46.1 | 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | M15 | -3.302 | 48.4 | 🚫 Sharpe -3.30 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | H1 | -3.332 | 46.0 | 🚫 Sharpe -3.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H1 | -3.355 | 46.8 | 🚫 Sharpe -3.36 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | USDJPY | D1 | -3.587 | 35.7 | 🚫 Sharpe -3.59 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | M15 | -3.644 | 45.5 | 🚫 Sharpe -3.64 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | M30 | -3.723 | 48.6 | 🚫 Sharpe -3.72 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | EURUSD | M15 | -3.849 | 42.6 | 🚫 Sharpe -3.85 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | M15 | -3.856 | 46.2 | 🚫 Sharpe -3.86 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | gold_momentum_breakout | GBPUSD | M30 | -3.88 | 45.9 | 🚫 Sharpe -3.88 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | XAUUSD | M30 | -3.989 | 42.0 | 🚫 Sharpe -3.99 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | EURUSD | H1 | -4.378 | 42.7 | 🚫 Sharpe -4.38 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | XAUUSD | M1 | -4.51 | 42.4 | 🚫 Sharpe -4.51 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | H1 | -4.672 | 45.0 | 🚫 Sharpe -4.67 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | EURUSD | M5 | -4.75 | 47.2 | 🚫 Sharpe -4.75 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | ETHUSD | H1 | -5.725 | 46.7 | 🚫 Sharpe -5.73 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | EURUSD | M30 | -5.856 | 33.3 | 🚫 Sharpe -5.86 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_bounce | EURUSD | M15 | -6.072 | 30.0 | 🚫 Sharpe -6.07 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPUSD | M15 | -6.275 | 40.8 | 🚫 Sharpe -6.28 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | XAUUSD | M5 | -6.588 | 46.7 | 🚫 Sharpe -6.59 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | M15 | -7.826 | 36.6 | 🚫 Sharpe -7.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | vwap_momentum | EURUSD | M5 | -9.193 | 25.0 | 🚫 Sharpe -9.19 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | GBPUSD | M5 | -9.829 | 21.1 | 🚫 Sharpe -9.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | EURUSD | M5 | -11.55 | 25.0 | 🚫 Sharpe -11.55 — strategy is actively losing money. Do not tune parameters yet.… |
| P1 | rsi_extremes_scalp | EURUSD | M1 | -12.123 | 26.9 | 🚫 Sharpe -12.12 — strategy is actively losing money. Do not tune parameters yet.… |
| P1 | bb_squeeze_scalp | EURUSD | M1 | -13.246 | 28.4 | 🚫 Sharpe -13.25 — strategy is actively losing money. Do not tune parameters yet.… |
| P2 | bb_mean_reversion | EURUSD | H1 | 2.442 | 57.1 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | orb | XAGUSD | M15 | 1.823 | 59.3 | 🎯 Near-PASS (Sharpe 1.82, WR 59% — needs +0.7pp). Add a regime filter (ADX > 20 … |
| P2 | rsi_bounce | XAUUSD | H4 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_mean_reversion | XAUUSD | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | XAUUSD | D1 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | cot_sentiment | XAUUSD | D1 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | XAUUSD | H1 | -0.272 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | XAUUSD | H1 | -0.887 | 50.2 | 💡 WR 50% but max DD 27%. Position sizing too aggressive or SL too wide. Try sl_a… |
| P2 | stoch_divergence | USDJPY | H4 | -2.957 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | XAUUSD | M30 | -3.933 | 33.3 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | GBPUSD | M30 | -3.991 | 33.3 | 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | EURUSD | H4 | -7.277 | 14.3 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_extremes_scalp | EURUSD | M5 | -8.843 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_mean_reversion | XAUUSD | H1 | -10.222 | 33.3 | 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_extremes_scalp | GBPUSD | M5 | -14.82 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | BTCUSD | D1 | -15.044 | 0.0 | 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_extremes_scalp | USDJPY | M5 | -22.692 | 0.0 | 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | GBPUSD | H1 | -50.0 | 0.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P3 | dual_ema_momentum | XAUUSD | D1 | 4.172 | 53.9 | 📈 Sharpe 4.17 is promising but WR 54% needs +6.1pp to reach 60%. Tighten entry: … |
| P3 | vwap_momentum | GBPUSD | H1 | 2.82 | 46.7 | 📈 Sharpe 2.82 is promising but WR 47% needs +13.3pp to reach 60%. Tighten entry:… |
| P3 | hikkake_trap | XAUUSD | D1 | 2.03 | 29.4 | 📈 Sharpe 2.03 is promising but WR 29% needs +30.6pp to reach 60%. Tighten entry:… |
| P3 | dual_ema_momentum | XAUUSD | H4 | 1.509 | 48.9 | 📈 Sharpe 1.51 is promising but WR 49% needs +11.1pp to reach 60%. Tighten entry:… |
| P3 | hikkake_trap | XAUUSD | H4 | 1.209 | 36.1 | 📈 Sharpe 1.21 is promising but WR 36% needs +23.9pp to reach 60%. Tighten entry:… |
| P3 | stoch_divergence | EURUSD | H1 | 1.135 | 42.9 | 📈 Sharpe 1.14 is promising but WR 43% needs +17.1pp to reach 60%. Tighten entry:… |
| P3 | session_momentum | XAUUSD | M15 | 0.919 | 36.8 | 📈 Sharpe 0.92 is promising but WR 37% needs +23.2pp to reach 60%. Tighten entry:… |
| P3 | session_momentum | XAUUSD | H1 | 0.787 | 38.7 | 📈 Sharpe 0.79 is promising but WR 39% needs +21.3pp to reach 60%. Tighten entry:… |
| P3 | vwap_momentum | GBPUSD | M30 | 0.68 | 42.0 | 📈 Sharpe 0.68 is promising but WR 42% needs +18.0pp to reach 60%. Tighten entry:… |
| P3 | vwap_momentum | XAUUSD | M15 | 0.316 | 38.8 | 🔧 Low WR (39%) but PF 1.05 — system captures large wins rarely. Typical of trend… |
| P3 | session_momentum | GBPUSD | H1 | 0.15 | 37.5 | 🔧 Low WR (38%) but PF 1.02 — system captures large wins rarely. Typical of trend… |
| P4 | bb_mean_reversion | XAUUSD | M30 | 0.337 | 62.5 | 📋 WR 62%, Sharpe 0.34. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | bb_mean_reversion | EURUSD | M30 | 0.288 | 61.9 | 📋 WR 62%, Sharpe 0.29. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | macd_trend | USDJPY | H1 | 0.178 | 53.9 | 📋 WR 54%, Sharpe 0.18. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_fractal | EURUSD | H4 | 0.157 | 55.2 | 📋 WR 55%, Sharpe 0.16. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_fractal | XAUUSD | H1 | 0.115 | 56.1 | 📋 WR 56%, Sharpe 0.11. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_momentum | XAUUSD | H1 | 0.025 | 50.0 | 📋 WR 50%, Sharpe 0.03. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_momentum | XAUUSD | M30 | 0.006 | 51.8 | 📋 WR 52%, Sharpe 0.01. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | vwap_momentum | XAUUSD | M30 | -0.161 | 39.8 | ❌ WR 40%, PF 0.97 — no edge detected. Entry signal does not predict direction be… |
| P4 | dual_ema_fractal | GBPUSD | H4 | -0.263 | 55.7 | 📋 WR 56%, Sharpe -0.26. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | session_momentum | XAUUSD | M30 | -0.32 | 35.4 | ❌ WR 35%, PF 0.94 — no edge detected. Entry signal does not predict direction be… |
| P4 | orb | XAGUSD | M5 | -0.475 | 55.2 | 📋 WR 55%, Sharpe -0.48. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | rvgi_cci_confluence | EURUSD | H4 | -0.66 | 48.9 | 📋 WR 49%, Sharpe -0.66. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | GBPUSD | H4 | -0.708 | 52.8 | 📋 WR 53%, Sharpe -0.71. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | cot_sentiment | EURUSD | D1 | -0.748 | 42.6 | 📋 WR 43%, Sharpe -0.75. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | macd_trend | USDJPY | D1 | -0.91 | 47.6 | 📋 WR 48%, Sharpe -0.91. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | vwap_momentum | EURUSD | M15 | -0.911 | 41.1 | 📋 WR 41%, Sharpe -0.91. Investigate avg_trade_duration — if trades close in < 1h… |
