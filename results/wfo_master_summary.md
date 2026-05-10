# WFO Master Summary

**Generated:** 2026-05-10 06:51:22  
**Config:** 5 windows | IS=70% | OOS=30%  
**Criterion:** Sharpe >= 1.5, WR >= 65%, Trades >= 5(H4+)/10(Others) per window (OOS); strategy passes if >= 70% of windows pass

---

## Results Overview

| Strategy | Pair | TF | Pass Rate | Windows | Verdict |
|----------|------|----|----------:|---------|---------|
| dual_ema_fractal | XAUUSD | H4 | 20% | 3/5 | FAIL |
| dual_ema_fractal | EURUSD | H4 | 0% | 1/5 | FAIL |
| rsi_pullback | XAUUSD | H4 | 20% | 3/5 | FAIL |
| rsi_pullback | EURUSD | H4 | 20% | 4/5 | FAIL |
| stat_arb_gold_silver | XAUUSD | H2 | 40% | 2/5 | FAIL |
| stat_arb_gold_silver | XAUUSD | H1 | 0% | 0/5 | FAIL |
| bb_mean_reversion | XAUUSD | H4 | 0% | 0/5 | FAIL |
| bb_mean_reversion | EURUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | XAUUSD | H4 | 0% | 0/5 | FAIL |
| stoch_divergence | EURUSD | H4 | 0% | 0/5 | FAIL |
| macd_trend | XAUUSD | H4 | 0% | 2/5 | FAIL |
| macd_trend | EURUSD | H4 | 0% | 1/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H4 | 60% | 3/5 | FAIL |
| gold_momentum_breakout | XAUUSD | H1 | 0% | 0/5 | FAIL |
| range_breakout | XAUUSD | H4 | 0% | 2/5 | FAIL |
| range_breakout | EURUSD | H4 | 20% | 1/5 | FAIL |
| session_momentum | XAUUSD | H4 | 40% | 2/5 | FAIL |
| session_momentum | EURUSD | H4 | 0% | 3/5 | FAIL |
| turtle_soup | XAUUSD | H4 | 0% | 0/5 | FAIL |
| turtle_soup | EURUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | XAUUSD | H4 | 0% | 0/5 | FAIL |
| dual_ema_momentum | EURUSD | H4 | 0% | 1/5 | FAIL |
| hikkake_trap | XAUUSD | H4 | 0% | 0/5 | FAIL |
| hikkake_trap | EURUSD | H4 | 0% | 0/5 | FAIL |
| orb | XAUUSD | H4 | 0% | 0/5 | FAIL |
| orb | EURUSD | H4 | 0% | 0/5 | FAIL |
| rvgi_cci_confluence | XAUUSD | H4 | 20% | 1/5 | FAIL |
| rvgi_cci_confluence | EURUSD | H4 | 0% | 1/5 | FAIL |
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
| naked_price_action | EURUSD | H4 | 0% | 0/5 | FAIL |
| volatility_squeeze_breakout | XAUUSD | H4 | 40% | 2/5 | FAIL |
| volatility_squeeze_breakout | EURUSD | H4 | 0% | 0/5 | FAIL |
| triple_macd_scalping | XAUUSD | M15 | 0% | 0/5 | FAIL |
| triple_macd_scalping | GBPUSD | M15 | 0% | 0/5 | FAIL |
| supertrend | XAUUSD | H4 | 20% | 2/5 | FAIL |
| supertrend | EURUSD | H4 | 0% | 2/5 | FAIL |
| ttm_squeeze | XAUUSD | H4 | 40% | 2/5 | FAIL |
| ttm_squeeze | EURUSD | H4 | 0% | 0/5 | FAIL |
| donchian_trend | BTCUSD | H1 | 0% | 0/5 | FAIL |
| donchian_trend | ETHUSD | H1 | 0% | 0/5 | FAIL |

---

## Summary

- **PASS:** 0 combo(s)
- **FAIL:** 54 combo(s)
- **ERRORS:** 0 combo(s)
- **Skipped:** rsi_pullback_legacy

---

## Per-Window Detail

### dual_ema_fractal — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.466 | 42.9 | 7 | FAIL |
| 2 | -1.827 | 50.0 | 14 | FAIL |
| 3 | 7.389 | 66.7 | 9 | PASS |
| 4 | 7.836 | 66.7 | 12 | PASS |
| 5 | 10.390 | 83.3 | 6 | PASS |

