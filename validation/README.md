# Strategy Validation Framework - Quick Start Guide

## Overview

This folder contains a **complete, production-ready validation framework** for trading strategies. It ensures all strategies pass a rigorous 6-phase testing process before being added to the trading engine.

## 📁 Folder Structure

```
/validation/
├── README.md                      ← You are here
├── strategies_structured.md        ← All 10 strategies (AI-readable format)
├── validation_config.yaml          ← Acceptance criteria + test rules
├── test_runner.py                  ← Python script: runs full validation
├── test_workflow.md                ← Detailed workflow + diagrams
├── validation_report.json          ← Generated after test run
├── strategy_validation.log         ← Test execution logs
└── archive/                        ← Disabled/archived strategies
    ├── disabled_strategies/
    └── test_results/
```

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install pyyaml
```

### Step 2: Run Full Validation Pipeline
```bash
cd /path/to/validation/
python test_runner.py
```

### Step 3: View Results
```bash
# Check summary
cat validation_report.json

# Watch live logs
tail -f strategy_validation.log
```

### Step 4: Review Approved Strategies
Strategies with `overall_status: APPROVED` are ready for engine integration.

---

## 📋 What's in Each File

### 1. **strategies_structured.md**
Contains all 10 trading strategies in a standardized, AI-readable format.

**Structure per strategy:**
```
STRATEGY: [Name]
ASSET: XAU/USD
TIMEFRAME: H1, H4, D1
CATEGORY: Trend | Reversion | Breakout | etc.

ENTRY RULES (Long): [Conditions]
ENTRY RULES (Short): [Conditions]

EXIT RULES:
  • Take Profit: [ATR multiple or pips]
  • Stop Loss: [ATR multiple or pips]

PARAMETERS (AI-Tunable):
  - param_1: [Min..Max] (default: X)
  - param_2: [Min..Max] (default: Y)

REGIME CONDITIONS:
  Works Best In: [Market type]
  Avoid In: [Market type]

EXPECTED BASELINE:
  Win Rate: X–Y%
  Sharpe: Z
  Drawdown: W%

RISK FACTORS & VALIDATION:
  • [Failure modes]
  • [AI checks]
```

**How to use:**
- AI systems can automatically parse this file
- Parameters are bounded → prevents overfitting
- Entry/exit logic is unambiguous → no subjective terms
- Backtesting engines can directly implement these rules

---

### 2. **validation_config.yaml**
Defines all acceptance criteria and test rules.

**Key sections:**
- `acceptance_criteria`: Min Sharpe, max drawdown, win rate requirements
- `test_phases`: 6-phase testing progression
- `optimization_constraints`: Prevent overfitting (walk-forward CV, parameter bounds)
- `failure_criteria`: When to stop testing a strategy
- `ai_responsibilities`: What AI must do in each phase
- `metrics`: Key performance indicators to track

**Example acceptance criteria:**
```yaml
acceptance_criteria:
  backtesting:
    minimum_win_rate: 0.50          # ≥50%
    minimum_sharpe_ratio: 1.0       # ≥1.0
    maximum_drawdown_percent: 15.0  # ≤15%
    minimum_trade_sample: 50        # ≥50 trades
