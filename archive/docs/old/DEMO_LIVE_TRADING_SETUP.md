# 🚀 DEMO LIVE TRADING SETUP - TOP 10 STRATEGIES

**Objective:** Switch from paper trading to demo live account with top 10 performing strategies  
**Date:** 2026-04-22  
**Status:** Ready to Execute  
**Target:** See real trades and results on demo account

---

## 📋 EXECUTION PLAN

### Phase A: Identify Top 10 Strategies (30 minutes)
1. Run full validation to test all 24 strategies
2. Identify top 10 by win rate
3. Document results

### Phase B: Update Configuration (15 minutes)
1. Update config/strategies.yaml with top 10 only
2. Update .env with demo account credentials
3. Verify changes

### Phase C: Redeploy & Test (15 minutes)
1. Run health check
2. Run single backtest on best strategy
3. Run full cycle on demo account

### Phase D: Monitor Results (Ongoing)
1. Watch Telegram alerts
2. Check dashboard hourly
3. Document trades

---

## 🎯 STEP-BY-STEP EXECUTION

### STEP 1: RUN VALIDATION TO IDENTIFY TOP 10

Run this command in PowerShell:

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Run validation to test all 24 strategies
python main.py --mode validate
```

**Duration:** 2-3 minutes  
**Output:** Will show performance metrics for each strategy

**Watch for:**
```
Strategy: triple_macd_scalping     | Win Rate: 65%  | Profit Factor: 2.1
Strategy: stat_arb_gold_silver     | Win Rate: 58%  | Profit Factor: 1.8
Strategy: range_breakout           | Win Rate: 52%  | Profit Factor: 1.4
[and so on...]
```

---

### STEP 2: CHECK VALIDATION RESULTS FILE

After validation completes, check the results:

```powershell
# View latest validation results
dir results\daily_validation\ /OD

# View the JSON results
type results\daily_validation\latest_validation.json
```

**Look for:**
- Win Rate (%)
- Profit Factor
- Trade Count
- Average P&L

**Note the TOP 10 strategies** by win rate.

---

### STEP 3: PREPARE TOP 10 LIST

Create a file with top 10 strategies in order by win rate:

```
1. [Strategy Name] - [Win Rate]%
2. [Strategy Name] - [Win Rate]%
3. [Strategy Name] - [Win Rate]%
... (top 10)
```

**Example (you'll get actual results):**
```
1. triple_macd_scalping        - 68%
2. stat_arb_gold_silver        - 62%
3. ma_crossover_scalp          - 58%
4. rsi_divergence_trade        - 56%
5. range_breakout              - 54%
6. mean_reversion_xau          - 52%
7. trend_following_h4          - 51%
8. momentum_entry              - 50%
9. support_resistance_bounce   - 48%
10. volatility_breakout        - 47%
```

---

### STEP 4: UPDATE CONFIG FILE

Open: `config\strategies.yaml`

```powershell
# Edit with notepad
notepad config\strategies.yaml
```

**Find this section:**
```yaml
strategies:
  active:
    - strategy_name_1
    - strategy_name_2
    # ... more strategies
```

**Replace with TOP 10 ONLY:**
```yaml
strategies:
  active:
    - triple_macd_scalping
    - stat_arb_gold_silver
    - ma_crossover_scalp
    - rsi_divergence_trade
    - range_breakout
    - mean_reversion_xau
    - trend_following_h4
    - momentum_entry
    - support_resistance_bounce
    - volatility_breakout
```

**Save the file** (Ctrl+S)

---

### STEP 5: UPDATE .ENV FOR DEMO ACCOUNT

Open: `.env` file

```powershell
notepad .env
```

**Find these lines:**
```
MT5_LOGIN=81633025
MT5_PASSWORD=your_password
MT5_SERVER=DukascopySA-Demo
TRADING_MODE=paper
```

**Update to DEMO LIVE:**
```
MT5_LOGIN=YOUR_DEMO_LOGIN      (Demo account number)
MT5_PASSWORD=your_password     (Same password)
MT5_SERVER=DukascopySA-Demo    (Demo server - keep this)
TRADING_MODE=live              (Change from "paper" to "live")
```

**Save the file** (Ctrl+S)

---

### STEP 6: VERIFY CONFIGURATION

Test that everything loads correctly:

```powershell
python main.py --mode health
```

**Expected output:**
```
Environment Verification
✅ MT5 Login: [DEMO_LOGIN]...
✅ MT5 Server: DukascopySA-Demo
✅ Database connection: OK
✅ Configuration: VALID
```

---

### STEP 7: TEST SINGLE BACKTEST

Before running full live trading, test one strategy:

```powershell
# Test best strategy on demo
python main.py --mode backtest --strategy triple_macd_scalping --pair XAUUSD
```

**Should show:**
- Strategy logic
- Historical performance
- No errors

---

### STEP 8: RUN FULL CYCLE ON DEMO

Now run the actual trading cycle with top 10:

```powershell
python main.py --mode paper-trade
```

**This will:**
1. Validate all 10 strategies
2. Execute actual trades on DEMO account
3. Send results to Telegram
4. Update dashboard with real trades

---

### STEP 9: MONITOR RESULTS

#### Check Telegram for Trade Alerts
```
Send: /status
Expected response: Real demo trades being executed

