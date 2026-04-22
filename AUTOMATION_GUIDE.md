# 🚀 TRADEPANEL AUTOMATION GUIDE
**Version:** 2.0  
**Date:** 2026-04-22  
**Scripts:** 2 (main.py + dashboard.py)  
**Status:** Production Ready  

---

## 📌 OVERVIEW

Two unified scripts consolidate all TradePanel operations:

1. **`main.py`** — Master control script for operations (paper trading, validation, backtesting, telegram, health checks)
2. **`dashboard.py`** — Web dashboard and monitoring interface

Each script uses **option flags** for easy configuration and automation.

---

## 🎯 QUICK START (2 minutes)

### Start Paper Trading
```bash
python main.py --mode paper-trade
```

### Start Dashboard
```bash
python dashboard.py --port 5000
# Then open: http://localhost:5000
```

### Start Telegram Bot
```bash
python main.py --mode telegram
```

### Run Full System (Everything)
```bash
python main.py --mode full
```

---

## 📚 MAIN.PY - MASTER CONTROL SCRIPT

### Available Modes

#### 1. Paper Trading Cycle
```bash
python main.py --mode paper-trade
```
**What it does:**
- Runs daily validation suite
- Executes paper trading
- Updates dashboards
- Logs results

**Output:** `logs/main.log`

#### 2. Validation Only
```bash
python main.py --mode validate
```
**What it does:**
- Tests all 25 strategies
- Validates parameters
- Generates performance matrix

**Output:** `logs/main.log`, `results/daily_validation/`

#### 3. Backtest Single Strategy
```bash
python main.py --mode backtest \
    --strategy range_breakout \
    --pair XAUUSD \
    --timeframe H4 \
    --limit 500
```
**Parameters:**
- `--strategy` (required): Strategy name
- `--pair` (optional): Pair (default: XAUUSD)
- `--timeframe` (optional): Timeframe (default: H1)
- `--limit` (optional): Bar limit

**Output:** Console output + `logs/main.log`

#### 4. Telegram Bot
```bash
python main.py --mode telegram
```
**What it does:**
- Starts Telegram bot
- Listens for commands
- Sends alerts

**Commands Available:**
- `/status` — Trading status
- `/balance` — Account balance
- `/active` — Open positions
- `/signals` — Recent signals
- `/analysis` — Market analysis
- `/health` — System health

**Output:** `logs/main.log`

#### 5. System Health Check
```bash
python main.py --mode health
```
**What it checks:**
- ✅ Environment variables
- ✅ Configuration files
- ✅ Database connection
- ✅ MT5 connection

**Output:** `logs/main.log`

