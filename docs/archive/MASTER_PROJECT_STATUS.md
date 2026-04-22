# 🎯 MASTER PROJECT STATUS & UPDATED PLAN

**Last Updated:** 2026-04-20  
**Current Phase:** 0 — Crisis Mode (Stabilize Bot)  
**Overall Completion:** 12% → 15% (after Phase 0)  
**Critical Issue:** Live bot failing with stale signals + order validation

---

## 📊 PROJECT OVERVIEW

### What This Project Is
**TradePanel** — Fully automated MT5 algorithmic trading platform
- Backtests strategies on 6+ years of historical data
- Walk-forward validates to prevent overfitting
- Executes paper trades live on MT5 demo account
- Sends Telegram notifications for every trade
- Runs 11 scheduled background jobs automatically

### Current State
- **Phase 1 Build:** 40% complete (backtesting + strategy validation done)
- **Paper Trading:** 10% complete (stubs exist, live bot has bugs)
- **Path B Enhancements:** 10% complete (Ensemble done, Components 2-5 queued)
- **Critical Issues:** 3 blocking live trading (see Phase 0 below)

---

## 🚨 PHASE 0: CRISIS MODE — Stabilize Live Bot

**Status:** 🔴 **URGENT** — Bot stuck in retry loop  
**Timeline:** 1–2 hours  
**Blocker For:** Everything else

### The Problem

Live bot started with this error loop:
```
SIGNAL DETECTED: SELL for GBPUSD on 2026-04-19 20:00:00
EXECUTING: SELL 0.1 lots on GBPUSD
FAILED to open trade: mt5.order_send returned None
[retry infinitely with same signal]
```

### Root Causes (3)

1. **Stale Signal Repetition** ← No deduplication
   - Same bar keeps generating same signal
   - No tracking of attempted signals
   - System retries endlessly

2. **Order Validation Missing** ← Returns None silently
   - No validation before send
   - No symbol market watch check
   - No error messages

3. **No Data Freshness Check** ← Using old data
   - Signal from 2026-04-19 when date is 2026-04-20
   - No validation that data is current

### Fixes Required (4 Components)

#### Fix 1: Signal Deduplication (30 min)
**File:** `forward_test/paper_engine.py`
**Change:** Track (strategy, symbol, bar_time) to prevent duplicate execution

**Before:**
```python
for strat_name, strategy in self.active_strategies.items():
    signal = self.signal_checker.get_signal(...)
    if signal != 0:
        self.order_manager.open_position(...)  # ← Executes every loop
```

**After:**
```python
self.attempted_signals = {}  # Track attempted signals

for strat_name, strategy in self.active_strategies.items():
    signal = self.signal_checker.get_signal(...)
    if signal != 0:
        signal_key = (strat_name, symbol, tf)
        bar_time = df.index[-2]
        
        if signal_key in self.attempted_signals and self.attempted_signals[signal_key] == bar_time:
            print("Already attempted on this bar, skipping")
            continue
        
        self.order_manager.open_position(...)
        self.attempted_signals[signal_key] = bar_time  # Mark as done
```

#### Fix 2: Order Validation (20 min)
**File:** `mt5_bridge/order_manager.py`
**Change:** Validate order structure before sending to MT5

**Add method:**
```python
def _validate_order(self, symbol, direction, lot):
    """Validate order parameters."""
    # 1. Check symbol exists
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol {symbol} not in market watch")
    
    # 2. Check lot size
    if lot < symbol_info.volume_min or lot > symbol_info.volume_max:
        raise ValueError(f"Lot {lot} outside [{symbol_info.volume_min}, {symbol_info.volume_max}]")
    
    # 3. Check liquidity
    if symbol_info.trade_tick_value == 0:
        raise ValueError(f"Symbol {symbol} has no liquidity")
    
    return True

def open_position(self, symbol, direction, lot, comment=""):
    """Open position with validation."""
    try:
        self._validate_order(symbol, direction, lot)
    except ValueError as e:
        print(f"Order validation failed: {e}")
        return None, str(e)
    
    # ... proceed with order creation ...
```

#### Fix 3: Data Freshness Check (15 min)
**File:** `forward_test/signal_checker.py`
**Change:** Warn if data is older than timeframe

**Add check:**
```python
def get_signal(self, strategy, symbol, timeframe):
    df = self.get_latest_data(symbol, timeframe)
    if df is None:
        return 0
    
    # Check data freshness
    latest_time = df.index[-1]
    from datetime import datetime, timedelta
    
    time_diff = datetime.utcnow() - latest_time
    timeframe_mins = {mt5.TIMEFRAME_M5: 5, mt5.TIMEFRAME_H1: 60, ...}[timeframe]
    
    if time_diff.total_seconds() > timeframe_mins * 60 * 1.5:
        print(f"WARNING: Data is {time_diff} old (>1.5 * {timeframe_mins}min)")
    
    # ... continue with signal generation ...
```

