# 🚀 TRADEPANEL COMPLETE SETUP & RUN GUIDE

**Version:** 3.0 (Consolidated Scripts + Automation)  
**Date:** 2026-04-22  
**Status:** Production Ready  

---

## 📍 YOU ARE HERE

This guide covers:
- ✅ Initial system testing
- ✅ Windows Task Scheduler setup (automated)
- ✅ Manual service management
- ✅ Complete monitoring workflow

---

## ⚡ QUICKSTART (10 minutes)

### 1. Test Your System
```batch
cd C:\path\to\TradePanel
test_health.bat
```
Expected output: All checks pass ✅

### 2. Setup Automation (Windows)
```batch
REM Right-click → Run as administrator
setup_scheduler.bat
```
Expected output: 4 tasks created ✅

### 3. Start Services
```batch
start_all.bat
```
Expected output:
- Dashboard running on http://localhost:5000
- Telegram bot listening for commands

### 4. Verify Everything Works
- Open browser: http://localhost:5000 ← Dashboard
- Send Telegram `/status` → Should get response
- Check logs: `tail_logs.bat` → Should be clean

**Done!** Your TradePanel is now automated and running.

---

## 🗂️ FILE STRUCTURE

```
TradePanel/
├── main.py                    ← Master control script (7 modes)
├── dashboard.py               ← Web dashboard + API
│
├── WINDOWS_SETUP.md           ← Windows Task Scheduler guide
├── AUTOMATION_GUIDE.md        ← All deployment methods
├── QUICK_REFERENCE.md         ← 2-minute command reference
├── SETUP_AND_RUN.md          ← This file
│
├── start_all.bat              ← Start all services
├── test_health.bat            ← System health check
├── setup_scheduler.bat        ← Create scheduled tasks
├── tail_logs.bat              ← View logs interactively
├── stop_services.bat          ← Stop all services
│
├── logs/                       ← Log files
│   ├── main.log
│   ├── dashboard.log
│   └── telegram_bot.log
│
├── results/                    ← Daily results
│   └── daily_validation/
│
└── config/
    └── strategies.yaml        ← Strategy configuration
```

---

## 🎯 THREE WAYS TO RUN TRADEPANEL

### Method 1: Manual/Interactive (Development)

Use when testing or developing:

```bash
# Terminal 1: Health check
python main.py --mode health

# Terminal 2: Dashboard
python dashboard.py --port 5000

# Terminal 3: Telegram bot
python main.py --mode telegram

# Terminal 4: Paper trading
python main.py --mode paper-trade

# Terminal 5: Validation
python main.py --mode validate
```

**Pros:** Full control, see all output, easy debugging  
**Cons:** Requires multiple terminal windows

---

### Method 2: Batch Scripts (Windows)

Use for local testing with automatic service management:

```batch
REM Start all services at once
start_all.bat

REM Later, stop all services
stop_services.bat
```

**Pros:** One command to start everything  
**Cons:** Still requires keeping windows open

---

### Method 3: Task Scheduler (Automated - Production)

Use for fully automated, hands-off operation:

```batch
REM One-time setup
setup_scheduler.bat

REM Services run automatically:
REM - Paper trading daily at 1:00 AM UTC
REM - Health check every 6 hours
REM - Telegram bot at Windows startup
REM - Dashboard at Windows startup
```

**Pros:** Fully automated, no manual intervention, 24/7 operation  
**Cons:** Need admin access for setup

---

## 🎬 QUICK START BY PLATFORM

### Windows 10/11 (Recommended for This Setup)

**Initial Setup:**
```batch
test_health.bat                    (Verify everything works)
setup_scheduler.bat                (Right-click → Run as admin)
```

**Daily Operation:**
- Tasks run automatically
- View dashboard: http://localhost:5000
- Check logs: `tail_logs.bat`
- Manual runs: `python main.py --mode <mode>`

See: **WINDOWS_SETUP.md**

---

### Linux/Mac with Cron

**Initial Setup:**
```bash
chmod +x main.py dashboard.py
python main.py --mode health    # Verify everything works
```

**Setup Cron:**
```bash
crontab -e
# Add these lines:
0 1 * * * cd /path/to/TradePanel && python main.py --mode paper-trade >> logs/cron.log 2>&1
0 */6 * * * cd /path/to/TradePanel && python main.py --mode health >> logs/health.log 2>&1
@reboot cd /path/to/TradePanel && nohup python main.py --mode telegram > logs/telegram.log 2>&1 &
@reboot cd /path/to/TradePanel && nohup python dashboard.py --port 5000 > logs/dashboard.log 2>&1 &
```

