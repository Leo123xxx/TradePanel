# Authorization Logging Implementation Guide

**Status:** Ready to integrate  
**Created:** May 10, 2026  
**Complexity:** Low-Medium (1-2 hours to integrate)

---

## 📋 Overview

This guide shows how to integrate authorization logging into your Telegram bot. All code is ready—you just need to add it to your existing files.

**What gets added:**
- Database table for tracking auth attempts (authorized & unauthorized)
- Python module for logging and querying auth data
- 5 new Telegram commands for viewing authorization logs
- Updated documentation

---

## ✅ Integration Steps

### Step 1: Create Database Schema

**File:** `database/migrations/auth_logging.sql`  
**Status:** ✅ Created and ready

Run this SQL in your database:

```bash
# Connect to your PostgreSQL database
psql -h localhost -U tradepanel -d tradepanel -f database/migrations/auth_logging.sql
```

This creates:
- `telegram_auth_log` table
- 3 indexes for fast lookups
- 3 views for analysis (`telegram_unauthorized_attempts`, `telegram_authorized_users`, `telegram_auth_daily_summary`)

---

### Step 2: Add Authorization Logger Module

**File:** `notifications/auth_logger.py`  
**Status:** ✅ Created and ready

This module handles:
- Logging auth attempts to the database
- Querying unauthorized attempts
- Listing authorized users
- Finding suspicious patterns
- Daily summaries

No changes needed—just use as-is.

---

### Step 3: Add Authorization Commands

**File:** `notifications/auth_commands.py`  
**Status:** ✅ Created and ready

This module provides 5 new commands:
- `/extract_chat_id` — Show your Chat ID (for authorized users)
- `/auth_log` — Show unauthorized attempts (admin)
- `/auth_users` — Show authorized users (admin)
- `/auth_daily` — Daily summary (admin)
- `/suspicious` — Find suspicious patterns (admin)

No changes needed—just use as-is.

---

### Step 4: Integrate into telegram_bot.py

**File:** `notifications/telegram_bot.py`  
**Action:** Modify existing file

#### 4a. Add imports at the top:

```python
from notifications.auth_logger import AuthorizationLogger
from notifications.auth_commands import AuthorizationCommands
```

#### 4b. Modify `__init__` method:

```python
class TelegramBot:
    MAX_MSG_LEN = 4096

    def __init__(self):
        load_dotenv()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.router = CommandRouter()
        self.app = None
        self.dashboard_process = None
        
        # NEW: Initialize auth logger and commands
        self.auth_logger = AuthorizationLogger(db_connection=None)  # or your DB object
        self.auth_commands = AuthorizationCommands(db_connection=None)  # or your DB object
```

#### 4c. Modify `auth_required` decorator:

Replace the current decorator with:

```python
def auth_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        
        allowed = os.getenv("ALLOWED_CHAT_IDS", "").split(",")
        primary = os.getenv("TELEGRAM_CHAT_ID")
        if primary:
            allowed.append(primary)
        
        if chat_id not in [a.strip() for a in allowed if a.strip()]:
            # NEW: Log unauthorized attempt
            self.auth_logger.log_attempt(
                chat_id=int(chat_id),
                status="unauthorized",
                command=update.message.text.split()[0] if update.message.text else "unknown",
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            logger.warning(f"Unauthorized access attempt: {chat_id}")
            await update.message.reply_html(
                f"⛔ <b>Unauthorized</b>\n\n"
                f"Your Chat ID:\n<code>{chat_id}</code>\n\n"
                f"Add this to <code>.env</code> file:\n<code>ALLOWED_CHAT_IDS={chat_id}</code>"
            )
            return
        
        # NEW: Log authorized attempt
        self.auth_logger.log_attempt(
            chat_id=int(chat_id),
            status="authorized",
            command=update.message.text.split()[0] if update.message.text else "unknown",
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        
        return await func(self, update, context)
    return wrapper
```

#### 4d. Register new commands in `start()` method:

Add to the handlers list (around line 116):

