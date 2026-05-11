# WFO Master Summary

**Generated:** 2026-05-11 10:48:12  
**Config:** 5 windows | IS=70% | OOS=30%  
**Criterion:** Sharpe >= 1.5, WR >= 65%, Trades >= 5(H4+)/10(Others) per window (OOS); strategy passes if >= 70% of windows pass

---

## Results Overview

| Strategy | Pair | TF | Pass Rate | Windows | Verdict |
|----------|------|----|----------:|---------|---------|
| dual_ema_fractal | XAUUSD | H4 | 60% | 3/5 | FAIL |
| dual_ema_fractal | EURUSD | H4 | 20% | 1/5 | FAIL |
| rsi_pullback | XAUUSD | H4 | 60% | 3/5 | FAIL |
| rsi_pullback | EURUSD | H4 | 80% | 4/5 | PASS |
| stat_arb_gold_silver | XAUUSD | H2 | 20% | 1/5 | FAIL |
| stat_arb_gold_silver | XAUUSD | H1 | 0% | 0/5 | FAIL |
| bb_mean_reversion | XAUUSD | H4 | 0% | 0/5 | FAIL |
| bb_mean_reversion | EURUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | XAUUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | EURUSD | H4 | 0% | 0/5 | FAIL |
| macd_trend | XAUUSD | H4 | 40% | 2/5 | FAIL |
| macd_trend | EURUSD | H4 | 20% | 1/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H4 | 60% | 3/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H1 | 0% | 0/5 | FAIL |
| range_breakout | XAUUSD | H4 | 40% | 2/5 | FAIL |
| range_breakout | EURUSD | H4 | 20% | 1/5 | FAIL |
| session_momentum | XAUUSD | H4 | 40% | 2/5 | FAIL |
| session_momentum | EURUSD | H4 | 60% | 3/5 | FAIL |
| turtle_soup | XAUUSD | H4 | 20% | 1/5 | FAIL |
| turtle_soup | EURUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | XAUUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | EURUSD | H4 | 20% | 1/5 | FAIL |
| hikkake_trap | XAUUSD | H4 | 0% | 0/5 | FAIL |
| hikkake_trap | EURUSD | H4 | 0% | 0/5 | FAIL |
| orb | XAUUSD | H4 | 0% | 0/5 | FAIL |
| orb | EURUSD | H4 | 0% | 0/5 | FAIL |
| rvgi_cci_confluence | XAUUSD | H4 | 20% | 1/5 | FAIL |
| rvgi_cci_confluence | EURUSD | H4 | 20% | 1/5 | FAIL |
| fast_ma_scalper | XAUUSD | M15 | 0% | 0/5 | FAIL |
| fast_ma_scalper | GBPUSD | M15 | 0% | 0/5 | FAIL |
| bb_squeeze_scalp | XAUUSD | M15 | 0% | 0/5 | FAIL |
| bb_squeeze_scalp | GBPUSD | M15 | 0% | 0/5 | FAIL |
| rsi_extremes_scalp | XAUUSD | M15 | 0% | 0/5 | FAIL |
| rsi_extremes_scalp | GBPUSD | M15 | 0% | 0/5 | FAIL |
| macd_zero_scalp | XAUUSD | M15 | 0% | 0/5 | FAIL |
| macd_zero_scalp | GBPUSD | M15 | 0% | 0/5 | FAIL |
| volatility_breakout_scalp | XAUUSD | M15 | 0% | 0/5 | FAIL |
| volatility_breakout_scalp | GBPUSD | M15 | 0% | 0/5 | FAIL |
| rsi_2 | XAUUSD | H4 | 0% | 0/5 | FAIL |
| rsi_2 | EURUSD | H4 | 0% | 0/5 | FAIL |
| swing_pullback | XAUUSD | H4 | 0% | 0/5 | FAIL |
| swing_pullback | EURUSD | H4 | 0% | 0/5 | FAIL |
| naked_price_action | XAUUSD | H4 | 40% | 2/5 | FAIL |
| naked_price_action | EURUSD | H4 | 20% | 1/5 | FAIL |
| volatility_squeeze_breakout | XAUUSD | H4 | 40% | 2/5 | FAIL |
| volatility_squeeze_breakout | EURUSD | H4 | 0% | 0/5 | FAIL |
| triple_macd_scalping | XAUUSD | M15 | 0% | 0/5 | FAIL |
| triple_macd_scalping | GBPUSD | M15 | 0% | 0/5 | FAIL |
| supertrend | XAUUSD | H4 | 20% | 1/5 | FAIL |
| supertrend | EURUSD | H4 | 60% | 3/5 | FAIL |
| ttm_squeeze | XAUUSD | H4 | 40% | 2/5 | FAIL |
| ttm_squeeze | EURUSD | H4 | 0% | 0/5 | FAIL |
| donchian_trend | BTCUSD | H1 | 0% | 0/5 | FAIL |
| donchian_trend | ETHUSD | H1 | 0% | 0/5 | FAIL |