See: **AUTOMATION_GUIDE.md** (Cron section)

---

### Linux with Systemd

**Initial Setup:**
```bash
chmod +x main.py dashboard.py
python main.py --mode health    # Verify everything works
```

**Create Service Files** (see AUTOMATION_GUIDE.md for details):
```bash
sudo nano /etc/systemd/system/tradepanel-paper.service
sudo nano /etc/systemd/system/tradepanel-telegram.service
sudo nano /etc/systemd/system/tradepanel-dashboard.service
sudo systemctl daemon-reload
sudo systemctl enable tradepanel-telegram
sudo systemctl start tradepanel-telegram
```

See: **AUTOMATION_GUIDE.md** (Systemd section)

---

### Docker (Cloud/VPS)

**Initial Setup:**
```bash
docker-compose up -d
docker-compose logs -f
```

See: **AUTOMATION_GUIDE.md** (Docker section)

---

## 📊 UNDERSTANDING THE SCRIPTS

### main.py — Master Control

**What it does:** Runs ALL trading operations

**Modes available:**
```
--mode paper-trade    Run daily trading cycle (5-10 min)
--mode validate       Test all strategies (2-3 min)
--mode backtest       Test single strategy (1-5 min)
--mode telegram       Start Telegram bot (24/7)
--mode health         System verification (30 sec)
--mode full           Everything except telegram (10-15 min)
--mode scheduler      For cron/automation integration
```

**Example usage:**
```bash
python main.py --mode health
python main.py --mode validate
python main.py --mode backtest --strategy range_breakout --pair XAUUSD
python main.py --mode paper-trade --quiet
```

**Flags:**
- `--quiet` — Suppress console output (log to file only)
- `--strategy NAME` — For backtest mode (required)
- `--pair PAIR` — For backtest (default: XAUUSD)
- `--timeframe TF` — For backtest (default: H1)
- `--limit N` — For backtest (optional bar limit)

---

### dashboard.py — Web Monitoring

**What it does:** Provides real-time dashboard and API

**Modes available:**
```
--port 5000           Web UI (default)
--host 0.0.0.0        Listen on all interfaces
--mode metrics        API only (no web UI)
--mode live           Console monitoring
```

**Access points:**
```
http://localhost:5000         → Dashboard HTML
http://localhost:5000/api/metrics  → All metrics (JSON)
http://localhost:5000/docs    → API documentation
```

**Example usage:**
```bash
python dashboard.py --port 5000                    (default)
python dashboard.py --port 8080 --host 0.0.0.0   (external access)
python dashboard.py --mode metrics                 (API only)
python dashboard.py --mode live                    (console)
```

---

## 🔄 DAILY WORKFLOW

### Automated (With Task Scheduler)

```
1:00 AM UTC
  ├─ Paper trading runs automatically
  │  ├─ Health check
  │  ├─ Validation suite
  │  └─ Paper trades
  └─ Results logged to logs/main.log

Every 6 hours
  ├─ Health check runs automatically
  └─ Results logged to logs/main.log

At Windows startup
  ├─ Telegram bot starts
  └─ Dashboard starts (port 5000)

24/7
  ├─ Dashboard accessible: http://localhost:5000
  ├─ Telegram bot listening for commands
  └─ Logs accumulating in logs/
```

### Manual (During Development)

```
Morning
  1. Run: python main.py --mode health
  2. Check: http://localhost:5000

Midday
  1. Run: python main.py --mode backtest --strategy range_breakout
  2. View: logs/main.log

Evening
  1. Run: python main.py --mode full
  2. Check: tail_logs.bat
  3. Review: results/daily_validation/
```

---

## ✅ VERIFICATION CHECKLIST

### Before First Automation Run

- [ ] Python 3.9+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file exists with all variables
- [ ] logs/ directory exists
- [ ] results/ directory exists
- [ ] Health check passes: `python main.py --mode health`
- [ ] Validation passes: `python main.py --mode validate`

### After Task Scheduler Setup

- [ ] All 4 tasks created: `schtasks /query /tn "TradePanel*"`
- [ ] Tasks are enabled (not disabled)
- [ ] No permissions errors in logs
- [ ] Dashboard accessible: http://localhost:5000
- [ ] Telegram bot responds to `/status`

### Daily Operations

