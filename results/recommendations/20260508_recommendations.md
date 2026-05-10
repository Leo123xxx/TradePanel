# TradePanel Recommendations — 20260508

Generated: 2026-05-08 02:58 UTC  
Report: `results/overnight/20260508_backtest_report.json`

---

## Summary

| Metric | Value |
|--------|-------|
| Total results | 147 |
| ✅ PASS | 12 (8%) |
| 🔄 REVIEW | 127 (86%) |
| ⏭ SKIP | 0 |

## 🔬 WFO Validation Status

| Strategy | Pair | TF | WFO Verdict | Notes |
|----------|------|----|-------------|-------|
| ma_crossover | EURUSD | H1 | WFO ERROR | Run error -- re-check deps |
| ma_crossover | GBPUSD | H4 | WFO ERROR | Run error -- re-check deps |

_WFO last run: 7 day(s) ago_

## ⚠️ Regressions (PASS → REVIEW)

- **dual_ema_fractal** XAUUSD H4 — Sharpe now 3.42, WR 63% — **Investigate immediately**
- **dual_ema_fractal** USDCAD H4 — Sharpe now 1.16, WR 60% — **Investigate immediately**
- **rsi_bounce** USDJPY H4 — Sharpe now 2.85, WR 67% — **Investigate immediately**
- **stat_arb_gold_silver** XAUUSD H1 — Sharpe now 3.32, WR 65% — **Investigate immediately**
- **ma_crossover** GBPUSD H4 — Sharpe now 2.67, WR 67% — **Investigate immediately**
- **ma_crossover** AUDUSD H4 — Sharpe now 4.04, WR 61% — **Investigate immediately**
- **ma_crossover** GBPJPY H4 — Sharpe now 2.76, WR 56% — **Investigate immediately**
- **bb_mean_reversion** XAUUSD H4 — Sharpe now 2.35, WR 55% — **Investigate immediately**
- **bb_mean_reversion** EURUSD H1 — Sharpe now 1.25, WR 60% — **Investigate immediately**
- **stoch_divergence** GBPUSD H4 — Sharpe now 3.26, WR 50% — **Investigate immediately**
- **stoch_divergence** AUDUSD H4 — Sharpe now 2.23, WR 50% — **Investigate immediately**
- **macd_trend** EURUSD H4 — Sharpe now 4.50, WR 64% — **Investigate immediately**
- **macd_trend** USDJPY H1 — Sharpe now 1.00, WR 58% — **Investigate immediately**
- **macd_trend** GBPJPY H4 — Sharpe now 4.50, WR 67% — **Investigate immediately**
- **gold_momentum_breakout** XAUUSD H4 — Sharpe now 3.57, WR 58% — **Investigate immediately**
- **gold_momentum_breakout** US500 H4 — Sharpe now 4.49, WR 65% — **Investigate immediately**
- **gold_momentum_breakout** USTEC H4 — Sharpe now 3.20, WR 62% — **Investigate immediately**
- **gold_momentum_breakout** AMD H4 — Sharpe now 4.46, WR 60% — **Investigate immediately**
- **gold_momentum_breakout** MSFT H4 — Sharpe now 3.25, WR 61% — **Investigate immediately**
- **range_breakout** XAUUSD H4 — Sharpe now 4.74, WR 58% — **Investigate immediately**
- **range_breakout** USOIL H4 — Sharpe now 2.45, WR 51% — **Investigate immediately**
- **range_breakout** US500 H4 — Sharpe now 0.84, WR 55% — **Investigate immediately**
- **ema_ribbon_trend** AAPL H4 — Sharpe now 3.92, WR 50% — **Investigate immediately**

## 🗑️ Removal / Escalation Queue

- 🟠 ESCALATE **bb_mean_reversion** XAUUSD H4 — 7 consecutive fails (Sharpe 2.35)
- 🟠 ESCALATE **stoch_divergence** USDJPY H4 — 7 consecutive fails (Sharpe -4.54)
- 🟠 ESCALATE **macd_trend** EURUSD H4 — 6 consecutive fails (Sharpe 4.50)
- 🟠 ESCALATE **cot_sentiment** GBPUSD D1 — 6 consecutive fails (Sharpe -2.24)
- 🟠 ESCALATE **cot_sentiment** USDJPY D1 — 6 consecutive fails (Sharpe -5.42)
- 🟡 WATCH **orb** EURUSD M15 — 1 consecutive fails, deadline in 24d (Sharpe -0.70)

