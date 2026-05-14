# WFO Master Summary

**Generated:** 2026-05-12 17:55:16  
**Config:** 3 windows | IS=70% | OOS=30%  
**Criterion:** Sharpe >= 1.5, WR >= 65%, Trades >= 5(H4+)/10(Others) per window (OOS); strategy passes if >= 70% of windows pass

---

## Results Overview

| Strategy | Pair | TF | Pass Rate | Windows | Verdict |
|----------|------|----|----------:|---------|---------|
| macd_zero_scalp | GBPUSD | H1 | 33% | 1/3 | FAIL |
| macd_zero_scalp | EURUSD | H1 | 0% | 0/3 | FAIL |

---

## Summary

- **PASS:** 0 combo(s)
- **FAIL:** 2 combo(s)
- **ERRORS:** 0 combo(s)
- **Skipped:** none

---

## Per-Window Detail

### macd_zero_scalp — GBPUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | -3.215 | 35.7 | 14 | FAIL |
| 2 | -10.459 | 33.3 | 9 | FAIL |
| 3 | 6.335 | 85.7 | 7 | PASS |

### macd_zero_scalp — EURUSD H1

| Window | OOS Sharpe | OOS WR% | Trades | Status |
|-------:|-----------:|--------:|-------:|--------|
| 1 | 3.505 | 58.3 | 12 | FAIL |
| 2 | -8.459 | 23.1 | 13 | FAIL |
| 3 | 0.727 | 66.7 | 6 | FAIL |
