# TradePanel Review Optimizer — 2026-05-03 06:20 UTC

Source: `20260501_backtest_report.json` | Mode: FULL | Promote ≥ 50.0% | Target ≥ 60.0%

---

## Part A — REVIEW Strategy Optimization

Strategies tested: 47 | Skipped: 0 | Promoted: 7

| Strategy | Pair | TF | Before WR% | After WR% | Δ | Sharpe | PF | Status |
|----------|------|----|-----------|----------|---|--------|-----|--------|
| ma_crossover | EURUSD | H1 | 55.6% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | EURUSD | H4 | 33.3% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | USDJPY | H1 | 47.4% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | USDJPY | D1 | 50.0% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | GBPJPY | H1 | 60.0% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | GBPJPY | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | AUDUSD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| ma_crossover | USDCAD | H1 | 0.0% | **80.0%** | +80.0pp | 11.32 | 4.58 | ✅ PASS |
| ma_crossover | USDCAD | H4 | 100.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | XAUUSD | D1 | 100.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | GBPUSD | H4 | 55.2% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | USOIL | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | US500 | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | USTEC | H1 | 44.4% | **64.3%** | +19.8pp | 0.13 | 1.16 | ✅ PASS |
| gold_momentum_breakout | USTEC | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | NVDA | H1 | 40.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | NVDA | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | AMD | H1 | 50.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | AMD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | MSFT | H1 | 50.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | MSFT | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| gold_momentum_breakout | AAPL | H1 | 44.4% | **50.0%** | +5.6pp | -3.20 | 0.89 | 🔶 NEAR |
| gold_momentum_breakout | AAPL | H4 | 50.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | EURUSD | H1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | EURUSD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | EURUSD | D1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | XAUUSD | H1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | XAUUSD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | XAUUSD | D1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | GBPUSD | H1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | GBPUSD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | USDJPY | H1 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | GBPJPY | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | AUDUSD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | USDCAD | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_bounce | USOIL | H4 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_pullback | XAUUSD | D1 | 57.6% | **68.2%** | +10.6pp | 5.89 | 2.47 | ✅ PASS |
| rsi_pullback | USDJPY | H4 | 57.5% | **62.5%** | +5.0pp | 2.01 | 1.32 | ✅ PASS |
| bb_squeeze_scalp | XAUUSD | M15 | 20.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | GBPJPY | M15 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | AUDUSD | M15 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | US500 | M15 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | USTEC | M15 | 0.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | NVDA | M15 | 100.0% | — | — | — | — | SKIP (NO_RESULT) |
| bb_squeeze_scalp | AAPL | M15 | 33.3% | — | — | — | — | SKIP (NO_RESULT) |
| rsi_extremes_scalp | XAUUSD | M15 | 46.9% | **51.5%** | +4.7pp | -3.81 | 0.64 | 🔶 NEAR |
| rsi_extremes_scalp | AUDUSD | M15 | 50.0% | **51.1%** | +1.1pp | -3.04 | 0.66 | 🔶 NEAR |

---

## Part B — PASS Combos on M15 + H1

Strategies tested: 13

| Strategy | Pair | Original TF | Original WR% | M15 WR% | H1 WR% | Better TF |
|----------|------|-------------|-------------|---------|--------|-----------|
| ma_crossover | EURUSD | D1 | 80.0% | — | — | **original** |
| ma_crossover | GBPUSD | H4 | 63.6% | — | — | **original** |
| ma_crossover | USDJPY | H4 | 66.7% | — | — | **original** |
| ma_crossover | AUDUSD | H1 | 100.0% | — | — | **original** |
| gold_momentum_breakout | XAUUSD | H4 | 63.9% | — | — | **original** |
| gold_momentum_breakout | US500 | H1 | 60.0% | — | — | **original** |
| rsi_pullback | XAUUSD | H4 | 60.0% | 47.3% | 43.4% | **original** |
| rsi_pullback | GBPJPY | H4 | 80.0% | 45.4% | 52.1% | **original** |
| rsi_pullback | AUDUSD | H4 | 60.0% | 50.9% | 53.7% | **original** |
| rsi_pullback | USOIL | H4 | 100.0% | 48.1% | 50.3% | **original** |
| bb_squeeze_scalp | USDJPY | M15 | 100.0% | — | — | **original** |
| rsi_extremes_scalp | GBPJPY | M15 | 66.7% | — | — | **original** |
| rsi_extremes_scalp | USOIL | M15 | 75.0% | — | — | **original** |

---

## Promoted to needs_tweaking (11 combos)

| Strategy | Pair | TF | WR% | Sharpe | PF | Source |
|----------|------|----|-----|--------|----|--------|
| ✅ ma_crossover | USDCAD | H1 | **80.0%** | 11.321 | 4.578 | review_optimizer_part_a |
| ✅ rsi_pullback | XAUUSD | D1 | **68.2%** | 5.894 | 2.467 | review_optimizer_part_a |
| ✅ gold_momentum_breakout | USTEC | H1 | **64.3%** | 0.127 | 1.164 | review_optimizer_part_a |
| ✅ rsi_pullback | USDJPY | H4 | **62.5%** | 2.014 | 1.317 | review_optimizer_part_a |
| 🔶 rsi_pullback | AUDUSD | H1 | **53.7%** | 0.294 | 1.095 | review_optimizer_part_b (from H4) |
| 🔶 rsi_pullback | GBPJPY | H1 | **52.1%** | 0.678 | 1.148 | review_optimizer_part_b (from H4) |
| 🔶 rsi_extremes_scalp | XAUUSD | M15 | **51.5%** | -3.815 | 0.641 | review_optimizer_part_a |
| 🔶 rsi_extremes_scalp | AUDUSD | M15 | **51.1%** | -3.039 | 0.658 | review_optimizer_part_a |
| 🔶 rsi_pullback | AUDUSD | M15 | **50.9%** | -3.256 | 0.626 | review_optimizer_part_b (from H4) |
| 🔶 rsi_pullback | USOIL | H1 | **50.3%** | -0.768 | 0.903 | review_optimizer_part_b (from H4) |
| 🔶 gold_momentum_breakout | AAPL | H1 | **50.0%** | -3.198 | 0.89 | review_optimizer_part_a |

---

## Next Steps

1. For each `needs_tweaking` entry, update the corresponding strategy block in `config/strategies.yaml`    with the `suggested_params`.
2. Re-run the overnight backtest: `python scripts/run_overnight_backtest.py`
3. Strategies that achieve WR ≥ 60.0% AND Sharpe ≥ 0.8 are candidates for the 2-week    forward test (see GO-LIVE ACCEPTANCE CRITERIA in strategies.yaml).
4. For SKIP (external data) entries (stat_arb_gold_silver, cot_sentiment, crypto_rsi_extremes)    — optimize manually by adjusting their respective strategy files.

_Generated by `scripts/review_optimizer.py` — 2026-05-03 06:20 UTC_