```

---

### 3. **test_runner.py**
Python script that orchestrates the entire validation pipeline.

**Main classes:**
- `StrategyValidator`: Orchestrates all 6 phases
- `TestPhase`: Enum for test phases
- `TestStatus`: Enum for test status (PENDING, PASSED, FAILED, etc.)
- `StrategyMetrics`: Data class for performance metrics

**Key methods:**
```python
validator = StrategyValidator('validation_config.yaml')
validator.load_strategies('strategies_structured.md')
results = validator.run_full_test_pipeline()
validator.generate_report('validation_report.json')
validator.print_summary()
```

**What it does:**
1. Loads all 10 strategies
2. Runs Phase 1 (Unit Test) for each
3. Runs Phase 2 (Backtest) for passed strategies
4. Runs Phase 3 (OOS Validation) if Phase 2 passed
5. Runs Phase 4 (Forward Test) for approved strategies
6. Runs Phase 5 (Acceptance Decision) to decide PASS/FAIL
7. Generates `validation_report.json`
8. Prints summary

---

### 4. **test_workflow.md**
Detailed documentation of the 6-phase testing workflow.

**Includes:**
- Mermaid diagram of full workflow
- Phase-by-phase checklist
- Key metrics reference
- Failure decision tree
- Deployment checklist

**Recommended reading order:**
1. Start with workflow diagram
2. Read Phase 1 checklist
3. Move through remaining phases
4. Review failure criteria
5. Use deployment checklist before adding to engine

---

## 🔄 The 6-Phase Testing Process

| Phase | Duration | What | Success Criteria |
|-------|----------|------|------------------|
| **1. Unit Test** | 1 hour | Logic correctness | No syntax errors |
| **2. Backtest** | 4 hours | 2+ years data, walk-forward | Sharpe ≥1.0, WR ≥50%, DD ≤15% |
| **3. OOS Validation** | 2 hours | 20% held-out data | OOS Sharpe ≥70% of IS |
| **4. Forward Test** | 4 weeks | Paper trading 50–100 trades | Sharpe ≥0.8, consistent with Phase 2 |
| **5. Acceptance** | 2 hours | Final review of all 4 phases | Confidence ≥75% |
| **6. Live Micro-Lot** | 6 weeks | Live trading 100+ trades | Win rate ≥45%, no halt conditions |

**Flow:**
```
Strategy → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 (optional) → Engine
          (Unit)   (BT)      (OOS)     (Paper)   (Accept)  (Live)
```

If any phase **FAILS**, strategy is either:
- **REJECTED** (not ready for engine)
- **ARCHIVED** (too weak; revisit later)
- **ABANDONED** (no viable edge)
- **REDESIGNED** (rework and retry)

---

## 📊 Key Metrics Explained

### Sharpe Ratio
- **Formula:** (Return - Risk-Free Rate) / Volatility
- **Target:** ≥1.0 (backtest), ≥0.8 (forward test)
- **Interpretation:** How much return per unit of risk
- **Example:** Sharpe 1.25 = 1.25% return per 1% volatility

### Win Rate
- **Formula:** # Winning Trades / Total Trades
- **Target:** ≥50% (backtest), ≥48% (forward test)
- **Interpretation:** Percentage of profitable trades
- **Note:** Can be low if RR ratio is high (e.g., 40% win rate with 1:3 RR is profitable)

### Max Drawdown
- **Formula:** (Trough - Peak) / Peak
- **Target:** ≤15% of account
- **Interpretation:** Largest peak-to-trough decline
- **Example:** $10,000 account, max DD 15% = max loss of $1,500

### Profit Factor
- **Formula:** Gross Profit / Gross Loss
- **Target:** ≥1.5
- **Interpretation:** Total wins vs. total losses
- **Example:** Profit factor 2.0 = wins are 2× total losses

---

## ⚠️ Failure Criteria (Stop Testing If Triggered)

| Failure | Condition | Action |
|---------|-----------|--------|
| **Too Weak** | Sharpe < 0.6 | ARCHIVE |
| **No Edge** | Win rate < 45% across all folds | ABANDON |
| **Risky** | Max drawdown > 20% | REDESIGN |
| **Divergence** | Forward test metrics diverge > 3σ | INVESTIGATE |

---

## 🎯 Acceptance Criteria Checklist

Before adding a strategy to the engine, verify:

- [ ] **Phase 1 (Unit)** ✅ PASSED
  - [ ] Entry/exit rules parse correctly
  - [ ] No syntax errors
  - [ ] Parameters have [Min..Max] bounds

- [ ] **Phase 2 (Backtest)** ✅ PASSED
  - [ ] Sharpe ≥ 1.0
  - [ ] Win rate ≥ 50%
  - [ ] Max drawdown ≤ 15%
  - [ ] ≥ 50 trades
  - [ ] Walk-forward validation complete

- [ ] **Phase 3 (OOS)** ✅ PASSED
  - [ ] OOS Sharpe ≥ 70% of in-sample
  - [ ] No overfitting detected
  - [ ] Metrics stable across holdout data

- [ ] **Phase 4 (Forward)** ✅ PASSED
  - [ ] Sharpe ≥ 0.8 (paper trading)
  - [ ] Win rate ≥ 48%
  - [ ] ≥ 30 paper trades
  - [ ] Consistent with backtest

- [ ] **Phase 5 (Accept)** ✅ PASSED
  - [ ] All 4 phases PASSED
  - [ ] Confidence score ≥ 75%
  - [ ] No major red flags
  - [ ] Metrics stable across all phases

---

## 🔧 How to Use This in Your Engine

### Option 1: Python Integration
```python
from validation.test_runner import StrategyValidator