### dual_ema_fractal — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 11.834 | 85.7 | 7 | PASS |
| 2 | 3.205 | 60.0 | 10 | FAIL |
| 3 | -2.482 | 52.6 | 19 | FAIL |
| 4 | -13.407 | 28.6 | 7 | FAIL |
| 5 | -18.366 | 20.0 | 5 | FAIL |

### rsi_pullback — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 6.901 | 75.0 | 12 | PASS |
| 2 | 9.748 | 80.0 | 5 | PASS |
| 3 | 0.843 | 50.0 | 8 | FAIL |
| 4 | 9.679 | 75.0 | 8 | PASS |
| 5 | 0.477 | 60.0 | 10 | FAIL |

### rsi_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.139 | 66.7 | 6 | PASS |
| 2 | 0.188 | 54.5 | 11 | FAIL |
| 3 | 6.516 | 66.7 | 12 | PASS |
| 4 | 4.556 | 66.7 | 6 | PASS |
| 5 | 14.085 | 83.3 | 6 | PASS |

### stat_arb_gold_silver — XAUUSD H2

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.611 | 47.1 | 34 | FAIL |
| 2 | 3.859 | 65.0 | 20 | PASS |
| 3 | 0.970 | 54.5 | 11 | FAIL |
| 4 | -3.881 | 40.7 | 54 | FAIL |
| 5 | 13.662 | 100.0 | 12 | PASS |

### stat_arb_gold_silver — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.792 | 50.8 | 63 | FAIL |
| 2 | -3.056 | 43.9 | 123 | FAIL |
| 3 | 0.666 | 48.3 | 29 | FAIL |
| 4 | -1.948 | 31.2 | 32 | FAIL |
| 5 | -0.612 | 48.9 | 88 | FAIL |

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
| 2 | 9.181 | 83.3 | 6 | PASS |
| 3 | 2.185 | 50.0 | 4 | FAIL |
| 4 | -1.209 | 66.7 | 3 | FAIL |
| 5 | 17.680 | 100.0 | 6 | PASS |

### macd_trend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -29.029 | 0.0 | 2 | FAIL |
| 2 | -50.000 | 0.0 | 2 | FAIL |
| 3 | -7.930 | 50.0 | 8 | FAIL |
| 4 | -5.109 | 50.0 | 2 | FAIL |
| 5 | 12.572 | 85.7 | 7 | PASS |

### gold_momentum_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.820 | 50.0 | 12 | FAIL |
| 2 | -0.682 | 50.0 | 12 | FAIL |
| 3 | 5.821 | 66.7 | 15 | PASS |
| 4 | 13.390 | 90.0 | 10 | PASS |
| 5 | 14.507 | 90.0 | 10 | PASS |

### gold_momentum_breakout — XAUUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.509 | 52.4 | 42 | FAIL |
| 2 | -3.190 | 43.5 | 46 | FAIL |
| 3 | 1.346 | 55.6 | 45 | FAIL |
| 4 | 0.221 | 56.4 | 39 | FAIL |
| 5 | -0.272 | 50.0 | 30 | FAIL |

### range_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.824 | 40.0 | 5 | FAIL |
| 2 | 14.064 | 100.0 | 2 | FAIL |
| 3 | 24.152 | 100.0 | 2 | FAIL |
| 4 | 9.325 | 87.5 | 8 | PASS |
| 5 | 12.661 | 83.3 | 6 | PASS |

### range_breakout — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.109 | 38.5 | 13 | FAIL |
| 2 | -5.108 | 45.0 | 20 | FAIL |
| 3 | 3.117 | 70.6 | 17 | PASS |
| 4 | -8.637 | 40.0 | 5 | FAIL |
| 5 | 8.565 | 75.0 | 4 | FAIL |

### session_momentum — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.206 | 41.7 | 12 | FAIL |
| 2 | 1.672 | 36.8 | 19 | FAIL |
| 3 | 6.987 | 54.5 | 22 | FAIL |
| 4 | 5.086 | 66.7 | 12 | PASS |
| 5 | 11.378 | 81.8 | 11 | PASS |

### session_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.729 | 66.7 | 6 | PASS |
| 2 | -0.709 | 62.5 | 8 | FAIL |
| 3 | 11.642 | 88.9 | 9 | PASS |
| 4 | 3.691 | 60.0 | 5 | FAIL |
| 5 | 8.034 | 71.4 | 7 | PASS |

