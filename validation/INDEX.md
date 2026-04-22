# Validation Framework Index

> **Framework Version:** 2.0  
> **Created:** April 17, 2026  
> **Status:** ✅ Ready for Production  
> **Location:** `/TradePanel/validation/`

---

## 📦 Complete Validation System

This folder contains a **complete, production-ready 6-phase validation framework** for trading strategies on XAU/USD (Gold).

### Files Overview

| File | Purpose | Use When |
|------|---------|----------|
| **README.md** | Quick start guide | You're new to the framework |
| **strategies_structured.md** | All 10 strategies (AI-readable) | Implementing or backtesting strategies |
| **validation_config.yaml** | Acceptance criteria + rules | Modifying test thresholds |
| **test_runner.py** | Python validation script | Running full 6-phase validation |
| **test_workflow.md** | Detailed workflow + diagrams | Understanding test progression |
| **INDEX.md** | This file | Navigation & overview |

---

## 🎯 What Each Component Does

### 1. **Structured Strategies** (strategies_structured.md)
✅ All 10 XAU/USD trading strategies in standardized format

**10 Strategies Included:**
1. MA Crossover Trend Following
2. Range Breakout
3. RSI Pullback in Trend
4. BB Mean Reversion
5. Swing Pullback (Price Action)
6. News Event Breakout
7. London/NY Session Momentum
8. Regime-Aware Trading (Multi-Asset)
9. Stochastic Divergence Bounce
10. ML Binary Signal Classifier

**Format per Strategy:**
- Entry/Exit Rules (precise conditions)
- Parameters (with [Min..Max] bounds)
- Expected baseline metrics
- Regime conditions
- Risk factors & validation notes

**Why This Format:**
- AI/backtesting engines can automatically parse
- No subjective terms (all conditions are testable)
- Parameter bounds prevent overfitting
- Clear expectations vs. reality check

---

### 2. **Validation Configuration** (validation_config.yaml)
✅ All acceptance criteria and test rules

**What It Defines:**
- Acceptance criteria (min Sharpe, max drawdown, etc.)
- 6-phase test progression
- Optimization constraints (prevent curve-fitting)
- Failure criteria (when to stop testing)
- AI responsibilities per phase
- Performance metrics to track

**Key Sections:**
```yaml
Minimum Requirements:
  ✓ Win Rate: ≥50% (backtest), ≥48% (forward)
  ✓ Sharpe Ratio: ≥1.0 (backtest), ≥0.8 (forward)
  ✓ Max Drawdown: ≤15%
  ✓ Min Trades: 50 (backtest), 30 (forward)

Test Phases:
  Phase 1: Unit Test (logic correctness) — 1 hour
  Phase 2: Backtest (2+ years data) — 4 hours
  Phase 3: OOS Validation (20% holdout) — 2 hours
  Phase 4: Forward Test (50–100 paper trades) — 4 weeks
  Phase 5: Acceptance (final review) — 2 hours
  Phase 6: Live Micro-Lot (100+ live trades) — 6 weeks
```

---

### 3. **Test Runner Script** (test_runner.py)
✅ Python script that runs full validation pipeline

**What It Does:**
1. Loads all 10 strategies
2. Runs Phase 1 (Unit Test) for each
3. Runs Phase 2 (Backtest) for passed strategies
4. Runs Phase 3 (OOS Validation)
5. Runs Phase 4 (Forward Test)
6. Runs Phase 5 (Acceptance Decision)
7. Generates `validation_report.json`
8. Prints summary

**How to Run:**
```bash
pip install pyyaml
python test_runner.py
```

**Output:**
- `validation_report.json` — Full results
- `strategy_validation.log` — Detailed logs
- Console summary — Approved/rejected count

**Main Classes:**
- `StrategyValidator`: Orchestrates all 6 phases
- `StrategyMetrics`: Performance metrics container
- `TestResult`: Phase-by-phase results

---

### 4. **Workflow Documentation** (test_workflow.md)
✅ Detailed explanation of 6-phase testing

**Includes:**
- **Mermaid Diagram:** Full test workflow visualization
- **Phase-by-Phase Checklist:** What happens in each phase
- **Key Metrics Reference:** Sharpe, drawdown, win rate, etc.
- **Failure Decision Tree:** When to stop and why
- **Deployment Checklist:** Pre-engine approval tasks
- **Code Examples:** How to integrate

