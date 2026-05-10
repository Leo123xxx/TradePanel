# Near-PASS Strategy Optimization Suite

**Created:** 2026-05-10  
**Purpose:** Automated parameter tuning for 8 strategies one metric away from PASS status  

---

## What This Suite Does

The optimization suite **automatically searches parameter combinations** for near-pass candidates to identify settings that cross PASS thresholds (Sharpe ≥ 1.5, Win Rate ≥ 65%).

Instead of manually tweaking parameters, the scripts:
1. Generate realistic synthetic OHLCV data per pair/timeframe
2. Run each strategy through actual backtest engine
3. Test hundreds of parameter combinations
4. Rank results by performance
5. Generate recommendations for config updates

---

## Files Created

### 1. **Main Optimization Scripts**

| Script | Purpose |
|--------|---------|
| `scripts/optimize_near_pass.py` | Core optimizer with focused parameter grids per strategy |
| `scripts/run_near_pass_suite.py` | Orchestrator that runs all strategies and aggregates results |
| `scripts/validate_near_pass_params.py` | Quick validator to compare old vs new parameters |

### 2. **Runner Scripts**

| Script | Purpose | Usage |
|--------|---------|-------|
| `RUN_NEAR_PASS_OPTIMIZATION.bat` | Windows batch runner | `RUN_NEAR_PASS_OPTIMIZATION.bat --quick` |
| `RUN_NEAR_PASS_OPTIMIZATION.ps1` | PowerShell runner | `.\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Quick` |

### 3. **Documentation**

| File | Purpose |
|------|---------|
| `docs/NEAR_PASS_OPTIMIZATION_GUIDE.md` | Complete user guide with troubleshooting |
| `results/STRATEGY_CONSOLIDATION_ANALYSIS.md` | Overall strategy analysis (created earlier) |

---

## Quick Start (3 Steps)

### Step 1: Run the Optimization Suite

```bash
# Option A: Batch file (Windows)
RUN_NEAR_PASS_OPTIMIZATION.bat

# Option B: PowerShell
.\RUN_NEAR_PASS_OPTIMIZATION.ps1

# Option C: Direct Python
python scripts/run_near_pass_suite.py
```

**What to expect:**
- 1-2 minutes for quick run
- 5-10 minutes for normal run
- 30+ minutes for extended run
- Progress printed to console
- Results saved to `results/optimization/`

### Step 2: Review the Report

```bash
# Open the summary report
results/optimization/near_pass_report.md
```

**Look for:**
- ✅ PASS status → Ready to deploy
- 🟡 PARTIAL status → Close, needs extension
- 🔄 WORKING status → More tuning needed

### Step 3: Update and Validate

If a strategy shows ✅ PASS:

```bash
# 1. Copy top parameters to config/strategies.yaml
# 2. Validate with quick backtest
python scripts/run_backtest.py --strategy hikkake_trap

# 3. If metrics hold, it's ready for live deployment
```

---

## The 8 Strategies

### Tier 1: Quick Wins (Low Gap)

| Strategy | Pair | Gap | What to Tune |
|----------|------|-----|--------------|
| **hikkake_trap** | GBPUSD | +2pp WR | Cooldown bars, TP/SL |
| **rsi_pullback** | GBPJPY | Validation | Extend data (80% WR) |
| **rsi_extremes_scalp** | USOIL | Validation | Extend data (75% WR) |

**Expected:** 1-2 promotions to PASS within 1-2 weeks

### Tier 2: Moderate Effort

| Strategy | Pair | Gap | What to Tune |
|----------|------|-----|--------------|
| **range_breakout** | US500 | +6.1pp WR | ADX filter, consolidation |
| **dual_ema_momentum** | XAUUSD | +8.1pp WR | ADX filter, EMA ranges |

**Expected:** 1-2 promotions after extended tuning (2-3 weeks)

### Tier 3: Challenging (Large Gaps)