### turtle_soup — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 2.255 | 57.1 | 28 | FAIL |
| 2 | 1.046 | 44.8 | 29 | FAIL |
| 3 | 2.722 | 58.6 | 29 | FAIL |
| 4 | -6.181 | 40.0 | 5 | FAIL |
| 5 | 0.073 | 60.0 | 5 | FAIL |

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
| 2 | -6.481 | 37.5 | 8 | FAIL |
| 3 | 4.979 | 62.5 | 8 | FAIL |
| 4 | 16.545 | 100.0 | 3 | FAIL |
| 5 | 3.929 | 60.0 | 5 | FAIL |

### dual_ema_momentum — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.000 | 100.0 | 1 | FAIL |
| 2 | 43.233 | 100.0 | 4 | FAIL |
| 3 | -4.682 | 33.3 | 6 | FAIL |
| 4 | -9.977 | 22.2 | 9 | FAIL |
| 5 | 3.650 | 71.4 | 7 | PASS |

### hikkake_trap — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -1.630 | 55.6 | 9 | FAIL |
| 2 | 0.249 | 50.0 | 10 | FAIL |
| 3 | 5.283 | 62.5 | 16 | FAIL |
| 4 | 1.280 | 50.0 | 10 | FAIL |
| 5 | 31.823 | 100.0 | 4 | FAIL |

### hikkake_trap — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.153 | 35.7 | 14 | FAIL |
| 2 | 2.332 | 44.4 | 9 | FAIL |
| 3 | -3.460 | 28.6 | 7 | FAIL |
| 4 | -9.191 | 14.3 | 7 | FAIL |
| 5 | -5.848 | 20.0 | 5 | FAIL |

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
| 1 | -0.126 | 46.7 | 15 | FAIL |
| 2 | 4.828 | 62.5 | 16 | FAIL |
| 3 | 2.825 | 57.1 | 14 | FAIL |
| 4 | 1.026 | 56.2 | 16 | FAIL |
| 5 | 6.215 | 66.7 | 15 | PASS |

### rvgi_cci_confluence — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 7.872 | 77.8 | 9 | PASS |
| 2 | -1.416 | 57.1 | 7 | FAIL |
| 3 | 0.846 | 54.5 | 11 | FAIL |
| 4 | -0.661 | 42.9 | 14 | FAIL |
| 5 | -17.386 | 18.2 | 11 | FAIL |

### fast_ma_scalper — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.993 | 45.0 | 460 | FAIL |
| 2 | -2.288 | 49.9 | 473 | FAIL |
| 3 | -2.481 | 50.4 | 427 | FAIL |
| 4 | -2.061 | 46.0 | 439 | FAIL |
| 5 | -2.309 | 43.0 | 460 | FAIL |

### fast_ma_scalper — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.879 | 44.5 | 317 | FAIL |
| 2 | -5.564 | 42.0 | 302 | FAIL |
| 3 | -4.881 | 45.0 | 329 | FAIL |
| 4 | -5.089 | 44.0 | 327 | FAIL |
| 5 | -4.885 | 45.0 | 311 | FAIL |

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
| 1 | -4.587 | 42.4 | 314 | FAIL |
| 2 | -3.470 | 48.2 | 311 | FAIL |
| 3 | -2.710 | 45.1 | 319 | FAIL |
| 4 | -2.556 | 46.3 | 294 | FAIL |
| 5 | -2.274 | 46.1 | 330 | FAIL |

### macd_zero_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.899 | 40.6 | 330 | FAIL |
| 2 | -6.652 | 38.5 | 299 | FAIL |
| 3 | -3.652 | 46.0 | 276 | FAIL |
| 4 | -3.358 | 49.4 | 308 | FAIL |
| 5 | -5.043 | 45.3 | 309 | FAIL |

### volatility_breakout_scalp — XAUUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.111 | 43.2 | 1612 | FAIL |
| 2 | -3.103 | 46.3 | 1455 | FAIL |
| 3 | -1.977 | 47.9 | 1287 | FAIL |
| 4 | -2.066 | 46.0 | 1138 | FAIL |
| 5 | -1.789 | 44.5 | 1095 | FAIL |

### volatility_breakout_scalp — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.728 | 39.6 | 1608 | FAIL |
| 2 | -5.269 | 42.1 | 1506 | FAIL |
| 3 | -4.121 | 46.7 | 1271 | FAIL |
| 4 | -3.850 | 46.7 | 1372 | FAIL |
| 5 | -4.608 | 45.9 | 1438 | FAIL |

