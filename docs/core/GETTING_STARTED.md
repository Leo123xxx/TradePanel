# Getting Started with TradePanel

Complete setup and installation guide for the MT5 trading bot.

---

## Prerequisites

- **Python 3.9+** (3.11 recommended)
- **MetaTrader 5** installed on your computer
- **PostgreSQL** (optional, for data logging)
- **Telegram Account** (optional, for notifications)

---

## Installation (10 minutes)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd TradePanel
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
- MetaTrader5 — MT5 API
- FastAPI — Web dashboard
- APScheduler — Task scheduling
- PostgreSQL — Database (optional)
- pyyaml — Configuration
- ta-lib — Technical analysis

---

## Configuration (5 minutes)

### 1. Edit config/config.yaml

**Account Setup:**
```yaml
system:
  mode: paper  # Change to 'live' for real trading
  log_level: INFO

risk_management:
  risk_per_trade_pct: 2.0        # 2% of account per trade
  max_lot_size: 0.15              # Max position size (Capped 2026-05-06)
  max_concurrent_positions: 5    # Max open trades
  max_drawdown_hard_pct: 15.0    # Auto-pause at 15% DD
```

**Your Trading Pairs:**
```yaml
pairs:
  XAUUSD:
    enabled: true
    spread_pips: 5.0
    slippage_pips: 2.0
    # ... other settings
```

### 2. Edit config/strategies.yaml

**Active Strategies:**
```yaml
strategies:
  - name: dual_ema_fractal
    enabled: true
    pairs: [EURUSD]
    timeframes: [H1]
  
  - name: rsi_bounce
    enabled: true
    pairs: [EURUSD]
    timeframes: [H1]
```

See STRATEGIES.md for all available strategies.

### 3. Set Environment Variables (optional)
```bash
export MT5_LOGIN=12345
export MT5_PASSWORD=your_password
export MT5_SERVER=YourBrokerServer
export TELEGRAM_TOKEN=your_bot_token
export TELEGRAM_CHAT_ID=your_chat_id
```

---

## Running the Bot

### 🚀 Unified Management (Recommended)
Use the unified `trade.bat` script for all operations:
```powershell
.\trade.bat start    # Start all services (Docker + MT5 Bridge)
.\trade.bat status   # Show container status
.\trade.bat logs     # Tail all service logs
.\trade.bat stop     # Stop all services
```

### Manual Execution (Python)
If you prefer running directly via Python:

#### Paper Trading (TEST MODE)
```bash
python main.py paper-trade
```

#### Live Trading (REAL MONEY)
```bash
python main.py live-trade
```

#### Backtesting
```bash
.\trade.bat backtest dual_ema_fractal EURUSD H1
# OR
python -m scripts.run_backtest --strategy dual_ema_fractal --pair EURUSD --timeframe H1
```

---

## Dashboard & Monitoring

### Web Dashboard
```
http://tradepanel.mraskwhy.local/
```

The **Modernized v1.1 Hub** shows real-time:
- **Active Strategy Configs**: View live parameters (Lots, ATR mults) for every enabled strategy.
- **Account Profiles**: Real-time balance, equity, and MT5 history sync.
- **Advanced Filters**: Server-side filtering for backtest history.
- **High Efficiency**: SWR-enabled caching for zero redundant API calls.

### REST API
```
http://localhost:8000/docs
```

API endpoints for:
- Getting balance
- Placing orders
- Viewing positions
- Trading history

### View Logs
The easiest way is:
```powershell
.\trade.bat logs
```

Or view specific files:
```bash
# Paper trading logs
tail -f logs/paper_engine.log

# API logs
tail -f logs/api.log

# Docker logs
docker logs tradepanel-scheduler -f
```

---

## Telegram Notifications (Optional)

### Setup Telegram Bot

1. Create a bot with @BotFather on Telegram
2. Get your chat ID from @userinfobot
3. Add to config.yaml:
```yaml
notifications:
  telegram_enabled: true
  telegram_token: "YOUR_BOT_TOKEN"
  telegram_chat_id: "YOUR_CHAT_ID"
```

You'll now get alerts for:
- Trade opens and closes
- Drawdown warnings
- System errors
- Daily P&L summaries

---

## Database Setup (Optional)

If you want to log all trades and signals:

### PostgreSQL Installation
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows - Download from postgresql.org
```

### Create Database
```bash
createdb tradepanel_db
psql tradepanel_db < schema.sql
```

### Add to config.yaml
```yaml
database:
  enabled: true
  host: localhost
  port: 5432
  user: postgres
  password: your_password
  database: tradepanel_db
```

---

## Common Configuration Changes

### Disable Certain Strategies
```yaml
# In config/strategies.yaml
bb_mean_reversion:
  enabled: false  # Won't run
```

### Change Risk Level
```yaml
# In config/config.yaml - reduce risk
risk_management:
  risk_per_trade_pct: 1.0    # 1% instead of 2%
  max_drawdown_hard_pct: 10.0  # 10% instead of 15%
```

### Add New Pair
```yaml
pairs:
  GBPUSD:
    enabled: true
    spread_pips: 1.5
    slippage_pips: 0.8
    # ... other settings
```

---

## Troubleshooting Setup

### MT5 Connection Failed
```
Error: "Could not connect to MT5"
```
**Fix:**
1. Open MetaTrader 5 on your computer
2. Go to Tools → Options → Expert Advisors
3. Enable "Allow automated trading"
4. Verify you're on the right broker server

### Port Already in Use
```
Error: "Address already in use :5000"
```
**Fix:**
```bash
# Change port in config.yaml
webapp:
  port: 5001  # Use different port
```

### Import Errors
```
Error: "ModuleNotFoundError: No module named 'MetaTrader5'"
```
**Fix:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## Next Steps

1. **Configure your account** → Edit config/config.yaml
2. **Start paper trading** → `python main.py paper-trade`
3. **Check dashboard** → Open http://localhost:5000
4. **Review logs** → `tail -f logs/*.log`
5. **Learn strategies** → Read STRATEGIES.md
6. **Fix issues** → See TROUBLESHOOTING.md

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| CPU | 2+ cores |
| RAM | 2 GB minimum, 4 GB recommended |
| Disk | 500 MB + space for market data |
| Network | Stable internet connection |
| OS | Windows / macOS / Linux |

---

**Stuck? Check TROUBLESHOOTING.md for common issues.**

