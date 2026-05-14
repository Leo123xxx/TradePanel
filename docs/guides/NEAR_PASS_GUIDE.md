# Near-PASS Strategy Optimization Guide

The near-pass optimization suite contains focused parameter tuning scripts for strategies that are "one metric away" from PASS status (Sharpe ≥ 1.5, Win Rate ≥ 65%).

## 1. Overview
Instead of manual tweaking, this suite:
1. Generates realistic synthetic OHLCV data.
2. Runs strategies through the backtest engine.
3. Tests hundreds of parameter combinations.
4. Ranks results by a composite score (`Sharpe * 0.4 + WR * 0.6`).

## 2. Quick Start

### Windows (Batch)
```powershell
./RUN_NEAR_PASS_OPTIMIZATION.bat --quick    # 5 min validation
./RUN_NEAR_PASS_OPTIMIZATION.bat           # 15 min normal run
./RUN_NEAR_PASS_OPTIMIZATION.bat --extended # 30+ min deep search
```

### Python (Direct)
```bash
python scripts/run_near_pass_suite.py --quick
python scripts/optimize_near_pass.py --strategy hikkake_trap
```

## 3. Interpreting Results

Results are saved to `results/data/near_pass_optimization.json` and summarized in `results/reports/near_pass_report.md`.

| Status | Action |
| :--- | :--- |
| ✅ **PASS** | Meets both thresholds. Copy params to `strategies.yaml`. |
| 🟡 **PARTIAL** | One threshold met. Try `--extended` search. |
| 🔄 **WORKING** | Improvements seen but below threshold. Review logic. |

## 4. Parameter Meaning by Strategy

*   **hikkake_trap**: `cooldown_bars`, `tp_atr_mult`, `sl_atr_mult`.
*   **session_momentum**: `fast_ema`, `slow_ema`, `min_adx_filter`.
*   **range_breakout**: `consolidation_bars`, `vol_threshold_mult`.
*   **rsi_pullback**: `rsi_pullback_lower`, `rsi_pullback_upper`.

## 5. Troubleshooting
*   **NO_TRADES**: Signal logic too strict. Loosen ADX/RSI filters.
*   **Low Sharpe**: Overfitting or synthetic data mismatch. Validate on M1 data.
*   **Timeout**: Grid too large. Use `--quick` or reduce value ranges.
