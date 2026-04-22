# ⚡ AGENT CODE FIX - QUICK REFERENCE

**File to Modify:** `scripts/daily_validation_suite.py`  
**Lines to Replace:** 113-150  
**Time to Fix:** 5 minutes

---

## 🔍 WHAT TO DO

Find this method in the file (starts at line 113):

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
        "gold_momentum_breakout",
        "range_breakout",
        "bb_mean_reversion",
        "session_momentum",
        "crypto_rsi_extremes",
        "stoch_divergence",
        "volatility_squeeze_breakout",
        # New 15 LeoDeX V2 strategies
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
```

---

## ✏️ REPLACE WITH THIS:

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
```

---

## 📋 STEP-BY-STEP FOR AGENTS

### Step 1: Open the File
```powershell
cd F:\REPOS\leo123xxx\TradePanel
notepad scripts\daily_validation_suite.py
```

### Step 2: Find the Method
Use `Ctrl+F` to find: `def validate_all_strategies`

Should be around line 113.

### Step 3: Delete Old Code
Select and delete lines 113-150 (everything including the hardcoded list)

### Step 4: Paste New Code
Paste the replacement code from the section above

### Step 5: Save File
Press `Ctrl+S` and close

---

## ✅ QUICK TEST AFTER FIX

```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -c "
import yaml
with open('config/strategies.yaml', 'r') as f:
    data = yaml.safe_load(f)
    active = data.get('active', [])
    print(f'✅ Found {len(active)} active strategies')
    for s in active:
        print(f'  - {s}')
"
```

Expected output:
```
✅ Found 10 active strategies
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

---

## 🚀 THEN RUN THE FULL TEST

```powershell
# 1. Health check
python main.py --mode health

# 2. Validation (should show 10 strategies now, not 25)
python main.py --mode validate

# 3. Check logs
tail -20 logs/main.log
```

Expected to see:
```
Loaded 10 active strategies from config
Testing 10 strategies x 5 pairs x 1 timeframes
```

---

## ⚠️ COMMON MISTAKES

❌ **Don't:** Only replace the list inside the brackets  
✅ **Do:** Replace the ENTIRE method including the hardcoded list

❌ **Don't:** Forget to save the file  
✅ **Do:** Press Ctrl+S after pasting

❌ **Don't:** Edit the wrong file  
✅ **Do:** Make sure you're editing `scripts/daily_validation_suite.py`

❌ **Don't:** Forget to check for another similar list elsewhere in the file  
✅ **Do:** Search the whole file for `strategies_to_test = [` to find ALL occurrences

---

## 📍 VERIFICATION CHECKLIST

- [ ] File opened: scripts/daily_validation_suite.py
- [ ] Found method: validate_all_strategies (line ~113)
- [ ] Old code deleted
- [ ] New code pasted
- [ ] File saved (Ctrl+S)
- [ ] Python test ran successfully
- [ ] Shows: "✅ Found 10 active strategies"
- [ ] Lists all 10 strategies correctly
- [ ] Health check passes
- [ ] Validation shows 10 strategies (not 25)

---

**Time:** 5-10 minutes  
**Difficulty:** EASY  
**Impact:** HIGH (enables demo live trading with top 10)  

🎯 **Ready for agents!**