#### 6. Full System (Everything)
```bash
python main.py --mode full
```
**What it does:**
1. Health check
2. Validation suite
3. Paper trading
4. (Does NOT start telegram - that's persistent)

**Use Case:** End-of-day complete validation

**Output:** `logs/main.log`, `results/daily_validation/`

#### 7. Scheduler Mode
```bash
python main.py --mode scheduler
```
**What it does:**
- Checks current time
- Runs appropriate tasks
- Used for cron/scheduler integration

**Output:** `logs/main.log`

---

## 🌐 DASHBOARD.PY - WEB MONITORING

### Start Web Dashboard
```bash
python dashboard.py --port 5000
```
**Access:** http://localhost:5000

### Accessible Endpoints
```
GET  http://localhost:5000/              → Web UI
GET  http://localhost:5000/api/metrics   → All metrics (JSON)
GET  http://localhost:5000/api/portfolio → Portfolio metrics
GET  http://localhost:5000/api/strategies → Strategy performance
GET  http://localhost:5000/api/health    → System health
GET  http://localhost:5000/api/trading   → Trading summary
GET  http://localhost:5000/docs          → API documentation
```

### Dashboard Modes

#### Web UI Mode (Default)
```bash
python dashboard.py --port 5000
```
- Opens web interface with real-time updates
- Auto-refreshes every 30 seconds
- Shows portfolio, health, strategies, trading summary

#### Metrics API Only
```bash
python dashboard.py --mode metrics
```
- Provides JSON API endpoints
- No web UI
- Good for external integrations

#### Live Monitoring
```bash
python dashboard.py --mode live
```
- Console-based live monitoring
- Real-time metrics updates
- Terminal-friendly format

### Custom Port & Host
```bash
# Listen on external network
python dashboard.py --port 8080 --host 0.0.0.0

# Custom internal port
python dashboard.py --port 9000 --host 127.0.0.1
```

---

## ⚙️ AUTOMATION SETUP

### Option 1: Manual Command Line

**Daily Paper Trading (from terminal):**
```bash
cd ~/TradePanel
python main.py --mode paper-trade
```

**Run Dashboard (separate terminal):**
```bash
cd ~/TradePanel
python dashboard.py --port 5000
```

**Run Telegram Bot (separate terminal):**
```bash
cd ~/TradePanel
python main.py --mode telegram
```

---

### Option 2: Cron Jobs (Linux/Mac)

**Edit crontab:**
```bash
crontab -e
```

**Add these lines:**
```bash
# Daily paper trading at 1:00 AM UTC
0 1 * * * cd /path/to/TradePanel && python main.py --mode paper-trade >> logs/cron-paper-trade.log 2>&1

# Daily validation at 6:00 AM UTC
0 6 * * * cd /path/to/TradePanel && python main.py --mode validate >> logs/cron-validate.log 2>&1

# Telegram bot (runs continuously)
@reboot cd /path/to/TradePanel && nohup python main.py --mode telegram > logs/telegram-bot.log 2>&1 &

# Dashboard (runs continuously)
@reboot cd /path/to/TradePanel && nohup python dashboard.py --port 5000 > logs/dashboard.log 2>&1 &

# Health check every 6 hours
0 */6 * * * cd /path/to/TradePanel && python main.py --mode health >> logs/cron-health.log 2>&1
```

**Verify cron jobs:**
```bash
crontab -l
```

---

### Option 3: Systemd Services (Linux)

#### Service 1: Paper Trading (Daily Task)
**Create `/etc/systemd/system/tradepanel-paper.timer`:**
```ini
[Unit]
Description=TradePanel Paper Trading Timer
Requires=tradepanel-paper.service

[Timer]
OnCalendar=*-*-* 01:00:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
```

**Create `/etc/systemd/system/tradepanel-paper.service`:**
```ini
[Unit]
Description=TradePanel Paper Trading
After=network.target

[Service]
Type=oneshot
User=your_username
WorkingDirectory=/path/to/TradePanel
ExecStart=/usr/bin/python3 main.py --mode paper-trade
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tradepanel-paper.timer
sudo systemctl start tradepanel-paper.timer
sudo systemctl status tradepanel-paper.timer
```

#### Service 2: Telegram Bot (Persistent)
**Create `/etc/systemd/system/tradepanel-telegram.service`:**
```ini
[Unit]
Description=TradePanel Telegram Bot
After=network.target
Wants=tradepanel-telegram.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TradePanel
ExecStart=/usr/bin/python3 main.py --mode telegram
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tradepanel-telegram
sudo systemctl start tradepanel-telegram
sudo systemctl status tradepanel-telegram
```

#### Service 3: Dashboard (Persistent)
**Create `/etc/systemd/system/tradepanel-dashboard.service`:**
```ini
[Unit]
Description=TradePanel Web Dashboard
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TradePanel
ExecStart=/usr/bin/python3 dashboard.py --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tradepanel-dashboard
sudo systemctl start tradepanel-dashboard
sudo systemctl status tradepanel-dashboard
```

**View logs:**
```bash
sudo journalctl -u tradepanel-telegram -f
sudo journalctl -u tradepanel-dashboard -f
```

---

### Option 4: Windows Task Scheduler

#### Task 1: Daily Paper Trading
1. Open Task Scheduler
2. Create Basic Task
3. Name: "TradePanel Paper Trading"
4. Trigger: Daily at 1:00 AM
5. Action:
   - Program: `C:\Python39\python.exe`
   - Arguments: `main.py --mode paper-trade`
   - Start in: `C:\path\to\TradePanel`

#### Task 2: Telegram Bot (Runs at Startup)
1. Create Basic Task
2. Name: "TradePanel Telegram Bot"
3. Trigger: At startup
4. Action:
   - Program: `C:\Python39\python.exe`
   - Arguments: `main.py --mode telegram`
   - Start in: `C:\path\to\TradePanel`

#### Task 3: Dashboard (Runs at Startup)
1. Create Basic Task
2. Name: "TradePanel Dashboard"
3. Trigger: At startup
4. Action:
   - Program: `C:\Python39\python.exe`
   - Arguments: `dashboard.py --port 5000`
   - Start in: `C:\path\to\TradePanel`

---

### Option 5: Docker Containers (Recommended for Production)

**Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs results/daily_validation

# Default: run paper trading
CMD ["python", "main.py", "--mode", "paper-trade"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  paper-trading:
    build: .
    container_name: tradepanel-paper
    command: python main.py --mode paper-trade
    volumes:
      - ./logs:/app/logs
      - ./results:/app/results
    env_file: .env
    restart: unless-stopped
    schedule:
      - "0 1 * * *"  # Daily at 1:00 AM UTC

  telegram-bot:
    build: .
    container_name: tradepanel-telegram
    command: python main.py --mode telegram
    volumes:
      - ./logs:/app/logs
    env_file: .env
    restart: always

  dashboard:
    build: .
    container_name: tradepanel-dashboard
    command: python dashboard.py --port 5000
    ports:
      - "5000:5000"
    volumes:
      - ./logs:/app/logs
      - ./results:/app/results
    env_file: .env
    restart: always
```

**Run:**
```bash
docker-compose up -d
docker-compose logs -f
```

---

## 📊 MONITORING & LOGS

### Log Locations
```
logs/main.log           — Main script operations
logs/dashboard.log      — Dashboard operations
logs/telegram_bot.log   — Telegram bot
logs/cron-*.log         — Cron job outputs
```

### View Logs
```bash
# Real-time main log
tail -f logs/main.log

# Real-time dashboard log
tail -f logs/dashboard.log

# Last 100 lines of telegram bot
tail -100 logs/telegram_bot.log

# Search for errors
grep ERROR logs/main.log
```

### Log Rotation (Linux)
**Create `/etc/logrotate.d/tradepanel`:**
```
/path/to/TradePanel/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 user user
    sharedscripts
}
```

---

## ✅ COMPLETE AUTOMATION EXAMPLE

### Daily Automated Trading Setup

**Step 1: Create startup script `start_all.sh`:**
```bash
#!/bin/bash

# Start all TradePanel services
cd /path/to/TradePanel

# Start Telegram bot (background)
nohup python main.py --mode telegram > logs/telegram-bot.log 2>&1 &
echo "✅ Telegram bot started"

# Start Dashboard (background)
nohup python dashboard.py --port 5000 > logs/dashboard.log 2>&1 &
echo "✅ Dashboard started"

# Wait for services to be ready
sleep 5

# Run daily cycle
python main.py --mode full
echo "✅ Daily cycle completed"
```

**Step 2: Make executable:**
```bash
chmod +x start_all.sh
```

**Step 3: Add to crontab:**
```bash
crontab -e
# Add:
0 0 * * * /path/to/TradePanel/start_all.sh >> /path/to/TradePanel/logs/start-all.log 2>&1
```

**Step 4: Verify:**
```bash
crontab -l
```

---

## 🚨 ERROR HANDLING

### Common Issues & Solutions

#### Issue: "Python not found"
```bash
# Use full path to Python
/usr/bin/python3 main.py --mode paper-trade
# Or
C:\Python39\python.exe main.py --mode paper-trade
```

#### Issue: ".env file not found"
```bash
# Ensure .env exists in TradePanel directory
ls -la .env
# Or create it:
cp .env.example .env
```

#### Issue: Database connection error
```bash
# Check database is running
psql -h 127.0.0.1 -U postgres -d trading_platform
# Check connection in logs
grep "database" logs/main.log
```

#### Issue: Permission denied
```bash
# Linux/Mac: Make script executable
chmod +x main.py dashboard.py
# Or run with python directly:
python main.py --mode paper-trade
```

---

## 📈 MONITORING CHECKLIST

**Daily:**
- [ ] Check logs for errors: `grep ERROR logs/main.log`
- [ ] Verify paper trading ran: Check `results/daily_validation/`
- [ ] Check dashboard is accessible: http://localhost:5000
- [ ] Verify telegram bot is online: Send `/status` command

**Weekly:**
- [ ] Review trading performance
- [ ] Check system health: `python main.py --mode health`
- [ ] Verify all strategies running
- [ ] Review alerts from past week

**Monthly:**
- [ ] Tier reassignments based on performance
- [ ] Update configuration if needed
- [ ] Archive old logs
- [ ] Plan for Phase 4 if Phase 3 passed

---

## 🎯 PRODUCTION DEPLOYMENT CHECKLIST

Before going live:

- [ ] All scripts have proper error handling
- [ ] Logging is configured and working
- [ ] Backups are in place
- [ ] Database is backed up daily
- [ ] .env file is secure (not in git)
- [ ] Cron/scheduler jobs are set up
- [ ] Dashboard is accessible and working
- [ ] Telegram bot is responding to commands
- [ ] MT5 connection is stable
- [ ] Email alerts configured (if needed)
- [ ] Health checks passing
- [ ] Log rotation configured
- [ ] Monitoring and alerting active

---

## 📞 SUPPORT & TROUBLESHOOTING

### Quick Debug Commands

```bash
# Test main script with verbose output
python main.py --mode health

# Test database connection
python -c "from data.db_client import DBClient; db = DBClient(); print(db.execute_query('SELECT 1'))"

# Test MT5 connection
python -c "from mt5_bridge.connector import MT5Connector; c = MT5Connector(); print('Connected' if c.is_connected() else 'Disconnected')"

# Test telegram bot
python main.py --mode telegram  # Should show "Bot is active"

# View all processes
ps aux | grep python
ps aux | grep tradepanel

# Kill specific process
pkill -f "main.py --mode telegram"
```

---

## 🚀 NEXT STEPS

1. **Choose automation method** (Cron, Systemd, Docker, etc.)
2. **Set up first automation** (e.g., daily paper trading)
3. **Monitor logs** for first week
4. **Verify automation** is working
5. **Add more tasks** (dashboard, telegram, etc.)
6. **Configure alerts** if needed
7. **Document your setup** for your team

---

**Status:** ✅ Production Ready  
**Scripts:** 2 (main.py + dashboard.py)  
**Options:** 7 modes + flexible automation  
**Support:** Comprehensive error handling & logging  

Start automating now! 🚀