---

## Summary

- **PASS:** 1 combo(s)
- **FAIL:** 53 combo(s)
- **ERRORS:** 0 combo(s)
- **Skipped:** none

---

## Per-Window Detail

### dual_ema_fractal — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.484 | 42.9 | 7 | FAIL |
| 2 | -1.827 | 50.0 | 14 | FAIL |
| 3 | 7.389 | 66.7 | 9 | PASS |
| 4 | 7.845 | 66.7 | 12 | PASS |
| 5 | 10.390 | 83.3 | 6 | PASS |

### dual_ema_fractal — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 11.834 | 85.7 | 7 | PASS |
| 2 | 3.206 | 60.0 | 10 | FAIL |
| 3 | -2.482 | 52.6 | 19 | FAIL |
| 4 | -13.410 | 28.6 | 7 | FAIL |
| 5 | -18.366 | 20.0 | 5 | FAIL |

### rsi_pullback — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 6.929 | 75.0 | 12 | PASS |
| 2 | 9.748 | 80.0 | 5 | PASS |
| 3 | 0.843 | 50.0 | 8 | FAIL |
| 4 | 9.679 | 75.0 | 8 | PASS |
| 5 | -0.218 | 50.0 | 10 | FAIL |

### rsi_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 10.273 | 80.0 | 5 | PASS |
| 2 | 0.188 | 54.5 | 11 | FAIL |
| 3 | 6.508 | 66.7 | 12 | PASS |
| 4 | 4.564 | 66.7 | 6 | PASS |
| 5 | 14.085 | 83.3 | 6 | PASS |

### stat_arb_gold_silver — XAUUSD H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.611 | 47.1 | 34 | FAIL |
| 2 | 3.859 | 65.0 | 20 | PASS |
| 3 | 0.970 | 54.5 | 11 | FAIL |
| 4 | -3.882 | 40.7 | 54 | FAIL |
| 5 | 0.798 | 44.4 | 18 | FAIL |

### stat_arb_gold_silver — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.792 | 50.8 | 63 | FAIL |
| 2 | -2.973 | 44.4 | 126 | FAIL |
| 3 | 0.666 | 48.3 | 29 | FAIL |
| 4 | -0.768 | 43.3 | 60 | FAIL |
| 5 | -0.994 | 47.7 | 88 | FAIL |

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
| 1 | 0.000 | 100.0 | 1 | FAIL |
| 2 | 21.746 | 100.0 | 2 | FAIL |
| 3 | 0.000 | 100.0 | 1 | FAIL |
| 4 | 0.000 | 0.0 | 0 | FAIL |
| 5 | 0.000 | 0.0 | 0 | FAIL |

### stoch_divergence — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 0.0 | 1 | FAIL |
| 2 | 0.000 | 0.0 | 1 | FAIL |
| 3 | 28.465 | 100.0 | 4 | FAIL |
| 4 | 0.000 | 100.0 | 1 | FAIL |
| 5 | 0.000 | 100.0 | 1 | FAIL |

### macd_trend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.045 | 50.0 | 4 | FAIL |
| 2 | 6.715 | 80.0 | 5 | PASS |
| 3 | 2.185 | 50.0 | 4 | FAIL |
| 4 | -1.209 | 66.7 | 3 | FAIL |
| 5 | 17.680 | 100.0 | 6 | PASS |

### macd_trend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -29.029 | 0.0 | 2 | FAIL |
| 2 | -50.000 | 0.0 | 2 | FAIL |
| 3 | -9.595 | 42.9 | 7 | FAIL |
| 4 | -5.109 | 50.0 | 2 | FAIL |
| 5 | 12.888 | 87.5 | 8 | PASS |

