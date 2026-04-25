# 🤖 TELEGRAM BOT SETUP GUIDE
**Date:** 2026-04-22  
**Status:** Ready to Deploy  
**Bot Token:** Configured in `.env`  

---

## 🚨 CURRENT STATUS

### ❌ **Problem**
Your Telegram bot is **NOT ACTIVE** because:
1. ✅ Token is configured in `.env` 
2. ❌ **Bot is never started** (no `await bot.start()` call)
3. ❌ **Event loop not initialized**

### ✅ **Solution**
Run the new startup script to activate the bot.

---

## 🚀 QUICK START (30 seconds)

### 1. Start the Bot
```bash
# In terminal, from TradePanel directory:
python scripts/start_telegram_bot.py
```

**Expected Output:**
```
[2026-04-22 10:15:30] Telegram Bot Startup
🤖 Initializing Telegram bot...
🚀 Starting bot polling...
✅ Bot is now active and listening for commands
   Available commands:
   /status   — System and account status
   /balance  — Balance and equity
   /active   — List open positions
   ...
⏸️  Press CTRL+C to stop the bot
```

### 2. Test the Bot
Open Telegram → Send `/status` to your bot  
**Expected Response:** Current system status, strategies, balance, etc.

### 3. Stop the Bot
Press `CTRL+C` in the terminal

---

## ✅ SETUP VERIFICATION

### Check 1: .env File Has Token ✅
```bash
# Verify token is set:
grep TELEGRAM_BOT_TOKEN .env
# Output should show: TELEGRAM_BOT_TOKEN=8710948452:AAE...
```

### Check 2: Bot Starts Successfully
```bash
python scripts/start_telegram_bot.py
# Should see: ✅ Bot is now active and listening for commands
```

### Check 3: Commands Work
Open Telegram and try:
```
/help      — Shows all available commands
/status    — Current trading status
/balance   — Account balance & equity
/active    — Open positions
/signals   — Recent strategy signals
/health    — System health
```

---

## 🔧 CONFIGURATION

### Required Environment Variables (in `.env`)
```
# Already Configured ✅
TELEGRAM_BOT_TOKEN=8710948452:AAEfavZLXrDl2ktAreNgYwRqPreFptp_RLA
TELEGRAM_CHAT_ID=5838483717
```

### Optional Configuration

**To change the chat ID:**
1. Open `.env`
2. Update `TELEGRAM_CHAT_ID` to your chat ID
3. Restart the bot

**To use a different bot:**
1. Create new bot via BotFather: https://t.me/botfather
2. Get the new token
3. Update `.env`: `TELEGRAM_BOT_TOKEN=your_new_token`
4. Restart the bot

---

## 📋 TELEGRAM BOT COMMANDS

Once the bot is running, use these commands:

### System Status
```
/status   — Current trading system status
/health   — System health (heartbeat, alerts)
/mode     — Operating mode (paper/live) and strategy list
```

### Account Information
```
/balance  — Current balance and equity
/active   — Open positions and entry prices
/risk     — Account drawdown and risk metrics
```

### Trading Intelligence
```
/signals  — Recent strategy signals (last 24h)
/analysis — Multi-timeframe market analysis
```

### Help
```
/help     — Show all available commands
```

---

## 🚀 DEPLOYMENT MODES

### Mode 1: Development (Interactive)
```bash
# Run in foreground for testing
python scripts/start_telegram_bot.py

# See all output in real-time
# Stop with CTRL+C
```

### Mode 2: Production (Background)

**On Linux/Mac:**
```bash
# Run as background process
nohup python scripts/start_telegram_bot.py > logs/telegram_bot.log 2>&1 &

# Verify it's running
ps aux | grep telegram_bot.py

# View logs
tail -f logs/telegram_bot.log

# Stop it
pkill -f telegram_bot.py
```

**On Windows:**
```bash
# Run as background process (PowerShell)
Start-Process python -ArgumentList "scripts/start_telegram_bot.py" -NoNewWindow -RedirectStandardOutput "logs/telegram_bot.log"

# View logs
Get-Content logs/telegram_bot.log -Wait

# Stop it
Stop-Process -Name python -Filter {$_.Path -like "*telegram_bot.py*"}
```

### Mode 3: Scheduled Restart (Systemd - Linux)

Create `/etc/systemd/system/telegrambot.service`:
```ini
[Unit]
Description=TradePanel Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TradePanel
ExecStart=/usr/bin/python3 scripts/start_telegram_bot.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegrambot
sudo systemctl start telegrambot
sudo systemctl status telegrambot
```

