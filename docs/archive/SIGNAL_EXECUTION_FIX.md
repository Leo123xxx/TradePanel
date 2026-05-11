# Signal Execution Problem & Solution

**Date:** May 10, 2026  
**Status:** IDENTIFIED & SOLVABLE  
**Priority:** HIGH

---

## 🔍 PROBLEM IDENTIFIED

**Why are signals NOT being executed?**

Your system generated **8 signals today but 0% were executed** because:

### Root Cause: PAPER MODE IS ENABLED
```
config/config.yaml → system.mode = "paper"
```

**In PAPER MODE:**
- ✅ Signals ARE generated correctly
- ✅ Risk checks pass
- ✅ OrderManager receives execute commands
- ❌ **But trades are NOT submitted to MT5** (paper mode prevents live order submission)

---

## 📊 Current System State

```
✓ System Mode:           PAPER (not LIVE)
✓ Active Strategies:     28 strategies enabled
✓ Trading Hours:         00:30 - 23:59 (Mon-Fri)
✓ Signal Detection:      Working (8 signals generated)
✓ Risk Checks:           Passing
✓ OrderManager:          Ready (but paper mode blocks execution)
```

---

## 🛑 Why Signals Aren't Taken: Risk Check Pipeline

Before executing ANY signal, the system runs these checks (in order):

```python
def risk_manager.check_all(strategy, symbol, lot_size, direction):
    # 0. IS BOT PAUSED?
    if is_bot_paused():  # Checks for MANUAL_PAUSE or CIRCUIT_BREAKER
        return False, "Bot is paused"
    
    # 1. Blocked pairs?
    if pair in ["USDZAR", "USDTRY"]:
        return False, "Pair is blocked"
    
    # 2. Strategy enabled?
    if not strategy.enabled:
        return False, "Strategy disabled"
    
    # 3-12. Other checks (margin, spread, trading hours, regime, etc.)
    ...
    
    # If ALL pass:
    return True, "All checks passed"
    ↓
    order_manager.open_position()  # SUBMITS ORDER
```

**Any failed check = Signal NOT executed**

---

## 🚀 SOLUTION: Three Steps to Enable Signal Execution

### STEP 1: Change to LIVE MODE
Edit `config/config.yaml`:

```yaml
system:
  mode: live          # ← Change from "paper" to "live"
  docker_enabled: true
```

**Effect:** Orders will now be submitted to MT5 immediately when signals trigger.

### STEP 2: Resume Bot (if paused)
```
Telegram: /status
          ↓
          Shows "⏸ BOT PAUSED" ?
          ↓
          /resume
```

**Why:** The bot might be manually paused via `/pause` command, blocking all trades.

### STEP 3: Verify Setup
```
Telegram: /status      → Check bot is ACTIVE
Telegram: /balance     → Verify account has free margin
Telegram: /mode        → Confirm live mode & 28 strategies active
Telegram: /signals     → Next signal will show trade approval option
```

---

## 🎯 IMPLEMENTATION: Signal Approval System

You want: **"Test the click for approval so we understand how it works end to end"**

This requires implementing a 3-part approval system:

### Part 1: Telegram Command (notifications/router.py)