### gold_momentum_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.820 | 50.0 | 12 | FAIL |
| 2 | -0.682 | 50.0 | 12 | FAIL |
| 3 | 5.687 | 66.7 | 15 | PASS |
| 4 | 13.444 | 90.0 | 10 | PASS |
| 5 | 14.507 | 90.0 | 10 | PASS |

### gold_momentum_breakout — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.509 | 52.4 | 42 | FAIL |
| 2 | -3.528 | 42.5 | 47 | FAIL |
| 3 | 1.342 | 55.6 | 45 | FAIL |
| 4 | 0.344 | 57.5 | 40 | FAIL |
| 5 | -0.272 | 50.0 | 30 | FAIL |

### range_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -7.163 | 40.0 | 5 | FAIL |
| 2 | 14.064 | 100.0 | 2 | FAIL |
| 3 | 24.152 | 100.0 | 2 | FAIL |
| 4 | 9.357 | 87.5 | 8 | PASS |
| 5 | 12.661 | 83.3 | 6 | PASS |

### range_breakout — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.109 | 38.5 | 13 | FAIL |
| 2 | -5.128 | 45.0 | 20 | FAIL |
| 3 | 3.442 | 68.8 | 16 | PASS |
| 4 | -8.637 | 40.0 | 5 | FAIL |
| 5 | 8.565 | 75.0 | 4 | FAIL |

### session_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.096 | 41.7 | 12 | FAIL |
| 2 | 1.672 | 36.8 | 19 | FAIL |
| 3 | 7.868 | 56.5 | 23 | FAIL |
| 4 | 5.110 | 66.7 | 12 | PASS |
| 5 | 11.378 | 81.8 | 11 | PASS |

### session_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.731 | 66.7 | 6 | PASS |
| 2 | -0.709 | 62.5 | 8 | FAIL |
| 3 | 11.642 | 88.9 | 9 | PASS |
| 4 | 3.691 | 60.0 | 5 | FAIL |
| 5 | 8.034 | 71.4 | 7 | PASS |

### turtle_soup — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.255 | 57.1 | 28 | FAIL |
| 2 | 1.363 | 46.7 | 30 | FAIL |
| 3 | 5.727 | 80.0 | 5 | PASS |
| 4 | -6.181 | 40.0 | 5 | FAIL |
| 5 | 0.074 | 60.0 | 5 | FAIL |

### turtle_soup — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.309 | 54.5 | 11 | FAIL |
| 2 | -1.906 | 44.4 | 9 | FAIL |
| 3 | 0.935 | 66.7 | 12 | FAIL |
| 4 | -5.971 | 41.7 | 12 | FAIL |
| 5 | -3.436 | 40.0 | 10 | FAIL |

### dual_ema_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.712 | 57.1 | 7 | FAIL |
| 2 | -4.418 | 42.9 | 7 | FAIL |
| 3 | 4.979 | 62.5 | 8 | FAIL |
| 4 | 16.545 | 100.0 | 3 | FAIL |
| 5 | 3.929 | 60.0 | 5 | FAIL |

### dual_ema_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 100.0 | 1 | FAIL |
| 2 | 43.237 | 100.0 | 4 | FAIL |
| 3 | -4.682 | 33.3 | 6 | FAIL |
| 4 | -9.994 | 22.2 | 9 | FAIL |
| 5 | 3.650 | 71.4 | 7 | PASS |

### hikkake_trap — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.633 | 55.6 | 9 | FAIL |
| 2 | 0.249 | 50.0 | 10 | FAIL |
| 3 | 5.283 | 62.5 | 16 | FAIL |
| 4 | 2.890 | 60.0 | 10 | FAIL |
| 5 | 31.823 | 100.0 | 4 | FAIL |

### hikkake_trap — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.160 | 35.7 | 14 | FAIL |
| 2 | 2.332 | 44.4 | 9 | FAIL |
| 3 | -3.460 | 28.6 | 7 | FAIL |
| 4 | -9.191 | 14.3 | 7 | FAIL |
| 5 | -5.844 | 20.0 | 5 | FAIL |

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
| 1 | -0.196 | 46.7 | 15 | FAIL |
| 2 | 5.018 | 64.7 | 17 | FAIL |
| 3 | 2.833 | 57.1 | 14 | FAIL |
| 4 | 1.026 | 56.2 | 16 | FAIL |
| 5 | 6.215 | 66.7 | 15 | PASS |