| Strategy | Pair | Gap | What to Tune |
|----------|------|-----|--------------|
| **session_momentum** | XAUUSD | +24.4pp WR | Entry filter (ADX min) |
| **session_momentum** | GBPJPY | +22.9pp WR | Same as above |
| **ema_ribbon_trend** | NVDA | Data | Extend window (20+ trades) |

**Expected:** 0-1 promotions (may need signal logic review)

---

## Parameter Grids Explained

Each strategy has a **focused parameter grid** tailored to its specific gap.

### Example: session_momentum (Needs +24pp WR)

```python
"params": {
    "fast_ema":           [8, 10, 12, 15, 20],      # Tighter fast EMA
    "slow_ema":           [20, 34, 50, 75],         # Higher slow EMA
    "min_adx_filter":     [25, 28, 30, 32],         # ← KEY: Increase ADX
    "vol_threshold_mult": [1.0, 1.2, 1.5],         # Volume filter
    "tp_atr_mult":        [1.8, 2.0, 2.2],
    "sl_atr_mult":        [0.8, 1.0],
}
```

**Why these ranges?**
- `min_adx_filter` is the main gap-filler (entry quality filter)
- Others test variations to find sweet spot
- Ranges are tight to avoid overfitting

### Grid Size Impact

| Grid Size | Combos | Time |
|-----------|--------|------|
| Conservative | 100–500 | 1–5 min |
| Normal | 500–2000 | 5–15 min |
| Aggressive | 2000–5000 | 15–30 min |
| Extended | 5000+ | 30+ min |

Use `--quick` for fast validation, `--extended` for thorough search.

---

## Understanding Results

### JSON Structure

```json
{
  "strategy_name": {
    "status": "OK",              // Status of the optimization
    "total_combos": 384,         // Total combinations tested
    "top_5": [
      {
        "score": 0.946,          // Composite metric (0-1)
        "pair": "GBPUSD",
        "tf": "H4",
        "params": {...},         // Parameter set
        "metrics": {
          "sharpe": 2.15,        // Risk-adjusted return
          "win_rate": 71.2,      // % winning trades
          "profit_factor": 1.42, // Gross profit / loss
          "max_dd": 3.2,         // Largest drawdown %
          "trades": 125,         // Total trades
          "pnl_zar": 5420.50     // P&L in ZAR
        }
      }
    ]
  }
}
```

### Score Calculation

```
score = (sharpe × 0.4) + ((win_rate / 100) × 0.6)
```

- Higher Sharpe = better risk-adjusted returns (40% weight)
- Higher Win Rate = more consistency (60% weight)

---

## Workflow Examples

### Example 1: Quick Validation (2 minutes)

```bash
# Run quick pass on all strategies
RUN_NEAR_PASS_OPTIMIZATION.bat --quick

# Check results
type results\optimization\near_pass_report.md

# If hikkake_trap shows PASS:
# - Update config/strategies.yaml
# - Run backtest to confirm
```

### Example 2: Focused Tuning (10 minutes)

```bash
# Focus on one strategy showing promise
python scripts/optimize_near_pass.py --strategy session_momentum

# Review results in:
# results/optimization/near_pass_optimization.json

# Test if new params improve baseline:
python scripts/validate_near_pass_params.py session_momentum XAUUSD H1 \
  --new-params '{"min_adx_filter": 28, "fast_ema": 12}'
```

### Example 3: Extended Search (30+ minutes)

```bash
# When quick run shows promise, dig deeper
RUN_NEAR_PASS_OPTIMIZATION.ps1 -Extended

# Compare with previous results
# diff results/optimization/near_pass_report.md \
#     results/optimization/near_pass_report_prev.md
```

---

## Integration with Daily Workflow

### Morning (5 min)

```bash
# Quick check on prioritized strategies
python scripts/run_near_pass_suite.py --quick

# Review `near_pass_report.md` for promotions
```

### Weekly (60 min)

```bash
# Full optimization on candidates close to PASS
RUN_NEAR_PASS_OPTIMIZATION.bat

# Update config with promotions
# Run full backtest to validate
python scripts/run_backtest.py
```

### Post-Promotion (20 min)

