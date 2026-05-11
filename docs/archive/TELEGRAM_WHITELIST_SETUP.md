# Telegram Bot Whitelist Setup Guide

**Date:** May 10, 2026  
**Status:** Ready to use  
**Updated:** Bot now shows your Chat ID for easy copying

---

## 🚀 Quick Start: Get Your Chat ID in 2 Minutes

### Option A: From Bot Error Message (Easiest)

Send any command to the **Raw-Demo** bot in Telegram:

```
/start
/help
/status
```

The bot will reply with:

```
⛔ Unauthorized

Your Chat ID:
5838483717

Add this to .env file:
ALLOWED_CHAT_IDS=5838483717
```

**✅ Copy that Chat ID** (it's in a code block for easy copying)

---

### Option B: Extract from Bot Logs (If Already Authorized)

If you've been added to the whitelist, you can also retrieve your Chat ID using:

```
/extract_chat_id
```

The bot responds with:

```
🔍 Your Chat ID
━━━━━━━━━━━━━━━━━━━━━━━━━

Chat ID:
5838483717

User: @yourname

To whitelist:
Add to .env:
ALLOWED_CHAT_IDS=5838483717
```

---

### Option C: View from Authorization Logs (Admin)

If you have access to the database, query the authorization logs:

```sql
SELECT chat_id, username, first_name, last_name, MAX(timestamp) as last_access
FROM telegram_auth_log
WHERE status = 'authorized'
GROUP BY chat_id, username, first_name, last_name
ORDER BY last_access DESC;
```

---

## Step 3: Add to .env File

**File Location:** `F:\REPOS\leo123xxx\TradePanel\TradePanel\.env`

**Current State:**
```bash
TELEGRAM_BOT_TOKEN=8710948452:AAEfavZLXrDl2ktAreNgYwRqPreFptp_RLA
TELEGRAM_CHAT_ID=5838483717
```

**Add This Line:**
```bash
ALLOWED_CHAT_IDS=5838483717
```

**Updated .env:**
```bash
TELEGRAM_BOT_TOKEN=8710948452:AAEfavZLXrDl2ktAreNgYwRqPreFptp_RLA
TELEGRAM_CHAT_ID=5838483717
ALLOWED_CHAT_IDS=5838483717
```

---

## Step 4: Restart Bot

**Option A: Via Python**
```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
python scripts/start_telegram_bot.py
```

**Option B: Via Task Scheduler**
1. Open Task Scheduler
2. Find: "TradePanel Telegram Bot" (or similar)
3. Right-click → Run

**Option C: Automatic (if scheduler task exists)**
Wait for next scheduled run

---

## Step 5: Test

Send any command in Telegram:

```
/start
```

**Expected Response:**
```
🤖 TradePanel Help

📊 Account & Positions
/status — System and account status
...
```

**If you see the help menu → ✅ Whitelisted!**

---

## ✅ Adding Multiple Users

If you want to allow other users (team members, etc.):

**In .env file:**
```bash
ALLOWED_CHAT_IDS=5838483717,9876543210,1122334455
```

**Steps:**
1. Each user sends `/start` to the bot
2. Get their Chat ID from the error message
3. Add to `ALLOWED_CHAT_IDS` (comma-separated, no spaces)
4. Restart bot
5. They can now use all commands

---

## 🔧 How the Whitelist Works

### Authorization Flow

```python
def auth_required(func):
    async def wrapper(update, context):
        chat_id = str(update.effective_chat.id)
        
        # Get allowed IDs from .env
        allowed = os.getenv("ALLOWED_CHAT_IDS", "").split(",")
        primary = os.getenv("TELEGRAM_CHAT_ID")
        
        # Check if user is in whitelist
        if chat_id not in [a.strip() for a in allowed if a.strip()]:
            # Show user their Chat ID
            show_error(f"Your Chat ID: {chat_id}")
            return
        
        # User authorized - execute command
        return await func(update, context)
```

### What Gets Checked

1. ✅ User's Chat ID extracted from Telegram message
2. ✅ Compared against `ALLOWED_CHAT_IDS` in .env
3. ✅ Also checks `TELEGRAM_CHAT_ID` (primary account)
4. ✅ If match found → Command executes
5. ❌ If no match → Shows error with Chat ID

---

## 📋 Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot's authentication token | `8710948452:AAE...` |
| `TELEGRAM_CHAT_ID` | Primary account Chat ID | `5838483717` |
| `ALLOWED_CHAT_IDS` | Whitelisted users (comma-separated) | `5838483717,1234567890` |

---

## 🔍 Finding Your Chat ID

### Method 1: From Bot Error (EASIEST)
1. Send any command to the bot
2. Read the error message
3. Your Chat ID is in the `<code>` block

### Method 2: Using @userinfobot
1. Open Telegram
2. Search for `@userinfobot`
3. Send `/start`
4. It shows your User ID

### Method 3: From .env
If you're the primary user, it's already in:
```bash
TELEGRAM_CHAT_ID=5838483717  # ← This is your Chat ID
```

---

## ✅ Troubleshooting

### Problem: Still Getting "Unauthorized" After Adding Chat ID

**Solution:**
1. ✅ Verify Chat ID copied correctly (no spaces)
2. ✅ Check .env file saved (Ctrl+S)
3. ✅ Restart the bot
4. ✅ Wait 10 seconds
5. ✅ Send command again

### Problem: Don't Know My Chat ID

**Solution:**
1. Send `/start` to the bot
2. Read the error response
3. Copy the Chat ID from the `<code>` block
4. Add to .env
5. Restart bot

### Problem: Multiple Users Not Working

**Check:**
1. Are all Chat IDs comma-separated?
   ```bash
   ALLOWED_CHAT_IDS=12345,67890,11111  ✅ CORRECT
   ALLOWED_CHAT_IDS=12345, 67890, 11111 ❌ WRONG (spaces)
   ```

2. No trailing commas:
   ```bash
   ALLOWED_CHAT_IDS=12345,67890  ✅ CORRECT
   ALLOWED_CHAT_IDS=12345,67890, ❌ WRONG (trailing comma)
   ```

3. Bot restarted after change

---

## 🎯 Common Scenarios

### Scenario 1: You're the Only User

```bash
# Option A: Use primary Chat ID
TELEGRAM_CHAT_ID=5838483717

# Option B: Use ALLOWED_CHAT_IDS
ALLOWED_CHAT_IDS=5838483717
```

**Both work the same way.** Use whichever feels natural.

---

### Scenario 2: You + Team Member

```bash
# Get both Chat IDs
ALLOWED_CHAT_IDS=5838483717,1234567890

# Restart bot
# Both users can now use all commands
```

---

### Scenario 3: You (Primary) + Multiple Users

```bash
# Keep primary in TELEGRAM_CHAT_ID
TELEGRAM_CHAT_ID=5838483717

# Add others to ALLOWED_CHAT_IDS
ALLOWED_CHAT_IDS=5838483717,1234567890,9876543210,5555555555
```

---

## 📚 Commands After Whitelisting

Once whitelisted, you can use:

```
/help              — Show all commands
/status            — Account status + positions
/balance           — Balance info
/active            — Open positions
/signals           — Recent signals
/backtest_report   — Last backtest results
/mode              — Active strategies
/pause [min]       — Pause bot temporarily
/resume            — Resume trading
/enable <name>     — Enable a strategy
/disable <name>    — Disable a strategy
```

---

## 🔐 Security Notes

✅ **Whitelist protects against:**
- Random Telegram users discovering your bot
- Unauthorized command execution
- Accidental token leaks

✅ **Best practices:**
- Keep Chat IDs private (don't share in public channels)
- Review `ALLOWED_CHAT_IDS` periodically
- Remove users when they leave the team
- Use strong `TELEGRAM_BOT_TOKEN` (already is)

---

## 📖 Implementation Details

### File: `notifications/telegram_bot.py`

**Authorization Decorator:**
```python
def auth_required(func):
    """Checks if user's Chat ID is whitelisted"""
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        allowed = os.getenv("ALLOWED_CHAT_IDS", "").split(",")
        primary = os.getenv("TELEGRAM_CHAT_ID")
        if primary:
            allowed.append(primary)
        
        if chat_id not in [a.strip() for a in allowed if a.strip()]:
            # NEW: Shows Chat ID for easy whitelisting
            await update.message.reply_html(
                f"⛔ <b>Unauthorized</b>\n\n"
                f"Your Chat ID:\n<code>{chat_id}</code>\n\n"
                f"Add this to .env file:\n<code>ALLOWED_CHAT_IDS={chat_id}</code>"
            )
            return
        
        return await func(self, update, context)
    return wrapper
```

**Applied To:** All command handlers
```python
@app.add_handler(CommandHandler("start", handler))

# Becomes:
@auth_required
async def handler(self, update, context):
    ...
```

---

## ✨ Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Send `/start` to bot | 10 sec |
| 2 | Copy Chat ID from error | 10 sec |
| 3 | Edit .env file | 30 sec |
| 4 | Restart bot | 10 sec |
| 5 | Test `/start` again | 10 sec |
| **Total** | **Full setup** | **~2 min** |

---

**Status:** Ready to whitelist ✅

Your bot will now show your Chat ID when you interact with it. Just copy it, add to .env, restart, and you're done!
