# WFO Master Summary

**Generated:** 2026-05-15 15:04:57  
**Config:** 5 windows | IS=70% | OOS=30%  
**Criterion:** Sharpe >= 1.5, WR >= 65%, Trades >= 5(H4+)/10(Others) per window (OOS); strategy passes if >= 70% of windows pass

---

## Results Overview

| Strategy | Pair | TF | Pass Rate | Windows | Verdict |
|----------|------|----|----------:|---------|---------|
| dual_ema_fractal | XAUUSD | H4 | 40% | 2/5 | FAIL |
| dual_ema_fractal | EURUSD | H4 | 20% | 1/5 | FAIL |
| rsi_pullback | XAUUSD | H4 | 60% | 3/5 | FAIL |
| rsi_pullback | EURUSD | H4 | 80% | 4/5 | PASS |
| ma_crossover | XAUUSD | H4 | 0% | 0/5 | FAIL |
| ma_crossover | EURUSD | H4 | 0% | 0/5 | FAIL |
| stat_arb_gold_silver | XAUUSD | H2 | 20% | 1/5 | FAIL |
| stat_arb_gold_silver | XAUUSD | H1 | 0% | 0/5 | FAIL |
| bb_mean_reversion | XAUUSD | H4 | 0% | 0/5 | FAIL |
| bb_mean_reversion | EURUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | XAUUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | EURUSD | H4 | 0% | 0/5 | FAIL |
| macd_trend | XAUUSD | H4 | 40% | 2/5 | FAIL |
| macd_trend | EURUSD | H4 | 20% | 1/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H4 | 40% | 2/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H1 | 0% | 0/5 | FAIL |
| range_breakout | XAUUSD | H4 | 40% | 2/5 | FAIL |
| range_breakout | EURUSD | H4 | 0% | 0/5 | FAIL |
| ema_ribbon_trend | XAUUSD | H4 | 0% | 0/5 | FAIL |
| ema_ribbon_trend | EURUSD | H4 | 0% | 0/5 | FAIL |
| session_momentum | XAUUSD | H4 | 20% | 1/5 | FAIL |
| session_momentum | EURUSD | H4 | 60% | 3/5 | FAIL |
| turtle_soup | XAUUSD | H4 | 20% | 1/5 | FAIL |
| turtle_soup | EURUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | XAUUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | EURUSD | H4 | 0% | 0/5 | FAIL |
| vwap_momentum | XAUUSD | H4 | 0% | 0/5 | FAIL |
| vwap_momentum | EURUSD | H4 | 0% | 0/5 | FAIL |
| hikkake_trap | XAUUSD | H4 | 0% | 0/5 | FAIL |
| hikkake_trap | EURUSD | H4 | 0% | 0/5 | FAIL |
| orb | XAUUSD | H4 | 0% | 0/5 | FAIL |
| orb | EURUSD | H4 | 0% | 0/5 | FAIL |
| rvgi_cci_confluence | XAUUSD | H4 | 40% | 2/5 | FAIL |
| rvgi_cci_confluence | EURUSD | H4 | 40% | 2/5 | FAIL |
| fast_ma_scalper | GBPUSD | H1 | 20% | 1/5 | FAIL |
| fast_ma_scalper | USDJPY | H1 | 20% | 1/5 | FAIL |
| bb_squeeze_scalp | USTEC | H2 | 20% | 1/5 | FAIL |
| bb_squeeze_scalp | XAUUSD | H2 | 0% | 0/5 | FAIL |
| rsi_extremes_scalp | XAUUSD | M15 | 0% | 0/5 | FAIL |
| rsi_extremes_scalp | GBPUSD | M15 | 0% | 0/5 | FAIL |
| macd_zero_scalp | GBPUSD | H1 | 0% | 0/5 | FAIL |
| macd_zero_scalp | EURUSD | H1 | 20% | 1/5 | FAIL |
| volatility_breakout_scalp | BTCUSD | H2 | 0% | 0/5 | FAIL |
| volatility_breakout_scalp | BTCUSD | H1 | 0% | 0/5 | FAIL |
| rsi_2 | XAUUSD | H4 | 0% | 0/5 | FAIL |
| rsi_2 | EURUSD | H4 | 0% | 0/5 | FAIL |
| swing_pullback | XAUUSD | H4 | 0% | 0/5 | FAIL |
| swing_pullback | EURUSD | H4 | 20% | 1/5 | FAIL |
| naked_price_action | XAUUSD | H4 | 40% | 2/5 | FAIL |
| naked_price_action | EURUSD | H4 | 0% | 0/5 | FAIL |
| volatility_squeeze_breakout | XAUUSD | H4 | 20% | 1/5 | FAIL |
| volatility_squeeze_breakout | EURUSD | H4 | 0% | 0/5 | FAIL |
| triple_macd_scalping | XAUUSD | M15 | 0% | 0/5 | FAIL |
| triple_macd_scalping | GBPUSD | M15 | 0% | 0/5 | FAIL |
| supertrend | XAUUSD | H4 | 40% | 2/5 | FAIL |
| supertrend | EURUSD | H4 | 40% | 2/5 | FAIL |
| ttm_squeeze | XAUUSD | H4 | 40% | 2/5 | FAIL |
| ttm_squeeze | EURUSD | H4 | 0% | 0/5 | FAIL |
| donchian_trend | BTCUSD | H1 | 0% | 0/5 | FAIL |
| donchian_trend | ETHUSD | H1 | 0% | 0/5 | FAIL |