```python
handlers = [
    # ... existing handlers ...
    ("extract_chat_id",  self.auth_commands.extract_chat_id_command),
    ("auth_log",         self.auth_commands.auth_log_command),
    ("auth_users",       self.auth_commands.auth_users_command),
    ("auth_daily",       self.auth_commands.auth_daily_command),
    ("suspicious",       self.auth_commands.suspicious_command),
]
```

---

### Step 5: Verify Database Connection (Optional)

If you want to actually log to the database, update the initialization:

```python
from database import get_connection  # or however you get DB connection

class TelegramBot:
    def __init__(self):
        # ... existing code ...
        
        # Connect to database
        try:
            db = get_connection()
            self.auth_logger = AuthorizationLogger(db_connection=db)
            self.auth_commands = AuthorizationCommands(db_connection=db)
        except Exception as e:
            logger.warning(f"Database connection failed: {e} - Using log-only mode")
            self.auth_logger = AuthorizationLogger(db_connection=None)
            self.auth_commands = AuthorizationCommands(db_connection=None)
```

If `db_connection=None`, logging happens to console only (safe for testing).

---

## 📊 How It Works

### Authorization Flow (Updated)

```
User sends message
    ↓
Extract Chat ID, username, first name, last name
    ↓
Check against ALLOWED_CHAT_IDS in .env
    ↓
If NOT authorized:
    ├─ Log to database/console: chat_id, username, command, status="unauthorized"
    └─ Show Chat ID + error
    
If authorized:
    ├─ Log to database/console: chat_id, username, command, status="authorized"
    └─ Execute command
    ↓
Format response
    ↓
Send to Telegram
```

### Database Tables

**`telegram_auth_log`** — Raw authorization events
```
| id | chat_id | username | first_name | last_name | status | command | timestamp |
|----|---------|----------|-----------|-----------|--------|---------|-----------|
| 1  | 5838483717 | leo123 | Leo | M | authorized | /status | 2026-05-10 16:45:30 |
| 2  | 9876543210 | unknown | NULL | NULL | unauthorized | /status | 2026-05-10 15:30:00 |
```

**`telegram_unauthorized_attempts`** (View) — Suspicious access
```
Shows Chat IDs with multiple unauthorized attempts
Helps identify bot discovery attacks
```

**`telegram_authorized_users`** (View) — User activity
```
Shows who has accessed the bot and how often
```

**`telegram_auth_daily_summary`** (View) — Daily trends
```
Shows daily counts of authorized vs unauthorized attempts
```

---

## 🔍 Query Examples

### Find all unauthorized attempts in last 24 hours
```sql
SELECT chat_id, username, command_attempted, COUNT(*) as attempts
FROM telegram_auth_log
WHERE status = 'unauthorized'
AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY chat_id, username, command_attempted
ORDER BY attempts DESC;
```

### Find suspicious IPs
```sql
SELECT ip_address, COUNT(*) as unauthorized_attempts
FROM telegram_auth_log
WHERE status = 'unauthorized'
AND ip_address IS NOT NULL
GROUP BY ip_address
HAVING COUNT(*) > 5
ORDER BY unauthorized_attempts DESC;
```

### Show authorized user activity
```sql
SELECT chat_id, username, COUNT(*) as commands, MAX(timestamp) as last_access
FROM telegram_auth_log
WHERE status = 'authorized'
GROUP BY chat_id, username
ORDER BY last_access DESC;
```

---

## 🎯 Using the New Commands

### For Authorized Users (Anyone)

**Get your Chat ID:**
```
/extract_chat_id

Returns:
🔍 Your Chat ID
━━━━━━━━━━━━━━━━━━━━━━━━━
Chat ID: 5838483717
User: @leo123
```

### For Admins (You)

**See who's trying to hack the bot:**
```
/auth_log 24 20
Shows last 24 hours, 20 results

/suspicious 5 24
Shows IPs with 5+ attempts in 24h
```

**Monitor user activity:**
```
/auth_users 50
Shows 50 most recent authorized users

/auth_daily 7
Shows daily summary for last 7 days
```

---

## ⚙️ Configuration

The system works in three modes:

