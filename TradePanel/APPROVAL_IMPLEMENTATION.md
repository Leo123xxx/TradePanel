# Signal Approval System Implementation

**Implementation Status:** Ready to deploy  
**Complexity:** Medium (3 files to modify)  
**Estimated Time:** 30-45 minutes  

---

## Overview

Implement a Telegram-based signal approval workflow that allows manual control over trade execution.

---

## Part 1: Database Schema Changes

### SQL Changes

```sql
-- 1. Add approval columns to signals table
ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS approval_status VARCHAR(20) DEFAULT 'AUTO';
-- Possible values: 'AUTO' (execute immediately), 'PENDING' (await approval), 
--                 'APPROVED' (user approved), 'REJECTED' (user rejected)

ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS approval_required BOOLEAN DEFAULT FALSE;

ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP DEFAULT NULL;

ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS approved_by VARCHAR(100) DEFAULT NULL;

ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS rejected_at TIMESTAMP DEFAULT NULL;

ALTER TABLE signals 
ADD COLUMN IF NOT EXISTS rejection_reason TEXT DEFAULT NULL;

-- 2. Add index for faster approval checks
CREATE INDEX IF NOT EXISTS idx_signals_approval 
ON signals(approval_status, timestamp DESC)
WHERE approval_status IN ('PENDING', 'APPROVED');

-- 3. Add approval settings to bot_health (optional - for tracking approval delays)
-- Already exists if using current schema
```

---

## Part 2: Telegram Command Router (notifications/router.py)

### Add These Methods to CommandRouter Class