---

## Summary

- **PASS:** 1 combo(s)
- **FAIL:** 59 combo(s)
- **ERRORS:** 0 combo(s)
- **Skipped:** none

---

## Per-Window Detail

### dual_ema_fractal — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.227 | 42.9 | 7 | FAIL |
| 2 | -1.827 | 50.0 | 14 | FAIL |
| 3 | 5.356 | 60.0 | 10 | FAIL |
| 4 | 9.399 | 70.0 | 10 | PASS |
| 5 | 10.234 | 85.7 | 7 | PASS |

### dual_ema_fractal — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 11.834 | 85.7 | 7 | PASS |
| 2 | 3.205 | 60.0 | 10 | FAIL |
| 3 | -2.482 | 52.6 | 19 | FAIL |
| 4 | -13.417 | 28.6 | 7 | FAIL |
| 5 | -18.366 | 20.0 | 5 | FAIL |

### rsi_pullback — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 6.920 | 75.0 | 12 | PASS |
| 2 | 9.748 | 80.0 | 5 | PASS |
| 3 | 0.843 | 50.0 | 8 | FAIL |
| 4 | 9.679 | 75.0 | 8 | PASS |
| 5 | -0.555 | 55.6 | 9 | FAIL |

### rsi_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 10.273 | 80.0 | 5 | PASS |
| 2 | 1.541 | 58.3 | 12 | FAIL |
| 3 | 6.518 | 66.7 | 12 | PASS |
| 4 | 4.577 | 66.7 | 6 | PASS |
| 5 | 14.085 | 83.3 | 6 | PASS |

### ma_crossover — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.387 | 50.0 | 4 | FAIL |
| 2 | 0.000 | 0.0 | 1 | FAIL |
| 3 | 2.307 | 50.0 | 4 | FAIL |
| 4 | 18.274 | 100.0 | 2 | FAIL |
| 5 | 7.634 | 66.7 | 3 | FAIL |

### ma_crossover — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | -50.000 | 0.0 | 3 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 48.712 | 100.0 | 3 | FAIL |

### stat_arb_gold_silver — XAUUSD H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.611 | 47.1 | 34 | FAIL |
| 2 | 3.859 | 65.0 | 20 | PASS |
| 3 | 0.970 | 54.5 | 11 | FAIL |
| 4 | -3.696 | 41.5 | 53 | FAIL |
| 5 | 0.798 | 44.4 | 18 | FAIL |

### stat_arb_gold_silver — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.792 | 50.8 | 63 | FAIL |
| 2 | -2.728 | 44.9 | 127 | FAIL |
| 3 | 0.666 | 48.3 | 29 | FAIL |
| 4 | -0.768 | 43.3 | 60 | FAIL |
| 5 | -0.869 | 48.4 | 93 | FAIL |

### bb_mean_reversion — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### bb_mean_reversion — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### stoch_divergence — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### stoch_divergence — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 1 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 100.0 | 1 | FAIL |
| 5 | 0.000 | 100.0 | 1 | FAIL |

### macd_trend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.045 | 50.0 | 4 | FAIL |
| 2 | 7.130 | 83.3 | 6 | PASS |
| 3 | 2.185 | 50.0 | 4 | FAIL |
| 4 | -1.209 | 66.7 | 3 | FAIL |
| 5 | 17.680 | 100.0 | 6 | PASS |