### rsi_2 — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 0.808 | 61.5 | 13 | FAIL |
| 2 | -2.564 | 46.7 | 15 | FAIL |
| 3 | 1.833 | 50.0 | 14 | FAIL |
| 4 | -1.479 | 50.0 | 20 | FAIL |
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
| 1 | 0.776 | 53.6 | 69 | FAIL |
| 2 | -3.204 | 44.3 | 61 | FAIL |
| 3 | -1.304 | 47.4 | 78 | FAIL |
| 4 | -1.903 | 46.0 | 111 | FAIL |
| 5 | 2.323 | 57.5 | 106 | FAIL |

### swing_pullback — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 1.293 | 56.1 | 66 | FAIL |
| 2 | -0.408 | 47.9 | 71 | FAIL |
| 3 | -0.175 | 49.5 | 95 | FAIL |
| 4 | -2.823 | 40.6 | 69 | FAIL |
| 5 | 1.866 | 58.9 | 185 | FAIL |

### naked_price_action — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.894 | 69.2 | 13 | PASS |
| 2 | -0.795 | 52.9 | 17 | FAIL |
| 3 | -7.067 | 45.5 | 11 | FAIL |
| 4 | -5.661 | 38.5 | 13 | FAIL |
| 5 | 8.059 | 84.6 | 13 | PASS |

### naked_price_action — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.343 | 50.0 | 12 | FAIL |
| 2 | -2.898 | 40.0 | 5 | FAIL |
| 3 | 3.736 | 60.0 | 5 | FAIL |
| 4 | 50.000 | 100.0 | 2 | FAIL |
| 5 | 5.745 | 75.0 | 4 | FAIL |

### volatility_squeeze_breakout — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.191 | 50.0 | 2 | FAIL |
| 2 | -4.405 | 50.0 | 2 | FAIL |
| 3 | -9.401 | 33.3 | 3 | FAIL |
| 4 | 5.098 | 71.4 | 14 | PASS |
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
| 1 | -4.380 | 48.3 | 201 | FAIL |
| 2 | -2.965 | 53.4 | 206 | FAIL |
| 3 | -1.131 | 54.4 | 206 | FAIL |
| 4 | 0.175 | 55.9 | 202 | FAIL |
| 5 | 0.975 | 53.2 | 203 | FAIL |

### triple_macd_scalping — GBPUSD M15

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -6.838 | 39.9 | 163 | FAIL |
| 2 | -6.471 | 41.1 | 158 | FAIL |
| 3 | -4.120 | 47.0 | 151 | FAIL |
| 4 | -3.486 | 49.4 | 180 | FAIL |
| 5 | -6.351 | 42.9 | 168 | FAIL |

### supertrend — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.208 | 41.7 | 12 | FAIL |
| 2 | 5.561 | 66.7 | 12 | PASS |
| 3 | -2.508 | 38.9 | 18 | FAIL |
| 4 | 5.472 | 58.3 | 12 | FAIL |
| 5 | 13.165 | 87.5 | 8 | PASS |

### supertrend — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -0.210 | 50.0 | 8 | FAIL |
| 2 | -2.871 | 50.0 | 10 | FAIL |
| 3 | -1.492 | 57.1 | 7 | FAIL |
| 4 | 11.301 | 85.7 | 7 | PASS |
| 5 | 23.153 | 100.0 | 8 | PASS |

### ttm_squeeze — XAUUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -5.224 | 52.2 | 23 | FAIL |
| 2 | -3.659 | 50.0 | 26 | FAIL |
| 3 | 5.351 | 69.0 | 29 | PASS |
| 4 | 6.253 | 65.0 | 20 | PASS |
| 5 | 4.398 | 64.0 | 25 | FAIL |

### ttm_squeeze — EURUSD H4

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -4.445 | 45.5 | 11 | FAIL |
| 2 | -3.962 | 43.8 | 16 | FAIL |
| 3 | -3.466 | 38.1 | 21 | FAIL |
| 4 | -2.472 | 36.8 | 19 | FAIL |
| 5 | 1.197 | 56.2 | 16 | FAIL |

### donchian_trend — BTCUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -2.524 | 50.6 | 160 | FAIL |
| 2 | -1.695 | 46.0 | 198 | FAIL |
| 3 | -1.532 | 46.7 | 197 | FAIL |
| 4 | -0.929 | 52.1 | 167 | FAIL |
| 5 | -0.742 | 49.5 | 196 | FAIL |

### donchian_trend — ETHUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -7.039 | 37.0 | 165 | FAIL |
| 2 | -2.158 | 51.5 | 196 | FAIL |
| 3 | -1.409 | 54.0 | 200 | FAIL |
| 4 | -1.659 | 54.4 | 184 | FAIL |
| 5 | -2.231 | 53.4 | 191 | FAIL |