#### Fix 4: Market Watch Symbol Selection (15 min)
**File:** `mt5_bridge/connector.py`
**Change:** Add all symbols to market watch on connect

**Add code:**
```python
def connect(self):
    """Connect to MT5 and ensure all symbols are in market watch."""
    if not mt5.initialize():
        print("Failed to initialize MT5")
        return False
    
    # Ensure all trading symbols are in market watch
    required_symbols = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
    for symbol in required_symbols:
        if not mt5.symbol_select(symbol, True):
            print(f"Warning: Could not add {symbol} to market watch")
    
    # ... continue with login ...
```

### Testing Phase 0

After applying 4 fixes:
```bash
python scripts/run_paper.py

# Expected behavior:
# 1. No repeated "SIGNAL DETECTED" for same bar
# 2. Orders execute OR fail with clear error message
# 3. No "mt5.order_send returned None" loops
# 4. All symbols appear in MT5 market watch
# 5. "Data is X old" warnings (if any)
```

### Phase 0 Success Criteria

- ✅ Signal not repeated on same bar
- ✅ Clear error messages if order fails
- ✅ No infinite retry loop
- ✅ All symbols in market watch
- ✅ Bot runs stable for >5 minutes without error spam

---

## 📈 PHASE 1: Path B Quick Wins (After Phase 0)

**Status:** ⏳ Queued (Blocked by Phase 0)  
**Timeline:** 4 hours  
**Expected Outcome:** +8–10% win rate improvement

### Components

| # | Component | Status | Time | Improvement |
|---|-----------|--------|------|-------------|
| 00A | Ensemble Voting | ✅ DONE | 1 hr | +5–10% |
| 00B | BB Mean Reversion Fix | 📝 Ready | 1.5 hrs | +40% PF |
| 00C | Session Momentum Fix | 📝 Ready | 1 hr | +20% PF |

### Quick Reference

**STEP 00A:** Test Ensemble (30 min)
```bash
python strategies/ensemble.py  # Should pass
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
# Expected: ~14-16 trades, 58-62% win rate, PF 1.9-2.1
```

**STEP 00B:** BB Mean Reversion Fix (1.5 hrs)
- Edit `strategies/bb_mean_reversion.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 2"
- Test: `python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1`
- Expected: PF > 1.25

**STEP 00C:** Session Momentum Fix (1 hr)
- Edit `strategies/session_momentum.py`
- Guide: `PATH_B_IMPLEMENTATION.md` Section "Component 3"
- Test: `python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1`
- Expected: PF > 1.20

---

## 🔧 PHASE 2: Path B Medium Wins (After Phase 1)

**Status:** ⏳ Queued (Blocked by Phase 1)  
**Timeline:** 5.5 hours  
**Expected Outcome:** +12–15% aggregate win rate

### Components

| # | Component | Status | Time | Improvement |
|---|-----------|--------|------|-------------|
| 00D | Regime Filter | 📝 Ready | 3 hrs | +15–20% |
| 00E | Multi-TF Confirmation | 📝 Ready | 2.5 hrs | +8–12% |

### Architecture (Phase 2 Additions)

```
Current (Phase 0-1):
  Paper Engine → Signal Checker → Strategies → Orders

After Phase 2:
  Paper Engine → Signal Checker → Strategies
                      ↓
                  Regime Filter (macro context)
                      ↓
                Multi-TF Confirmation
                      ↓
                Orders to MT5
```

---

## 📋 PHASE 3: Original Tasks (After Path B)

**Status:** ⏳ Queued (Blocked by Phase 2)  
**Timeline:** 2–3 weeks  
**Scope:** Original STEP 00–20 from Phase 1 build

### Key Tasks

- STEP 00: Telegram Bot Fixes (7 fixes)
- STEP 0–5: Data Ingestion + Crypto Deployment
- STEP 19–20: Full System Test + Phase 1 Complete

### Parallel to Phase 3

While Phase 3 is running:
- Monitor paper trading performance (2–4 weeks)
- Verify strategies meet promotion criteria
- Prepare for Phase 2: Live Trading

---

## 🎯 OVERALL TIMELINE

```
NOW (2026-04-20):
  Phase 0: CRISIS MODE — Stabilize Bot
    └─ 1–2 hours: Apply 4 emergency fixes
    └─ Success: Bot runs stable, no retry loops

Week 1 (After Phase 0):
  Phase 1: Path B Quick Wins
    └─ 4 hours: Ensemble + BB Fix + Session Fix
    └─ Success: +8–10% win rate

Week 1–2:
  Phase 2: Path B Medium Wins
    └─ 5.5 hours: Regime Filter + Multi-TF
    └─ Success: +12–15% aggregate win rate