Add new command:
```python
def approve_trade(self, signal_id: str) -> str:
    """
    Approve a pending signal for execution.
    Usage: /approve_trade <signal_id>
    """
    try:
        # 1. Find pending signal in database
        query = """
            SELECT signal_id, strategy_id, pair, direction FROM signals
            WHERE signal_id = %s AND approval_status = 'PENDING'
        """
        result = self.db.execute_query(query, (signal_id,))
        if not result:
            return f"❌ Signal not found or already approved/rejected"
        
        sig_id, strat_id, pair, direction = result[0]
        
        # 2. Update signal approval status
        self.db.execute_query(
            "UPDATE signals SET approval_status = 'APPROVED', approved_at = NOW() "
            "WHERE signal_id = %s",
            (signal_id,)
        )
        
        # 3. Notify user
        return (
            f"✅ Signal APPROVED\n"
            f"Strategy: {strat_id}\n"
            f"Pair: {pair} {direction}\n"
            f"Will execute on next cycle"
        )
    except Exception as e:
        return f"❌ Error: {e}"

def reject_trade(self, signal_id: str) -> str:
    """Reject a pending signal."""
    try:
        self.db.execute_query(
            "UPDATE signals SET approval_status = 'REJECTED', rejected_at = NOW() "
            "WHERE signal_id = %s",
            (signal_id,)
        )
        return f"❌ Signal rejected and will not execute"
    except Exception as e:
        return f"❌ Error: {e}"
```

### Part 2: Database Schema Update (signals table)

Add columns:
```sql
ALTER TABLE signals ADD COLUMN approval_status VARCHAR(20) DEFAULT 'AUTO';
-- Values: 'AUTO' (execute immediately), 'PENDING' (wait for approval), 'APPROVED', 'REJECTED'

ALTER TABLE signals ADD COLUMN approval_required BOOLEAN DEFAULT FALSE;
ALTER TABLE signals ADD COLUMN approved_at TIMESTAMP;
ALTER TABLE signals ADD COLUMN rejected_at TIMESTAMP;
```

### Part 3: Paper Engine (forward_test/paper_engine.py)

Check approval before executing:
```python
# In _process_symbol() method, before open_position():

# Check if signal requires approval
if signal_approval_required:
    approval_status = self._get_signal_approval(signal_id)
    
    if approval_status == 'PENDING':
        print(f"[PENDING] Signal {signal_id} awaiting Telegram approval")
        return  # Don't execute yet
    
    if approval_status == 'REJECTED':
        print(f"[REJECTED] Signal {signal_id} was rejected by user")
        return  # Don't execute
    
    # 'APPROVED' or 'AUTO' = proceed with execution

# Execute the trade
res, msg = self.order_manager.open_position(...)
```

---

## 📋 Configuration: Enable Approval Mode (Optional)

Add to `config/config.yaml`:

```yaml
risk_management:
  signal_approval_required: false   # true = require Telegram approval
  auto_approve_after_minutes: 5     # Auto-execute if not approved in 5 min
  approval_notif_channel: "main"    # Send approval requests to main channel
```

---

## 🔧 Implementation Sequence

### Quick Start (RECOMMENDED - No Approval)
1. Edit `config/config.yaml`: Change `mode: "paper"` → `mode: "live"`
2. Telegram: `/resume` (if bot paused)
3. Wait for next signal
4. Trade will execute automatically

### With Approval Flow
1. Complete Quick Start above
2. Add columns to `signals` table (SQL above)
3. Update `router.py` with approve/reject commands
4. Update `paper_engine.py` to check approval status
5. Set `config.yaml` → `signal_approval_required: true`
6. Test: Next signal will wait for Telegram approval

---

## 📊 End-to-End Testing Workflow

### Test Scenario: Manual Approval

```
1. Signal Generated
   └─> Strategy detects EURUSD BUY setup
   └─> Signal stored in DB with approval_status='PENDING'
   
2. Telegram Notification
   └─> Bot sends: "🛰 New Signal Approval Needed"
   │   └─> EURUSD BUY | 0.1 lot | SL: 1.0500 | TP: 1.0600
   │   └─> [✅ APPROVE] [❌ REJECT] [⏭️ AUTO-EXPIRE]

3. User Action
   └─> Click: ✅ APPROVE
   └─> Command: /approve_trade <signal_id>
   
4. Execution
   └─> approval_status updated to 'APPROVED'
   └─> Paper engine sees APPROVED status
   └─> order_manager.open_position() called
   └─> Order submitted to MT5
   └─> Position opens in account
   
5. Confirmation
   └─> Telegram: "✅ Trade Executed"
   │   └─> EURUSD BUY 0.1 lot @ 1.0550
   │   └─> SL: 1.0500 | TP: 1.0600
   │   └─> Ticket: 12345678
   
6. Position Management
   └─> telegram /active  → Shows open position
   └─> Breakeven management kicks in
   └─> Reversal signals close position
   └─> Or targets hit automatically
```

