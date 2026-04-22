# 🚀 AGENT TESTING & FIX INSTRUCTIONS
**Status:** Configuration not loading properly  
**Date:** 2026-04-22  
**Objective:** Fix strategy selection to use top 10 from config file  
**Priority:** HIGH - Blocking demo live trading

---

## 📋 PROBLEM SUMMARY

**What's Wrong:**
- ❌ Config file has "active:" section with top 10 strategies
- ❌ But system ignores it and still tests all 25 strategies
- ❌ Telegram bot shows only 2 old strategies instead of 10
- ❌ Dashboard shows PAPER mode instead of LIVE

**Root Cause:**
The file `scripts/daily_validation_suite.py` has a **hardcoded list** of 25 strategies (line 120-148) instead of reading from the config file.

**How to Find It:**
```
File: scripts/daily_validation_suite.py
Lines: 120-148
Code: strategies_to_test = [ ... list of 25 hardcoded strategy names ... ]
```

---

## 🔧 THE FIX (2 files to modify)

### FILE 1: scripts/daily_validation_suite.py

**Location:** Line 113-150 (the `validate_all_strategies()` method)

**Current Code (BROKEN):**
```python
def validate_all_strategies(self):
    """Validate all 25 strategies against quality thresholds."""
    logger.info("Starting strategy validation...")

    pairs = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
    timeframes = ["H1"]

    strategies_to_test = [
        # Original 10 strategies
        "moving_average_crossover",
        "rsi_bounce",
        "macd_trend",
        ... (25 total hardcoded)
    ]
```

**Fixed Code:**
```python
def validate_all_strategies(self):
    """Validate strategies from config file."""
    logger.info("Starting strategy validation...")

    pairs = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
    timeframes = ["H1"]

    # READ FROM CONFIG FILE INSTEAD OF HARDCODED LIST
    config_path = PROJECT_ROOT / "config" / "strategies.yaml"
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Get active strategies from config
        strategies_to_test = config_data.get('active', [])
        
        if not strategies_to_test:
            logger.warning("No active strategies found in config. Using all 25 strategies.")
            strategies_to_test = [
                "moving_average_crossover",
                "rsi_bounce",
                "macd_trend",
                "gold_momentum_breakout",
                "range_breakout",
                "bb_mean_reversion",
                "session_momentum",
                "crypto_rsi_extremes",
                "stoch_divergence",
                "volatility_squeeze_breakout",
                "institutional_silver_bullet",
                "ict_judas_swing",
                "turtle_soup",
                "dual_ema_momentum",
                "triple_macd_scalping",
                "dual_ema_fractal",
                "rsi_2",
                "vwap_momentum",
                "hikkake_trap",
                "orb",
                "rvgi_cci_confluence",
                "volatility_contraction",
                "stat_arb_gold_silver",
                "naked_price_action",
                "cot_sentiment",
            ]
        else:
            logger.info(f"Loaded {len(strategies_to_test)} active strategies from config")
    except Exception as e:
        logger.error(f"Error reading config: {e}. Using all 25 strategies.")
        strategies_to_test = [
            "moving_average_crossover",
            "rsi_bounce",
            # ... (fallback to all 25)
        ]
```

### FILE 2: scripts/daily_validation_suite.py - Second Location

**There may be ANOTHER hardcoded list in the `generate_summary_csv()` method**

Search for: `strategies = [` or `STRATEGY_LIST = [` in the same file

If found, apply the same fix: replace hardcoded list with config file reading.

---

## 📝 TESTING PROCEDURE FOR AGENTS

### TEST 1: Verify Config File Has Active Section

```bash
# Run this command
cd F:\REPOS\leo123xxx\TradePanel
head -20 config/strategies.yaml

# Expected Output:
# # ============================================================================
# # ACTIVE STRATEGIES - TOP 10 BY WIN RATE (Updated 2026-04-22)
# # ============================================================================
# active:
#   - dual_ema_fractal
#   - cot_sentiment
#   - rsi_bounce
#   ... (10 total)
```

**Pass Criteria:** ✅ Active section exists with 10 strategies listed

---

### TEST 2: Check Code Has Been Modified

```bash
# Run this command
cd F:\REPOS\leo123xxx\TradePanel
grep -n "config_data = yaml.safe_load" scripts/daily_validation_suite.py

# Expected Output:
# Should find the line where we read from config
# If it returns nothing, the fix hasn't been applied yet
```

**Pass Criteria:** ✅ Code reads from config file (not hardcoded)

---

### TEST 3: Run Health Check

```powershell
cd F:\REPOS\leo123xxx\TradePanel
python main.py --mode health

# Expected Output:
# [OK] MT5 Login: 81633025
# [OK] Database connection: OK
# [OK] MT5 connection: OK
# HEALTH CHECK SUMMARY: 4/4 passed
```

**Pass Criteria:** ✅ All 4 checks pass

---

### TEST 4: Run Validation with New Code

```powershell
cd F:\REPOS\leo123xxx\TradePanel
python main.py --mode validate

# Expected Output should show:
# Testing 10 strategies x 5 pairs x 1 timeframes
# (NOT "Testing 25 strategies")
```

