# 🖥️ WINDOWS TASK SCHEDULER SETUP GUIDE

**Date:** 2026-04-22  
**Platform:** Windows 10/11  
**Status:** Ready to Deploy  

---

## 📋 QUICK START (5 minutes)

### Step 1: Test Your Setup
```batch
test_health.bat
```
This runs a health check and validation to verify everything works.

### Step 2: Setup Automation (Option A: Automatic)
```batch
setup_scheduler.bat
```
**Important:** Right-click and select "Run as administrator"

This creates 4 scheduled tasks:
- Daily paper trading (1:00 AM UTC)
- Health check (every 6 hours)
- Telegram bot (at Windows startup)
- Dashboard (at Windows startup)

### Step 3: Start Services Now
```batch
start_all.bat
```
This starts the dashboard and telegram bot immediately.

---

## 🎯 WHAT EACH BATCH SCRIPT DOES

### `test_health.bat`
Runs system verification before automation setup.
- ✅ Health check (30 seconds)
- ✅ Validation suite (2-3 minutes)
- ✅ Checks FastAPI installation

**Run this first** to ensure system is ready.

### `start_all.bat`
Starts all services for manual/development use.
- 🌐 Dashboard on http://localhost:5000
- 🤖 Telegram bot (listening for commands)
- 📊 Optional daily cycle

Keep the terminal windows open while services are running.

### `setup_scheduler.bat`
Creates Windows Task Scheduler automation.
- ⏰ Runs daily at 1:00 AM UTC
- 💾 Logs to logs/main.log
- 🔄 Health check every 6 hours
- 🚀 Telegram bot & Dashboard at startup

**Requires Administrator privileges.**

### `tail_logs.bat`
View log files in real-time.
- Interactive menu
- View main log, dashboard log, telegram log
- Last 50 lines displayed

### `stop_services.bat`
Gracefully stop all running services.
- Kills dashboard windows
- Kills telegram bot processes
- Safe to run anytime

---

## ⚙️ SETUP AUTOMATION STEP-BY-STEP

### Option 1: Automatic Setup (Recommended)

1. **Right-click `setup_scheduler.bat`**
   - Select "Run as administrator"

2. **Confirm UAC prompt** (if asked)

3. **Watch for confirmation messages**
   - ✓ Task created: Daily Paper Trading (1:00 AM UTC)
   - ✓ Task created: Health Check
   - ✓ Task created: Telegram Bot
   - ✓ Task created: Dashboard

4. **Verify tasks were created:**
   ```batch
   schtasks /query /tn "TradePanel*"
   ```

### Option 2: Manual Setup (Advanced)

Open Command Prompt as Administrator and run:

**Task 1: Daily Paper Trading**
```batch
schtasks /create /tn "TradePanel - Paper Trading" /tr "python main.py --mode paper-trade --quiet" /sc daily /st 01:00
```

**Task 2: Health Check (every 6 hours)**
```batch
schtasks /create /tn "TradePanel - Health Check" /tr "python main.py --mode health --quiet" /sc hourly /mo 6
```

**Task 3: Telegram Bot (at startup)**
```batch
schtasks /create /tn "TradePanel - Telegram Bot" /tr "python main.py --mode telegram --quiet" /sc onstart /ru SYSTEM
```

**Task 4: Dashboard (at startup)**
```batch
schtasks /create /tn "TradePanel - Dashboard" /tr "python dashboard.py --port 5000" /sc onstart /ru SYSTEM
```

---

## 🔧 TASK SCHEDULER MANAGEMENT

### View All TradePanel Tasks
```batch
schtasks /query /tn "TradePanel*"
```

### Run a Task Immediately
```batch
schtasks /run /tn "TradePanel - Paper Trading"
```

### Change Task Time

**Change daily paper trading time to 2:00 AM:**
```batch
schtasks /change /tn "TradePanel - Paper Trading" /st 02:00
```

### Delete a Task

**Remove the daily paper trading task:**
```batch
schtasks /delete /tn "TradePanel - Paper Trading" /f
```

### View Task History

**Open Event Viewer:**
1. Press `Windows + R`
2. Type `eventvwr`
3. Go to Windows Logs → Application
4. Filter for "TradePanel"

---

## 📊 MONITORING & LOGS

### View Logs Interactively
```batch
tail_logs.bat
```

### View Specific Log File
```batch
REM PowerShell: View last 50 lines
powershell -NoProfile -Command "Get-Content -Path 'logs\main.log' -Tail 50"

REM Or use more command
more logs\main.log
```

### Follow Log in Real-Time
```batch
REM PowerShell: Follow log as it updates
powershell -NoProfile -Command "Get-Content -Path 'logs\main.log' -Wait"
```

### Log File Locations
```
logs\main.log           — Main script operations
logs\dashboard.log      — Dashboard operations
logs\telegram_bot.log   — Telegram bot activity
results\               — Daily validation results
```

---

## 🚀 DAILY OPERATION WORKFLOW

### Morning (Check Status)
```batch
REM Option 1: View dashboard
start http://localhost:5000

REM Option 2: Check logs
tail_logs.bat
```

### Manual Operations (During Day)
```batch
REM Run health check
python main.py --mode health

REM Run validation
python main.py --mode validate

REM Run backtest
python main.py --mode backtest --strategy range_breakout --pair XAUUSD
```

