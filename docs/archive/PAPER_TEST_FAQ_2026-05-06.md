# 🎯 Paper Test FAQ — Your 3 Critical Questions Answered

**Date:** May 6, 2026  
**Status:** System is running, but dashboard data needs verification  
**Last Backtest:** May 5, 2026 (35 PASS out of 148 combos)

---

## **Question 1: How do I see the latest details of the paper test?**

### ✅ Real-Time Monitoring (4 methods)

#### **Method A: Telegram Alerts (LIVE)**
- You should be receiving **TRADE_OPEN**, **TRADE_CLOSE**, and **SIGNAL_ALERT** messages
- First trade typically appears within **2–4 hours** of paper mode starting
- Expected **5–15 signals per day** during London/US trading hours
- **Check:** Are you receiving Telegram notifications? If silent for >30 min during trading hours → problem

#### **Method B: Docker Logs (REAL-TIME)**
```powershell
# Watch scheduler (where signal detection runs every 1 minute)
docker logs tradepanel-scheduler -f

# Watch backend (where trade execution happens every 5 minutes)
docker logs tradepanel-backend -f
```

What to look for:
```
✓ [PaperEngine] Loaded 23 strategies
✓ Successfully loaded XX strategies
✓ Signal detected: [strategy] [pair] [timeframe]
✓ Order executed: [strategy] [pair] [direction] [size]
✓ No errors or exceptions
```

#### **Method C: Dashboard at http://localhost:3000 (BUT SEE ISSUE BELOW)**
- Real-time equity curve should update
- Open positions should show
- Trade history should log

**⚠️ CRITICAL ISSUE:** Your dashboard shows **3 PASS / 84 total**, but backtest showed **35 PASS / 148 total**
- This suggests dashboard is showing OLD or FILTERED data
- See "Question 3" section for investigation steps

#### **Method D: Direct Database Query**
```sql
-- Check how many backtests passed
SELECT status, COUNT(*) FROM backtests GROUP BY status;
-- Should show: PASS=35, REVIEW=90, ERROR=23 if using latest data

-- Check live paper trades
SELECT COUNT(*) as paper_trades_generated FROM paper_trades 
WHERE trade_date >= CURRENT_DATE;

-- Check current equity progression
SELECT timestamp, equity FROM account_equity 
ORDER BY timestamp DESC LIMIT 10;
```

---

## **Question 2: Do I need to do WFO (Walk Forward Optimization)?**

### ✅ SHORT ANSWER: **NOT for starting paper mode, but understand the distinction**

#### **What Happened in Backtest (May 5, 2026)**
```
Backtesting = Testing with FIXED parameters (from config/strategies.yaml dated 2026-04-29)
Result: 35 PASS combos confirmed

These parameters are:
  ✓ RSI_PULLBACK: rsi_period=14, rsi_pullback_lower=38, etc.
  ✓ DUAL_EMA_FRACTAL: ema_fast=50, ema_slow=200, adx_min=25, etc.
  ✓ ... and so on for all 23 strategies
```

#### **What Happens in Paper Mode (NOW)**
```
Paper Testing = Testing with SAME FIXED parameters (from config/strategies.yaml)
No re-optimization = No parameter changes mid-test

Paper mode uses EXACTLY the same parameters that backtested successfully
```

#### **When You'd Need WFO**
```
Walk Forward Optimization = Rolling-window re-optimization of parameters
Example:
  - Test period 1 (Jan-Feb): Optimize params, trade live (Mar-Apr)
  - Test period 2 (Feb-Mar): Optimize params, trade live (May-Jun)
  - ... rolling window continues

When to use WFO:
  ✓ AFTER initial 48-hour paper test passes
  ✓ IF you want to improve performance by re-tuning mid-test
  ✓ IF you notice strategies underperforming vs backtest (forward test WR < 90% of backtest)

You DON'T need it now because:
  ✓ Parameters already validated (35 PASS combos)
  ✓ You're in 48-hour PROOF-OF-CONCEPT phase
  ✓ After proof succeeds, then optimize if needed
```

