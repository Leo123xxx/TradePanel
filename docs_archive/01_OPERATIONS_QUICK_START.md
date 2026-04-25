# 🚀 OPERATIONS & QUICK START GUIDE
**Version:** 1.0  
**Last Updated:** 2026-04-23  
**Audience:** Operations & DevOps Teams

---

## 📋 TABLE OF CONTENTS
1. [Quick Start (5 minutes)](#quick-start)
2. [Daily Operations](#daily-operations)
3. [Monitoring & Alerts](#monitoring)
4. [Troubleshooting](#troubleshooting)
5. [System Commands Reference](#commands)

---

## ⚡ QUICK START

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- MT5 Trading Platform (with demo/live account)
- Telegram Bot Token & Chat ID

### Installation (First Time)

```bash
# 1. Clone repository
git clone <your-repo-url> TradePanel
cd TradePanel

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your credentials:
# - MT5_LOGIN=your_account_number
# - MT5_PASSWORD=your_password
# - TELEGRAM_BOT_TOKEN=your_token
# - TELEGRAM_CHAT_ID=your_chat_id

# 4. Setup database
python scripts/setup_database.py

# 5. Verify system health
python main.py --mode health
```

### Start Trading (Every Day)

```bash
# Terminal 1: Web Dashboard
python dashboard.py --port 5000
# Open: http://localhost:5000

# Terminal 2: Paper/Live Trading
python main.py --mode paper-trade

# Terminal 3: Telegram Bot
python scripts/start_telegram_bot.py

# Terminal 4: Monitor Logs
tail -f logs/main.log
```

---

## 📊 DAILY OPERATIONS

### Morning Routine (5 minutes)

```bash
# 1. Check system health
python main.py --mode health

# Expected output:
# HEALTH CHECK SUMMARY: 4/4 passed
```

### In Telegram Bot

```
Send: /status
Expected: Shows mode, active strategies, account balance

Send: /balance
Expected: Displays account equity and today's P&L

Send: /active
Expected: Lists open positions
```

### On Dashboard (http://localhost:5000)

- View live trades in real-time
- Monitor P&L and win rate
- See strategy performance breakdown
- Check account equity curve

---

### Throughout Day (Every 4 hours)

```bash
# 1. Check Telegram for alerts
Send: /status

# 2. Review dashboard metrics
- Open positions
- Current P&L
- Win rate tracking

# 3. Monitor logs for errors
tail -20 logs/main.log
```

### Evening Routine (5 minutes)

```bash
# 1. Get daily summary
Telegram: /status

# 2. Document daily results
- Total trades
- Win rate
- P&L
- Any errors or warnings

# 3. Check logs for overnight issues
cat logs/main.log | grep ERROR
```

---

## 🔔 MONITORING & ALERTS

### Telegram Commands

| Command | Purpose | Example Response |
|---------|---------|-------------------|
| `/status` | System & account status | Mode: LIVE, Strategies: 10, Balance: $10,000 |
| `/balance` | Account equity & P&L | Equity: $10,250, Daily P&L: +$250 |
| `/active` | Open positions | 3 open trades, Total risk: $300 |
| `/signals` | Latest trading signals | BUY XAUUSD H1, BUY EURUSD M5 |
| `/risk` | Account risk metrics | Max drawdown: 5%, Daily loss limit: $200 |
| `/mode` | Operating mode | Mode: LIVE (not PAPER), Top 10 strategies active |
| `/health` | System health check | All systems operational |
| `/help` | Command help | Lists all available commands |

### Dashboard Metrics

**Real-time Updates** (every 30 seconds):
- Account Equity
- Open Positions
- Win Rate %
- Profit Factor
- Daily P&L
- Maximum Drawdown

**Charts & Analysis:**
- 24-hour P&L curve
- Strategy performance comparison
- Win/Loss distribution
- Equity growth over time

---

## 🔧 TROUBLESHOOTING

### Issue: "MT5 Connection Failed"

```bash
# Check if MT5 is running
# - Open MT5 trading platform
# - Verify login credentials in .env
# - Verify network connectivity

# Restart connection
python main.py --mode health

# If still failing
1. Kill all Python processes: taskkill /F /IM python.exe
2. Restart MT5
3. Wait 30 seconds
4. Run: python main.py --mode health
```

### Issue: "Database Connection Error"

```bash
# Check PostgreSQL is running
# Windows:
Get-Service postgresql*

# Linux/Mac:
sudo service postgresql status

# Verify credentials in .env
# DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Restart database
sudo service postgresql restart
```

### Issue: "Telegram Bot Not Responding"

```bash
# Restart the bot
taskkill /F /IM python.exe
Start-Sleep -Seconds 3
python scripts/start_telegram_bot.py

# Check logs
cat logs/telegram_bot.log

# If still failing
# 1. Verify TELEGRAM_BOT_TOKEN in .env
# 2. Verify TELEGRAM_CHAT_ID in .env
# 3. Restart bot
```

### Issue: "No Trades Being Executed"

```bash
# Check if trading is active
Telegram: /mode
# Should show: "Mode: LIVE"

# Verify strategies are active
Telegram: /status
# Should show: "Active Strategies: 10"

# Check market conditions
Telegram: /signals
# Should see recent signals

# If no signals
1. Verify market is open (forex/commodities trade 24/5)
2. Check logs: tail logs/main.log
3. Ensure strategy parameters are correct
```

### Issue: "Bot Showing Old Data"

```bash
# Restart all services
taskkill /F /IM python.exe
Start-Sleep -Seconds 5

# Clear cache
Remove-Item -Path "logs\*.log" -Force
Remove-Item -Path "results\daily_validation\dashboard_*.json" -Force

# Restart
python main.py --mode health
python main.py --mode paper-trade
python dashboard.py --port 5000
python scripts/start_telegram_bot.py
```

---

## 💻 SYSTEM COMMANDS REFERENCE

### Operation Modes

```bash
# Health Check
python main.py --mode health
# Verifies all systems (MT5, Database, Telegram, Config)

# Run Validation
python main.py --mode validate
# Tests all 25 strategies, updates metrics

# Paper/Live Trading
python main.py --mode paper-trade
# Executes trading cycle with active strategies

# Backtest Single Strategy
python main.py --mode backtest --strategy dual_ema_fractal --pair XAUUSD
# Tests specific strategy on historical data

# Start Telegram Bot
python scripts/start_telegram_bot.py
# Connects to Telegram, enables commands

# Start Dashboard
python dashboard.py --port 5000
# Launches web UI on http://localhost:5000

# Run Full Cycle
python main.py --mode full
# Runs validation + paper-trade + updates dashboard
```

### Service Management

```powershell
# Windows - Start all services
.\start_all.bat

# Windows - Stop all services
.\stop_services.bat

# Windows - Health check
.\test_health.bat

# Windows - View logs
.\tail_logs.bat

# Kill all Python processes
taskkill /F /IM python.exe
```

### Log Files

```bash
# Main application log
tail -f logs/main.log

# Dashboard log
tail -f logs/dashboard.log

# Telegram bot log
tail -f logs/telegram_bot.log

# Search for errors
grep ERROR logs/main.log

# Search for specific strategy
grep "dual_ema_fractal" logs/main.log
```

---

## 📈 PERFORMANCE METRICS

### Key Performance Indicators

**Daily Metrics:**
- Total Trades
- Win Rate %
- Profit Factor (earnings / losses)
- Maximum Drawdown
- Daily P&L
- Risk/Reward Ratio

**Strategy Metrics:**
- Win Rate per Strategy
- Trades per Strategy
- Average Win
- Average Loss
- Best Performing Strategy

**Account Metrics:**
- Account Equity
- Used Margin
- Free Margin
- Daily Returns %
- Monthly Returns %

### Expected Performance (Phase 3)

- **Win Rate:** 50%+ (matching validation)
- **Profit Factor:** 1.3+ (earning 30% more than losing)
- **Daily Trades:** 20-50 trades
- **Maximum Drawdown:** < 10%
- **Monthly Returns:** 5-15%

---

## 🔒 SECURITY BEST PRACTICES

### Credential Management

- ✅ Store all secrets in `.env` file
- ✅ Never commit `.env` to git
- ✅ Rotate credentials quarterly
- ✅ Use strong passwords (20+ characters)
- ✅ Enable 2FA on MT5 account
- ✅ Enable 2FA on Telegram account

### System Security

- ✅ Keep Python packages updated
- ✅ Run on isolated network/VM
- ✅ Enable firewalls (only port 5000 externally)
- ✅ Use HTTPS for dashboard
- ✅ Monitor for unauthorized access
- ✅ Regular backup of database

### Account Safety

- ✅ Position sizing: max 1% risk per trade
- ✅ Daily loss limit: stop at 2% account loss
- ✅ Maximum open positions: limit to 5
- ✅ Emergency stop button: taskkill /F /IM python.exe
- ✅ Monitor drawdown continuously

---

## 📞 GETTING HELP

### Check Documentation
1. Look in the errors section above
2. Review logs: `tail -f logs/main.log`
3. Run health check: `python main.py --mode health`

### Common Issues Resolution
1. Restart all services: `./stop_services.bat` → wait 5 seconds → `./start_all.bat`
2. Clear cache and restart
3. Check .env file credentials
4. Verify MT5 is running and connected
5. Check internet connectivity

### Escalation
1. Document the error and log output
2. Check logs/main.log for error message
3. Note time and exact steps to reproduce
4. Contact development team with full context

---

## 🎯 DAILY CHECKLIST

- [ ] Morning: Run `/health` in Telegram
- [ ] Monitor: Check dashboard every 4 hours
- [ ] Afternoon: Review active positions via `/active`
- [ ] Evening: Get daily summary with `/status`
- [ ] End of day: Document results in log file
- [ ] Weekly: Review strategy performance
- [ ] Monthly: Check account metrics & profitability

---

**Status:** ✅ Production Ready  
**Support:** Check logs and Telegram commands first  
**Next Level:** See 02_ARCHITECTURE_DEPLOYMENT.md for technical details

🚀 **Keep it simple, monitor regularly, stay alert!**