Send: /balance
Expected response: Demo account balance with P&L

Send: /active
Expected response: Open demo positions
```

#### Check Dashboard
```
Open: http://localhost:5000
Expected: Live trades from demo account showing
```

#### Check Logs
```powershell
.\tail_logs.bat
```

Expected: Trade execution logs for top 10 strategies

---

## 📊 UNDERSTANDING THE RESULTS

### What You'll See

**Successful trade execution:**
```
[15:30:00] INFO - Strategy: triple_macd_scalping
[15:30:01] INFO - Signal: BUY XAUUSD H1
[15:30:02] INFO - Position Opened: 0.1 lot
[15:30:03] INFO - Entry Price: 2450.50
[15:30:04] INFO - Stop Loss: 2445.00
[15:30:05] INFO - Take Profit: 2460.00

[Later...]
[16:45:00] INFO - Position Closed: PROFIT
[16:45:01] INFO - Exit Price: 2460.00
[16:45:02] INFO - P&L: +$50.00
```

### Metrics to Watch
```
Win Rate:        Should be similar to validation
Profit Factor:   Actual earnings / losses
P&L:             Daily profit or loss
Drawdown:        Peak loss from high
Trade Count:     Number of trades executed
```

---

## 🎯 EXPECTED OUTCOMES

### If Everything Works ✅
- Top 10 strategies execute on demo account
- Real trades appear in Telegram
- Dashboard shows live results
- P&L updates in real-time
- No errors in logs

### If Issues Occur ⚠️
- Check logs: `.\tail_logs.bat`
- Verify .env has correct demo credentials
- Run: `python main.py --mode health`
- Check MT5 connection
- Verify demo account has funds

---

## 📱 TELEGRAM MONITORING

### Commands to Use Daily

```
/status      → See all trades and P&L
/balance     → Check account equity
/active      → View open positions
/signals     → See latest signals
/risk        → Check drawdown
```

**Expected frequency:**
- New trade alerts: Every few minutes (depending on strategy timeframes)
- P&L updates: Hourly or after trade closes
- Error alerts: If issues occur

---

## 🔄 DAILY ROUTINE FOR DEMO TRADING

### Morning (5 minutes)
```
1. Check Telegram: /status
2. View dashboard: http://localhost:5000
3. Note any overnight trades
4. Check for any errors
```

### Throughout Day (2 minutes every 2-3 hours)
```
1. Send Telegram: /balance
2. Note current P&L
3. Monitor open positions: /active
4. Check dashboard for updates
```

### Evening (5 minutes)
```
1. View daily summary: /status
2. Check total P&L
3. Review closed trades
4. Check logs: .\tail_logs.bat
```

### Weekly (1 hour every Sunday)
```
1. Calculate weekly P&L
2. Win rate by strategy
3. Best/worst performers
4. Compare to Phase 3 paper trading results
5. Document in file
```

---

## ⚠️ CRITICAL BEFORE YOU START

### Verify Demo Account
```
1. Login to MT5 with demo credentials
2. Check account has funds ($1000+ recommended)
3. Verify demo server connection
4. Check account leverage (20:1 default)
5. Test manual trade execution
```

### Backup Current Config
```powershell
# Backup paper trading config
copy config\strategies.yaml config\strategies.yaml.backup
copy .env .env.backup
```

### Know How to Stop
```
If issues arise:
1. Run: stop_services.bat
2. Or: python main.py --mode health
3. Check logs: .\tail_logs.bat
4. Close all positions manually in MT5 if needed
```

---

## 🚨 RISK MANAGEMENT FOR DEMO

### Position Sizing
```
Conservative (Recommended):
- Start with 0.01 lot per trade
- Increase to 0.05 lot if stable
- Maximum 0.1 lot per trade
- Never exceed account risk limit
```

### Daily Limits
```
Stop trading if:
- Daily loss exceeds -$100
- Drawdown exceeds -15%
- More than 3 consecutive losses
- System error occurs
```

### Account Rules
```
Minimum balance: $500
If drops below: Pause trading, investigate
Maximum risk per trade: 1% of account
Maximum daily risk: 2% of account
```

---

## 📋 PRE-EXECUTION CHECKLIST

Before running demo live trading:

**Configuration**
- [ ] Top 10 strategies identified
- [ ] config/strategies.yaml updated
- [ ] .env file updated with demo credentials
- [ ] Demo account has funds
- [ ] MT5 demo connection verified

**Safety**
- [ ] Backups created (.backup files)
- [ ] Test mode verified working
- [ ] Health check passing
- [ ] Single backtest successful
- [ ] Stop procedures documented

**Monitoring**
- [ ] Telegram bot tested
- [ ] Dashboard accessible
- [ ] Logs directory exists
- [ ] Contact info saved
- [ ] Alert rules set

**Knowledge**
- [ ] Understand trade execution flow
- [ ] Know how to monitor
- [ ] Know how to stop
- [ ] Know what results mean
- [ ] Have daily routine planned

---

## 🎯 SUCCESS CRITERIA FOR DEMO PHASE

### First Hour
- [ ] Strategies loaded successfully
- [ ] System running without errors
- [ ] Dashboard showing activity
- [ ] Telegram alerts working

### First Day
- [ ] Multiple trades executed
- [ ] Win rate tracking correctly
- [ ] P&L updating
- [ ] Logs recording trades
- [ ] No critical errors

### First Week
- [ ] Win rate ≥ 50% (consistent with validation)
- [ ] Profit factor ≥ 1.0
- [ ] Drawdown < 10%
- [ ] All 10 strategies running
- [ ] Daily P&L positive most days

---

## 📊 REPORTING TEMPLATE

Create this file daily: `DEMO_TRADING_LOG_YYYY-MM-DD.txt`

```
DEMO TRADING REPORT - 2026-04-22

