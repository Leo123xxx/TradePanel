# TradePanel Telegram Bot — Complete Documentation

**Updated:** May 10, 2026  
**Status:** Operational with improved whitelist feedback  
**Commands:** 30+ available

---

## 🤖 Overview

The TradePanel Telegram Bot provides real-time control and monitoring of your trading system via Telegram messaging.

**Features:**
- ✅ Real-time account status & positions
- ✅ Signal monitoring & approval
- ✅ Strategy control (enable/disable)
- ✅ Performance analytics
- ✅ System health monitoring
- ✅ Automated daily reports

---

## 🚀 Getting Started

### Part 1: Whitelist Your Chat ID (Required)

See: **TELEGRAM_WHITELIST_SETUP.md** (quick 2-minute setup)

**Quick version:**
```
1. Send /start to bot
2. Copy Chat ID from error message
3. Add to .env: ALLOWED_CHAT_IDS=YOUR_ID
4. Restart bot
5. Send /start again → Success ✅
```

### Part 2: Start Using Commands

```
/help              — Full command list
/status            — Account summary
/signals           — Recent signals
/active            — Open positions
```

---

## 📖 Complete Command Reference

### 📊 Account & Monitoring

#### `/status`
Shows account status, open positions, and bot state.

```
💹 System Status
👤 Account: 123456
💰 Equity: 10,500 ZAR
🟢 Bot Status: ACTIVE
🛠 Mode: LIVE (28 strategies)
📊 Open Positions: 3
  ▲ EURUSD 0.1 lot +50 ZAR
  ▼ GBPUSD 0.2 lot -25 ZAR
  ▲ XAUUSD 0.05 lot +150 ZAR
```

---

#### `/balance`
Current account balance and free margin.

```
💰 Balance Info
Balance: 10,000 ZAR
Equity: 10,500 ZAR
Free Margin: 7,500 ZAR
```

---

#### `/active`
All open positions with entry, SL, TP, and profit.

```
📊 Active Positions

🔵 BUY EURUSD (Ticket: 12345)
└ Entry: 1.0850 | SL: 1.0800 | TP: 1.0950
└ Profit: +50.00 ZAR | Duration: 2h 15m
```

---

#### `/risk`
Risk metrics: drawdown, margin level, daily P&L.

```
📈 Risk Status
Equity: 10,500 ZAR
Margin Level: 140%
Drawdown: 5.0%
Daily P&L: +250 ZAR
```

---

### 🛰️ Signal Management

#### `/signals`
Recent signals from last 24 hours with trading targets.

```
🛰 Recent Strategy Signals

EURUSD BUY | Strategy: dual_ema_momentum
  Entry: 1.0850-1.0870 | SL: 1.0800 | TP1: 1.0900 | TP2: 1.0950
  Status: ✅ TAKEN | 2h 15m ago

GBPUSD SELL | Strategy: ema_ribbon_trend
  Entry: 1.2750-1.2780 | SL: 1.2850 | TP1: 1.2650 | TP2: 1.2550
  Status: ⏳ Not taken | 30m ago
```

---

#### `/pending_trades`
Signals awaiting manual approval (if approval mode enabled).

```
⏳ Trades Awaiting Approval (2)

EURUSD BUY | dual_ema_momentum
  Created: 14:23 SAST (2m ago)
  /approve_trade_abc123 or /reject_trade_abc123

XAUUSD SELL | volatility_breakout
  Created: 14:18 SAST (7m ago)
  /approve_trade_def456 or /reject_trade_def456
```

---

#### `/approve_trade <signal_id>`
Approve a pending signal for execution.

```
✅ Trade Approved

Signal ID: abc123
Pair: EURUSD
Direction: BUY
Strategy: dual_ema_momentum

Will execute on next cycle (within 15 min)
```

---

#### `/reject_trade <signal_id> [reason]`
Reject a signal (prevent execution).

```
❌ Trade Rejected

Pair: EURUSD
Direction: BUY
Reason: Spread too wide

This signal will NOT execute.
```

---

### 📈 Analysis & Reports

#### `/backtest_report`
Summary of last overnight backtest.

```
📊 Last Overnight Backtest
🕒 2026-05-10 02:00 UTC
━━━━━━━━━━━━━━━
✅ Pass: 35  ⚠️ Review: 8  ❌ Skip: 2

🏆 Top Performers:
  • dual_ema_momentum EURUSD H1
    WR=65.2% | Sharpe=1.45
  • turtle_soup XAUUSD M5
    WR=58.3% | Sharpe=1.12
```

---

#### `/best_pairs`
Top pairs ranked by win rate.

```
📈 Best Pairs by Win Rate
━━━━━━━━━━━━━━━
🥇 EURUSD   62.5% avg WR  (12 combos)
🥈 XAUUSD   58.3% avg WR  (8 combos)
🥉 GBPUSD   56.1% avg WR  (9 combos)
```

---

#### `/top_strategies`
Top 5 strategies by Sharpe ratio.

