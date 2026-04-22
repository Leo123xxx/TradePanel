# 🤖 Agent Handover Ready — Path B Tasks

> **Date:** 2026-04-20  
> **Status:** ✅ READY FOR AGENT  
> **Next Action:** Agent starts with STEP 00A test, then proceeds through 00B–00E

---

## 📋 What's Been Prepared

### ✅ COMPLETED Work (By Leo's Team)

1. **Strategic Analysis**
   - ✅ Analyzed current strategies (3 Tier-1, 3 Tier-2, 1 Tier-3)
   - ✅ Identified +20% win rate improvement path
   - ✅ Created comprehensive enhancement plan

2. **Component 1: Ensemble Voting (DONE)**
   - ✅ `strategies/ensemble.py` created (voting mechanism)
   - ✅ `scripts/run_backtest.py` updated (added ensemble to STRATEGY_MAP)
   - ✅ `config/strategies.yaml` updated (ensemble enabled)
   - ✅ Ready to test immediately

3. **Documentation & Guides**
   - ✅ `PATH_B_IMPLEMENTATION.md` — detailed step-by-step for all 5 components
   - ✅ `PATH_B_BUILD_PROGRESS.md` — progress tracking + expected results
   - ✅ `STRATEGY_ENHANCEMENT_PLAN.md` — strategic overview
   - ✅ `AGENT_HANDOVER.md` — updated with all Path B tasks

---

## 🎯 What Agent Should Do Now

### Phase 1: Quick Wins (4 hours)

**STEP 00A: Test Ensemble (30 min)**
```bash
# Test file exists
python strategies/ensemble.py
# Expected: "[ENSEMBLE] All tests passed ✓"

# Run baseline backtest
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
# Expected: ~14–16 trades, 58–62% win rate, PF 1.9–2.1
```
**If ✓:** Move to 00B

**STEP 00B: BB Mean Reversion Fix (1.5 hrs)**
- File to edit: `strategies/bb_mean_reversion.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 2"
- 3 small edits (RSI threshold, volume spike, support detection)
- Test: `python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1`
- Expected: PF 0.69 → 1.25–1.35

**STEP 00C: Session Momentum Fix (1 hr)**
- File to edit: `strategies/session_momentum.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 3"
- 3 small edits (time window, volume filter, session bias)
- Test: `python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1`
- Expected: PF 0.99 → 1.20–1.30

**After 00A–00C:** +8–10% aggregate win rate ✓

---

### Phase 2: Medium Wins (5.5 hours, if time)

**STEP 00D: Regime Filter (3 hrs)**
- Create: `data/macro_feed.py` + `risk/regime_classifier.py`
- Update: `forward_test/paper_engine.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 4"
- Setup: Register API keys (Alpha Vantage, FRED) in `.env`
- Expected: +15–20% win rate by filtering trades against macro trends

**STEP 00E: Multi-TF Confirmation (2.5 hrs)**
- Update: `strategies/base_strategy.py`, `config/strategies.yaml`, `forward_test/paper_engine.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 5"
- Expected: +8–12% win rate, -20–30% false signals

**After 00D–00E:** +12–15% aggregate win rate ✓

---

## 📚 Documentation Provided

| File | Purpose | Status |
|------|---------|--------|
| `PATH_B_IMPLEMENTATION.md` | Full implementation guide (all 5 components) | ✅ Ready |
| `PATH_B_BUILD_PROGRESS.md` | Status tracking + verification checklist | ✅ Ready |
| `STRATEGY_ENHANCEMENT_PLAN.md` | Strategic overview + why 20% improvement is possible | ✅ Ready |
| `AGENT_HANDOVER.md` | **← THIS IS WHAT TO HAND TO AGENT** | ✅ Updated |

---

## ✅ Alignment Checklist — Verify Before Handing Off

- ✅ Ensemble.py exists and has generate_signals() method
- ✅ run_backtest.py imports EnsembleStrategy
- ✅ config/strategies.yaml has ensemble entry with enabled: true
- ✅ PATH_B_IMPLEMENTATION.md has detailed guides for Components 2–5
- ✅ AGENT_HANDOVER.md has updated task queue with Path B priorities
- ✅ All three PATH_B_*.md files are in the TradePanel root
- ✅ Success criteria are clear (win rate targets, PF targets, test commands)

---

## 🚀 How to Hand Off to Agent

**Give agent:**
1. Tell them: "Check AGENT_HANDOVER.md Section 6 — Path B tasks are ready"
2. Point them to: STEP 00A quick test
3. Reference guides: PATH_B_IMPLEMENTATION.md has all details
4. Expected timeline: 4 hrs minimum (00A–00C), up to 9 hrs if doing all 5 components

**Agent starts with:**
```bash
cd F:\REPOS\leo123xxx\TradePanel
python strategies/ensemble.py
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
```

**If backtests pass:** Move to STEP 00B

---

## 📊 Expected Outcome

**Current Baseline:**
- Avg Win Rate: 52%
- Profit Factor: 1.72
- Sharpe Ratio: ~4.5

**After Path B (all 5 components):**
- **Win Rate: 62–65% (+10–13%)**
- **Profit Factor: 2.05–2.20 (+20–25%)**
- **Sharpe Ratio: 5.5–6.0 (+20–25%)**

**After Path B (minimum 00A–00C only):**
- **Win Rate: 58–60% (+6–8%)**
- **Profit Factor: 1.85–1.95 (+8–13%)**

---

## ⚙️ System Status — Ready for Agent

| Component | Files | Status | Test |
|-----------|-------|--------|------|
| Ensemble | ensemble.py, run_backtest.py, config.yaml | ✅ Ready | `python scripts/ensemble.py` |
| BB Fix | strategies/bb_mean_reversion.py | 📝 Guide provided | `python scripts/run_backtest.py --strategy bb_mean_reversion` |
| Session Fix | strategies/session_momentum.py | 📝 Guide provided | `python scripts/run_backtest.py --strategy session_momentum` |
| Regime | macro_feed.py, regime_classifier.py | 📝 Guide + API setup | `--regime-filter` flag |
| Multi-TF | base_strategy.py, config.yaml, paper_engine | 📝 Guide provided | `--confirm-tf H4` flag |

---

## ⏭️ After Path B (If Agent Completes)

Agent can then move to:
1. **STEP 00** — Telegram Bot Fixes (if still in scope)
2. **STEP 0–5** — Data Ingestion & Crypto Deployment
3. **STEP 19–20** — System Test & Phase 1 Complete

But Path B completion is the priority for **+20% win rate gain**.

---

**✅ Everything is aligned and ready. Hand off AGENT_HANDOVER.md to the agent.**

*Last verified: 2026-04-20 22:00 UTC*