---

## ✅ Verification Checklist

After implementing, verify with:

```
□ /status           → Bot shows ACTIVE (not PAUSED)
□ /balance          → Account has free margin
□ /mode             → Shows 28 active strategies, LIVE mode
□ /signals          → Shows recent signals
□ /active           → Shows open positions (after first trade)
□ logs              → results/cleanup_backup.log shows trade execution
```

---

## 🎓 How Manual Approval Works: Flow Diagram

```
SIGNAL GENERATED
    ↓
Is approval_required?
    ├─ NO → Execute immediately (current behavior)
    │
    └─ YES → Send approval request to Telegram
        ↓
    User receives: "New Trade Approval Needed"
        ↓
    User clicks: [✅ APPROVE] or [❌ REJECT]
        ↓
    ┌───────────────┬──────────────┐
    ↓               ↓              ↓
[APPROVED]     [REJECTED]    [AUTO-EXPIRED after 5 min]
    ↓               ↓              ↓
Execute      Don't execute   Execute/Reject
order        signal          based on setting
    ↓
Order sent to MT5
    ↓
Position opens
    ↓
Manage position (breakeven, reversal, TP/SL)
```

---

## 🚨 Important Notes

1. **Paper Mode vs Live Mode**
   - Paper: Signals generated, risk checks pass, but NO trades sent to MT5
   - Live: Signals → Risk checks → OrderManager → MT5 (REAL TRADES)

2. **Approval vs Paper Mode**
   - These are INDEPENDENT settings
   - Approval = Manual gate before execution
   - Paper/Live mode = Where orders are sent
   - You need BOTH: Live mode + (Optional) Approval

3. **Signal Execution Interval**
   - Signals checked every 15 minutes (signal_outcome_check_interval: 900s)
   - If signal approval required: Wait for approval during this check
   - After 5 minutes: Auto-execute or auto-reject (configurable)

4. **Risk Checks Run First**
   - Approval gate comes AFTER risk checks pass
   - If risk check fails: Signal blocked before approval gate

---

## 📞 Troubleshooting

**Q: I changed to live mode but signals still not executing**  
A: Check if bot is paused: Telegram `/status` → `/resume`

**Q: Telegram shows "RiskCheck Failed" in signal entry**  
A: One of 12 risk checks is blocking the signal:
   - Check margin (balance sufficient?)
   - Check trading hours (within allowed times?)
   - Check spread (too wide?)
   - Check regime filters (macro bias?)

**Q: Approval button not showing up**  
A: Need to implement Part 1-3 of approval system (code above)

**Q: Signal took too long to execute**  
A: Normal - checked every 15 minutes, takes 1-2 cycles to process

---

## 📝 Files to Modify

```
1. config/config.yaml
   └─ system.mode: change "paper" → "live"

2. notifications/router.py (OPTIONAL - for approval)
   └─ Add: approve_trade(), reject_trade() methods
   └─ Add to help text: /approve_trade, /reject_trade

3. forward_test/paper_engine.py (OPTIONAL - for approval)
   └─ Add approval check in _process_symbol()

4. Database schema (OPTIONAL - for approval)
   └─ ALTER TABLE signals ADD approval columns
```

---

## ✨ Summary

**Root Cause:** System in PAPER mode  
**Quick Fix:** Change `config.yaml` mode to "live"  
**Expected Result:** Signals will execute as trades  
**Next Step:** Implement approval flow (optional but recommended)

Ready to test? Edit config/config.yaml and set `system.mode: live` 🚀