System Status:
  - Strategies Active: 10
  - Account: DEMO (Dukas...03025)
  - Balance: $XXX
  - Equity: $XXX

Trading Results:
  - Trades Executed: X
  - Wins: X
  - Losses: X
  - Win Rate: X%
  - Daily P&L: $X
  - Drawdown: X%

Top Performers Today:
  1. [Strategy] - [# trades] [win rate]
  2. [Strategy] - [# trades] [win rate]

Issues/Alerts:
  - [Any issues noted]

Notes:
  - [Observations]
  - [Patterns]
  - [Action items]
```

---

## 🚀 EXECUTION SEQUENCE

```
NOW:
  1. Run validation: python main.py --mode validate
  2. Wait 2-3 minutes for results
  3. Note top 10 strategies
  
NEXT (5 minutes):
  4. Update config/strategies.yaml
  5. Update .env file
  6. Save both files
  
THEN (5 minutes):
  7. Run: python main.py --mode health
  8. Verify no errors
  
FINALLY (10 minutes):
  9. Run: python main.py --mode paper-trade
  10. Monitor Telegram and dashboard
  11. Watch for first trades
```

**Total time:** 30 minutes to see first live demo trades

---

## 📞 TROUBLESHOOTING

### "Demo account not connecting"
```
1. Verify MT5 is open
2. Check .env credentials
3. Run: python main.py --mode health
4. Check logs: .\tail_logs.bat
5. Reconnect to MT5
```

### "No trades executed"
```
1. Check /status in Telegram
2. Verify strategies loaded: /mode
3. Check market hours (forex trades during market open)
4. Run: python main.py --mode validate
5. Check logs for strategy issues
```

### "Wrong account trading"
```
1. Stop immediately: python main.py --mode health
2. Check .env file
3. Verify MT5 login
4. Restart system
```

---

## ✅ FINAL CHECKLIST

Before you click Execute:

- [ ] Top 10 strategies identified from validation
- [ ] config/strategies.yaml updated
- [ ] .env updated for demo account
- [ ] Backups created
- [ ] Demo account ready and funded
- [ ] Health check passing
- [ ] Understand monitoring procedure
- [ ] Know how to stop if needed
- [ ] Daily routine planned
- [ ] Reporting template prepared

---

## 🎉 YOU'RE READY!

Once you complete these steps:
1. You'll see REAL trades on demo account
2. Real P&L results (not simulated)
3. Real execution speeds
4. Real slippage (if any)
5. Real market conditions

**This bridges Phase 3 (paper) → Phase 4 (live)**

---

**Document:** DEMO_LIVE_TRADING_SETUP.md  
**Status:** Ready for Execution  
**Next Step:** Run validation and identify top 10  

🚀 **Ready to see real trading results?** 🚀