```
🏅 Top 5 Strategies by Sharpe
━━━━━━━━━━━━━━━
1. ✅ dual_ema_momentum
   Sharpe=1.45 | WR=65.2% | DD=12.3% | T1
2. ✅ turtle_soup
   Sharpe=1.23 | WR=58.3% | DD=15.1% | T2
```

---

#### `/analysis`
Multi-timeframe market regime analysis.

```
📊 Market Analysis
━━━━━━━━━━━━━━━
Global Macro Bias: BULLISH (+0.8)
USD Strength: NEUTRAL (0.2)
Risk Sentiment: RISK-ON (+0.6)

M1/M5:  BULLISH  (Fast momentum)
H1/H4:  NEUTRAL  (Consolidation)
D1:     BULLISH  (Uptrend)
```

---

#### `/signal_performance`
Signal accuracy over last 7 days.

```
📊 Signal Performance (7d)
━━━━━━━━━━━━━━━
🟢 dual_ema_momentum
   WR: 65.0% (13/20) | Avg: +12.5 pips
🟡 turtle_soup
   WR: 42.1% (8/19) | Avg: +2.3 pips
🔴 ema_ribbon_trend
   WR: 38.9% (7/18) | Avg: -8.1 pips
```

---

### 🛠️ Strategy Control

#### `/mode`
Show active strategies and trading mode.

```
🛠 Operating Mode: LIVE

📋 Active Strategies (28):
  • dual_ema_momentum [T1]
    └ EURUSD, GBPUSD (H1, H4)
  • turtle_soup [T2]
    └ XAUUSD, XAGUSD (M5, M15)
  • ... and 26 more
```

---

#### `/enable <strategy_name>`
Enable a strategy.

```
✅ Enabled bb_mean_reversion

Change takes effect on next strategy cycle.
```

---

#### `/disable <strategy_name>`
Disable a strategy.

```
⛔ Disabled bb_mean_reversion

No new trades will be generated for this strategy.
```

---

### ⏸️ Bot Control

#### `/pause [minutes]`
Pause the bot (block new trades).

```
⏸ Bot paused for 30 minutes

New entries blocked until 15:23 SAST.
Existing positions continue normally.
```

---

#### `/resume`
Resume trading after pause.

```
▶️ Bot resumed

Trading re-enabled. New signals will execute.
```

---

#### `/news_blackout [minutes]`
Block trades during news events.

```
🔇 News blackout active until 16:00 SAST

No new entries allowed. Existing trades continue.
```

---

### 🏥 System Health

#### `/health`
System health and last heartbeat.

```
🏥 System Health
🟢 Last heartbeat: 2026-05-10 14:57:49
⚠️ Alerts (24h): 2
```

---

#### `/backups`
Database backup status.

```
💾 Database Backups Status
━━━━━━━━━━━━━━━
Local Backups (Latest 3):
  📁 trading_platform_20260510_020000.sql.gz
    └ 02:00 SAST | 125.4 MB
  📁 trading_platform_20260509_020000.sql.gz
    └ 02:00 SAST | 124.8 MB

Cloud Sync Status:
🟢 2026-05-10 02:00 SAST
   └ R2: ✅ | S3: ✅
```

---

#### `/data`
Data coverage - latest bar per pair.

```
📡 Data Coverage
━━━━━━━━━━━━━━━
🟢 EURUSD  M1: 05-10 14:57  D1: 2026-05-10
🟢 XAUUSD  M1: 05-10 14:56  D1: 2026-05-10
🔴 BTCUSD  M1: 05-10 14:45  D1: 2026-05-09
```

---

### 🖊️ Manual Trading

#### `/trade <symbol> <BUY|SELL> <lots>`
Log a manual trade entry.

```
✅ Manual trade logged

Symbol: EURUSD
Direction: BUY
Lots: 0.1
Entry: 1.0850

Use /close_manual <ticket> to exit.
```

---

#### `/close_manual <ticket>`
Log a manual trade exit.

```
✅ Manual trade closed

EURUSD BUY @ 1.0850 → SELL @ 1.0900
P&L: +50.00 ZAR
```

---

### 🔐 Authorization & Monitoring

#### `/extract_chat_id`
Extract your Chat ID from logs (if authorized).

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

#### `/auth_log [hours] [limit]`
Show unauthorized access attempts (admin).

```
Usage: /auth_log 24 20

🚨 Unauthorized Access Attempts (24h)
━━━━━━━━━━━━━━━━━━━━━━━━━
Chat ID: 9876543210
User: Unknown User
Command: /status
Time: 2026-05-10 14:30:25
Attempts: 3
```

---

#### `/auth_users [limit]`
Show authorized users and activity (admin).

```
Usage: /auth_users 50

✅ Authorized Users
━━━━━━━━━━━━━━━━━━━━━━━━━
1. @yourname
   Chat ID: 5838483717
   Commands: 245
   Last Access: 2026-05-10 16:45:30
```

---

#### `/auth_daily [days]`
Show daily authorization summary (admin).

