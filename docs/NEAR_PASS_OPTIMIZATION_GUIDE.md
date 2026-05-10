# Near-PASS Strategy Optimization Guide

**Created:** 2026-05-10  
**Purpose:** Instructions for using the near-pass optimization suite  

---

## Overview

The near-pass optimization suite contains focused parameter tuning scripts for **8 strategy combinations** that are one metric away from PASS status (Sharpe ≥ 1.5, Win Rate ≥ 65%).

### The 8 Near-PASS Candidates

| Priority | Strategy | Pair | TF | Gap | Fix |
|----------|----------|------|-----|-----|-----|
| 1 | `hikkake_trap` | GBPUSD | H4 | +2pp WR | Cooldown/TP/SL tuning |
| 2 | `session_momentum` | XAUUSD | H1 | +24.4pp WR | Entry filter tightening |
| 3 | `session_momentum` | GBPJPY | H1 | +22.9pp WR | Same as above |
| 4 | `range_breakout` | US500 | H4 | +0.32 S + 6.1pp WR | Consolidation/ADX tuning |
| 5 | `dual_ema_momentum` | XAUUSD | H1 | +0.34 S + 8.1pp WR | ADX filter + EMA ranges |
| 6 | `rsi_pullback` | GBPJPY | H4 | Validation (80% WR) | Extend data sample |
| 7 | `rsi_extremes_scalp` | USOIL | M15 | Validation (75% WR) | Extend data sample |
| 8 | `ema_ribbon_trend` | NVDA | H4 | Data extension | Get 20+ trades minimum |

---

## Quick Start

### Option 1: Batch File (Easiest for Windows)

```bash
# Normal run (recommended first attempt)
./RUN_NEAR_PASS_OPTIMIZATION.bat

# Quick validation (fewer combinations, ~5 min)
./RUN_NEAR_PASS_OPTIMIZATION.bat --quick

# Extended search (more aggressive, ~30+ min)
./RUN_NEAR_PASS_OPTIMIZATION.bat --extended
```

### Option 2: PowerShell

```powershell
# Normal run
.\RUN_NEAR_PASS_OPTIMIZATION.ps1

# Quick run
.\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Quick

# Extended run
.\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Extended

# Specific strategy only
.\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Strategy session_momentum
```

### Option 3: Direct Python

```bash
# Full suite
python scripts/run_near_pass_suite.py

# Quick run
python scripts/run_near_pass_suite.py --quick

# Single strategy
python scripts/optimize_near_pass.py --strategy hikkake_trap

# Multiple strategies
python scripts/optimize_near_pass.py --strategy session_momentum range_breakout
```

---

## Understanding the Results

### Output Files

After running, two files will be created in `results/optimization/`:

#### 1. **near_pass_optimization.json** (Raw Data)
```json
{
  "hikkake_trap": {
    "status": "OK",
    "total_combos": 384,
    "top_5": [
      {
        "params": {
          "cooldown_bars": 4,
          "tp_atr_mult": 2.0,
          "sl_atr_mult": 0.8,
          "atr_period": 14
        },
        "metrics": {
          "sharpe": 2.15,
          "win_rate": 71.2,
          "profit_factor": 1.42,
          "max_dd": 3.2,
          "trades": 125,
          "pnl_zar": 5420.50
        },
        "pair": "GBPUSD",
        "tf": "H4",
        "score": 0.946
      },
      ...
    ]
  },
  ...
}
```

#### 2. **near_pass_report.md** (Summary Report)
- Overview table with best Sharpe/WR per strategy
- Detailed results for each strategy's top 5 parameter sets
- Status indicators (✅ PASS, 🟡 PARTIAL, 🔄 WORKING)
- Recommendations for next steps

### Interpreting the Metrics

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| **Sharpe** | ≥ 1.5 | Risk-adjusted returns (higher = better) |
| **Win Rate** | ≥ 65% | Percentage of profitable trades |
| **Profit Factor** | ≥ 1.0 | Gross profit / Gross loss ratio |
| **Max Drawdown** | < 20% | Largest peak-to-trough decline |
| **Trades** | ≥ 10 | Minimum sample size for reliability |
| **Score** | 0.0–1.0 | Composite metric (Sharpe × 0.4 + WR × 0.6) |

