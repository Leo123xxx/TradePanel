# 🔴 CRITICAL ISSUES — Diagnostic Report

**Date:** 2026-04-20  
**Status:** Live bot failing with stale signals and order failures  
**Severity:** HIGH — Bot is stuck in retry loop

---

## Issues Identified

### 1. ❌ **Stale Signal Repetition** (PRIMARY ISSUE)

**Symptom:** Same signal `2026-04-19 20:00:00` detected multiple times
```
SIGNAL DETECTED: SELL for GBPUSD on 2026-04-19 20:00:00  [repeated 4+ times]
```

**Root Cause:** No signal deduplication or state management
- Signal checker fetches new data and generates signal
- But same bar keeps generating same signal
- **No tracking of which signals have been attempted**
- System retries the same signal indefinitely

**Files Involved:**
- `forward_test/signal_checker.py` — no signal state tracking
- `forward_test/paper_engine.py` — no deduplication logic

**Fix:** Add signal timestamp tracking to prevent duplicates

---

### 2. ❌ **MT5 Order Failure** (SECONDARY ISSUE)

**Symptom:** `mt5.order_send returned None`
```
EXECUTING: SELL 0.1 lots on GBPUSD
FAILED to open trade: mt5.order_send returned None (check connection or request format)
```

**Root Causes (Multiple):**
1. Order structure validation missing
2. Symbol not added to market watch
3. Order timing issue (trying to order on incomplete bar)
4. MT5 not fully initialized

**Files Involved:**
- `mt5_bridge/order_manager.py` — order creation/validation
- `forward_test/paper_engine.py` — order timing

**Fix:** Add order validation + symbol market watch + better error handling

---

### 3. ⚠️ **Data Freshness Issue** (CONTRIBUTING)

**Symptom:** Using 2026-04-19 data when current date is 2026-04-20
- Signal timestamp is from YESTERDAY
- Suggests MT5 isn't providing current bar data

**Root Cause:** 
- Possible: MT5 connection is stale
- Possible: Data gap (no new bar since yesterday)
- Possible: Timeframe mismatch (checking M5 when bar closed at H1)

**Fix:** Add data freshness check + force MT5 reconnect

---

## Project Structure Issues

### 📁 Current Structure Problems

```
TradePanel/
├── forward_test/
│   ├── paper_engine.py      ← Processes signals
│   └── signal_checker.py    ← Fetches live data + generates signals
├── mt5_bridge/
│   ├── order_manager.py     ← Sends orders
│   └── connector.py         ← MT5 connection
└── data/
    └── db_client.py         ← Database access
```

**Problems:**
1. ❌ No signal state tracking (which signals already attempted?)
2. ❌ No order validation before send (is order structure correct?)
3. ❌ No data freshness checks (is data current?)
4. ❌ No MT5 market watch management (symbol added?)
5. ❌ No retry logic with backoff (just loops immediately)

---

## What Needs to Happen

### IMMEDIATE FIXES (Critical — Do First)

#### Fix 1: Signal Deduplication (Paper Engine)
**Problem:** Same signal attempted repeatedly  
**Solution:** Track attempted signal bars by timestamp

```python
# Add to PaperEngine.__init__():
self.attempted_signals = {}  # {(strat_name, symbol, tf): timestamp}

# In _process_symbol(), before executing order:
signal_key = (strat_name, symbol, mt5_tf)
latest_bar_time = df_signals.index[-2]

if signal_key in self.attempted_signals:
    if self.attempted_signals[signal_key] == latest_bar_time:
        print(f"Signal already attempted on this bar, skipping")
        return

# After successful order attempt:
self.attempted_signals[signal_key] = latest_bar_time
```

#### Fix 2: Order Validation (Order Manager)
**Problem:** Sending malformed orders to MT5  
**Solution:** Validate order structure before send

```python
# Add to OrderManager.open_position():
def _validate_order(self, symbol, direction, lot):
    """Validate order parameters before sending to MT5."""
    # 1. Check symbol exists
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol {symbol} not in market watch")
    
    # 2. Check lot is valid
    if lot < symbol_info.volume_min or lot > symbol_info.volume_max:
        raise ValueError(f"Lot {lot} outside range [{symbol_info.volume_min}, {symbol_info.volume_max}]")
    
    # 3. Check volume exists
    if symbol_info.trade_tick_value == 0:
        raise ValueError(f"Symbol {symbol} has no liquidity")
    
    return True
```

#### Fix 3: Data Freshness Check (Signal Checker)
**Problem:** Using stale data  
**Solution:** Check that data is current

```python
# Add to SignalChecker.get_signal():
latest_time = datetime.fromtimestamp(df.index[-1].timestamp())
current_time = datetime.utcnow()

time_diff_sec = (current_time - latest_time).total_seconds()
if time_diff_sec > 300:  # 5 min for M5, adjust for timeframe
    print(f"WARNING: Data is {time_diff_sec}s old, may not be live")
```

#### Fix 4: Symbol Market Watch (Connector)
**Problem:** Symbol not selected in MT5  
**Solution:** Ensure all symbols are in market watch on connect