validator = StrategyValidator('validation/validation_config.yaml')
validator.load_strategies('validation/strategies_structured.md')

# Run full pipeline
results = validator.run_full_test_pipeline()

# Add approved strategies to engine
approved_strategies = [
    name for name, results in results.items() 
    if all(r.status == 'PASSED' for r in results if r.phase != TestPhase.LIVE_MICRO)
]

for strategy_name in approved_strategies:
    engine.register_strategy(strategy_name)
```

### Option 2: Manual Review
1. Run `python test_runner.py`
2. Check `validation_report.json`
3. Review any REJECTED strategies
4. Manually approve PASSED strategies
5. Add to engine config

### Option 3: Continuous Integration
```bash
# Add to CI/CD pipeline (e.g., GitHub Actions)
- name: Validate Strategies
  run: |
    cd validation/
    python test_runner.py
    if ! grep -q '"overall_status": "APPROVED"' validation_report.json; then
      exit 1  # Fail CI if any strategy not approved
    fi
```

---

## 📈 Post-Deployment Monitoring

After a strategy is in the engine:

1. **Daily:** Monitor live P&L, drawdown, win rate
2. **Weekly:** Generate performance report; compare to paper baseline
3. **Monthly:** Analyze performance by regime (trend vs. range)
4. **Quarterly:** Retire strategies if Sharpe < 0.8 OOS

**Auto-Retirement Rule:**
If a strategy's OOS Sharpe < 0.8 for 2 consecutive weeks, auto-disable and flag for review.

---

## 🛠️ Customization

Want to modify the framework?

1. **Change acceptance criteria:** Edit `validation_config.yaml`
   ```yaml
   acceptance_criteria:
     backtesting:
       minimum_sharpe_ratio: 1.2  # Raise threshold
   ```

2. **Add a new strategy:** Add to `strategies_structured.md` following the template

3. **Add custom validation:** Modify `test_runner.py`
   ```python
   def run_phase_2_backtest(self, strategy):
       # Your custom backtesting logic here
       pass
   ```

4. **Change test phases:** Edit `test_phases` in `validation_config.yaml`

---

## ❓ FAQ

**Q: Can I skip phases?**  
A: No. All 6 phases must pass for engine approval. This prevents overfitting and ensures robustness.

**Q: What if a strategy fails Phase 4?**  
A: Investigate the cause:
- Is paper trading execution different? (slippage, latency)
- Did market conditions change?
- Is there a bug in the strategy logic?
Then either redesign or abandon.

**Q: How do I update parameters after Phase 2?**  
A: You cannot optimize parameters in Phase 3+ (that's overfitting). Only the best parameters from Phase 2 are used in Phases 3–5.

**Q: What's the minimum time to approve a strategy?**  
A: ~4 weeks (Phases 1–5 take ~1 week; Phase 4 forward test takes ~3 weeks).

**Q: Can I run strategies in parallel?**  
A: Yes. The validator processes all strategies independently; you can parallelize across multiple cores/machines.

---

## 📞 Support

For questions or issues:

1. Check `test_workflow.md` for detailed workflow
2. Review `validation_config.yaml` for rules
3. Check `strategy_validation.log` for error messages
4. Inspect `validation_report.json` for detailed results

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Apr 17, 2026 | Initial structured framework; 6-phase testing |
| 1.0 | (Previous) | Legacy unstructured validation |

---

**Last Updated:** April 17, 2026  
**Framework Version:** 2.0  
**Status:** ✅ Production Ready