### Status Indicators

- ✅ **PASS** — Strategy meets both Sharpe (≥1.5) and WR (≥65%) thresholds
- 🟡 **PARTIAL** — One threshold met, working on the other
- 🔄 **WORKING** — Both metrics below threshold but showing improvement
- ❌ **NO_RESULTS** — No valid parameter combinations found

---

## What to Do After Running

### If Strategy Shows ✅ PASS

1. **Copy the top parameter set**
   ```yaml
   # Example: hikkake_trap shows PASS with these params:
   cooldown_bars: 4
   tp_atr_mult: 2.0
   sl_atr_mult: 0.8
   atr_period: 14
   ```

2. **Update config/strategies.yaml**
   ```yaml
   hikkake_trap:
     enabled: true
     pairs: [GBPUSD]
     timeframes: [H4]
     params:
       cooldown_bars: 4        # NEW VALUE
       tp_atr_mult: 2.0        # NEW VALUE
       sl_atr_mult: 0.8        # NEW VALUE
       atr_period: 14
   ```

3. **Run backtest to validate**
   ```bash
   python scripts/run_backtest.py --strategy hikkake_trap
   ```

4. **If confirmed, update overnight automation**
   - Results will be tracked in `results/demotion_tracker.json`
   - Strategy will be monitored for consecutive failures

### If Strategy Shows 🟡 PARTIAL

1. **Review the gap**
   - Does it need +0.2 Sharpe? Focus on risk metrics (tp_atr_mult, sl_atr_mult)
   - Does it need +5pp WR? Focus on entry filters (ADX min, RSI thresholds)

2. **Run extended search**
   ```bash
   python scripts/run_near_pass_suite.py --extended
   ```

3. **Compare top parameter sets**
   - Look for patterns in successful parameters
   - Test edge values (e.g., if top result is cooldown_bars=4, test 3-5)

### If Strategy Shows 🔄 WORKING

1. **Extended optimization needed**
   ```bash
   python scripts/optimize_near_pass.py --strategy session_momentum --extended
   ```

2. **Consider hybrid approaches**
   - Combine best parameters from different pairs
   - Test on longer backtest windows

3. **Check for data quality issues**
   - Some strategies may have timezone alignment problems
   - Verify in `data/ingestion.py` that SAST → UTC conversion is correct

---

## Advanced Usage

### Testing Single Strategy with Custom Pair

```bash
python scripts/optimize_near_pass.py --strategy dual_ema_momentum --pair XAGUSD
```

### Running Multiple Strategies in Parallel

```bash
# In separate terminal windows:
python scripts/optimize_near_pass.py --strategy hikkake_trap
python scripts/optimize_near_pass.py --strategy session_momentum
python scripts/optimize_near_pass.py --strategy range_breakout
```

### Extracting Raw Data Programmatically

```python
import json
from pathlib import Path

opt_file = Path("results/optimization/near_pass_optimization.json")
with open(opt_file) as f:
    data = json.load(f)

# Get best hikkake_trap result
best_hikkake = data["hikkake_trap"]["top_5"][0]
print(f"Best Sharpe: {best_hikkake['metrics']['sharpe']}")
print(f"Best WR: {best_hikkake['metrics']['win_rate']}")
print(f"Parameters: {best_hikkake['params']}")
```

---

## Troubleshooting

### "NO_TRADES" Status

**Cause:** Strategy generated no trades in backtests  
**Fix:**
1. Loosen entry filters (reduce ADX min, RSI thresholds)
2. Extend backtest window in param grid
3. Check data alignment (UTC vs SAST)

### Very Low Sharpe on Scalpers

**Cause:** M15+ scalpers running on synthetic data vs real M1 data  
**Fix:**
1. Ensure timeframe in `config/strategies.yaml` is M5 or higher
2. Test on actual MT5 data instead of synthetic OHLCV

### Winning Parameters Don't Transfer to Live