**Read This For:**
- Understanding why 6 phases exist
- What success looks like per phase
- How to interpret metrics
- Decision rules for PASS/FAIL

---

## 🚀 How to Use This System

### Scenario 1: Validate All Strategies
```bash
# 1. Run full validation
python test_runner.py

# 2. Check results
cat validation_report.json

# 3. Review approved strategies
grep '"overall_status": "APPROVED"' validation_report.json

# 4. Add to engine
# (strategies with overall_status: APPROVED are ready)
```

### Scenario 2: Understand a Specific Strategy
```bash
# 1. Open strategies_structured.md
# 2. Find "STRATEGY: [Name]"
# 3. Check:
#    - Entry Rules (when to buy/sell)
#    - Parameters (what AI can tune)
#    - Expected Baseline (target metrics)
#    - Risk Factors (what can go wrong)
```

### Scenario 3: Modify Acceptance Criteria
```bash
# 1. Edit validation_config.yaml
# 2. Change minimum_sharpe_ratio: 1.0 → 1.2 (raise threshold)
# 3. Run test_runner.py again
# 4. More strategies will fail (stricter threshold)
```

### Scenario 4: Add a New Strategy
```bash
# 1. Edit strategies_structured.md
# 2. Add new section:
#    STRATEGY: [Your Strategy Name]
#    ENTRY RULES (Long): ...
#    ENTRY RULES (Short): ...
#    EXIT RULES: ...
#    PARAMETERS: ...
#    etc.
# 3. Run test_runner.py
# 4. New strategy goes through full validation
```

---

## 📊 The 6-Phase Validation Process

```
PHASE 1: Unit Test (1 hour)
  ↓ Check entry/exit logic is programmatically correct
  ↓ No syntax errors? → PASS → Continue
  ✗ Syntax errors? → FAIL → Fix and retry

PHASE 2: Backtest (4 hours)
  ↓ Run 2+ years historical data with walk-forward CV
  ↓ Sharpe ≥1.0, WR ≥50%, DD ≤15%? → PASS → Continue
  ✗ Too weak? → ARCHIVE
  ✗ No edge? → ABANDON
  ✗ Too risky? → REDESIGN

PHASE 3: Out-of-Sample (2 hours)
  ↓ Test on 20% held-out data (no optimization)
  ↓ OOS Sharpe ≥70% of IS Sharpe? → PASS → Continue
  ✗ Overfitting detected? → REWORK parameters

PHASE 4: Forward Test (4 weeks)
  ↓ Paper trade 50–100 real trades
  ↓ Sharpe ≥0.8, consistent with Phase 2? → PASS → Continue
  ✗ Diverges from backtest? → INVESTIGATE

PHASE 5: Acceptance (2 hours)
  ↓ Review all 4 phases; confidence ≥75%?
  ✓ YES → APPROVED (ready for engine)
  ✗ NO → REJECTED (not ready)

PHASE 6: Live Micro-Lot (6 weeks, optional)
  ↓ Risk 0.5% per trade on live account
  ↓ Win rate ≥45%, no halt conditions?
  ✓ YES → Live trading approved ✓
  ✗ NO → AUTO-HALT (investigate)
```

---

## ✅ Approval Checklist

Before adding strategy to trading engine:

```
Phase 1: Unit Test
  ☐ Entry/exit rules parse correctly
  ☐ No syntax errors
  ☐ All parameters have [Min..Max]

Phase 2: Backtest
  ☐ Sharpe ≥ 1.0
  ☐ Win rate ≥ 50%
  ☐ Max drawdown ≤ 15%
  ☐ ≥ 50 trades
  ☐ Walk-forward validation complete

Phase 3: OOS Validation
  ☐ OOS Sharpe ≥ 70% of IS Sharpe
  ☐ No overfitting
  ☐ Metrics stable

Phase 4: Forward Test
  ☐ Sharpe ≥ 0.8
  ☐ Win rate ≥ 48%
  ☐ ≥ 30 paper trades
  ☐ Consistent with Phase 2

Phase 5: Acceptance
  ☐ All 4 phases PASSED
  ☐ Confidence ≥ 75%
  ☐ No red flags

Ready to Add to Engine! ✓
```

---

## 🎓 Key Concepts

