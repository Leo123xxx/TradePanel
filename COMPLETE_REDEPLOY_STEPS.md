# 🚀 COMPLETE REDEPLOY & DATABASE REFRESH
**Status:** Full system reset and fresh deployment with top 10 strategies  
**Date:** 2026-04-22  
**Objective:** Clear all old data and redeploy with latest configuration

---

## ⚠️ IMPORTANT: Do These Steps IN ORDER

---

## STEP 1: STOP ALL RUNNING SERVICES (2 minutes)

**Open PowerShell as Administrator:**

```powershell
# Kill all Python processes
taskkill /F /IM python.exe

# Wait 3 seconds
Start-Sleep -Seconds 3

# Verify all processes are killed
Get-Process python -ErrorAction SilentlyContinue
# Should return nothing
```

**Or use the batch file:**
```powershell
cd F:\REPOS\leo123xxx\TradePanel
.\stop_services.bat
```

---

## STEP 2: CLEAR OLD DATA & CACHES (3 minutes)

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Clear old logs
Remove-Item -Path "logs\*" -Force -Recurse -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "logs" -Force

# Clear old results (keep structure)
Remove-Item -Path "results\daily_validation\*.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "results\daily_validation\*.csv" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "results\backtests\*" -Force -Recurse -ErrorAction SilentlyContinue

# Clear old data cache
Remove-Item -Path "data\cache\*.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "data\cache\*.pkl" -Force -ErrorAction SilentlyContinue

Write-Host "Old data cleared!"
```

---

## STEP 3: VERIFY NEW CONFIGURATION (2 minutes)

Verify the config file has the top 10 strategies:

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Check that strategies.yaml has the new "active" section
Select-String -Path "config\strategies.yaml" -Pattern "^active:" -Context 0,15

# Should show output like:
# active:
#   - dual_ema_fractal
#   - cot_sentiment
#   - rsi_bounce
#   ... (10 total)
```

Verify .env has LIVE mode enabled:

```powershell
# Check .env file
Select-String -Path ".env" -Pattern "TRADING_MODE"

# Should show:
# TRADING_MODE=live
```

---

## STEP 4: REBUILD DATABASE (5 minutes)

**IMPORTANT: This will reset the trading database to fresh state**

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Run health check to rebuild database tables
python main.py --mode health

# Expected output:
# [OK] MT5 Login: 81633025
# [OK] Database connection: OK
# [OK] MT5 connection: OK
# HEALTH CHECK SUMMARY: 4/4 passed
```

---

## STEP 5: RUN FULL VALIDATION WITH LATEST CONFIG (5 minutes)

This will validate all 25 strategies and populate the database with fresh results:

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Run validation (this tests all strategies with new config)
python main.py --mode validate

# Expected output:
# Starting strategy validation...
# Testing 25 strategies x 5 pairs x 1 timeframes
# Validation complete: 125 tests executed
# SUCCESS: Daily automation completed
```

---

## STEP 6: VERIFY TOP 10 ARE ACTIVE (2 minutes)

Check that the system now sees all 10 top strategies:

```powershell
# View the latest validation results
cd F:\REPOS\leo123xxx\TradePanel
Get-Content "results\daily_validation\summary_*.csv" | Select-Object -First 15

# Should show all top 10 strategies with their win rates
```

---

## STEP 7: START FRESH DEMO TRADING CYCLE (5 minutes)

Run the paper trading cycle with fresh data:

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# This will use the new top 10 strategies
python main.py --mode paper-trade

# Expected output:
# DAILY PAPER TRADING CYCLE START
# Testing 10 active strategies (from config)
# Dashboard updated with fresh data
# CYCLE COMPLETE: 100.0% strategies passed validation
```

---

## STEP 8: START DASHBOARD (LIVE DATA)

**Terminal 1 - Dashboard:**
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python dashboard.py --port 5000
```

Open browser: **http://localhost:5000**

Expected to see:
- ✅ 10 active strategies (not 2!)
- ✅ LIVE mode (not PAPER)
- ✅ Fresh validation results
- ✅ Empty portfolio (no trades yet)
- ✅ Ready for trading signals

---

## STEP 9: START TELEGRAM BOT (LIVE ALERTS)

**Terminal 2 - Telegram Bot:**
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python scripts/start_telegram_bot.py
```

Expected to see:
- ✅ Bot connects to Telegram API
- ✅ Starts listening for commands
- ✅ No UnicodeEncodeError
- ✅ Ready to receive /status commands

---

## STEP 10: TEST TELEGRAM COMMANDS

Send these commands in Telegram to verify fresh data:

```
/status      → Should show: Mode: LIVE, Active Strategies: 10
/balance     → Should show: Account balance and equity
/mode        → Should show: Operating Mode: LIVE
```

Expected responses:
- ✅ Mode shows "LIVE" (not "PAPER")
- ✅ Active Strategies shows "10" (not "2")
- ✅ All 10 strategies listed
- ✅ Fresh bot status (no old cached data)

---

## ✅ VERIFICATION CHECKLIST

After completing all steps above, verify:

- [ ] All Python processes stopped
- [ ] Old logs and data cleared
- [ ] Config file has top 10 strategies in "active" section
- [ ] .env shows TRADING_MODE=live
- [ ] Health check passes 4/4
- [ ] Validation shows 125/125 tests passed
- [ ] Dashboard shows 10 active strategies
- [ ] Dashboard shows LIVE mode
- [ ] Telegram bot starts without errors
- [ ] /status shows Mode: LIVE
- [ ] /status shows Active Strategies: 10
- [ ] /balance returns account data
- [ ] Dashboard http://localhost:5000 loads with fresh data

---

## 🚀 EXPECTED RESULTS AFTER REDEPLOY

| Metric | Before | After |
|--------|--------|-------|
| **Active Strategies** | 2 (old cached) | 10 (top performers) |
| **Mode** | PAPER | LIVE |
| **Database** | Old data | Fresh validation |
| **Bot Status** | Showing old info | Showing latest |
| **Dashboard** | 2 strategies | 10 strategies |

---

## 📞 IF SOMETHING FAILS

**If health check fails:**
```powershell
# Check MT5 connection manually
python main.py --mode health
# Look at error output, verify MT5 is open
```

**If validation fails:**
```powershell
# Check log files
type logs\main.log
# Look for error messages
```

**If Telegram bot won't start:**
```powershell
# Check token in .env
Select-String -Path ".env" -Pattern "TELEGRAM"
# Verify token is correct
```

**If database errors:**
```powershell
# Check PostgreSQL is running
Get-Service | Where-Object {$_.Name -like "*postgre*"}
# Should show: Running
```

---

## 🎯 SUCCESS INDICATORS

After full redeploy, you'll know it worked when:

1. ✅ Dashboard shows 10 strategies (not 2)
2. ✅ Dashboard shows "LIVE mode" (not PAPER)
3. ✅ Telegram /status shows "Active Strategies: 10"
4. ✅ Telegram /status shows "Operating Mode: LIVE"
5. ✅ Fresh validation results visible
6. ✅ No old cached data in logs
7. ✅ Bot responding with current data

---

## 📋 TIME ESTIMATE

| Step | Time |
|------|------|
| Stop services | 2 min |
| Clear old data | 3 min |
| Verify config | 2 min |
| Rebuild database | 5 min |
| Run validation | 5 min |
| Verify results | 2 min |
| Start services | 3 min |
| **TOTAL** | **22 minutes** |

---

**Status:** Ready for complete redeploy  
**Next:** Execute steps 1-10 in order  
**Goal:** Fresh system with top 10 strategies running in LIVE mode

🚀 **Let's redeploy!**