### macd_trend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -29.029 | 0.0 | 2 | FAIL |
| 2 | -50.000 | 0.0 | 2 | FAIL |
| 3 | -5.747 | 50.0 | 4 | FAIL |
| 4 | 0.000 | 100.0 | 1 | FAIL |
| 5 | 12.572 | 85.7 | 7 | PASS |

### gold_momentum_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.926 | 54.5 | 11 | FAIL |
| 2 | -1.499 | 46.7 | 15 | FAIL |
| 3 | 4.235 | 62.5 | 8 | FAIL |
| 4 | 10.553 | 83.3 | 6 | PASS |
| 5 | 20.924 | 100.0 | 9 | PASS |

### gold_momentum_breakout — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.720 | 59.5 | 37 | FAIL |
| 2 | 0.931 | 57.7 | 52 | FAIL |
| 3 | 0.985 | 54.3 | 35 | FAIL |
| 4 | 0.213 | 57.1 | 35 | FAIL |
| 5 | -0.990 | 50.0 | 36 | FAIL |

### range_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -14.761 | 25.0 | 4 | FAIL |
| 2 | 14.064 | 100.0 | 2 | FAIL |
| 3 | 0.000 | 100.0 | 1 | FAIL |
| 4 | 9.475 | 83.3 | 6 | PASS |
| 5 | 11.131 | 80.0 | 5 | PASS |

### range_breakout — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.267 | 27.3 | 11 | FAIL |
| 2 | -5.503 | 46.7 | 15 | FAIL |
| 3 | 1.238 | 66.7 | 18 | FAIL |
| 4 | -14.065 | 25.0 | 4 | FAIL |
| 5 | 50.000 | 100.0 | 2 | FAIL |

### ema_ribbon_trend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 14.254 | 100.0 | 2 | FAIL |
| 2 | -36.268 | 0.0 | 4 | FAIL |
| 3 | -50.000 | 0.0 | 2 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 5.074 | 75.0 | 4 | FAIL |

### ema_ribbon_trend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 3.875 | 50.0 | 2 | FAIL |
| 3 | -2.696 | 33.3 | 3 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### session_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.531 | 41.7 | 12 | FAIL |
| 2 | 1.104 | 35.0 | 20 | FAIL |
| 3 | 8.111 | 56.5 | 23 | FAIL |
| 4 | 4.725 | 63.6 | 11 | FAIL |
| 5 | 11.378 | 81.8 | 11 | PASS |

### session_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.725 | 66.7 | 6 | PASS |
| 2 | -0.710 | 62.5 | 8 | FAIL |
| 3 | 11.642 | 88.9 | 9 | PASS |
| 4 | 1.749 | 50.0 | 6 | FAIL |
| 5 | 8.034 | 71.4 | 7 | PASS |

### turtle_soup — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.255 | 57.1 | 28 | FAIL |
| 2 | 1.787 | 48.4 | 31 | FAIL |
| 3 | 5.727 | 80.0 | 5 | PASS |
| 4 | -5.071 | 50.0 | 4 | FAIL |
| 5 | -0.331 | 50.0 | 4 | FAIL |

### turtle_soup — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.309 | 54.5 | 11 | FAIL |
| 2 | -1.906 | 44.4 | 9 | FAIL |
| 3 | 0.935 | 66.7 | 12 | FAIL |
| 4 | -3.420 | 41.7 | 12 | FAIL |
| 5 | -9.832 | 27.3 | 11 | FAIL |

### dual_ema_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### dual_ema_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### vwap_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### vwap_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### hikkake_trap — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.632 | 55.6 | 9 | FAIL |
| 2 | 0.249 | 50.0 | 10 | FAIL |
| 3 | 5.283 | 62.5 | 16 | FAIL |
| 4 | 3.784 | 60.0 | 10 | FAIL |
| 5 | 31.823 | 100.0 | 4 | FAIL |

### hikkake_trap — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.139 | 35.7 | 14 | FAIL |
| 2 | 2.332 | 44.4 | 9 | FAIL |
| 3 | -3.460 | 28.6 | 7 | FAIL |
| 4 | -9.191 | 14.3 | 7 | FAIL |
| 5 | -5.845 | 20.0 | 5 | FAIL |

### orb — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### orb — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 0 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### rvgi_cci_confluence — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -50.000 | 0.0 | 5 | FAIL |
| 2 | 6.412 | 63.6 | 11 | FAIL |
| 3 | 7.199 | 71.4 | 7 | PASS |
| 4 | -0.318 | 50.0 | 8 | FAIL |
| 5 | 6.731 | 73.3 | 15 | PASS |