### Mode 1: Log-Only (Default, Safe)
```python
self.auth_logger = AuthorizationLogger(db_connection=None)
```
- Logs to console/file only
- No database writes
- Perfect for testing

### Mode 2: Full Logging (Recommended)
```python
db = get_connection()
self.auth_logger = AuthorizationLogger(db_connection=db)
```
- Logs to database
- Can query historical data
- Can view via Telegram commands

### Mode 3: Disabled
```python
self.auth_logger = AuthorizationLogger(db_connection=None)
# Don't call log_attempt()
```
- No logging at all
- If you don't want the overhead

---

## 🔒 Security Considerations

✅ **What's protected:**
- All authorization attempts logged
- Unauthorized attempts flagged with Chat ID
- Can detect bot discovery attacks
- Can track suspicious IPs

✅ **What's NOT logged:**
- Command results (only command names)
- User messages (only commands)
- Sensitive data (tokens, passwords)

⚠️ **Best practices:**
- Review `/auth_log` monthly for suspicious patterns
- Add new users only after confirming identity
- Remove inactive users from `ALLOWED_CHAT_IDS`
- Keep database backups

---

## 📝 Implementation Checklist

- [ ] Run `auth_logging.sql` in database
- [ ] Copy `auth_logger.py` to `notifications/`
- [ ] Copy `auth_commands.py` to `notifications/`
- [ ] Add imports to `telegram_bot.py`
- [ ] Add `auth_logger` and `auth_commands` initialization
- [ ] Update `auth_required` decorator
- [ ] Register new command handlers
- [ ] Restart bot
- [ ] Test with `/extract_chat_id`
- [ ] Test with `/auth_log` (as admin)
- [ ] Review logs for first 24 hours

---

## 🧪 Testing

### Test 1: Unauthorized Access
```
1. From new Telegram account
2. Send: /status
3. Expected: Unauthorized error + Chat ID displayed
4. Check DB: SELECT * FROM telegram_auth_log WHERE status='unauthorized'
5. Should see your attempt logged
```

### Test 2: Authorized Access
```
1. Whitelist your Chat ID
2. Send: /status
3. Expected: Status message shown
4. Check DB: SELECT * FROM telegram_auth_log WHERE status='authorized'
5. Should see your attempt logged
```

### Test 3: Extract Chat ID Command
```
1. Send: /extract_chat_id
2. Expected: Your Chat ID displayed
3. Confirms logging is working
```

### Test 4: Admin Commands
```
1. Send: /auth_log
2. Expected: Recent unauthorized attempts
3. Send: /auth_users
4. Expected: Authorized users list
5. Send: /auth_daily
6. Expected: Daily summary
```

---

## 🚀 Deployment Steps

**Minimal (Log-only):**
1. Copy `auth_logger.py` and `auth_commands.py`
2. Update imports in `telegram_bot.py`
3. Add decorator logging (no DB needed)
4. Restart bot
5. Done

**Full (With database):**
1. Run `auth_logging.sql`
2. Copy module files
3. Update imports
4. Add DB connection
5. Register commands
6. Restart bot

**Time:** 30 minutes for minimal, 1 hour for full

---

## 📖 Files Created

| File | Purpose | Size |
|------|---------|------|
| `database/migrations/auth_logging.sql` | Database schema | 1.2 KB |
| `notifications/auth_logger.py` | Logging module | 4.8 KB |
| `notifications/auth_commands.py` | Commands module | 6.2 KB |
| `AUTHORIZATION_LOGGING_IMPLEMENTATION.md` | This guide | 6.0 KB |

**Total new code:** ~18 KB

---

## 🆘 Troubleshooting

**Q: Commands returning empty results?**
A: Make sure database connection is passed. In log-only mode, check console logs.

**Q: Database connection errors?**
A: Either provide correct connection or use log-only mode (db_connection=None).

**Q: Chat IDs not being logged?**
A: Verify decorator is wrapping all commands and log_attempt() is being called.

**Q: Commands showing "Error"?**
A: Check logs for exceptions. Likely a database connection issue.

---

**Ready to integrate?** Start with Step 1 above!