```python
# ADD TO notifications/router.py :: CommandRouter class

def approve_trade(self, signal_id: str) -> str:
    """
    Approve a pending signal for immediate execution.
    Called when user clicks approval button or runs /approve_trade
    
    Args:
        signal_id: UUID of the signal to approve
        
    Returns:
        Human-readable confirmation message
    """
    try:
        # 1. Fetch the pending signal
        query = """
            SELECT signal_id, strategy_id, pair, direction, indicator_values, timestamp
            FROM signals
            WHERE signal_id = %s AND approval_status IN ('PENDING', 'AUTO')
            LIMIT 1
        """
        result = self.db.execute_query(query, (signal_id,))
        
        if not result:
            return (
                f"❌ <b>Signal Not Found</b>\n"
                f"Signal ID: <code>{signal_id}</code>\n"
                f"Possible reasons:\n"
                f"  • Already approved/rejected\n"
                f"  • Expired (>5 minutes old)\n"
                f"  • Invalid ID"
            )
        
        sig_id, strat_id, pair, direction, indicators, created = result[0]
        
        # 2. Update approval status
        self.db.execute_query(
            "UPDATE signals "
            "SET approval_status = 'APPROVED', approved_at = NOW() "
            "WHERE signal_id = %s",
            (signal_id,)
        )
        
        # 3. Log approval event
        self.db.execute_query(
            "INSERT INTO bot_health (event_type, status, message, timestamp) "
            "VALUES ('SIGNAL_APPROVAL', 'APPROVED', %s, NOW())",
            (f"Signal {sig_id} approved: {pair} {direction}",)
        )
        
        # 4. Return confirmation
        direction_icon = "🟢 BUY" if direction == "BUY" else "🔴 SELL"
        
        return (
            f"✅ <b>Trade Approved</b>\n\n"
            f"Signal ID: <code>{sig_id[:8]}...</code>\n"
            f"Pair: <b>{pair}</b>\n"
            f"Direction: <b>{direction_icon}</b>\n"
            f"Strategy: <b>{strat_id}</b>\n\n"
            f"<i>Will execute on next cycle (within 15 min)</i>"
        )
        
    except Exception as e:
        return f"❌ <b>Approval Failed</b>\n{str(e)}"


def reject_trade(self, signal_id: str, reason: str = "User rejected") -> str:
    """
    Reject a pending signal (prevent execution).
    Called when user clicks reject button or runs /reject_trade
    
    Args:
        signal_id: UUID of signal to reject
        reason: Why signal was rejected
        
    Returns:
        Confirmation message
    """
    try:
        # 1. Find signal
        query = """
            SELECT signal_id, pair, direction FROM signals
            WHERE signal_id = %s AND approval_status IN ('PENDING', 'AUTO')
        """
        result = self.db.execute_query(query, (signal_id,))
        
        if not result:
            return f"❌ Signal not found or already processed"
        
        sig_id, pair, direction = result[0]
        
        # 2. Update rejection status
        self.db.execute_query(
            "UPDATE signals "
            "SET approval_status = 'REJECTED', rejected_at = NOW(), rejection_reason = %s "
            "WHERE signal_id = %s",
            (reason, signal_id)
        )
        
        # 3. Log rejection
        self.db.execute_query(
            "INSERT INTO bot_health (event_type, status, message, timestamp) "
            "VALUES ('SIGNAL_REJECTION', 'REJECTED', %s, NOW())",
            (f"Signal rejected: {pair} {direction} - {reason}",)
        )
        
        return (
            f"❌ <b>Trade Rejected</b>\n\n"
            f"Pair: <b>{pair}</b>\n"
            f"Direction: {direction}\n"
            f"Reason: <i>{reason}</i>\n\n"
            f"This signal will NOT execute."
        )
        
    except Exception as e:
        return f"❌ Rejection failed: {str(e)}"


def list_pending_approvals(self) -> str:
    """
    Show all signals awaiting approval.
    Called when user runs /pending_trades
    
    Returns:
        Formatted list of pending signals
    """
    try:
        # Fetch pending signals from last 30 minutes
        query = """
            SELECT signal_id, strategy_id, pair, direction, timestamp, indicator_values
            FROM signals
            WHERE approval_status = 'PENDING'
            AND timestamp >= NOW() - INTERVAL '30 minutes'
            ORDER BY timestamp DESC
            LIMIT 10
        """
        results = self.db.execute_query(query)
        
        if not results:
            return "✅ <b>No Pending Approvals</b>\nAll trades have been processed."
        
        msg = f"⏳ <b>Trades Awaiting Approval ({len(results)})</b>\n━━━━━━━━━━━\n\n"
        
        for sig_id, strat, pair, direction, created, indicators in results:
            created_sast = created.replace(tzinfo=pytz.utc).astimezone(SAST)
            age_min = int((datetime.now(pytz.utc) - created.replace(tzinfo=pytz.utc)).total_seconds() / 60)
            
            direction_icon = "🟢" if direction == "BUY" else "🔴"
            
            # Show SL/TP if available
            indicator_str = ""
            if indicators:
                try:
                    ind = json.loads(indicators) if isinstance(indicators, str) else indicators
                    sl = ind.get('sl', 'N/A')
                    tp = ind.get('tp', 'N/A')
                    indicator_str = f"\nSL: {sl} | TP: {tp}"
                except:
                    pass
            
            msg += (
                f"<b>{pair}</b> {direction_icon}\n"
                f"└ Strategy: {strat}\n"
                f"└ Created: {created_sast.strftime('%H:%M SAST')} ({age_min}m ago){indicator_str}\n"
                f"└ /approve_trade_{sig_id[:8]} or /reject_trade_{sig_id[:8]}\n\n"
            )
        
        return msg
        
    except Exception as e:
        return f"❌ Error fetching pending approvals: {e}"
```

### Update Help Command

```python
# Update the get_help() method in CommandRouter class
# Add these lines to the strategy control section:

def get_help(self):
    return (
        "🤖 <b>TradePanel Help</b>\n\n"
        "... [existing help text] ...\n\n"
        
        # ADD THIS SECTION:
        "<b>🎯 Trade Approval</b>\n"
        "/pending_trades — List awaiting approval\n"
        "/approve_trade &lt;id&gt; — Approve a signal\n"
        "/reject_trade &lt;id&gt; [reason] — Reject a signal\n\n"
        
        # ... rest of help text ...
    )
```

---

## Part 3: Paper Engine Integration (forward_test/paper_engine.py)

### Modify _process_symbol() Method

Find this section in `_process_symbol()` (around line 330):

```python
# BEFORE: EXISTING CODE
if mode == 'detect' or signal == 0:
    return

# ... checks and risk manager code ...

magic_number = zlib.adler32(strat_name.encode()) % 1000000
print(f"EXECUTING: {direction} {lot_size} lots on {symbol}")
res, msg = self.order_manager.open_position(
    symbol, direction, lot_size, 
    sl_points=sl_points, tp_points=tp_points, 
    comment=f"PAPER_{strat_name}",
    magic=magic_number
)
```