### Evening (Monitor Automation)
```batch
REM View latest logs
tail_logs.bat

REM Verify tasks are scheduled
schtasks /query /tn "TradePanel*"
```

---

## 🐛 TROUBLESHOOTING

### Issue: "Access Denied" when running setup_scheduler.bat

**Solution:** Right-click → Run as administrator

### Issue: "Python not found"

**Solution:** Add Python to PATH
1. Install Python with "Add Python to PATH" checkbox
2. Or manually add Python directory to system PATH:
   - System Properties → Environment Variables
   - Add Python install directory (e.g., `C:\Python39`)

### Issue: Tasks created but not running

**Solution:** Check Task Scheduler settings
1. Open Task Scheduler
2. Find "TradePanel" tasks
3. Right-click → Properties → General
4. Ensure "Run with highest privileges" is checked
5. Set user to "SYSTEM"

### Issue: Dashboard not accessible on http://localhost:5000

**Solution:**
1. Check if service is running: `tasklist | findstr python`
2. Check if port 5000 is in use: `netstat -ano | findstr 5000`
3. Try different port: `python dashboard.py --port 8080`
4. Check logs: `tail_logs.bat`

### Issue: Telegram bot not responding

**Solution:**
1. Check token in .env file
2. Restart telegram service: `stop_services.bat` then `start_all.bat`
3. View logs: `tail_logs.bat` → Option 3

### Issue: Tasks keep failing

**Solution:**
1. Check logs: `tail_logs.bat` → Option 4
2. Run test: `test_health.bat`
3. Verify .env file exists with all variables
4. Check database connection: `python main.py --mode health`

---

## ✅ VERIFICATION CHECKLIST

### After Running setup_scheduler.bat
- [ ] All 4 tasks created in Task Scheduler
- [ ] No error messages in console
- [ ] `schtasks /query /tn "TradePanel*"` shows all tasks

### Daily Before Trading
- [ ] Health check passes: `python main.py --mode health`
- [ ] Validation passes: `python main.py --mode validate`
- [ ] Dashboard accessible: http://localhost:5000
- [ ] Telegram bot responding: Send `/status` in Telegram

### Weekly
- [ ] Review logs for errors: `tail_logs.bat`
- [ ] Verify tasks are running: `schtasks /query /tn "TradePanel*"`
- [ ] Check system health: `python main.py --mode health`

---

## 📈 PRODUCTION CHECKLIST

Before going live:

- [ ] Test health passes: `test_health.bat`
- [ ] Tasks are created: `schtasks /query /tn "TradePanel*"`
- [ ] Logs directory exists with proper permissions
- [ ] .env file configured with all variables
- [ ] Backups are in place (database backup script)
- [ ] Email alerts configured (optional)
- [ ] Monitoring set up (check logs daily)
- [ ] Rollback plan documented

---

## 🔐 SECURITY NOTES

### Protect Credentials
- .env file should NOT be in git or shared
- Add to .gitignore: `echo .env >> .gitignore`
- Restrict file permissions: Right-click → Properties → Security

### Task Scheduler Security
- Tasks run as "SYSTEM" user
- Ensure only administrators can modify tasks
- Review task history regularly

### Log Security
- Logs may contain sensitive info
- Rotate logs regularly (weekly recommended)
- Archive old logs securely

---

## 🚀 NEXT STEPS

1. **Run test:** `test_health.bat`
2. **Setup automation:** `setup_scheduler.bat` (as admin)
3. **Start services:** `start_all.bat`
4. **Monitor dashboard:** http://localhost:5000
5. **Check logs daily:** `tail_logs.bat`

---

## 📞 QUICK COMMANDS

```batch
REM Test setup
test_health.bat

REM Start all services
start_all.bat

REM Setup Windows Task Scheduler
setup_scheduler.bat

REM View logs
tail_logs.bat

REM Stop all services
stop_services.bat

REM Run health check manually
python main.py --mode health

REM Run validation manually
python main.py --mode validate

REM Run paper trading manually
python main.py --mode paper-trade

REM Start dashboard on custom port
python dashboard.py --port 8080

REM List all TradePanel tasks
schtasks /query /tn "TradePanel*"

REM Run a task immediately
schtasks /run /tn "TradePanel - Paper Trading"

REM Delete a task
schtasks /delete /tn "TradePanel - Paper Trading" /f
```

---

## 🎯 ARCHITECTURE

```
TradePanel (Windows)
├── main.py (Master Control)
│   ├── --mode paper-trade  → Daily trading cycle
│   ├── --mode validate     → Test strategies
│   ├── --mode telegram     → Bot (24/7)
│   ├── --mode health       → System check
│   └── --mode backtest     → Strategy testing
│
├── dashboard.py (Web UI)
│   ├── Port 5000
│   ├── http://localhost:5000
│   └── Real-time metrics
│
└── Automation (Windows Task Scheduler)
    ├── 1:00 AM UTC → Paper Trading
    ├── Every 6 hours → Health Check
    ├── At Startup → Telegram Bot
    └── At Startup → Dashboard
```

---

**Status:** ✅ Ready to Deploy  
**Tested on:** Windows 10/11  
**Python:** 3.9+  

🚀 **Start automating now!**