Week 2–4:
  Phase 3: Original Tasks + Demo Run
    └─ Telegram Fixes, Data Ingestion, System Test
    └─ 2–4 weeks: Stable demo run for promotion to live

Week 4+:
  Phase 4: LIVE TRADING (if Phase 1–3 pass)
    └─ Deploy to live account
    └─ Monitor real P&L, correlations, risk limits
```

**Total Project Duration:** 4–6 weeks to live trading (if all tests pass)

---

## 📊 Completion Breakdown

| Phase | Task | Status | Time | Cum. %|
|-------|------|--------|------|--------|
| 0 | Crisis Fix | ⏳ 1–2h | 1–2h | 15% |
| 1A | Ensemble Test | ✅ Ready | 0.5h | 20% |
| 1B | BB + Session Fix | ⏳ 2.5h | 3h | 30% |
| 2 | Regime + Multi-TF | ⏳ 5.5h | 8.5h | 50% |
| 3 | Telegram + System | ⏳ 20h | 28.5h | 75% |
| 4 | Demo Run (2–4w) | ⏳ 40–80h | 68–108h | 100% |

---

## 🚦 Current Blockers & Dependencies

```
BLOCKED NOW: Phase 1 ← Waiting for Phase 0
BLOCKED NOW: Phase 2 ← Waiting for Phase 1
BLOCKED NOW: Phase 3 ← Waiting for Phase 2
BLOCKED NOW: Live Trading ← Waiting for Phase 3 + 2–4 week demo run
```

**Critical Path:**
```
Phase 0 (1–2h) → Phase 1 (4h) → Phase 2 (5.5h) → Phase 3 (20h) → Demo (40–80h) → Live
```

---

## 📋 Files & Documentation

### Diagnostic & Planning
- ✅ `DIAGNOSTIC_REPORT.md` — Critical issues analysis + fixes
- ✅ `MASTER_PROJECT_STATUS.md` ← This file

### Path B Implementation
- ✅ `STRATEGY_ENHANCEMENT_PLAN.md` — Strategic rationale
- ✅ `PATH_B_IMPLEMENTATION.md` — Step-by-step guides (all 5 components)
- ✅ `PATH_B_BUILD_PROGRESS.md` — Progress tracking

### Original Tasks
- ✅ `AGENT_HANDOVER.md` — Updated with Path B priorities
- ✅ `Phase1_Execution_Plan.md` — Original Phase 1 build plan

---

## 🎓 What's Different from Original Plan

| Original Plan | Updated Plan | Reason |
|---------------|--------------|--------|
| Start with STEP 00 (Telegram fixes) | Phase 0 (Bot stabilization) first | Live bot is broken; need immediate fix |
| Then STEP 0–5 (data ingestion) | Then Phase 1 (Path B quick wins) | +10% win rate ROI is higher priority |
| Then STEP 19–20 (system test) | Then Phase 2 (Path B medium wins) | +15% cumulative win rate needed |
| Then STEP 00 Telegram fixes | Then original STEP 00–20 | Sequence corrected based on dependencies |

---

## ✅ Action Items

### For Leo (Right Now)

1. **Review** `DIAGNOSTIC_REPORT.md` (5 min)
2. **Decide:** Apply Phase 0 fixes now or have agent do it? (Decision)
3. **Coordinate:** If agent applies fixes, provide DIAGNOSTIC_REPORT + instructions

### For Agent (After Phase 0 Approval)

1. Read `DIAGNOSTIC_REPORT.md` (Section "Fixes Required")
2. Apply 4 emergency fixes to paper_engine.py, order_manager.py, etc.
3. Test bot with `python scripts/run_paper.py`
4. Report: No retry loops, clear error messages, stable for >5 min?
5. If ✓: Resume Path B (Components 00B–00C)

### Success Metrics

- **Phase 0 Done:** Bot runs >5 min without error loop
- **Phase 1 Done:** Ensemble backtests 58–62% win rate
- **Phase 2 Done:** Aggregate win rate 62–65% (10–13% improvement)
- **Phase 3 Done:** All 7 Telegram commands working
- **Demo Run:** 2–4 weeks stable trading < -15% drawdown
- **Go-Live:** All criteria met, ready for 0.1% of capital

---

## 🎯 Bottom Line

| Metric | Status |
|--------|--------|
| **Live Bot** | 🔴 Broken (retry loop) — Fix in Phase 0 (1–2h) |
| **Path B Status** | 🟡 10% (Ensemble done, 4 components queued) |
| **Overall Project** | 🟡 15% (Phase 0 + Phase 1A done) |
| **Next Milestone** | Phase 0 completion (2h) → Resume Path B (4h) |
| **Full Delivery** | 4–6 weeks (including 2–4 week demo run) |

---

**Next Action:** Apply Phase 0 emergency fixes or assign to agent with this document.