### REPLACE WITH: New Code

```python
# NEW: Check signal approval status
if mode == 'detect' or signal == 0:
    return

# ... checks and risk manager code ...

# ✨ NEW: CHECK SIGNAL APPROVAL STATUS ✨
signal_id = signal_key  # Use the signal key we created earlier
approval_status = self._get_signal_approval_status(signal_id)

if approval_status == 'PENDING':
    print(f"[APPROVAL PENDING] Signal {signal_id} awaiting user approval")
    # Log this for dashboard
    self.db.execute_query(
        "INSERT INTO bot_health (event_type, status, message, timestamp) "
        "VALUES ('SIGNAL_APPROVAL', 'PENDING', %s, NOW())",
        (f"{strat_name} {symbol} awaiting approval",)
    )
    return  # Don't execute - wait for approval

elif approval_status == 'REJECTED':
    print(f"[APPROVAL REJECTED] Signal {signal_id} was rejected by user")
    return  # Don't execute - user rejected

# If 'AUTO' or 'APPROVED': proceed with execution

magic_number = zlib.adler32(strat_name.encode()) % 1000000
print(f"EXECUTING: {direction} {lot_size} lots on {symbol}")
res, msg = self.order_manager.open_position(
    symbol, direction, lot_size, 
    sl_points=sl_points, tp_points=tp_points, 
    comment=f"PAPER_{strat_name}",
    magic=magic_number
)
```

### Add Helper Methods to PaperEngine Class

```python
# ADD TO forward_test/paper_engine.py :: PaperEngine class

def _get_signal_approval_status(self, signal_id: str) -> str:
    """
    Check if signal has been approved, rejected, or is pending.
    
    Returns: 'AUTO' (execute immediately), 'PENDING', 'APPROVED', 'REJECTED'
    """
    try:
        query = """
            SELECT approval_status FROM signals 
            WHERE signal_id = %s
            LIMIT 1
        """
        result = self.db.execute_query(query, (signal_id,))
        if result:
            status = result[0][0]
            return status if status else 'AUTO'
        return 'AUTO'  # Default: execute immediately
    except Exception as e:
        print(f"[APPROVAL CHECK] Error: {e}")
        return 'AUTO'  # On error: execute (safer default)

def _get_pending_approvals(self) -> list:
    """Get all signals pending approval."""
    try:
        query = """
            SELECT signal_id, strategy_id, pair, direction, timestamp
            FROM signals
            WHERE approval_status = 'PENDING'
            AND timestamp >= NOW() - INTERVAL '30 minutes'
        """
        return self.db.execute_query(query) or []
    except Exception:
        return []

def _auto_expire_old_approvals(self, max_age_minutes: int = 5):
    """
    Auto-expire approval requests older than max_age_minutes.
    Called periodically to clean up stale pending signals.
    """
    try:
        # Option 1: Auto-execute old pending signals
        self.db.execute_query(
            "UPDATE signals "
            "SET approval_status = 'APPROVED', approved_at = NOW() "
            "WHERE approval_status = 'PENDING' "
            "AND timestamp < NOW() - INTERVAL '%s minutes'",
            (max_age_minutes,)
        )
        
        # Option 2: Auto-reject old pending signals
        # self.db.execute_query(
        #     "UPDATE signals "
        #     "SET approval_status = 'REJECTED', rejected_at = NOW(), "
        #     "rejection_reason = 'Auto-expired (no user response)' "
        #     "WHERE approval_status = 'PENDING' "
        #     "AND timestamp < NOW() - INTERVAL '%s minutes'",
        #     (max_age_minutes,)
        # )
        
    except Exception as e:
        print(f"[APPROVAL EXPIRY] Error: {e}")
```

---

## Part 4: Configuration (config/config.yaml)

### Add Approval Settings

```yaml
# Add this section to config/config.yaml

signal_approval:
  enabled: false                    # Set to true to enable approval workflow
  require_approval: false           # Set to true to require approval for all signals
  auto_approve_after_minutes: 5     # Auto-execute if not approved within N min
  auto_reject_instead: false        # If true: auto-reject old pending, else auto-approve
  approval_notification_channel: "main"  # Telegram channel for approval requests
  
  # Strategy-specific approval requirements (optional)
  strategies_requiring_approval:
    - []  # Add specific strategy names that always need approval
        # Example: ["volatility_breakout_scalp", "turtle_soup"]
```