**Pass Criteria:** ✅ Shows "Testing 10 strategies" not "Testing 25 strategies"

---

### TEST 5: Check Logs Show Active Strategies

```bash
cd F:\REPOS\leo123xxx\TradePanel
tail -50 logs/main.log | grep -E "(Loaded|active|strategies)"

# Expected Output:
# Loaded 10 active strategies from config
# (or similar message showing it read the config)
```

**Pass Criteria:** ✅ Logs show config was read and 10 strategies loaded

---

### TEST 6: Run Paper Trading Cycle

```powershell
cd F:\REPOS\leo123xxx\TradePanel
python main.py --mode paper-trade

# Expected Output:
# Testing 10 strategies x 5 pairs x 1 timeframes
# Should see validation complete with 50 tests (10 strategies x 5 pairs)
```

**Pass Criteria:** ✅ Shows 50 tests (10x5) not 125 tests (25x5)

---

### TEST 7: Check Dashboard Data

```bash
cd F:\REPOS\leo123xxx\TradePanel
# List latest dashboard file
ls -lt results/daily_validation/dashboard_*.json | head -1

# Check content
cat results/daily_validation/dashboard_*.json | grep -i "active\|strategy" | head -10
```

**Pass Criteria:** ✅ Dashboard shows 10 active strategies

---

### TEST 8: Check Telegram Bot Response

Send in Telegram:
```
/status
```

Expected response should show:
```
Operating Mode: LIVE
Active Strategies: 10
  - dual_ema_fractal
  - cot_sentiment
  - rsi_bounce
  - vwap_momentum
  - session_momentum
  - moving_average_crossover
  - rsi_2
  - range_breakout
  - turtle_soup
  - orb
```

**Pass Criteria:** ✅ Shows exactly 10 active strategies from the top 10 list

---

## ✅ COMPLETE TEST CHECKLIST

After making the fix, verify all tests pass:

- [ ] TEST 1: Config file has active section with 10 strategies
- [ ] TEST 2: Code has been modified to read from config
- [ ] TEST 3: Health check passes 4/4
- [ ] TEST 4: Validation shows "Testing 10 strategies" (not 25)
- [ ] TEST 5: Logs show config was read successfully
- [ ] TEST 6: Paper trading shows 50 tests (10x5) not 125 tests (25x5)
- [ ] TEST 7: Dashboard data includes the 10 active strategies
- [ ] TEST 8: Telegram /status shows 10 active strategies with correct names

---

## 🚀 DEPLOYMENT AFTER FIX

Once all tests pass:

```powershell
# 1. Stop all services
taskkill /F /IM python.exe

# 2. Clear old data
Remove-Item -Path "logs\*" -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "results\daily_validation\*" -Force -ErrorAction SilentlyContinue

# 3. Restart with fresh data
python main.py --mode health
python main.py --mode validate
python main.py --mode paper-trade

# 4. Start monitoring
python dashboard.py --port 5000
python scripts/start_telegram_bot.py
```

---

## 📞 DEBUGGING IF TESTS FAIL

### If TEST 2 fails (code not modified):
```
The fix hasn't been applied. Check that:
1. File: scripts/daily_validation_suite.py was edited
2. Line 120-148 area has the new config reading code
3. File was saved correctly
```

### If TEST 4 fails (still shows 25 strategies):
```
The hardcoded list is still being used. Check:
1. Did you modify the right file? (scripts/daily_validation_suite.py)
2. Is there another hardcoded list elsewhere in the file?
3. Search for all occurrences of "strategies_to_test = ["
4. Apply fix to ALL occurrences
```

### If TEST 5 fails (logs don't show config load):
```
Config file isn't being read. Check:
1. Is config/strategies.yaml in the right location?
2. Does it have valid YAML syntax?
3. Does it have "active:" section at the top level?
4. Check logs for error messages
```

### If TEST 8 fails (Telegram still shows 2 strategies):
```
Bot is caching old data. You must:
1. Kill the telegram bot: taskkill /F /IM python.exe
2. Wait 5 seconds
3. Restart it: python scripts/start_telegram_bot.py
4. Try /status command again
```

---

## 📊 SUCCESS METRICS

| Metric | Before Fix | After Fix |
|--------|-----------|----------|
| Strategies Tested | 25 (hardcoded) | 10 (from config) |
| Tests Per Run | 125 (25×5) | 50 (10×5) |
| Execution Time | ~3 seconds | ~1-2 seconds |
| Dashboard Shows | 25 strategies | 10 strategies |
| Telegram /status | 2 strategies | 10 strategies |
| Mode | PAPER | LIVE |

---

## 🎯 FINAL VERIFICATION

After deploying the fix, the system should:

1. ✅ Read config/strategies.yaml
2. ✅ Load only 10 active strategies (not all 25)
3. ✅ Display them in Telegram and dashboard
4. ✅ Test them in validation runs
5. ✅ Execute them in paper trading mode
6. ✅ Show LIVE mode (not PAPER)

---

**Status:** Ready for agent deployment  
**Time to Fix:** 15-20 minutes  
**Risk Level:** LOW (config-only change, no database modifications)  
**Rollback:** Easy (revert the file changes)

🚀 **Hand over to agents for implementation**
