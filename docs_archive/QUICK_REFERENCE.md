# ⚡ TRADEPANEL QUICK REFERENCE
**For:** All users  
**Length:** 2 minutes to master both scripts  

---

## 🎯 TWO SCRIPTS, EVERYTHING COVERED

| Script | Purpose | Example |
|--------|---------|---------|
| **main.py** | Operations & control | `python main.py --mode paper-trade` |
| **dashboard.py** | Monitoring & web UI | `python dashboard.py --port 5000` |

---

## 🚀 MAIN.PY - OPERATIONS (One-off commands)

### Start Here
```bash
python main.py --help  # See all options
```

### Most Common Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `python main.py --mode paper-trade` | Run daily trading cycle | Console + logs/main.log |
| `python main.py --mode validate` | Test all strategies | Console + results/ |
| `python main.py --mode health` | System health check | Console |
| `python main.py --mode telegram` | Start Telegram bot | Telegram commands active |
| `python main.py --mode full` | Run everything | Console + full logs |

### Backtesting
```bash
# Test single strategy
python main.py --mode backtest --strategy range_breakout --pair XAUUSD --timeframe H4

# With bar limit
python main.py --mode backtest --strategy ma_crossover --pair EURUSD --limit 500
```

### Options for All Modes
```bash
--quiet    # Suppress console output (log to file only)
--help     # Show all available modes
```

---

## 🌐 DASHBOARD.PY - MONITORING (Persistent server)

### Start Dashboard
```bash
python dashboard.py --port 5000
# Open: http://localhost:5000
```

### Access Points
```
Web UI:     http://localhost:5000
API:        http://localhost:5000/api/metrics
Docs:       http://localhost:5000/docs
```

### Custom Configuration
```bash
python dashboard.py --port 8080 --host 0.0.0.0  # External access
python dashboard.py --mode metrics                # API only
```

---

## 🎬 QUICK START (5 minutes)

### Setup 1: Interactive Mode
```bash
# Terminal 1: Start paper trading
python main.py --mode paper-trade

# Terminal 2: Start dashboard
python dashboard.py --port 5000

# Terminal 3: Start telegram bot
python main.py --mode telegram

# Then access: http://localhost:5000
```

### Setup 2: Automated (1 cron job)
```bash
# Add to crontab:
0 1 * * * cd /path/to/TradePanel && python main.py --mode paper-trade
```

### Setup 3: Production (systemd)
```bash
# See AUTOMATION_GUIDE.md for full setup
```

---

## 📋 MODES EXPLAINED

### main.py Modes

**paper-trade** — Daily trading cycle
- Runs validation suite
- Executes paper trades  
- Updates dashboards
- Duration: 5-10 minutes
- **Use:** Automated daily

**validate** — Test all strategies
- Tests 25 strategies
- Validates parameters
- No actual trading
- Duration: 2-3 minutes
- **Use:** Verification before trading

**backtest** — Test single strategy
- Requires: `--strategy NAME`
- Optional: `--pair`, `--timeframe`, `--limit`
- Full historical backtest
- Duration: 1-5 minutes depending on data
- **Use:** Strategy testing

**telegram** — Start bot
- Listens for `/command` messages
- Responds with trading info
- Runs forever (press CTRL+C to stop)
- **Use:** Manual monitoring & alerts

**health** — System check
- Verifies all connections
- Tests configuration
- Duration: 30 seconds
- **Use:** Troubleshooting

**full** — Run everything
- Validation + Paper Trading
- Does not include Telegram (separate)
- Duration: 10-15 minutes
- **Use:** End-of-day validation

**scheduler** — For cron integration
- Checks time, runs appropriate tasks
- Automatically decides what to execute
- **Use:** Cron/scheduler jobs

### dashboard.py Modes

**web** — Web UI (default)
- Shows dashboard interface
- Real-time updates (every 30s)
- Metrics + charts
- **Access:** http://localhost:5000

**metrics** — API only
- JSON endpoints
- No web interface
- Good for integrations
- **Access:** http://localhost:5000/api/metrics

**live** — Console monitoring
- Terminal-based monitoring
- Real-time updates
- No web UI needed

---

## 🔄 TYPICAL DAILY WORKFLOW

### Manual (During Development)
```bash
# Morning: Check health
python main.py --mode health

# Midday: Backtest a strategy
python main.py --mode backtest --strategy range_breakout

# End of day: Full validation
python main.py --mode full

# Evening: Monitor dashboard
python dashboard.py --port 5000
```

### Automated (Production)
```bash
# 1:00 AM UTC: Cron runs paper-trade automatically
# 24/7: Telegram bot responds to commands
# 24/7: Dashboard available on port 5000
# No manual intervention needed!
```