### rvgi_cci_confluence — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 4.567 | 66.7 | 6 | PASS |
| 2 | -0.903 | 60.0 | 5 | FAIL |
| 3 | 3.505 | 71.4 | 7 | PASS |
| 4 | 0.897 | 44.4 | 9 | FAIL |
| 5 | 1.383 | 42.9 | 7 | FAIL |

### fast_ma_scalper — GBPUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.744 | 50.0 | 4 | FAIL |
| 2 | 7.329 | 75.0 | 4 | FAIL |
| 3 | 6.793 | 66.7 | 6 | PASS |
| 4 | -5.921 | 25.0 | 4 | FAIL |
| 5 | -12.765 | 16.7 | 6 | FAIL |

### fast_ma_scalper — USDJPY H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 11.108 | 83.3 | 6 | PASS |
| 2 | -1.603 | 50.0 | 4 | FAIL |
| 3 | 0.000 | 0.0 | 1 | FAIL |
| 4 | 0.183 | 62.5 | 8 | FAIL |
| 5 | 4.998 | 75.0 | 4 | FAIL |

### bb_squeeze_scalp — USTEC H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 1 | FAIL |
| 2 | 0.000 | 100.0 | 1 | FAIL |
| 3 | 0.000 | 100.0 | 1 | FAIL |
| 4 | 6.188 | 66.7 | 6 | PASS |
| 5 | -4.551 | 50.0 | 2 | FAIL |

### bb_squeeze_scalp — XAUUSD H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.937 | 60.0 | 5 | FAIL |
| 2 | -2.148 | 40.0 | 5 | FAIL |
| 3 | 18.099 | 100.0 | 2 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 100.0 | 1 | FAIL |

### rsi_extremes_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -50.000 | 0.0 | 2 | FAIL |
| 2 | 0.000 | 0.0 | 1 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 1.213 | 60.0 | 5 | FAIL |
| 5 | -4.300 | 40.0 | 5 | FAIL |

### rsi_extremes_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 1 | FAIL |
| 2 | 0.000 | 0.0 | 0 | FAIL |
| 3 | -47.975 | 0.0 | 2 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 1 | FAIL |

### macd_zero_scalp — GBPUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.047 | 33.3 | 3 | FAIL |
| 2 | -50.000 | 0.0 | 2 | FAIL |
| 3 | -3.706 | 40.0 | 5 | FAIL |
| 4 | -6.400 | 40.0 | 5 | FAIL |
| 5 | 19.064 | 100.0 | 4 | FAIL |

### macd_zero_scalp — EURUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.851 | 50.0 | 6 | FAIL |
| 2 | 0.404 | 55.6 | 9 | FAIL |
| 3 | 4.257 | 60.0 | 5 | FAIL |
| 4 | 1.805 | 66.7 | 6 | PASS |
| 5 | -1.225 | 60.0 | 5 | FAIL |

### volatility_breakout_scalp — BTCUSD H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.989 | 47.6 | 63 | FAIL |
| 2 | -3.305 | 43.1 | 72 | FAIL |
| 3 | -1.841 | 42.6 | 68 | FAIL |
| 4 | 0.169 | 55.7 | 61 | FAIL |
| 5 | 3.582 | 62.5 | 72 | FAIL |

### volatility_breakout_scalp — BTCUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.061 | 43.0 | 121 | FAIL |
| 2 | -1.084 | 54.5 | 145 | FAIL |
| 3 | -2.932 | 48.6 | 146 | FAIL |
| 4 | -4.273 | 42.1 | 121 | FAIL |
| 5 | -2.829 | 46.9 | 111 | FAIL |

### rsi_2 — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.808 | 61.5 | 13 | FAIL |
| 2 | -1.573 | 50.0 | 14 | FAIL |
| 3 | 1.833 | 50.0 | 14 | FAIL |
| 4 | 0.774 | 57.1 | 21 | FAIL |
| 5 | 1.600 | 55.6 | 9 | FAIL |

### rsi_2 — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.695 | 53.3 | 15 | FAIL |
| 2 | -9.600 | 33.3 | 15 | FAIL |
| 3 | 4.432 | 60.0 | 5 | FAIL |
| 4 | 3.907 | 62.5 | 8 | FAIL |
| 5 | 7.639 | 66.7 | 3 | FAIL |

### swing_pullback — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.205 | 57.7 | 26 | FAIL |
| 2 | -4.489 | 42.3 | 26 | FAIL |
| 3 | -0.234 | 57.9 | 19 | FAIL |
| 4 | -0.006 | 60.0 | 15 | FAIL |
| 5 | 5.170 | 58.8 | 34 | FAIL |

