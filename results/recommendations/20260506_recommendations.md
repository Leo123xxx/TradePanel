# TradePanel Recommendations — 20260506

Generated: 2026-05-06 02:24 UTC  
Report: `results/overnight/20260506_backtest_report.json`

---

## Summary

| Metric | Value |
|--------|-------|
| Total results | 148 |
| ✅ PASS | 35 (24%) |
| 🔄 REVIEW | 90 (61%) |
| ⏭ SKIP | 0 |

## 🗑️ Removal / Escalation Queue

- 🟠 ESCALATE **macd_trend** EURUSD H4 — 6 consecutive fails (Sharpe -2.48)
- 🟠 ESCALATE **cot_sentiment** GBPUSD D1 — 6 consecutive fails (Sharpe 0.03)
- 🟠 ESCALATE **cot_sentiment** USDJPY D1 — 6 consecutive fails (Sharpe -5.13)
- 🟡 WATCH **orb** EURUSD M15 — 1 consecutive fails, deadline in 26d (Sharpe -4.87)

## 🎯 Near-PASS Candidates (prioritise these)

| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker |
|----------|------|----|--------|-----|-----|---------|
| session_momentum | XAUUSD | H1 | 1.254 | 35.6 | 13.6 | WR 35.6% needs +24.4pp |
| session_momentum | GBPJPY | H1 | 1.226 | 37.1 | 2.6 | WR 37.1% needs +22.9pp |
| range_breakout | US500 | H4 | 0.683 | 53.9 | 0.6 | Sharpe 0.68 (+0.32 needed), WR 53.9% (+6.1pp needed) |
| dual_ema_momentum | XAUUSD | H1 | 0.657 | 51.9 | 8.4 | Sharpe 0.66 (+0.34 needed), WR 51.9% (+8.1pp needed) |
| session_momentum | GBPUSD | H1 | 0.631 | 35.6 | 2.8 | Sharpe 0.63 (+0.37 needed), WR 35.6% (+24.4pp needed) |

## 🔧 Priority Tuning Hints (P1 + P2)

_P1 = immediate action required / P2 = high value next test_

### turtle_soup — AUDUSD H4
**Action:** 🚫 Sharpe -1.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -1.20 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.84 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_momentum — GBPJPY H4
**Action:** 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.2% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.24 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### stat_arb_gold_silver — XAUUSD M15
**Action:** 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 186.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.24 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.79 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover — EURUSD H1
**Action:** 🚫 Sharpe -1.29 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -1.29 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp — US500 M15
**Action:** 🚫 Sharpe -1.38 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 60.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 28 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.38 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on US500 unless confirmed by live data