### Sharpe Ratio
- **What:** Risk-adjusted return per unit of volatility
- **Target:** ≥1.0 (backtest), ≥0.8 (forward)
- **Example:** Sharpe 1.5 = 1.5% return per 1% volatility

### Walk-Forward Validation
- **What:** Cross-validate parameters across multiple time windows
- **Why:** Prevents curve-fitting (overfitting to past data)
- **How:** Divide 2 years into 4 folds; optimize each fold independently

### Out-of-Sample (OOS) Testing
- **What:** Test on 20% data that was never used for optimization
- **Why:** Ensures edge is real, not statistical accident
- **Target:** OOS Sharpe ≥ 70% of in-sample Sharpe

### Forward Testing
- **What:** Paper trading on real market data (but not your real money)
- **Why:** Simulate real execution (slippage, spreads, latency)
- **Duration:** 4 weeks minimum (50–100 trades)

---

## 📁 File Structure

```
/TradePanel/
├── validation/                    ← NEW VALIDATION SYSTEM
│   ├── README.md                  ← Quick start (read first!)
│   ├── INDEX.md                   ← This file (navigation)
│   ├── strategies_structured.md    ← All 10 strategies
│   ├── validation_config.yaml      ← Acceptance criteria
│   ├── test_runner.py              ← Validation script
│   ├── test_workflow.md            ← Detailed workflow
│   ├── validation_report.json      ← Generated report
│   ├── strategy_validation.log     ← Generated logs
│   └── archive/                    ← Archived strategies
│
├── config/                        ← (existing)
├── data/                          ← (existing)
├── strategies/                    ← (existing)
└── ... (other existing files)
```

---

## 🔧 Quick Commands

```bash
# Install dependencies
pip install pyyaml

# Run full validation
python test_runner.py

# View results
cat validation_report.json

# Watch logs
tail -f strategy_validation.log

# Check approved strategies
grep '"overall_status": "APPROVED"' validation_report.json | wc -l
```

---

## 📖 Reading Guide

**If you're new to this framework:**
1. Read `README.md` (5 min)
2. Skim `strategies_structured.md` (Strategy #1 only, 5 min)
3. Read `test_workflow.md` - Workflow Diagram section (10 min)
4. Run `python test_runner.py` (observe output)
5. Check `validation_report.json` (review results)

**If you're implementing a strategy:**
1. Go to `strategies_structured.md`
2. Find your strategy
3. Extract Entry/Exit Rules + Parameters
4. Implement in your backtest engine
5. Run full validation

**If you're modifying criteria:**
1. Edit `validation_config.yaml`
2. Change thresholds as needed
3. Run `python test_runner.py` again
4. Review `validation_report.json`

---

## ⚠️ Important Notes

1. **No Skipping Phases:** All 6 phases must pass for engine approval
2. **No Re-Optimization:** Once Phase 2 ends, parameters are locked (prevents overfitting)
3. **Time Commitment:** Full validation takes ~4 weeks (due to Phase 4 forward test)
4. **Auto-Retirement:** Strategies with Sharpe < 0.8 OOS for 2+ weeks are auto-disabled
5. **Version Control:** Keep `validation_report.json` history to track strategy performance

---

## 🚨 Failure Scenarios

| Failure | Action | Resolution |
|---------|--------|-----------|
| Sharpe < 0.6 (Phase 2) | ARCHIVE | Revisit later (strategy may need redesign) |
| Win rate < 45% | ABANDON | No viable edge; discard |
| Drawdown > 20% | REDESIGN | Tighten stops; reduce position size |
| OOS << IS (Phase 3) | OVERFIT | Simplify; re-optimize with fewer parameters |
| Forward << Backtest (Phase 4) | INVESTIGATE | Check data quality, execution, slippage |
| Confidence < 75% (Phase 5) | CONDITIONAL | Approve with caveats; monitor closely |

---

## 🎉 Next Steps

1. ✅ You now have a **complete validation framework**
2. ✅ All 10 strategies are **structured & AI-ready**
3. ✅ All 4 components are **isolated in `/validation/` folder**
4. ✅ Ready to **run full pipeline**: `python test_runner.py`

**What happens next:**
- Run validation on each strategy
- Approve strategies that pass all 6 phases
- Add approved strategies to your trading engine
- Monitor live performance weekly

---

**Framework Status:** ✅ Production Ready  
**Last Updated:** April 17, 2026  
**Version:** 2.0  
**Maintainer:** AI Validation System