**Cause:** Potential overfitting on synthetic data  
**Fix:**
1. Validate with extended backtest window (2+ years of data)
2. Run walk-forward validation (WFO) separately
3. Monitor first 50 trades in paper mode before live

### Optimization Takes Too Long

**Cause:** Large parameter grids (exponential combinations)  
**Fix:**
1. Use `--quick` flag to sample fewer combinations
2. Focus on 2-3 key parameters instead of all
3. Reduce value ranges (e.g., `[20, 25, 28]` instead of `[15, 20, 25, 28, 30]`)

---

## Expected Outcomes

### Tier 1 Outcome (Best Case)
- 3+ strategies achieve ✅ PASS status
- Parameters are statistically robust across 100+ trades
- Ready for live/paper deployment immediately

### Tier 2 Outcome (Good Case)
- 5+ strategies show 🟡 PARTIAL progress
- Combined improvements move 2-3 to PASS after extended tuning
- Weekly optimization cycles to refine parameters

### Tier 3 Outcome (Baseline)
- Data quality validation reveals issues
- Strategies work on synthetic data but fail on real data
- Points to data alignment or signal logic bugs

---

## Integration with Daily Workflow

### After Successful PASS Promotion

```bash
# 1. Update config/strategies.yaml with new parameters
# 2. Run backtest validation
python scripts/run_backtest.py

# 3. Monitor results for 1 week
# 4. If stable, include in live trading

# 5. Track performance in demotion_tracker.json
# 6. Monthly review to optimize further
```

### Weekly Optimization Schedule

```
Monday:    Run near-pass suite (--quick flag for speed)
Tuesday:   Review results, update strategies.yaml
Wednesday: Full backtest run with new parameters
Thursday:  Monitor overnight backtest results
Friday:    Generate weekly summary, plan next week
```

---

## Reference: Parameter Meaning by Strategy

### hikkake_trap
- `cooldown_bars` — Bars to wait after false breakout before next entry (4-8 typical)
- `tp_atr_mult` — Take profit = entry ± (ATR × tp_atr_mult)
- `sl_atr_mult` — Stop loss = entry ± (ATR × sl_atr_mult)

### session_momentum
- `fast_ema` — Fast moving average period (8-20)
- `slow_ema` — Slow moving average period (34-50)
- `min_adx_filter` — Minimum ADX for trend confirmation (25-32 recommended for higher WR)
- `vol_threshold_mult` — Volume spike multiplier (1.0-1.5)

### range_breakout
- `consolidation_bars` — Bars forming range (10-25)
- `vol_threshold_mult` — Volume surge multiplier (1.2-1.8)
- `adx_min_filter` — Minimum ADX for breakout confirmation (15-28)

### dual_ema_momentum
- `fast_ema` — Fast EMA period (8-30)
- `slow_ema` — Slow EMA period (50-200)
- `adx_min` — Minimum ADX for trend bias (20-30)

### rsi_pullback
- `rsi_pullback_lower` — RSI lower threshold for pullback (30-40)
- `rsi_pullback_upper` — RSI upper threshold for trend (50-60)
- `fast_ema` / `slow_ema` — Trend context filters

### rsi_extremes_scalp
- `oversold` — RSI level for low (20-30)
- `overbought` — RSI level for high (70-80)
- `rsi_period` — RSI calculation period (7-14)

---

## Next Steps

1. **Run the suite** → `RUN_NEAR_PASS_OPTIMIZATION.bat` or PowerShell equivalent
2. **Review the report** → `results/optimization/near_pass_report.md`
3. **Identify promotions** → Check for ✅ PASS status
4. **Update config** → `config/strategies.yaml` with new parameters
5. **Validate live** → Run backtest and monitor for 1 week
6. **Deploy to live** → If metrics hold, activate in production

---

## Questions or Issues?

- Check `results/optimization/near_pass_optimization.json` for detailed metrics
- Review strategy signal logic in `strategies/` folder
- Examine recent backtest reports in `results/overnight/`
- Check `results/demotion_tracker.json` for historical failure patterns