- [ ] Logs are being written to logs/
- [ ] No ERROR messages in logs: `grep ERROR logs/main.log`
- [ ] Dashboard shows latest data
- [ ] Validation results in results/daily_validation/
- [ ] Tasks ran at scheduled times: Check Event Viewer

---

## 🐛 COMMON ISSUES & SOLUTIONS

### "Python not found"
```batch
REM Solution: Add Python to PATH
REM Or use full path: C:\Python39\python.exe main.py --mode health
```

### "Module not found: fastapi"
```batch
pip install fastapi uvicorn
```

### "Cannot create task: Access Denied"
```batch
REM Solution: Right-click setup_scheduler.bat → Run as administrator
```

### "Dashboard not accessible"
```batch
REM Check if already running: tasklist | findstr dashboard
REM Check port 5000: netstat -ano | findstr 5000
REM Try different port: python dashboard.py --port 8080
```

### "Telegram bot not responding"
```batch
REM Check token: grep TELEGRAM_BOT_TOKEN .env
REM Restart: stop_services.bat, then start_all.bat
REM View logs: tail_logs.bat
```

### "Task not running at scheduled time"
```batch
REM Check logs: tail_logs.bat
REM Run manually: schtasks /run /tn "TradePanel - Paper Trading"
REM Check Event Viewer for errors
REM Verify task properties: Task Scheduler > TradePanel > Properties
```

---

## 📈 PRODUCTION READINESS

### Before Live Trading

- [ ] Test health passes ✅
- [ ] Validation tests all pass ✅
- [ ] Paper trading runs successfully ✅
- [ ] Dashboard displays correctly ✅
- [ ] Telegram bot responds to all commands ✅
- [ ] Logs are clean (no errors) ✅
- [ ] Task Scheduler is configured ✅
- [ ] Backups are in place ✅
- [ ] Monitoring plan is documented ✅

---

## 📞 DOCUMENTATION MAP

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **QUICK_REFERENCE.md** | 2-minute cheat sheet | Daily command reference |
| **WINDOWS_SETUP.md** | Windows Task Scheduler detailed | Setting up Windows automation |
| **AUTOMATION_GUIDE.md** | All deployment methods | Linux/Mac/Docker setup |
| **SETUP_AND_RUN.md** | This document | Complete overview |

---

## 🎓 LEARNING PATH

1. **First Time?** Start here:
   - Read: QUICK_REFERENCE.md (2 min)
   - Run: test_health.bat (1 min)
   - Run: start_all.bat (30 sec)

2. **Setting Up Automation?** Continue here:
   - Read: WINDOWS_SETUP.md (Windows) or AUTOMATION_GUIDE.md (Linux/Mac)
   - Run: setup_scheduler.bat or equivalent
   - Monitor: tail_logs.bat

3. **Troubleshooting?** Check these sections:
   - QUICK_REFERENCE.md → Common Problems
   - WINDOWS_SETUP.md → Troubleshooting
   - logs/ directory for detailed error messages

---

## 🚀 NEXT STEPS

### Immediate (Today)
1. ✅ Run `test_health.bat`
2. ✅ Run `setup_scheduler.bat` (as admin)
3. ✅ Run `start_all.bat`
4. ✅ Verify dashboard: http://localhost:5000

### Short Term (This Week)
1. Monitor logs daily
2. Verify automation is working
3. Test Telegram commands
4. Review trading results

### Medium Term (Next 2-4 Weeks)
1. Run Phase 3 validation (2-4 weeks paper trading)
2. Monitor for any issues
3. Prepare for Phase 4 (live trading)

### Long Term (Phase 4+)
1. Transition to live trading
2. Monitor 24/7
3. Adjust tier assignments based on real performance
4. Plan Phase 5+ enhancements

---

## 💾 BACKUP CHECKLIST

**Before going live, backup:**
- [ ] Database: SQL dump
- [ ] Configuration: config/ folder
- [ ] .env file (encrypted)
- [ ] logs/ folder (monthly archive)
- [ ] Code: Git repository

---

## 📞 SUPPORT & DEBUG

### Check System Health
```bash
python main.py --mode health
```

### View Real-Time Logs
```bash
tail_logs.bat
```

### Run Full Validation
```bash
python main.py --mode validate
```

### Test Telegram Bot
Open Telegram and send:
```
/status
/health
/balance
/help
```

### Test Dashboard
```bash
start http://localhost:5000
```

---

**Status:** ✅ Production Ready  
**Last Updated:** 2026-04-22  
**Tested On:** Windows 10/11, Linux, macOS  

🎯 **You're all set! TradePanel is ready to run.** 🎯