### rvgi_cci_confluence — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 7.873 | 77.8 | 9 | PASS |
| 2 | -1.415 | 57.1 | 7 | FAIL |
| 3 | 1.887 | 60.0 | 10 | FAIL |
| 4 | -0.660 | 42.9 | 14 | FAIL |
| 5 | -17.386 | 18.2 | 11 | FAIL |

### fast_ma_scalper — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.967 | 45.1 | 459 | FAIL |
| 2 | -2.284 | 50.0 | 476 | FAIL |
| 3 | -2.582 | 49.9 | 429 | FAIL |
| 4 | -2.044 | 46.1 | 438 | FAIL |
| 5 | -2.323 | 43.2 | 458 | FAIL |

### fast_ma_scalper — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.951 | 44.2 | 317 | FAIL |
| 2 | -5.419 | 42.2 | 303 | FAIL |
| 3 | -4.920 | 44.9 | 330 | FAIL |
| 4 | -5.138 | 43.8 | 329 | FAIL |
| 5 | -4.955 | 44.7 | 309 | FAIL |

### bb_squeeze_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.719 | 40.0 | 5 | FAIL |
| 2 | -2.971 | 50.0 | 4 | FAIL |
| 3 | 0.000 | 100.0 | 1 | FAIL |
| 4 | 50.000 | 100.0 | 2 | FAIL |
| 5 | 6.089 | 50.0 | 2 | FAIL |

### bb_squeeze_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 1.878 | 50.0 | 2 | FAIL |
| 2 | -3.620 | 50.0 | 2 | FAIL |
| 3 | -2.323 | 66.7 | 3 | FAIL |
| 4 | -1.251 | 50.0 | 2 | FAIL |
| 5 | -3.643 | 50.0 | 2 | FAIL |

### rsi_extremes_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.936 | 45.5 | 11 | FAIL |
| 2 | -6.480 | 45.5 | 11 | FAIL |
| 3 | 0.715 | 64.3 | 14 | FAIL |
| 4 | -2.716 | 46.1 | 13 | FAIL |
| 5 | -10.254 | 25.0 | 12 | FAIL |

### rsi_extremes_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -11.162 | 30.8 | 13 | FAIL |
| 2 | -5.178 | 40.0 | 20 | FAIL |
| 3 | -11.702 | 30.0 | 10 | FAIL |
| 4 | 5.247 | 66.7 | 6 | FAIL |
| 5 | -16.908 | 33.3 | 6 | FAIL |

### macd_zero_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.623 | 42.2 | 313 | FAIL |
| 2 | -3.427 | 48.5 | 311 | FAIL |
| 3 | -2.695 | 45.0 | 320 | FAIL |
| 4 | -2.526 | 46.4 | 293 | FAIL |
| 5 | -2.273 | 46.0 | 328 | FAIL |

### macd_zero_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.011 | 40.4 | 332 | FAIL |
| 2 | -6.652 | 38.5 | 299 | FAIL |
| 3 | -3.756 | 45.9 | 279 | FAIL |
| 4 | -3.402 | 49.2 | 309 | FAIL |
| 5 | -5.043 | 45.3 | 309 | FAIL |

### volatility_breakout_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.054 | 43.3 | 1614 | FAIL |
| 2 | -3.103 | 46.3 | 1455 | FAIL |
| 3 | -2.043 | 47.8 | 1289 | FAIL |
| 4 | -2.112 | 45.8 | 1134 | FAIL |
| 5 | -1.791 | 44.4 | 1094 | FAIL |

### volatility_breakout_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.688 | 39.7 | 1606 | FAIL |
| 2 | -5.264 | 42.1 | 1509 | FAIL |
| 3 | -4.103 | 46.8 | 1281 | FAIL |
| 4 | -3.866 | 46.7 | 1373 | FAIL |
| 5 | -4.603 | 45.9 | 1430 | FAIL |

### rsi_2 — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.808 | 61.5 | 13 | FAIL |
| 2 | -2.564 | 46.7 | 15 | FAIL |
| 3 | 1.833 | 50.0 | 14 | FAIL |
| 4 | -0.595 | 55.0 | 20 | FAIL |
| 5 | 2.963 | 57.1 | 7 | FAIL |

### rsi_2 — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 4.951 | 58.8 | 17 | FAIL |
| 2 | -9.600 | 33.3 | 15 | FAIL |
| 3 | 4.432 | 60.0 | 5 | FAIL |
| 4 | 3.907 | 62.5 | 8 | FAIL |
| 5 | 50.000 | 100.0 | 2 | FAIL |