```python
# Add to MT5Connector.connect():
required_symbols = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
for symbol in required_symbols:
    if not mt5.symbol_select(symbol, True):
        print(f"Warning: Could not add {symbol} to market watch")
```

---

### STRUCTURAL IMPROVEMENTS (Next)

#### Fix 5: Retry Logic with Backoff
**Problem:** Immediate retry loop (floods MT5)  
**Solution:** Add exponential backoff

```python
# In PaperEngine.run_once():
self.failed_attempts = {}  # {(strat, symbol): (count, timestamp)}

# Before retry:
key = (strat_name, symbol)
if key in self.failed_attempts:
    count, last_time = self.failed_attempts[key]
    wait_secs = min(2 ** count, 60)  # Backoff: 1, 2, 4, 8, ... 60 sec
    if time.time() - last_time < wait_secs:
        print(f"Backoff: Waiting {wait_secs}s before retry")
        return
```

#### Fix 6: Separate Trading Intervals
**Problem:** Signal check and order execution on same loop  
**Solution:** Different frequencies

```python
# Run signal check every 1 min (frequent)
# Run order execution every 5 min (less frequent, less spam)
```

---

## Path Forward — Implementation Sequence

### Phase 1: Emergency Stabilization (1–2 hours)

1. **Add signal deduplication** (paper_engine.py)
   - Track (strat, symbol, bar_time)
   - Skip if already attempted
   
2. **Add order validation** (order_manager.py)
   - Check symbol exists
   - Check lot size valid
   - Check liquidity exists

3. **Add market watch setup** (connector.py)
   - Ensure symbols are selected on connect

4. **Add data freshness check** (signal_checker.py)
   - Print warning if data > 5 min old

5. **Test bot again**
   ```bash
   python scripts/run_paper.py
   # Should not retry same signal
   # Should validate orders
   # Should handle MT5 errors gracefully
   ```

### Phase 2: Structural Improvements (2–3 hours)

1. **Add backoff retry logic**
2. **Separate signal check from order execution**
3. **Add comprehensive logging**
4. **Add MT5 health checks**

### Phase 3: Path B Integration (After Stabilization)

- Resume Path B component builds (Components 2–5)
- Ensure new strategies work with stabilized bot

---

## Updated Master Plan — Where We Are

```
PHASE 0: CRISIS MODE — Fix Critical Issues
  ├─ ✅ Identified: Stale signals + order validation + data freshness
  ├─ ⏳ ACTION: Apply 4 emergency fixes (1–2 hrs)
  └─ ✅ TARGET: Bot runs without retry loop, orders work

PHASE 1: Path B Quick Wins (4 hours)
  ├─ ✅ STEP 00A: Ensemble (complete + ready to test)
  ├─ ⏳ STEP 00B: BB Mean Reversion Fix
  ├─ ⏳ STEP 00C: Session Momentum Fix
  └─ Expected: +8–10% win rate

PHASE 2: Path B Medium Wins (5.5 hours)
  ├─ ⏳ STEP 00D: Regime Filter
  ├─ ⏳ STEP 00E: Multi-TF Confirmation
  └─ Expected: +12–15% aggregate win rate

PHASE 3: Original Tasks (2–3 weeks)
  ├─ ⏳ STEP 00: Telegram Bot Fixes
  ├─ ⏳ STEP 0–5: Data Ingestion & Deployment
  ├─ ⏳ STEP 19–20: System Test & Phase 1 Complete
  └─ Expected: Phase 1 Ready for Go-Live

CURRENT STATUS:
  Phase 0: 30% (identified issues, need implementation)
  Phase 1: 10% (Ensemble done, Components 2–3 queued)
  Phase 2: 0% (queued after Phase 1)
  Phase 3: 0% (queued after Phase 2)
```

---

## Immediate Actions Required

**Step 1:** Apply 4 emergency fixes (see Phase 1 above)
**Step 2:** Test bot with `python scripts/run_paper.py`
**Step 3:** Verify: No repeated signals, orders execute or fail gracefully
**Step 4:** Resume Path B when bot is stable

**Estimated time:** 1–2 hours to stabilize

---

## Files That Need Changes

| File | Issue | Fix | Time |
|------|-------|-----|------|
| `forward_test/paper_engine.py` | No signal dedup | Track attempted signals | 30 min |
| `mt5_bridge/order_manager.py` | No validation | Validate order structure | 20 min |
| `forward_test/signal_checker.py` | No freshness check | Add timestamp validation | 15 min |
| `mt5_bridge/connector.py` | No market watch | Add symbol_select on connect | 15 min |

**Total:** ~80 minutes for emergency fixes

---

## Success Criteria — Phase 0 Complete

- ✅ Same signal not repeated on same bar
- ✅ Orders either execute OR fail with clear error (not return None)
- ✅ No infinite retry loop
- ✅ All symbols added to market watch
- ✅ Data freshness logged

Once Phase 0 is complete, resume Path B builds.

---

**RECOMMENDATION:** Do emergency fixes first (1–2 hrs), then resume Path B (9 hrs total after stabilization).

**Total new timeline:** 10–11 hours (3 hours emergency + 9 hours Path B)