```bash
# After strategy is promoted to config
# 1. Validate it passes backtest criteria
# 2. Monitor demotion_tracker.json for 1 week
# 3. If stable, include in live trading
```

---

## Troubleshooting

### "NO_TRADES" for All Parameter Sets

**Cause:** Strategy signal logic is too strict or data issue  
**Fix:**
1. Loosen filters in parameter grid (lower ADX min, wider RSI bands)
2. Check UTC/SAST timezone alignment in data ingestion
3. Review strategy signal logic for inverted conditions

### Wins on Synthetic, Loses on Real Data

**Cause:** Overfitting to synthetic OHLCV  
**Fix:**
1. Validate parameters on actual MT5 historical data
2. Run walk-forward optimization (WFO) instead
3. Extend backtest window and require minimum trades

### Optimization Takes Forever

**Cause:** Too many parameters or values  
**Fix:**
1. Use `--quick` flag (samples every 2nd combo)
2. Reduce parameter ranges (e.g., 3 values instead of 5)
3. Focus on 2-3 key parameters instead of all

### Parameters Work in Optimizer, Fail in Live

**Cause:** Real market conditions differ from synthetic data  
**Fix:**
1. Test in paper trading first (2-4 weeks minimum)
2. Monitor win rate in demotion_tracker.json
3. If falling below 60%, revert parameters

---

## Advanced: Custom Parameter Grids

Edit `scripts/optimize_near_pass.py` to customize grids:

```python
NEAR_PASS_GRIDS = {
    "my_strategy": {
        "pair": "EURUSD",
        "timeframe": "H4",
        "focus": "win_rate",
        "params": {
            "custom_param_1": [10, 20, 30],      # Test values
            "custom_param_2": [0.5, 1.0, 1.5],
            # ... more params
        }
    }
}
```

Then run:
```bash
python scripts/optimize_near_pass.py --strategy my_strategy
```

---

## Expected Results

### Optimistic Scenario (Tier 1 + 2)
- Week 1: 2-3 strategies promoted to PASS
- Week 2-3: 2-3 more strategies reach PASS after extended tuning
- Result: **5-6 additional PASS strategies** to the existing 35

### Realistic Scenario (Tier 1 + Partial)
- Week 1: 1-2 strategies promoted to PASS
- Week 2-3: 2-3 more show improvement (🟡 PARTIAL)
- Week 4+: Some PARTIAL → PASS after further refinement
- Result: **2-4 additional PASS strategies**

### Conservative Scenario
- Some strategies show data quality issues
- Parameter ranges need manual review
- Signal logic bugs identified and fixed
- Result: **Insights for next development cycle**

---

## Next Steps

1. **Run the suite**
   ```bash
   RUN_NEAR_PASS_OPTIMIZATION.bat
   ```

2. **Review results**
   ```bash
   type results\optimization\near_pass_report.md
   ```

3. **Promote PASS strategies**
   - Update `config/strategies.yaml`
   - Run `python scripts/run_backtest.py` to validate
   - Monitor for 1 week in paper trading

4. **Extend tuning for 🟡 PARTIAL strategies**
   - Run with `--extended` flag
   - Compare parameter sets across top results
   - Test edge values

5. **Monitor weekly**
   - Check `results/demotion_tracker.json` for regressions
   - Maintain 35+ PASS strategies in active pool

---

## Reference Documents

| Document | Use When |
|----------|----------|
| `docs/NEAR_PASS_OPTIMIZATION_GUIDE.md` | Need detailed instructions |
| `results/STRATEGY_CONSOLIDATION_ANALYSIS.md` | Want overall strategy landscape |
| `results/optimization/near_pass_report.md` | After running optimization |
| `results/agent_handover_20260506.md` | Need context on what's been done |

---

## Questions?

- **How do I know if parameters are good?** → Look for Sharpe ≥1.5 AND Win Rate ≥65%
- **Should I update config immediately?** → Validate in backtest first, then paper trade
- **What if nothing passes?** → Check signal logic, data alignment, or run extended search
- **Can I combine different parameter sets?** → Not recommended; test each independently

---

*End of Near-PASS Optimization Suite Documentation*