```
Usage: /auth_daily 7

📊 Authorization Summary (7d)
━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 2026-05-10
   Attempts: 45 | Unique Users: 2
```

---

#### `/suspicious [threshold] [hours]`
Show suspicious access patterns (admin).

```
Usage: /suspicious 5 24

🚨 Suspicious Access Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━
IP: 192.168.1.100
Attempts: 8 | Unique Chat IDs: 2
```

---

### 📞 System Commands

#### `/help`
Full command list (this page).

#### `/dashboard`
Link to web dashboard.

```
🔗 TradePanel Web Dashboard:
http://localhost:5000

(Only accessible from your machine)
```

---

## 🔧 Architecture

### File Structure
```
notifications/
├── telegram_bot.py         ← Main bot logic
├── router.py               ← Command responses
├── analyzer.py             ← Market analysis
├── templates.py            ← Message templates
├── auth_logger.py          ← Authorization logging
└── auth_commands.py        ← Auth monitoring commands

database/migrations/
└── auth_logging.sql        ← Auth log schema + views

scripts/
└── start_telegram_bot.py   ← Start the bot
```

### Startup Sequence
```
1. Load .env (token, chat ID, credentials)
2. Create TelegramBot instance
3. Set up command handlers (30+ commands)
4. Start listening for messages
5. Check authorization on each message
6. Route to appropriate handler
7. Send formatted response
```

### Authorization Flow
```
User sends message
    ↓
Extract Chat ID from Telegram
    ↓
Check against ALLOWED_CHAT_IDS in .env
    ↓
If not authorized: Show Chat ID + error
If authorized: Execute command
    ↓
Format response using templates.py
    ↓
Send to Telegram
```

---

## 🔐 Security

### Authentication
- ✅ Each user needs whitelisted Chat ID
- ✅ Token secured in .env (not in code)
- ✅ Commands log authorization attempts
- ✅ No command echoes sensitive data

### Authorization
```python
@auth_required  # Decorator on every command handler
async def handle_status(self, update, context):
    # Only executes if Chat ID is whitelisted
    return await update.message.reply_html(status_msg)
```

### Whitelisting
```bash
# Single user
TELEGRAM_CHAT_ID=5838483717

# Multiple users
ALLOWED_CHAT_IDS=5838483717,1234567890,9876543210
```

---

## 📋 Setup Checklist

- [ ] Get TELEGRAM_BOT_TOKEN (already in .env)
- [ ] Get your Chat ID (send /start, copy from error)
- [ ] Add to .env: `ALLOWED_CHAT_IDS=YOUR_ID`
- [ ] Start bot: `python scripts/start_telegram_bot.py`
- [ ] Test: `/start` → see help menu
- [ ] Test: `/status` → see account info
- [ ] Test: `/signals` → see pending signals
- [ ] Enable commands needed for your workflow

---

## 🚀 Quick Testing Commands

```
/start              → Bot initialization
/help               → Full help menu
/status             → Quick account overview
/signals            → See signals
/active             → See positions
/backtest_report    → Last overnight results
```

---

## ⚡ Common Workflows

### Workflow 1: Monitor Daily
```
Morning:   /status         → Check account
           /backtest_report → Review overnight results
           
Throughout day:
           /signals        → Watch new signals
           /active         → Monitor positions
           
Evening:   /risk           → Review daily results
```

---

### Workflow 2: Control Trading
```
Before trades:
  /mode             → Verify 28 strategies enabled
  /pause 60         → Pause for events
  
After events:
  /resume           → Resume trading
  /signals          → Check pending
```

---

### Workflow 3: Strategy Management
```
Review poor strategies:
  /top_strategies   → Find underperforming
  /signal_performance → Check win rates
  
Make adjustments:
  /disable <name>   → Turn off poor strategy
  /enable <name>    → Turn on good strategy
```

---

## 🐛 Troubleshooting

### "Unauthorized" Error
**Solution:** See TELEGRAM_WHITELIST_SETUP.md

### Command Not Responding
1. Check bot process: `python scripts/start_telegram_bot.py`
2. Check internet connection
3. Verify Chat ID is whitelisted
4. Restart bot

### Message Too Long (Split)
Commands with lots of data auto-split at 4096 chars.
This is normal - read all messages.

### Bot Offline
```powershell
# Check if running
tasklist | find "python"

# If not, restart
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
python scripts/start_telegram_bot.py
```

---

## 📞 Next Steps

1. **Get Whitelisted:** See TELEGRAM_WHITELIST_SETUP.md
2. **Test Commands:** Start with `/help` and `/status`
3. **Monitor Signals:** Use `/signals` and `/active`
4. **Control Bot:** Use `/pause`, `/resume`, `/enable`, `/disable`
5. **Track Performance:** Use `/backtest_report` and `/top_strategies`

---

**Bot Status:** ✅ Operational  
**Commands Available:** 30+  
**Whitelist System:** ✅ Improved with Chat ID display  
**Last Updated:** May 10, 2026

Ready to use! See TELEGRAM_WHITELIST_SETUP.md to get started. 🚀