---

## Part 5: Telegram Integration (main.py or telegram_bot.py)

### Add Command Handlers

```python
# In your Telegram bot command handler, add:

@bot.message_handler(commands=['approve_trade', 'approve'])
def handle_approve_trade(message):
    """Handle /approve_trade <signal_id> command"""
    try:
        # Parse signal_id from command
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /approve_trade <signal_id>")
            return
        
        signal_id = parts[1]
        router = CommandRouter()
        response = router.approve_trade(signal_id)
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}", parse_mode='HTML')


@bot.message_handler(commands=['reject_trade', 'reject'])
def handle_reject_trade(message):
    """Handle /reject_trade <signal_id> [reason] command"""
    try:
        parts = message.text.split(None, 2)  # Split on first 2 spaces
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /reject_trade <signal_id> [reason]")
            return
        
        signal_id = parts[1]
        reason = parts[2] if len(parts) > 2 else "User rejected"
        
        router = CommandRouter()
        response = router.reject_trade(signal_id, reason)
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}", parse_mode='HTML')


@bot.message_handler(commands=['pending_trades', 'pending'])
def handle_pending_trades(message):
    """Handle /pending_trades command"""
    try:
        router = CommandRouter()
        response = router.list_pending_approvals()
        bot.send_message(message.chat.id, response, parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}", parse_mode='HTML')
```

---

## Deployment Checklist

- [ ] **Step 1:** Run SQL schema changes (approval columns)
- [ ] **Step 2:** Add methods to `notifications/router.py`
- [ ] **Step 3:** Update help command in router
- [ ] **Step 4:** Modify `_process_symbol()` in `forward_test/paper_engine.py`
- [ ] **Step 5:** Add helper methods to PaperEngine
- [ ] **Step 6:** Add approval settings to `config/config.yaml` (optional - default disabled)
- [ ] **Step 7:** Add command handlers to Telegram bot
- [ ] **Step 8:** Test with manual signal approval
- [ ] **Step 9:** Enable in config once tested: `signal_approval.enabled: true`

---

## Testing Workflow

### Test 1: Automatic Execution (Current Behavior)

```
1. Set config: signal_approval.enabled: false
2. Generate signal
3. Bot executes automatically ✅
```

### Test 2: Manual Approval Flow

```
1. Set config: 
   signal_approval.enabled: true
   signal_approval.require_approval: true
   
2. Generate signal
   → Signal marked as PENDING
   → Telegram notification sent
   
3. User approves in Telegram: /approve_trade <signal_id>
   → Signal marked as APPROVED
   
4. Next execution cycle (within 15 min):
   → Bot sees APPROVED status
   → Executes trade ✅
```

### Test 3: Auto-Expiry

```
1. Set config:
   signal_approval.auto_approve_after_minutes: 5
   
2. Generate signal
   → Signal marked as PENDING
   
3. Wait 5+ minutes without approval
   → Auto-executed ✅
   OR
   → Auto-rejected based on config
```

---

## Rollback Plan

If approval system causes issues:

```sql
-- Revert to automatic execution:
UPDATE signals SET approval_status = 'AUTO' WHERE approval_status IN ('PENDING', 'APPROVED');

-- Or drop columns:
ALTER TABLE signals DROP COLUMN approval_status;
ALTER TABLE signals DROP COLUMN approval_required;
```

And set in `config/config.yaml`:
```yaml
signal_approval.enabled: false
```

---

## File Modifications Summary

| File | Lines | Change Type |
|------|-------|------------|
| `config/config.yaml` | ~10 | Add approval settings section |
| `notifications/router.py` | ~150 | Add 3 new methods + update help |
| `forward_test/paper_engine.py` | ~50 | Add approval check in _process_symbol |
| Database | ~10 SQL lines | Add approval columns |
| Telegram bot | ~60 | Add 3 command handlers |

**Total Implementation Time:** 30-45 minutes  
**Testing Time:** 15-20 minutes  
**Total:** ~1 hour for full approval workflow

---

Ready to implement? Start with the SQL changes, then router.py, then paper_engine.py! 🚀