### dual_ema_fractal — GBPUSD H1
**Action:** 🚫 Sharpe -1.45 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -1.45 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — EURUSD H4
**Action:** 🚫 Sharpe -1.49 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.49 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### cot_sentiment — XAUUSD D1
**Action:** 🚫 Sharpe -1.56 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 33.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.56 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.81 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### dual_ema_fractal — GBPJPY H4
**Action:** 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.59 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.79 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_extremes_scalp — EURUSD M15
**Action:** 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -1.59 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.79 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap — GBPUSD H4
**Action:** 🚫 Sharpe -1.62 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (44%) >> LONG (24%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 33.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.62 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.81 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_momentum — US500 H4
**Action:** 🚫 Sharpe -1.77 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (55%) >> SHORT (38%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Sharpe -1.77 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.78 — marginal edge, consider disabling on US500 unless confirmed by live data

### orb — GBPJPY M15
**Action:** 🚫 Sharpe -1.81 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -1.81 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.78 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### macd_trend — EURUSD H1
**Action:** 🚫 Sharpe -1.93 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.1% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.93 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — EURUSD H1
**Action:** 🚫 Sharpe -1.97 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.97 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb — AUDUSD M15
**Action:** 🚫 Sharpe -2.01 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -2.01 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.75 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### session_momentum — EURUSD H1
**Action:** 🚫 Sharpe -2.43 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 27.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.43 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover — GBPUSD H4
**Action:** 🚫 Sharpe -2.45 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (58%) >> LONG (35%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 43.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.45 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend — EURUSD H4
**Action:** 🚫 Sharpe -2.48 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 18 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.48 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum — EURUSD H4
**Action:** 🚫 Sharpe -2.55 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (50%) >> SHORT (35%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 42.2% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.55 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### ma_crossover — USDJPY H1
**Action:** 🚫 Sharpe -2.65 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.2% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.65 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.68 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### dual_ema_fractal — AUDUSD H4
**Action:** 🚫 Sharpe -2.67 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.67 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.68 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H4
**Action:** 🚫 Sharpe -2.75 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.5% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.75 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — USOIL H4
**Action:** 🚫 Sharpe -2.75 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 28.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.75 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.65 — marginal edge, consider disabling on USOIL unless confirmed by live data

### hikkake_trap — USOIL H4
**Action:** 🚫 Sharpe -2.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (41%) >> SHORT (11%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 26.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 22.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -2.83 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.66 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_extremes_scalp — USOIL M15
**Action:** 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.93 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on USOIL unless confirmed by live data

### ma_crossover — EURUSD H4
**Action:** 🚫 Sharpe -2.96 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.4% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 18 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.96 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.66 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H1
**Action:** 🚫 Sharpe -3.01 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.01 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### macd_trend — US500 H4
**Action:** 🚫 Sharpe -3.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (70%) >> SHORT (33%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Only 22 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.20 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on US500 unless confirmed by live data

### orb — GBPUSD M15
**Action:** 🚫 Sharpe -3.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (56%) >> SHORT (40%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Sharpe -3.20 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### session_momentum — AUDUSD H1
**Action:** 🚫 Sharpe -3.29 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 27.6% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.29 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rvgi_cci_confluence — EURUSD H1
**Action:** 🚫 Sharpe -3.42 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.1% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.42 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### crypto_rsi_extremes — BTCUSD H4
**Action:** 🚫 Sharpe -3.57 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 38.1% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 21.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.57 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### orb — XAUUSD M15
**Action:** 🚫 Sharpe -3.58 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 22.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.58 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### turtle_soup — GBPJPY H4
**Action:** 🚫 Sharpe -3.65 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (51%) >> SHORT (24%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 42.2% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.65 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### hikkake_trap — EURUSD H4
**Action:** 🚫 Sharpe -3.70 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 28.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.70 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — BTCUSD H4
**Action:** 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 40.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.83 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### macd_trend — AUDUSD H4
**Action:** 🚫 Sharpe -3.99 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.99 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### ma_crossover — GBPUSD H1
**Action:** 🚫 Sharpe -4.05 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (52%) >> SHORT (36%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 43.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.05 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — USDCAD H4
**Action:** 🚫 Sharpe -4.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 41.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.13 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_extremes_scalp — XAUUSD M15
**Action:** 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.20 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.51 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### orb — EURUSD M15
**Action:** 🚫 Sharpe -4.87 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (50%) >> SHORT (35%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 42.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.87 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.51 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### crypto_rsi_extremes — ETHUSD H4
**Action:** 🚫 Sharpe -4.87 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 32.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -4.87 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.48 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### cot_sentiment — USDJPY D1
**Action:** 🚫 Sharpe -5.14 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.1% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 50.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -5.14 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.49 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### ma_crossover — USDCAD H4
**Action:** 🚫 Sharpe -5.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Sharpe -5.32 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.47 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### rsi_extremes_scalp — AUDUSD M15
**Action:** 🚫 Sharpe -5.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (53%) >> LONG (39%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 45.2% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.33 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.44 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_extremes_scalp — GBPUSD M15
**Action:** 🚫 Sharpe -5.70 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (53%) >> LONG (21%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 37.9% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -5.70 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.42 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend — NVDA H4
**Action:** 🚫 Sharpe -6.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 40.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.33 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.27 — marginal edge, consider disabling on NVDA unless confirmed by live data

### rsi_extremes_scalp — GBPJPY M15
**Action:** 🚫 Sharpe -6.43 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -6.43 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.40 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_extremes_scalp — USDJPY M15
**Action:** 🚫 Sharpe -6.77 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 23.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.77 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.38 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### bb_squeeze_scalp — AUDUSD M15
**Action:** 🚫 Sharpe -6.94 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (56%) >> SHORT (27%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 44.8% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 29 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.94 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.36 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### bb_squeeze_scalp — EURUSD M15
**Action:** 🚫 Sharpe -20.15 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 7.7% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -20.15 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.05 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — XAUUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### stoch_divergence — GBPUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### stoch_divergence — GBPJPY H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### stoch_divergence — AUDUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### gold_momentum_breakout — AMD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### vwap_momentum — GBPJPY M15
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### vwap_momentum — BTCUSD M15
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 0.8 → reduce lot size on this pair or pause strategy

### ma_crossover — EURUSD D1
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.07 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.84 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### crypto_rsi_extremes — BTCUSD D1
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 28.6% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.48 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.69 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### stoch_divergence — XAUUSD H4
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.67 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### crypto_rsi_extremes — ETHUSD D1
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -8.99 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.26 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### bb_squeeze_scalp — GBPUSD M15
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 14.3% < 48.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -18.38 < 0.8 → reduce lot size on this pair or pause strategy
  - Profit factor 0.11 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

---

## Appendix — Full REVIEW Strategy Tuning List

| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |
|----------|----------|------|----|--------|-----|--------|
| P1 | turtle_soup | AUDUSD | H4 | -1.196 | 51.9 | 🚫 Sharpe -1.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | GBPJPY | H4 | -1.239 | 43.2 | 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stat_arb_gold_silver | XAUUSD | M15 | -1.241 | 46.0 | 🚫 Sharpe -1.24 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | EURUSD | H1 | -1.292 | 53.0 | 🚫 Sharpe -1.29 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | US500 | M15 | -1.376 | 60.7 | 🚫 Sharpe -1.38 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPUSD | H1 | -1.45 | 51.6 | 🚫 Sharpe -1.45 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | H4 | -1.492 | 47.4 | 🚫 Sharpe -1.49 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | XAUUSD | D1 | -1.558 | 33.3 | 🚫 Sharpe -1.56 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPJPY | H4 | -1.585 | 44.4 | 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | EURUSD | M15 | -1.594 | 52.5 | 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | GBPUSD | H4 | -1.622 | 33.3 | 🚫 Sharpe -1.62 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | US500 | H4 | -1.77 | 48.1 | 🚫 Sharpe -1.77 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | GBPJPY | M15 | -1.813 | 49.0 | 🚫 Sharpe -1.81 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H1 | -1.927 | 45.1 | 🚫 Sharpe -1.93 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | H1 | -1.967 | 46.7 | 🚫 Sharpe -1.97 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | AUDUSD | M15 | -2.011 | 53.4 | 🚫 Sharpe -2.01 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | EURUSD | H1 | -2.43 | 27.3 | 🚫 Sharpe -2.43 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | GBPUSD | H4 | -2.447 | 43.8 | 🚫 Sharpe -2.45 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H4 | -2.479 | 44.4 | 🚫 Sharpe -2.48 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | EURUSD | H4 | -2.552 | 42.2 | 🚫 Sharpe -2.55 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | USDJPY | H1 | -2.654 | 43.2 | 🚫 Sharpe -2.65 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | AUDUSD | H4 | -2.673 | 46.0 | 🚫 Sharpe -2.67 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H4 | -2.749 | 45.5 | 🚫 Sharpe -2.75 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | USOIL | H4 | -2.755 | 42.9 | 🚫 Sharpe -2.75 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | USOIL | H4 | -2.826 | 26.8 | 🚫 Sharpe -2.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | USOIL | M15 | -2.925 | 45.8 | 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | EURUSD | H4 | -2.965 | 44.4 | 🚫 Sharpe -2.96 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H1 | -3.007 | 45.9 | 🚫 Sharpe -3.01 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | US500 | H4 | -3.202 | 50.0 | 🚫 Sharpe -3.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | GBPUSD | M15 | -3.205 | 48.0 | 🚫 Sharpe -3.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | AUDUSD | H1 | -3.288 | 27.6 | 🚫 Sharpe -3.29 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | H1 | -3.423 | 43.1 | 🚫 Sharpe -3.42 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | crypto_rsi_extremes | BTCUSD | H4 | -3.566 | 38.1 | 🚫 Sharpe -3.57 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | XAUUSD | M15 | -3.579 | 42.9 | 🚫 Sharpe -3.58 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPJPY | H4 | -3.652 | 42.2 | 🚫 Sharpe -3.65 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | EURUSD | H4 | -3.697 | 28.3 | 🚫 Sharpe -3.70 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | BTCUSD | H4 | -3.829 | 40.0 | 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | AUDUSD | H4 | -3.988 | 42.9 | 🚫 Sharpe -3.99 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | GBPUSD | H1 | -4.047 | 43.7 | 🚫 Sharpe -4.05 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | USDCAD | H4 | -4.127 | 41.7 | 🚫 Sharpe -4.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | XAUUSD | M15 | -4.203 | 46.9 | 🚫 Sharpe -4.20 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | EURUSD | M15 | -4.867 | 42.9 | 🚫 Sharpe -4.87 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | crypto_rsi_extremes | ETHUSD | H4 | -4.872 | 32.3 | 🚫 Sharpe -4.87 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | USDJPY | D1 | -5.135 | 36.1 | 🚫 Sharpe -5.14 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | USDCAD | H4 | -5.315 | 48.5 | 🚫 Sharpe -5.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | AUDUSD | M15 | -5.329 | 45.2 | 🚫 Sharpe -5.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | GBPUSD | M15 | -5.695 | 37.9 | 🚫 Sharpe -5.70 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | NVDA | H4 | -6.328 | 40.0 | 🚫 Sharpe -6.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | GBPJPY | M15 | -6.434 | 46.0 | 🚫 Sharpe -6.43 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | USDJPY | M15 | -6.773 | 23.8 | 🚫 Sharpe -6.77 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | AUDUSD | M15 | -6.939 | 44.8 | 🚫 Sharpe -6.94 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | EURUSD | M15 | -20.149 | 7.7 | 🚫 Sharpe -20.15 — strategy is actively losing money. Do not tune parameters yet.… |
| P2 | rsi_bounce | XAUUSD | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | GBPUSD | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | GBPJPY | H4 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | AUDUSD | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | gold_momentum_breakout | AMD | H4 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | vwap_momentum | GBPJPY | M15 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | vwap_momentum | BTCUSD | M15 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | EURUSD | D1 | -1.069 | 66.7 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | crypto_rsi_extremes | BTCUSD | D1 | -2.475 | 28.6 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | XAUUSD | H4 | -3.673 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | crypto_rsi_extremes | ETHUSD | D1 | -8.994 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | GBPUSD | M15 | -18.377 | 14.3 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P3 | session_momentum | XAUUSD | H1 | 1.254 | 35.6 | 📈 Sharpe 1.25 is promising but WR 36% needs +24.4pp to reach 60%. Tighten entry:… |
| P3 | session_momentum | GBPJPY | H1 | 1.226 | 37.1 | 📈 Sharpe 1.23 is promising but WR 37% needs +22.9pp to reach 60%. Tighten entry:… |
| P3 | range_breakout | US500 | H4 | 0.683 | 53.9 | 📈 Sharpe 0.68 is promising but WR 54% needs +6.1pp to reach 60%. Tighten entry: … |
| P3 | dual_ema_momentum | XAUUSD | H1 | 0.657 | 51.9 | 📈 Sharpe 0.66 is promising but WR 52% needs +8.1pp to reach 60%. Tighten entry: … |
| P3 | session_momentum | GBPUSD | H1 | 0.631 | 35.6 | 📈 Sharpe 0.63 is promising but WR 36% needs +24.4pp to reach 60%. Tighten entry:… |
| P3 | hikkake_trap | US500 | H4 | 0.609 | 39.3 | 📈 Sharpe 0.61 is promising but WR 39% needs +20.7pp to reach 60%. Tighten entry:… |
| P3 | hikkake_trap | GBPJPY | H4 | 0.325 | 36.7 | 🔧 Low WR (37%) but PF 1.05 — system captures large wins rarely. Typical of trend… |
| P3 | cot_sentiment | GBPUSD | D1 | 0.026 | 48.8 | 🔧 Marginal edge (WR 49%, PF 1.00). Check long_win_rate vs short_win_rate — if on… |
| P4 | dual_ema_fractal | EURUSD | H4 | 0.305 | 52.0 | 📋 WR 52%, Sharpe 0.30. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | range_breakout | EURUSD | H4 | 0.297 | 54.4 | 📋 WR 54%, Sharpe 0.30. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | ema_ribbon_trend | BTCUSD | H4 | 0.263 | 59.0 | 📋 WR 59%, Sharpe 0.26. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_fractal | XAUUSD | H1 | 0.144 | 52.1 | 📋 WR 52%, Sharpe 0.14. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rsi_pullback | USDJPY | H4 | 0.143 | 57.5 | 📋 WR 57%, Sharpe 0.14. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | bb_squeeze_scalp | GBPJPY | M15 | 0.119 | 59.1 | 📋 WR 59%, Sharpe 0.12. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rvgi_cci_confluence | GBPJPY | H4 | 0.041 | 51.4 | 📋 WR 51%, Sharpe 0.04. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | cot_sentiment | EURUSD | D1 | -0.033 | 48.3 | 📋 WR 48%, Sharpe -0.03. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | XAUUSD | H4 | -0.142 | 57.6 | 📋 WR 58%, Sharpe -0.14. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | bb_squeeze_scalp | XAUUSD | M15 | -0.278 | 38.5 | ❌ WR 38%, PF 0.95 — no edge detected. Entry signal does not predict direction be… |
| P4 | ma_crossover | AUDUSD | H4 | -0.285 | 56.5 | 📋 WR 57%, Sharpe -0.29. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ma_crossover | GBPJPY | H4 | -0.33 | 46.3 | 📋 WR 46%, Sharpe -0.33. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | ETHUSD | H4 | -0.445 | 50.0 | 📋 WR 50%, Sharpe -0.45. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_fractal | GBPUSD | H4 | -0.749 | 51.6 | 📋 WR 52%, Sharpe -0.75. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | gold_momentum_breakout | XAUUSD | H1 | -0.781 | 49.8 | 📋 WR 50%, Sharpe -0.78. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | GBPUSD | H4 | -0.817 | 51.2 | 📋 WR 51%, Sharpe -0.82. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_momentum | GBPUSD | H4 | -0.823 | 50.0 | 📋 WR 50%, Sharpe -0.82. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | rvgi_cci_confluence | AUDUSD | H4 | -0.843 | 57.5 | 📋 WR 57%, Sharpe -0.84. Investigate avg_trade_duration — if trades close in < 1h… |