### swing_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.378 | 46.1 | 39 | FAIL |
| 2 | -2.266 | 48.8 | 41 | FAIL |
| 3 | 0.058 | 52.9 | 34 | FAIL |
| 4 | 2.061 | 48.0 | 25 | FAIL |
| 5 | 10.072 | 78.4 | 37 | PASS |

### naked_price_action — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.893 | 69.2 | 13 | PASS |
| 2 | 1.250 | 58.8 | 17 | FAIL |
| 3 | -8.276 | 41.7 | 12 | FAIL |
| 4 | -5.661 | 38.5 | 13 | FAIL |
| 5 | 8.059 | 84.6 | 13 | PASS |

### naked_price_action — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.343 | 50.0 | 12 | FAIL |
| 2 | -4.855 | 25.0 | 4 | FAIL |
| 3 | 3.736 | 60.0 | 5 | FAIL |
| 4 | 50.000 | 100.0 | 2 | FAIL |
| 5 | 5.745 | 75.0 | 4 | FAIL |

### volatility_squeeze_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.192 | 50.0 | 2 | FAIL |
| 2 | -4.405 | 50.0 | 2 | FAIL |
| 3 | -9.401 | 33.3 | 3 | FAIL |
| 4 | 1.920 | 64.3 | 14 | FAIL |
| 5 | 6.616 | 66.7 | 12 | PASS |

### volatility_squeeze_breakout — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -50.000 | 0.0 | 3 | FAIL |
| 2 | 0.000 | 0.0 | 1 | FAIL |
| 3 | 0.000 | 0.0 | 0 | FAIL |
| 4 | 0.000 | 100.0 | 1 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### triple_macd_scalping — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.449 | 48.5 | 202 | FAIL |
| 2 | -2.763 | 53.9 | 204 | FAIL |
| 3 | -1.008 | 54.8 | 208 | FAIL |
| 4 | -0.027 | 55.4 | 204 | FAIL |
| 5 | 0.734 | 52.0 | 204 | FAIL |

### triple_macd_scalping — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.588 | 40.2 | 164 | FAIL |
| 2 | -6.489 | 41.1 | 158 | FAIL |
| 3 | -4.107 | 47.7 | 151 | FAIL |
| 4 | -3.775 | 48.6 | 177 | FAIL |
| 5 | -6.554 | 42.1 | 171 | FAIL |

### supertrend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.208 | 41.7 | 12 | FAIL |
| 2 | 6.345 | 75.0 | 12 | PASS |
| 3 | -2.607 | 38.9 | 18 | FAIL |
| 4 | 5.467 | 58.3 | 12 | FAIL |
| 5 | 11.536 | 77.8 | 9 | PASS |

### supertrend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.184 | 44.4 | 9 | FAIL |
| 2 | -3.726 | 45.5 | 11 | FAIL |
| 3 | 0.725 | 62.5 | 8 | FAIL |
| 4 | 11.301 | 85.7 | 7 | PASS |
| 5 | 24.819 | 100.0 | 8 | PASS |

### ttm_squeeze — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 1.121 | 66.7 | 6 | FAIL |
| 2 | -10.246 | 44.4 | 9 | FAIL |
| 3 | -4.307 | 55.6 | 9 | FAIL |
| 4 | 12.608 | 81.8 | 11 | PASS |
| 5 | 7.011 | 78.6 | 14 | PASS |

### ttm_squeeze — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.950 | 40.0 | 5 | FAIL |
| 2 | 0.520 | 50.0 | 6 | FAIL |
| 3 | -1.453 | 50.0 | 6 | FAIL |
| 4 | 1.826 | 50.0 | 6 | FAIL |
| 5 | 3.866 | 57.1 | 7 | FAIL |

### donchian_trend — BTCUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.827 | 51.0 | 145 | FAIL |
| 2 | -2.280 | 44.9 | 178 | FAIL |
| 3 | -1.840 | 46.5 | 170 | FAIL |
| 4 | -0.721 | 54.3 | 151 | FAIL |
| 5 | -0.916 | 49.1 | 167 | FAIL |

### donchian_trend — ETHUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -7.768 | 34.9 | 149 | FAIL |
| 2 | -3.111 | 48.0 | 175 | FAIL |
| 3 | -1.878 | 51.8 | 170 | FAIL |
| 4 | -2.197 | 52.0 | 175 | FAIL |
| 5 | -1.858 | 54.8 | 168 | FAIL |