#### **Decision Tree**
```
START HERE: Should I run WFO now?
│
├─ IF: Paper test hasn't started yet → NO, start paper test first
├─ IF: Paper test running fine (WR ≥ 90% of backtest) → NO, keep using current params
├─ IF: Paper test underperforming (WR < 80% of backtest) → YES, run WFO after 48h test
└─ IF: You want to squeeze every 1% performance improvement → YES, but only AFTER initial pass
```

### 🎯 **Your Action**
**Do NOT run WFO now.** Start paper mode monitoring. After 48 hours, if forward test WR ≥ 63% (90% of backtest's 70.8%), **no optimization needed**. If WR drops below 60%, investigate why and consider WFO.

---

## **Question 3: Why aren't all trading pairs in dashboard/Telegram? Are parameters applied?**

### ⚠️ **CRITICAL ISSUE: Dashboard Discrepancy**

Your screenshot shows:
```
Dashboard Data: 3 PASSED / 18 REVIEW / 63 FAILED / 84 TOTAL
Backtest Data:  35 PASS / 90 REVIEW / 23 ERROR / 148 TOTAL
```

**This is a 75% difference.** Something is wrong with what the dashboard is displaying.

### **Diagnosis Checklist**

#### **1️⃣ Is the dashboard querying stale data?**
```powershell
# Check when backtest data was last inserted into database
docker exec tradepanel-db psql -U postgres -d tradepanel \
  -c "SELECT MAX(created_at) FROM backtests;"

# Should be recent (2026-05-05 or later)
# If it's older, backtest results weren't saved to DB
```

#### **2️⃣ Are all 23 strategies enabled in config?**
```powershell
# Count enabled strategies
$yaml = Get-Content "config\strategies.yaml" -Raw
[regex]::Matches($yaml, "enabled:\s*true") | Measure-Object | Select-Object -ExpandProperty Count
# Should return ~23
```

Expected enabled (from config):
```
ENABLED (should be 23):
✓ ma_crossover
✓ gold_momentum_breakout
✓ stat_arb_gold_silver
✓ hikkake_trap
✓ range_breakout
✓ dual_ema_fractal
✓ rsi_pullback
✓ ema_ribbon_trend
✓ cot_sentiment
✓ session_momentum
✓ turtle_soup
✓ dual_ema_momentum
✓ orb
✓ rvgi_cci_confluence
✓ rsi_extremes_scalp
✓ bb_squeeze_scalp
✓ macd_trend
✓ rsi_bounce
✓ vwap_momentum
... and more
```

#### **3️⃣ Are all 16 trading pairs configured?**
```powershell
# Check config.yaml for trading pairs
$yaml = Get-Content "config\config.yaml" -Raw
if ($yaml -match "trading_pairs:\s*\n((?:  - .+\n)*?)") {
    $pairs = [regex]::Matches($matches[1], "  - (.+?)(?:\n|$)") | ForEach-Object { $_.Groups[1].Value }
    $pairs | ForEach-Object { Write-Host $_ }
    Write-Host "Total: $($pairs.Count)"
}
```

Expected **16 pairs**:
```
EURUSD  GBPUSD  USDJPY  XAUUSD  XAGUSD
GBPJPY  AUDUSD  USDCAD  USDZAR  USOIL
BTCUSD  ETHUSD  US500   USTEC   NVDA  AMD
```

#### **4️⃣ Are parameters actually being loaded by paper_engine?**

The paper_engine loads parameters from `config/strategies.yaml` like this:
```python
# From paper_engine.py line 162
custom_params = strat_data.get('parameters', None)
self.active_strategies[strat_name] = strategy_class(custom_params)
```

This means each strategy gets its parameters from the YAML file.

**How to verify parameters are applied:**
```powershell
# Check the paper_engine logs for parameter loading confirmation
docker logs tradepanel-backend -f 2>&1 | Select-String -Pattern "parameters|param|loaded" -Context 1

# Or check if paper trade orders have parameters in the database
docker exec tradepanel-db psql -U postgres -d tradepanel \
  -c "SELECT strategy, parameters FROM paper_trades LIMIT 5;"
```

### **Why Dashboard Shows Different Numbers**

Most likely cause: **Dashboard is showing a filtered or old view**

Possible scenarios:
1. **Filtering by status** - maybe only showing "completed" backtests, not all runs
2. **Old data** - database still has results from an earlier, failed backtest run
3. **Wrong timeframe** - maybe showing only last 7 days of results
4. **Incomplete import** - backtest results never saved to DB

### **How to Fix**

#### **Step A: Clear old backtest data (OPTIONAL)**
```powershell
# Backup database first
docker exec tradepanel-db pg_dump -U postgres tradepanel > backup_2026-05-06.sql

# Clear old backtest runs (keep last 7 days)
docker exec tradepanel-db psql -U postgres -d tradepanel \
  -c "DELETE FROM backtests WHERE created_at < CURRENT_DATE - INTERVAL '7 days';"
```

#### **Step B: Verify paper_engine is loading all strategies**
```powershell
# Watch the logs as paper_engine starts
docker logs tradepanel-backend --tail 100 | Select-String -Pattern "Loaded|Successfully|strategy"

# Should see something like:
# [PaperEngine] Loaded TIER_1 strategy: dual_ema_fractal (TRADE mode)
# [PaperEngine] Loaded TIER_2 strategy: rsi_bounce (TRADE mode)
# ... repeated for all 23 strategies
# [PaperEngine] Successfully loaded 23 strategies.
```

#### **Step C: Verify all trading pairs are active**
Check logs for pair subscription:
```powershell
docker logs tradepanel-backend | Select-String -Pattern "pairs|symbols|connected"

# Should see all 16 pairs being requested:
# EURUSD, GBPUSD, USDJPY, XAUUSD, XAGUSD, BTCUSD, ETHUSD, etc.
```

#### **Step D: Manually refresh dashboard data**
```powershell
# Stop and restart paper_engine
docker restart tradepanel-backend

# Wait 30 seconds, then check logs
docker logs tradepanel-backend -f

# Dashboard should start showing fresh data from paper trades
```

---

## **Summary: Your Next Actions**

| Question | Answer | Action |
|----------|--------|--------|
| **How to see paper test?** | Telegram + docker logs + http://localhost:3000 | Monitor all 3 sources; compare to backtest metrics |
| **Need WFO?** | NO (use same parameters from backtest) | Start 48-hour test with current params; optimize AFTER if needed |
| **All pairs visible?** | Dashboard data discrepancy detected | Run diagnostics; verify 23 strategies + 16 pairs are enabled |

### **IMMEDIATE TODO**

```powershell
# 1. Verify strategies and pairs are enabled
cd F:\REPOS\leo123xxx\TradePanel
.\PAPER_TEST_DIAGNOSTIC.ps1  # Run the diagnostic script

# 2. Watch live logs
docker logs tradepanel-backend -f
docker logs tradepanel-scheduler -f

# 3. Check Telegram for trade notifications
# Wait for first signal (usually 2-4 hours)

# 4. Visit http://localhost:3000 
# Compare dashboard data with READY_FOR_PAPER_TESTING_2026-05-05.md
# If still showing 3 PASS vs 35 PASS → database issue needs fixing
```

---

## **Final Reminder**

**You DO NOT need to change anything right now.** The paper_engine is using the correct parameters that passed validation. Monitor for 48 hours, track metrics, and let the system prove itself. If forward test WR ≥ 63%, you're ready for live trading without any parameter re-optimization.

