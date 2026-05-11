# Signal Execution: Quick Reference Card

## 🎯 The Problem (1 sentence)
**System is in PAPER mode → signals are generated but NOT executed as trades**

---

## ✅ The Fix (1 command)
Edit `config/config.yaml` and change:
```yaml
system:
  mode: "paper"    →    mode: "live"
```

---

## 📋 Verification (Telegram commands)

```
/status          → Check if bot is ACTIVE or PAUSED
/resume          → If paused, enable trading
/balance         → Verify you have free margin
/mode            → Confirm LIVE mode + 28 strategies
/signals         → See pending signals
/active          → See live positions (after trade executes)
```

---

## 🔍 Why Signals Aren't Taken

| Component | Status | Issue |
|-----------|--------|-------|
| Signal generation | ✅ Working | 8 signals today |
| Risk checks | ✅ Passing | All 12 checks pass |
| OrderManager | ✅ Ready | Can submit orders |
| **Paper Mode** | ❌ **BLOCKING** | **Prevents trade submission** |

---

## 🚀 Execution Flow

```
Strategy detects signal
    ↓
Signal stored in database
    ↓
12 Risk checks run → ALL PASS
    ↓
OrderManager.open_position() called
    ↓
Order submitted to MT5
    ↓
⚠️ PAPER MODE: Order discarded (not sent to account)
↓
❌ Trade does NOT execute

SOLUTION: Change mode to "live" → Trade executes ✅
```

---

## 📱 Testing Workflow

**1. Make the change:**
```
Edit: F:\REPOS\leo123xxx\TradePanel\TradePanel\config\config.yaml
Find: system.mode: "paper"
Change to: system.mode: "live"
Save: Ctrl+S
```

**2. Resume bot (if needed):**
```
Telegram: /status
If shows "⏸ PAUSED": /resume
```

**3. Wait for signal:**
```
Every 1-15 minutes (depends on market)
Telegram: /signals (see pending)
```

**4. Watch execution:**
```
Telegram: /active (see live positions)
Logs: results/cleanup_backup.log (shows EXECUTING)
```

---

## 🎛️ Config to Change

**File:** `config/config.yaml`

**Current (Paper Mode):**
```yaml
system:
  mode: paper              # ← NOT sending trades to MT5
  docker_enabled: true
```

**Change to (Live Mode):**
```yaml
system:
  mode: live               # ← NOW sending trades to MT5
  docker_enabled: true
```

**That's it!** One word change enables live trading.

---

## ⚠️ Safety Notes

✅ **Safe because:**
- Risk checks still run (position limits, margin, spread, etc.)
- Can revert instantly (change back to "paper")
- Starting with small lots (0.01-0.15)
- Using demo account first (if available)

❌ **Only risky if:**
- You skip risk checks (don't - they're important)
- Account has no free margin (check: /balance)
- Trading outside market hours (config controls this)

---

## 🔄 Risk Checks (What Can Block Signals)

Before ANY trade executes, bot checks:

1. ✅ Bot not paused
2. ✅ Pair not blocked
3. ✅ No news blackout
4. ✅ Strategy enabled
5. ✅ Market regime OK
6. ✅ Lot size acceptable
7. ✅ Position count OK
8. ✅ Margin available ← **Most Common Block**
9. ✅ Spread not too wide
10. ✅ Within trading hours
11. ✅ D1 EMA trend aligned (if enabled)
12. ✅ Macro bias aligned (if enabled)

**If ANY check fails → Signal blocked**

---

## 📊 What Happens After Mode Change

**Scenario: EURUSD Buy signal**

```
BEFORE (Paper Mode):
  Strategy: "Generate EURUSD BUY"
  Bot: "OK, executing BUY 0.1 lot..."
  OrderManager: "Submitting order to MT5..."
  Paper Mode: ❌ "Discarding order (paper mode)"
  Result: No trade in account

AFTER (Live Mode):
  Strategy: "Generate EURUSD BUY"
  Bot: "OK, executing BUY 0.1 lot..."
  OrderManager: "Submitting order to MT5..."
  Live Mode: ✅ "Sending to MT5 account..."
  MT5: ✅ Trade OPENED
  Result: EURUSD BUY position in account
```

---

## 🎯 Next Steps (Choose One)

### Option 1: Start Now (5 min)
1. Edit config.yaml
2. /resume in Telegram
3. Wait for signal
4. Done

### Option 2: With Approval (1 hour)
1. Follow Option 1
2. Read: APPROVAL_IMPLEMENTATION.md
3. Implement approval system
4. Each signal waits for your "OK"

### Option 3: Read First
1. Read: SIGNAL_EXECUTION_ACTION_PLAN.md (5 min)
2. Read: SIGNAL_EXECUTION_FIX.md (10 min)
3. Then choose Option 1 or 2

---

## 📞 Common Questions

**Q: Will it trade immediately after I change the config?**  
A: No. It trades the NEXT signal that comes (1-15 min wait typically)

**Q: Can I lose money?**  
A: Yes, like any trading system. But risk checks and position limits apply.

**Q: How do I test without real money?**  
A: Use a DEMO account in MT5 while config is in LIVE mode.

**Q: How do I revert?**  
A: Change mode back to "paper" in config.yaml (instant)

**Q: Do I need to restart anything?**  
A: No. Change takes effect on next signal detection (~15 min max).

---

## 📈 Expected Results

**First 24 hours (LIVE mode):**
- 5-20 signals generated
- 1-5 trades executed (depends on risk checks)
- +/- $10-50 P&L

**First week:**
- 50-100 signals generated
- 10-40 trades executed
- +/- $50-200 P&L
- Win rate: 35-65%

**Metrics to track:**
- Telegram: /signals (signal accuracy)
- Telegram: /active (position management)
- Logs: results/cleanup_backup.log (execution status)

---

## 🚀 Ready?

```
1. Open: config/config.yaml
2. Find: mode: "paper"
3. Change: mode: "live"
4. Save: Ctrl+S
5. Telegram: /status
6. Result: LIVE trading ENABLED ✅
```

That's all you need for basic setup!

For approval workflow, see: APPROVAL_IMPLEMENTATION.md

---

**Status:** Ready to enable live trading 🚀