---

## 📊 TELEGRAM COMMANDS

Once bot is running, send these in Telegram:

| Command | Returns |
|---------|---------|
| `/status` | Trading status & strategy list |
| `/balance` | Account balance & equity |
| `/active` | Open positions & entries |
| `/signals` | Recent signals (last 24h) |
| `/analysis` | Multi-timeframe analysis |
| `/health` | System health status |
| `/risk` | Drawdown & risk metrics |
| `/help` | List all commands |

---

## 📈 DASHBOARD METRICS

What you see on http://localhost:5000:

**Portfolio Status**
- Strategy count
- Test pass rate
- Overall status

**System Health**
- Database: OK/ERROR
- MT5: Connected/Disconnected
- Alerts (24h): Number

**Trading Summary**
- Today trades
- Win rate
- P&L today

**Top Strategies**
- Strategy name & pair
- Win rate %
- Trade count
- Average P&L

---

## ⚙️ CONFIGURATION

### Required (.env file)
```
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=your_server
DB_HOST=127.0.0.1
DB_NAME=trading_platform
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Optional
```
DEFAULT_PAIR=XAUUSD
DEFAULT_TIMEFRAME=H1
```

---

## 🚨 COMMON PROBLEMS

| Problem | Solution |
|---------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "TELEGRAM_BOT_TOKEN not found" | Add token to .env file |
| "Database connection error" | Check PostgreSQL is running |
| "MT5 not connected" | Verify MT5 terminal is open |
| "Port already in use" | Use different port: `--port 8080` |
| "Permission denied" | Make script executable: `chmod +x main.py` |

---

## 🎯 CHEAT SHEET

### Quick Copy-Paste

**Test everything:**
```bash
python main.py --mode health && python main.py --mode validate
```

**Start full system:**
```bash
nohup python main.py --mode telegram > logs/telegram.log 2>&1 &
nohup python dashboard.py --port 5000 > logs/dashboard.log 2>&1 &
python main.py --mode paper-trade
```

**Add daily automation (crontab):**
```bash
0 1 * * * cd /path/to/TradePanel && python main.py --mode paper-trade
```

**Check if processes running:**
```bash
ps aux | grep python | grep -E "main|dashboard"
```

**Stop all processes:**
```bash
pkill -f "python.*main.py"
pkill -f "python.*dashboard.py"
```

---

## 📚 FULL DOCUMENTATION

For complete details, see:
- **AUTOMATION_GUIDE.md** — Setup & automation (cron, systemd, Docker)
- **TELEGRAM_BOT_SETUP.md** — Telegram bot detailed guide
- **FINAL_AGENT_HANDOVER_PHASE3.md** — Phase 3-4 roadmap

---

## ✅ VERIFICATION CHECKLIST

### First Time Setup
- [ ] Python 3.9+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file configured: `ls -la .env`
- [ ] Logs directory exists: `mkdir -p logs`
- [ ] Test health check: `python main.py --mode health`
- [ ] Test validation: `python main.py --mode validate`
- [ ] Start dashboard: `python dashboard.py --port 5000`

### Daily Checks
- [ ] Health check passing: `python main.py --mode health`
- [ ] Dashboard accessible: http://localhost:5000
- [ ] Telegram bot responding: Send `/status`
- [ ] No errors in logs: `grep ERROR logs/*.log`

---

## 🚀 LAUNCH SEQUENCES

### Development (Interactive)
```bash
# Terminal 1
python main.py --mode validate

# Terminal 2
python dashboard.py --port 5000

# Terminal 3
python main.py --mode telegram
```

### Production (Automated)
```bash
# 1 cron job
0 1 * * * python main.py --mode full

# 2 systemd services
systemctl start tradepanel-telegram
systemctl start tradepanel-dashboard
```

### Testing (Quick)
```bash
python main.py --mode health
python main.py --mode backtest --strategy range_breakout
```

---

## 💡 TIPS

1. **Use `--quiet` flag** to suppress console output when running in background
2. **Check logs** regularly: `tail -f logs/main.log`
3. **Dashboard auto-refreshes** every 30 seconds - no manual refresh needed
4. **Telegram bot runs 24/7** - good for monitoring while away
5. **Backtest is quick** - use for strategy testing without full cycle
6. **Health check first** - verify system before running trades
7. **Full mode at night** - run complete validation when not trading

---

**That's it!** 🎉  
Two scripts, all operations covered. Pick your mode, run it, done.

For detailed setup → **AUTOMATION_GUIDE.md**  
For troubleshooting → **Logs in logs/ directory**  
For Telegram help → **TELEGRAM_BOT_SETUP.md**