### swing_pullback — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.787 | 53.6 | 69 | FAIL |
| 2 | -3.006 | 45.9 | 61 | FAIL |
| 3 | -1.596 | 47.6 | 82 | FAIL |
| 4 | -1.907 | 46.0 | 111 | FAIL |
| 5 | 2.364 | 57.5 | 106 | FAIL |

### swing_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 1.070 | 56.1 | 66 | FAIL |
| 2 | -0.275 | 49.3 | 71 | FAIL |
| 3 | -0.179 | 49.5 | 95 | FAIL |
| 4 | -2.829 | 40.6 | 69 | FAIL |
| 5 | 1.822 | 58.9 | 185 | FAIL |

### naked_price_action — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.892 | 69.2 | 13 | PASS |
| 2 | 0.504 | 58.8 | 17 | FAIL |
| 3 | -8.519 | 41.7 | 12 | FAIL |
| 4 | -5.661 | 38.5 | 13 | FAIL |
| 5 | 8.059 | 84.6 | 13 | PASS |

### naked_price_action — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.343 | 50.0 | 12 | FAIL |
| 2 | -4.855 | 25.0 | 4 | FAIL |
| 3 | 3.736 | 60.0 | 5 | FAIL |
| 4 | 10.512 | 80.0 | 5 | PASS |
| 5 | 5.745 | 75.0 | 4 | FAIL |

### volatility_squeeze_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.192 | 50.0 | 2 | FAIL |
| 2 | -4.405 | 50.0 | 2 | FAIL |
| 3 | -9.401 | 33.3 | 3 | FAIL |
| 4 | 5.140 | 71.4 | 14 | PASS |
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
| 1 | -4.563 | 47.8 | 201 | FAIL |
| 2 | -2.987 | 53.4 | 206 | FAIL |
| 3 | -1.003 | 54.6 | 207 | FAIL |
| 4 | 0.183 | 55.9 | 202 | FAIL |
| 5 | 0.956 | 52.9 | 204 | FAIL |

### triple_macd_scalping — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.752 | 40.2 | 164 | FAIL |
| 2 | -6.408 | 41.5 | 159 | FAIL |
| 3 | -4.056 | 47.4 | 152 | FAIL |
| 4 | -3.586 | 49.2 | 179 | FAIL |
| 5 | -6.417 | 42.5 | 167 | FAIL |

### supertrend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.208 | 41.7 | 12 | FAIL |
| 2 | 3.909 | 64.3 | 14 | FAIL |
| 3 | -1.559 | 44.4 | 18 | FAIL |
| 4 | 5.472 | 58.3 | 12 | FAIL |
| 5 | 13.198 | 87.5 | 8 | PASS |

### supertrend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.187 | 50.0 | 8 | FAIL |
| 2 | -2.877 | 50.0 | 10 | FAIL |
| 3 | 1.944 | 71.4 | 7 | PASS |
| 4 | 11.301 | 85.7 | 7 | PASS |
| 5 | 26.208 | 100.0 | 8 | PASS |

### ttm_squeeze — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.224 | 52.2 | 23 | FAIL |
| 2 | -3.156 | 52.0 | 25 | FAIL |
| 3 | 5.350 | 69.0 | 29 | PASS |
| 4 | 6.253 | 65.0 | 20 | PASS |
| 5 | 4.396 | 64.0 | 25 | FAIL |

### ttm_squeeze — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.445 | 45.5 | 11 | FAIL |
| 2 | -3.962 | 43.8 | 16 | FAIL |
| 3 | -3.206 | 38.1 | 21 | FAIL |
| 4 | -2.472 | 36.8 | 19 | FAIL |
| 5 | 0.883 | 50.0 | 16 | FAIL |

### donchian_trend — BTCUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.672 | 50.0 | 162 | FAIL |
| 2 | -1.681 | 46.0 | 198 | FAIL |
| 3 | -1.665 | 46.2 | 197 | FAIL |
| 4 | -0.723 | 52.7 | 167 | FAIL |
| 5 | -0.818 | 49.0 | 198 | FAIL |

### donchian_trend — ETHUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -7.095 | 37.0 | 165 | FAIL |
| 2 | -2.215 | 51.5 | 196 | FAIL |
| 3 | -1.338 | 54.3 | 199 | FAIL |
| 4 | -1.665 | 54.1 | 183 | FAIL |
| 5 | -2.199 | 53.1 | 192 | FAIL |