---

## 🐛 TROUBLESHOOTING

### Issue: "TELEGRAM_BOT_TOKEN not found"

**Solution:** Add token to `.env`:
```bash
echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
```

### Issue: "timeout waiting for bot response"

**Possible Causes:**
- Internet connection problem
- Telegram API is down (check https://status.telegram.org)
- Bot token is invalid or expired

**Solution:**
1. Verify internet connection
2. Check token is correct in `.env`
3. Create new bot via @BotFather if token is old

### Issue: "ModuleNotFoundError: No module named 'telegram'"

**Solution:** Install required package:
```bash
pip install python-telegram-bot
```

### Issue: Bot doesn't respond to commands

**Causes:**
1. Bot not actually running (check terminal)
2. Chat ID mismatch (verify in `.env`)
3. Bot not added to group/private chat

**Solution:**
```bash
# Verify bot is running:
ps aux | grep telegram_bot

# If not, restart:
python scripts/start_telegram_bot.py

# Ensure you're messaging the correct bot in Telegram
```

### Issue: "Cannot send message: Chat not found"

**Solution:**
1. Get your correct chat ID:
   - Message the bot with `/start`
   - Check logs for chat ID
   - Update `.env` with correct chat ID
2. Restart bot

---

## 📊 MONITORING & LOGS

### Log Location
```
logs/telegram_bot.log  — All bot activity
```

### View Live Logs
```bash
# Linux/Mac:
tail -f logs/telegram_bot.log

# Windows PowerShell:
Get-Content logs/telegram_bot.log -Wait
```

### Example Log Output
```
[2026-04-22 10:15:30] Telegram Bot — INFO — Initializing Telegram bot...
[2026-04-22 10:15:31] Telegram Bot — INFO — Starting bot polling...
[2026-04-22 10:15:32] Telegram Bot — INFO — Bot is now active
[2026-04-22 10:15:45] Telegram Bot — INFO — Received command: /status
[2026-04-22 10:15:46] Telegram Bot — INFO — Sent status response to chat
```

---

## 🔐 SECURITY NOTES

### Protect Your Token
```bash
# Token should NEVER be in version control
# Keep .env file gitignored:
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "Remove .env from tracking"
```

### Rotate Token Regularly
```bash
# If token is compromised:
1. Message @BotFather: /revoke
2. Get new token
3. Update .env
4. Restart bot
```

### Limit Chat Access
```bash
# Only set TELEGRAM_CHAT_ID to YOUR personal chat
# Don't share token with others
# Use read-only operations in group chats
```

---

## ✅ INTEGRATION WITH PHASE 3

### Automated Notifications

The Telegram bot will **automatically send alerts** when:
- ✅ Daily cycle completes (every 1:00 AM UTC)
- ✅ Strategy underperforms (WR < 40%)
- ✅ Daily loss exceeds threshold ($750)
- ✅ System health degrades

### Monitoring Schedule

**Daily (Automatic):**
- P&L summary sent at 1:00 AM UTC
- Any alerts triggered automatically

**Manual (On Demand):**
- `/status` — Check anytime
- `/balance` — Check current equity
- `/active` — See open positions
- `/analysis` — Market analysis

---

## 🚀 NEXT STEPS

### To Activate Telegram Bot Now:

1. **Start the bot:**
   ```bash
   python scripts/start_telegram_bot.py
   ```

2. **Keep it running:** Don't close the terminal

3. **Test commands:** Send `/status` in Telegram

4. **For production:** Run as background service (see Deployment Modes above)

### To Integrate with Phase 3:

The bot is now ready to:
- ✅ Send daily paper trading alerts
- ✅ Respond to on-demand status queries
- ✅ Provide real-time trading intelligence
- ✅ Alert on system issues

---

## 📞 SUPPORT

### Bot Not Working?

Check in this order:
1. Is terminal showing "✅ Bot is now active"?
2. Is `.env` file present with token?
3. Can you run `/help` command?
4. Check `logs/telegram_bot.log` for errors

### Telegram Changes?

If Telegram API changes and bot breaks:
1. Reinstall package: `pip install --upgrade python-telegram-bot`
2. Restart bot: `python scripts/start_telegram_bot.py`
3. Check logs for specific error messages

---

**Status:** ✅ Ready to Deploy  
**Action Required:** Run `python scripts/start_telegram_bot.py`  
**Estimated Time:** 30 seconds to activate  

🤖 **Bot will be active immediately after running the startup script!**