## 🎯 Near-PASS Candidates (prioritise these)

| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker |
|----------|------|----|--------|-----|-----|---------|
| hikkake_trap | GBPUSD | H4 | 5.496 | 68.0 | 0.8 | WR 68.0% needs +2.0pp |
| ema_ribbon_trend | NVDA | H4 | 4.837 | 40.0 | 0.3 | WR 40.0% needs +30.0pp |
| range_breakout | XAUUSD | H4 | 4.744 | 58.1 | 8.2 | WR 58.1% needs +11.9pp |
| macd_trend | EURUSD | H4 | 4.497 | 63.6 | 0.5 | WR 63.6% needs +6.4pp |
| macd_trend | GBPJPY | H4 | 4.495 | 66.7 | 1.8 | WR 66.7% needs +3.3pp |

## 🔧 Priority Tuning Hints (P1 + P2)

_P1 = immediate action required / P2 = high value next test_

### ma_crossover — EURUSD D1
**Action:** 🚫 Sharpe -1.11 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (55%) >> LONG (22%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 20 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.11 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.85 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_momentum — GBPJPY H4
**Action:** 🚫 Sharpe -1.17 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 25 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.17 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.84 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### hikkake_trap — USOIL H4
**Action:** 🚫 Sharpe -1.22 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (45%) >> SHORT (0%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 44.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.22 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.84 — marginal edge, consider disabling on USOIL unless confirmed by live data

### dual_ema_momentum — USTEC H4
**Action:** 🚫 Sharpe -1.31 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (69%) >> SHORT (36%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 54.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 24 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.31 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.82 — marginal edge, consider disabling on USTEC unless confirmed by live data

### turtle_soup — BTCUSD H4
**Action:** 🚫 Sharpe -1.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 22.5% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.32 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.82 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### range_breakout — EURUSD H4
**Action:** 🚫 Sharpe -1.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 51.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.33 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — XAUUSD H4
**Action:** 🚫 Sharpe -1.34 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 35.7% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -1.34 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.78 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover — EURUSD H4
**Action:** 🚫 Sharpe -1.42 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (59%) >> LONG (33%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 48.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.42 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.81 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — AUDUSD H4
**Action:** 🚫 Sharpe -1.50 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 55.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.50 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.80 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### rsi_extremes_scalp — EURUSD M15
**Action:** 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 52.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.59 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.79 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_mean_reversion — XAUUSD H1
**Action:** 🚫 Sharpe -1.63 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.63 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### session_momentum — GBPUSD H1
**Action:** 🚫 Sharpe -1.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.83 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.77 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — GBPUSD H4
**Action:** 🚫 Sharpe -1.84 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.84 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.77 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — EURUSD H4
**Action:** 🚫 Sharpe -1.88 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.88 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### macd_trend — EURUSD H1
**Action:** 🚫 Sharpe -1.95 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 47.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -1.95 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.76 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### turtle_soup — ETHUSD H4
**Action:** 🚫 Sharpe -2.02 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.02 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.74 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### cot_sentiment — GBPUSD D1
**Action:** 🚫 Sharpe -2.24 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 36.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.24 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### dual_ema_fractal — EURUSD H1
**Action:** 🚫 Sharpe -2.33 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.33 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.72 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### orb — AUDUSD M15
**Action:** 🚫 Sharpe -2.38 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 53.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.38 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal — GBPJPY H4
**Action:** 🚫 Sharpe -2.41 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.41 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### ma_crossover — EURUSD H1
**Action:** 🚫 Sharpe -2.62 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (53%) >> SHORT (40%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 46.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.62 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.68 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### dual_ema_fractal — USOIL H4
**Action:** 🚫 Sharpe -2.76 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 44.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.76 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.67 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rsi_extremes_scalp — USOIL M15
**Action:** 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.93 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on USOIL unless confirmed by live data

### rvgi_cci_confluence — EURUSD H1
**Action:** 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -2.93 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.66 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rvgi_cci_confluence — GBPUSD H1
**Action:** 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.08 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### orb — GBPJPY M15
**Action:** 🚫 Sharpe -3.18 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 48.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.18 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.64 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### bb_mean_reversion — GBPUSD H1
**Action:** 🚫 Sharpe -3.36 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.36 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.63 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### turtle_soup — USDCAD H4
**Action:** 🚫 Sharpe -3.51 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (54%) >> SHORT (29%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 40.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.51 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on USDCAD unless confirmed by live data

### ma_crossover — USDJPY H1
**Action:** 🚫 Sharpe -3.55 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (70%) >> SHORT (33%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 45.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.55 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### macd_trend — USTEC H4
**Action:** 🚫 Sharpe -3.55 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: LONG (58%) >> SHORT (33%) — consider disabling SHORT trades.
**Backtest suggestions:**
  - Win rate 43.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.55 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.61 — marginal edge, consider disabling on USTEC unless confirmed by live data

### crypto_rsi_extremes — BTCUSD H4
**Action:** 🚫 Sharpe -3.66 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 38.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 21.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.66 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### macd_trend — AUDUSD H4
**Action:** 🚫 Sharpe -3.69 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.69 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### orb — XAUUSD M15
**Action:** 🚫 Sharpe -3.72 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 21.6% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -3.72 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.56 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_extremes_scalp — AUDUSD M15
**Action:** 🚫 Sharpe -3.75 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 52.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 19 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.75 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### dual_ema_fractal — AUDUSD H4
**Action:** 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.83 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### bb_mean_reversion — US500 H4
**Action:** 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 14 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.83 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on US500 unless confirmed by live data

### session_momentum — EURUSD H1
**Action:** 🚫 Sharpe -3.92 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 43.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.92 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.57 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### hikkake_trap — EURUSD H4
**Action:** 🚫 Sharpe -3.98 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Direction:** Directional bias: SHORT (48%) >> LONG (36%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 42.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -3.98 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.58 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### bb_squeeze_scalp — US500 M15
**Action:** 🚫 Sharpe -4.07 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 57.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -4.07 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.53 — marginal edge, consider disabling on US500 unless confirmed by live data

### stoch_divergence — GBPJPY H4
**Action:** 🚫 Sharpe -4.53 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 15 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -4.53 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.52 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### stoch_divergence — USDJPY H4
**Action:** 🚫 Sharpe -4.54 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 16 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -4.54 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.55 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### session_momentum — AUDUSD H1
**Action:** 🚫 Sharpe -5.32 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 45.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.32 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.47 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### cot_sentiment — USDJPY D1
**Action:** 🚫 Sharpe -5.42 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 31.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Max drawdown 51.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
  - Sharpe -5.42 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.45 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### crypto_rsi_extremes — ETHUSD H4
**Action:** 🚫 Sharpe -5.75 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 32.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -5.75 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.43 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### bb_squeeze_scalp — XAUUSD M15
**Action:** 🚫 Sharpe -6.13 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.13 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.42 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_extremes_scalp — GBPJPY M15
**Action:** 🚫 Sharpe -6.43 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 46.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Sharpe -6.43 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.40 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### rsi_extremes_scalp — USDJPY M15
**Action:** 🚫 Sharpe -6.77 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 23.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 21 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.77 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.38 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### ema_ribbon_trend — BTCUSD H4
**Action:** 🚫 Sharpe -7.23 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -7.23 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.34 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### rsi_extremes_scalp — XAUUSD M15
**Action:** 🚫 Sharpe -10.54 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 38.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 13 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -10.54 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.15 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### ma_crossover — USDJPY H4
**Action:** 🚫 Sharpe -13.37 — strategy is actively losing money. Do not tune parameters yet. Diagnose signal logic: check entry condition direction, ensure spread/commission are accounted for, and verify data alignment (SAST vs UTC).
**Backtest suggestions:**
  - Win rate 30.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 10 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -13.37 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.14 — marginal edge, consider disabling on USDJPY unless confirmed by live data

### hikkake_trap — GBPUSD H4
**Action:** 🎯 Near-PASS (Sharpe 5.50, WR 68% — needs +2.0pp). Add a regime filter (ADX > 20 or EMA200 gate) to prune losing trades and close the WR gap.
**Direction:** Directional bias: SHORT (68%) >> LONG (0%) — consider disabling LONG trades.
**Backtest suggestions:**
  - Win rate 68.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Win rate 68.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 25 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend — NVDA H4
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### macd_trend — GBPJPY H4
**Action:** 🎯 Near-PASS (Sharpe 4.50, WR 67% — needs +3.3pp). Add a regime filter (ADX > 20 or EMA200 gate) to prune losing trades and close the WR gap.
**Backtest suggestions:**
  - Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 27 trades — widen oversold/overbought thresholds or relax ADX filter

### gold_momentum_breakout — AMD H4
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### ema_ribbon_trend — AAPL H4
**Action:** 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### stoch_divergence — GBPUSD H4
**Action:** 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 4 trades — widen oversold/overbought thresholds or relax ADX filter

### rsi_bounce — USDJPY H4
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### ma_crossover — GBPUSD H4
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 66.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Win rate 66.7% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 3 trades — widen oversold/overbought thresholds or relax ADX filter

### stoch_divergence — AUDUSD H4
**Action:** 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 2 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_mean_reversion — USDJPY H4
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter

### bb_squeeze_scalp — AUDUSD M15
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 83.3% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 1.58 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend — XAUUSD H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### ema_ribbon_trend — MSFT H4
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### cot_sentiment — XAUUSD D1
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### vwap_momentum — GBPJPY M15
**Action:** 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 100.0% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
  - Only 1 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe 0.00 < 2.0 → reduce lot size on this pair or pause strategy

### bb_squeeze_scalp — GBPJPY M15
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.16 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.85 — marginal edge, consider disabling on GBPJPY unless confirmed by live data

### crypto_rsi_extremes — ETHUSD D1
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -1.17 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.83 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### stoch_divergence — EURUSD H4
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 60.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -2.22 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.71 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — AUDUSD H4
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.27 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.60 — marginal edge, consider disabling on AUDUSD unless confirmed by live data

### crypto_rsi_extremes — BTCUSD D1
**Action:** 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 28.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.27 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend — USTEC H4
**Action:** 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 25.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 4 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.53 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.59 — marginal edge, consider disabling on USTEC unless confirmed by live data

### rsi_bounce — XAUUSD H4
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 50.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -3.63 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.55 — marginal edge, consider disabling on XAUUSD unless confirmed by live data

### rsi_bounce — USOIL H4
**Action:** 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 22.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 9 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -4.36 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.50 — marginal edge, consider disabling on USOIL unless confirmed by live data

### ema_ribbon_trend — ETHUSD H4
**Action:** 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 6 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -6.99 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.27 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### rsi_bounce — EURUSD H4
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 40.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -7.18 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.35 — marginal edge, consider disabling on EURUSD unless confirmed by live data

### rsi_bounce — GBPUSD H4
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -10.77 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.19 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### ema_ribbon_trend — US500 H4
**Action:** 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -11.80 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.13 — marginal edge, consider disabling on US500 unless confirmed by live data

### bb_squeeze_scalp — GBPUSD M15
**Action:** 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 20.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 5 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -15.54 < 2.0 → reduce lot size on this pair or pause strategy
  - Profit factor 0.14 — marginal edge, consider disabling on GBPUSD unless confirmed by live data

### bb_squeeze_scalp — EURUSD M15
**Action:** 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -29.45 < 2.0 → reduce lot size on this pair or pause strategy

### stoch_divergence — XAUUSD H4
**Action:** 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or relax entry filters before tuning parameters.
**Backtest suggestions:**
  - Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
  - Only 2 trades — widen oversold/overbought thresholds or relax ADX filter
  - Sharpe -50.00 < 2.0 → reduce lot size on this pair or pause strategy

---

## Appendix — Full REVIEW Strategy Tuning List

| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |
|----------|----------|------|----|--------|-----|--------|
| P1 | ma_crossover | EURUSD | D1 | -1.113 | 40.0 | 🚫 Sharpe -1.11 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | GBPJPY | H4 | -1.171 | 36.0 | 🚫 Sharpe -1.17 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | USOIL | H4 | -1.218 | 44.7 | 🚫 Sharpe -1.22 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_momentum | USTEC | H4 | -1.309 | 54.2 | 🚫 Sharpe -1.31 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | BTCUSD | H4 | -1.323 | 50.8 | 🚫 Sharpe -1.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | range_breakout | EURUSD | H4 | -1.334 | 51.2 | 🚫 Sharpe -1.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | XAUUSD | H4 | -1.341 | 50.9 | 🚫 Sharpe -1.34 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | EURUSD | H4 | -1.418 | 48.6 | 🚫 Sharpe -1.42 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | AUDUSD | H4 | -1.503 | 55.4 | 🚫 Sharpe -1.50 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | EURUSD | M15 | -1.594 | 52.5 | 🚫 Sharpe -1.59 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | XAUUSD | H1 | -1.625 | 46.4 | 🚫 Sharpe -1.63 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | GBPUSD | H1 | -1.835 | 48.0 | 🚫 Sharpe -1.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | GBPUSD | H4 | -1.842 | 47.1 | 🚫 Sharpe -1.84 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | EURUSD | H4 | -1.88 | 47.8 | 🚫 Sharpe -1.88 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | EURUSD | H1 | -1.946 | 47.3 | 🚫 Sharpe -1.95 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | ETHUSD | H4 | -2.022 | 46.7 | 🚫 Sharpe -2.02 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | GBPUSD | D1 | -2.242 | 36.5 | 🚫 Sharpe -2.24 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | EURUSD | H1 | -2.329 | 46.2 | 🚫 Sharpe -2.33 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | AUDUSD | M15 | -2.381 | 53.3 | 🚫 Sharpe -2.38 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | GBPJPY | H4 | -2.409 | 46.8 | 🚫 Sharpe -2.41 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | EURUSD | H1 | -2.622 | 46.7 | 🚫 Sharpe -2.62 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | USOIL | H4 | -2.755 | 44.7 | 🚫 Sharpe -2.76 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | USOIL | M15 | -2.925 | 45.8 | 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | EURUSD | H1 | -2.929 | 43.7 | 🚫 Sharpe -2.93 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rvgi_cci_confluence | GBPUSD | H1 | -3.075 | 43.4 | 🚫 Sharpe -3.08 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | GBPJPY | M15 | -3.177 | 48.0 | 🚫 Sharpe -3.18 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | GBPUSD | H1 | -3.36 | 50.0 | 🚫 Sharpe -3.36 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | turtle_soup | USDCAD | H4 | -3.508 | 40.7 | 🚫 Sharpe -3.51 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ma_crossover | USDJPY | H1 | -3.546 | 45.2 | 🚫 Sharpe -3.55 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | USTEC | H4 | -3.548 | 43.3 | 🚫 Sharpe -3.55 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | crypto_rsi_extremes | BTCUSD | H4 | -3.659 | 38.1 | 🚫 Sharpe -3.66 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | macd_trend | AUDUSD | H4 | -3.691 | 46.1 | 🚫 Sharpe -3.69 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | orb | XAUUSD | M15 | -3.724 | 42.5 | 🚫 Sharpe -3.72 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | AUDUSD | M15 | -3.75 | 52.6 | 🚫 Sharpe -3.75 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | dual_ema_fractal | AUDUSD | H4 | -3.831 | 46.3 | 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_mean_reversion | US500 | H4 | -3.834 | 42.9 | 🚫 Sharpe -3.83 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | EURUSD | H1 | -3.924 | 43.9 | 🚫 Sharpe -3.92 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | hikkake_trap | EURUSD | H4 | -3.984 | 42.6 | 🚫 Sharpe -3.98 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | US500 | M15 | -4.071 | 57.1 | 🚫 Sharpe -4.07 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stoch_divergence | GBPJPY | H4 | -4.529 | 46.7 | 🚫 Sharpe -4.53 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | stoch_divergence | USDJPY | H4 | -4.536 | 37.5 | 🚫 Sharpe -4.54 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | session_momentum | AUDUSD | H1 | -5.323 | 45.0 | 🚫 Sharpe -5.32 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | cot_sentiment | USDJPY | D1 | -5.423 | 31.5 | 🚫 Sharpe -5.42 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | crypto_rsi_extremes | ETHUSD | H4 | -5.751 | 32.3 | 🚫 Sharpe -5.75 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | bb_squeeze_scalp | XAUUSD | M15 | -6.127 | 33.3 | 🚫 Sharpe -6.13 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | GBPJPY | M15 | -6.434 | 46.0 | 🚫 Sharpe -6.43 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | USDJPY | M15 | -6.773 | 23.8 | 🚫 Sharpe -6.77 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | ema_ribbon_trend | BTCUSD | H4 | -7.228 | 33.3 | 🚫 Sharpe -7.23 — strategy is actively losing money. Do not tune parameters yet. … |
| P1 | rsi_extremes_scalp | XAUUSD | M15 | -10.543 | 38.5 | 🚫 Sharpe -10.54 — strategy is actively losing money. Do not tune parameters yet.… |
| P1 | ma_crossover | USDJPY | H4 | -13.369 | 30.0 | 🚫 Sharpe -13.37 — strategy is actively losing money. Do not tune parameters yet.… |
| P2 | hikkake_trap | GBPUSD | H4 | 5.496 | 68.0 | 🎯 Near-PASS (Sharpe 5.50, WR 68% — needs +2.0pp). Add a regime filter (ADX > 20 … |
| P2 | ema_ribbon_trend | NVDA | H4 | 4.837 | 40.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | macd_trend | GBPJPY | H4 | 4.495 | 66.7 | 🎯 Near-PASS (Sharpe 4.50, WR 67% — needs +3.3pp). Add a regime filter (ADX > 20 … |
| P2 | gold_momentum_breakout | AMD | H4 | 4.46 | 60.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | AAPL | H4 | 3.917 | 50.0 | 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | GBPUSD | H4 | 3.257 | 50.0 | 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | USDJPY | H4 | 2.845 | 66.7 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ma_crossover | GBPUSD | H4 | 2.668 | 66.7 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | AUDUSD | H4 | 2.231 | 50.0 | 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_mean_reversion | USDJPY | H4 | 2.213 | 40.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | AUDUSD | M15 | 1.583 | 83.3 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | XAUUSD | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | MSFT | H4 | 0.0 | 0.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | cot_sentiment | XAUUSD | D1 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | vwap_momentum | GBPJPY | M15 | 0.0 | 100.0 | 📉 Only 1 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | GBPJPY | M15 | -1.164 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | crypto_rsi_extremes | ETHUSD | D1 | -1.173 | 25.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | EURUSD | H4 | -2.219 | 60.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | AUDUSD | H4 | -3.266 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | crypto_rsi_extremes | BTCUSD | D1 | -3.272 | 28.6 | 📉 Only 7 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | USTEC | H4 | -3.529 | 25.0 | 📉 Only 4 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | XAUUSD | H4 | -3.626 | 50.0 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | USOIL | H4 | -4.365 | 22.2 | 📉 Only 9 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | ETHUSD | H4 | -6.992 | 33.3 | 📉 Only 6 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | EURUSD | H4 | -7.184 | 40.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | rsi_bounce | GBPUSD | H4 | -10.774 | 33.3 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | ema_ribbon_trend | US500 | H4 | -11.803 | 33.3 | 📉 Only 3 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | GBPUSD | M15 | -15.541 | 20.0 | 📉 Only 5 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | bb_squeeze_scalp | EURUSD | M15 | -29.445 | 0.0 | 📉 Only 8 trades — sample too small for reliable stats. Extend backtest window or… |
| P2 | stoch_divergence | XAUUSD | H4 | -50.0 | 0.0 | 📉 Only 2 trades — sample too small for reliable stats. Extend backtest window or… |
| P3 | range_breakout | XAUUSD | H4 | 4.744 | 58.1 | 📈 Sharpe 4.74 is promising but WR 58% needs +11.9pp to reach 70%. Tighten entry:… |
| P3 | macd_trend | EURUSD | H4 | 4.497 | 63.6 | 📈 Sharpe 4.50 is promising but WR 64% needs +6.4pp to reach 70%. Tighten entry: … |
| P3 | gold_momentum_breakout | US500 | H4 | 4.489 | 64.9 | 📈 Sharpe 4.49 is promising but WR 65% needs +5.1pp to reach 70%. Tighten entry: … |
| P3 | ma_crossover | AUDUSD | H4 | 4.044 | 61.3 | 📈 Sharpe 4.04 is promising but WR 61% needs +8.7pp to reach 70%. Tighten entry: … |
| P3 | gold_momentum_breakout | XAUUSD | H4 | 3.567 | 57.5 | 📈 Sharpe 3.57 is promising but WR 58% needs +12.5pp to reach 70%. Tighten entry:… |
| P3 | dual_ema_fractal | XAUUSD | H4 | 3.417 | 63.5 | 📈 Sharpe 3.42 is promising but WR 63% needs +6.5pp to reach 70%. Tighten entry: … |
| P3 | stat_arb_gold_silver | XAUUSD | H1 | 3.324 | 64.5 | 📈 Sharpe 3.32 is promising but WR 65% needs +5.5pp to reach 70%. Tighten entry: … |
| P3 | gold_momentum_breakout | MSFT | H4 | 3.246 | 61.1 | 📈 Sharpe 3.25 is promising but WR 61% needs +8.9pp to reach 70%. Tighten entry: … |
| P3 | gold_momentum_breakout | USTEC | H4 | 3.202 | 61.7 | 📈 Sharpe 3.20 is promising but WR 62% needs +8.3pp to reach 70%. Tighten entry: … |
| P3 | rsi_pullback | XAGUSD | H4 | 3.089 | 54.2 | 📈 Sharpe 3.09 is promising but WR 54% needs +15.8pp to reach 70%. Tighten entry:… |
| P3 | dual_ema_momentum | XAUUSD | H4 | 2.998 | 50.0 | 📈 Sharpe 3.00 is promising but WR 50% needs +20.0pp to reach 70%. Tighten entry:… |
| P3 | rsi_pullback | GBPUSD | H4 | 2.925 | 58.3 | 📈 Sharpe 2.93 is promising but WR 58% needs +11.7pp to reach 70%. Tighten entry:… |
| P3 | rsi_pullback | XAUUSD | H4 | 2.8 | 60.0 | 📈 Sharpe 2.80 is promising but WR 60% needs +10.0pp to reach 70%. Tighten entry:… |
| P3 | ma_crossover | GBPJPY | H4 | 2.762 | 55.6 | 📈 Sharpe 2.76 is promising but WR 56% needs +14.4pp to reach 70%. Tighten entry:… |
| P3 | hikkake_trap | US500 | H4 | 2.537 | 60.5 | 📈 Sharpe 2.54 is promising but WR 60% needs +9.5pp to reach 70%. Tighten entry: … |
| P3 | range_breakout | USOIL | H4 | 2.451 | 50.9 | 📈 Sharpe 2.45 is promising but WR 51% needs +19.1pp to reach 70%. Tighten entry:… |
| P3 | bb_mean_reversion | XAUUSD | H4 | 2.353 | 55.0 | 📈 Sharpe 2.35 is promising but WR 55% needs +15.0pp to reach 70%. Tighten entry:… |
| P3 | hikkake_trap | XAUUSD | H4 | 2.298 | 57.9 | 📈 Sharpe 2.30 is promising but WR 58% needs +12.1pp to reach 70%. Tighten entry:… |
| P3 | rsi_pullback | EURUSD | H4 | 2.23 | 58.1 | 📈 Sharpe 2.23 is promising but WR 58% needs +11.9pp to reach 70%. Tighten entry:… |
| P3 | bb_mean_reversion | EURUSD | H1 | 1.249 | 59.5 | 📈 Sharpe 1.25 is promising but WR 60% needs +10.5pp to reach 70%. Tighten entry:… |
| P3 | rvgi_cci_confluence | GBPUSD | H4 | 1.206 | 59.2 | 📈 Sharpe 1.21 is promising but WR 59% needs +10.8pp to reach 70%. Tighten entry:… |
| P3 | dual_ema_fractal | USDCAD | H4 | 1.165 | 60.0 | 📈 Sharpe 1.16 is promising but WR 60% needs +10.0pp to reach 70%. Tighten entry:… |
| P3 | macd_trend | USDJPY | H1 | 0.996 | 57.6 | 📈 Sharpe 1.00 is promising but WR 58% needs +12.4pp to reach 70%. Tighten entry:… |
| P3 | range_breakout | US500 | H4 | 0.837 | 54.9 | 📈 Sharpe 0.84 is promising but WR 55% needs +15.1pp to reach 70%. Tighten entry:… |
| P3 | session_momentum | XAUUSD | H1 | 0.603 | 54.5 | 📈 Sharpe 0.60 is promising but WR 55% needs +15.5pp to reach 70%. Tighten entry:… |
| P3 | dual_ema_momentum | XAUUSD | H1 | 0.067 | 45.5 | 🔧 Marginal edge (WR 45%, PF 1.01). Check long_win_rate vs short_win_rate — if on… |
| P4 | dual_ema_momentum | GBPUSD | H4 | 0.537 | 55.2 | 📋 WR 55%, Sharpe 0.54. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | turtle_soup | GBPJPY | H4 | 0.47 | 50.7 | 📋 WR 51%, Sharpe 0.47. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | dual_ema_fractal | XAUUSD | H1 | 0.439 | 55.6 | 📋 WR 56%, Sharpe 0.44. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | ma_crossover | GBPUSD | H1 | 0.356 | 58.1 | 📋 WR 58%, Sharpe 0.36. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rvgi_cci_confluence | GBPJPY | H4 | 0.346 | 52.7 | 📋 WR 53%, Sharpe 0.35. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rvgi_cci_confluence | EURUSD | H4 | 0.22 | 54.7 | 📋 WR 55%, Sharpe 0.22. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | rsi_pullback | USDJPY | H4 | 0.143 | 57.5 | 📋 WR 57%, Sharpe 0.14. Investigate avg_trade_duration — if trades close in < 1h … |
| P4 | hikkake_trap | GBPJPY | H4 | -0.076 | 51.9 | 📋 WR 52%, Sharpe -0.08. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | orb | GBPUSD | M15 | -0.18 | 60.0 | 📋 WR 60%, Sharpe -0.18. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | ma_crossover | USDCAD | H4 | -0.294 | 66.7 | 📋 WR 67%, Sharpe -0.29. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_momentum | US500 | H4 | -0.486 | 52.9 | 📋 WR 53%, Sharpe -0.49. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | bb_squeeze_scalp | USTEC | M15 | -0.499 | 53.9 | 📋 WR 54%, Sharpe -0.50. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_fractal | EURUSD | H4 | -0.538 | 53.6 | 📋 WR 54%, Sharpe -0.54. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | turtle_soup | AUDUSD | H4 | -0.675 | 50.0 | 📋 WR 50%, Sharpe -0.67. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | orb | EURUSD | M15 | -0.701 | 52.4 | 📋 WR 52%, Sharpe -0.70. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | cot_sentiment | EURUSD | D1 | -0.748 | 42.6 | 📋 WR 43%, Sharpe -0.75. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | session_momentum | GBPJPY | H1 | -0.758 | 47.5 | 📋 WR 48%, Sharpe -0.76. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | gold_momentum_breakout | XAUUSD | H1 | -0.763 | 51.3 | 📋 WR 51%, Sharpe -0.76. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | rsi_extremes_scalp | GBPUSD | M15 | -0.817 | 53.3 | 📋 WR 53%, Sharpe -0.82. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_fractal | GBPUSD | H4 | -0.871 | 54.2 | 📋 WR 54%, Sharpe -0.87. Investigate avg_trade_duration — if trades close in < 1h… |
| P4 | dual_ema_fractal | GBPUSD | H1 | -0.976 | 53.3 | 📋 WR 53%, Sharpe -0.98. Investigate avg_trade_duration — if trades close in < 1h… |
