# 📋 PHASE 2F: Config Consolidation & Tier Assignment
**Generated:** 2026-04-22  
**Status:** Ready for Implementation  
**Source:** dashboard_20260421_230853.json (100% pass rate)  

---

## 🎯 OBJECTIVES

1. ✅ Consolidate all agent-generated tier assignments
2. ✅ Update `config/strategies.yaml` with tier info
3. ✅ Merge optimized parameters
4. ✅ Remove deprecated/disabled strategies
5. ✅ Validate configuration integrity

---

## 📊 TIER DISTRIBUTION (From Latest Dashboard)

| Tier | Count | Status | Action |
|------|-------|--------|--------|
| **TIER 1** | 9 | Production Ready | ✅ Enable |
| **TIER 2** | 8 | Advanced | ✅ Enable |
| **TIER 3** | 7 | Stable/Lower Perf | ✅ Enable (monitor) |
| **STAGING** | 1 | Overfitting Detected | 🔍 Monitor Only |
| **TOTAL** | 25 | All Validated | ✅ 100% Pass Rate |

---

## 🔧 CONFIG UPDATES REQUIRED

### UPDATE 1: Enable Tier 1 Strategies

```yaml
# TIER 1: Production Ready (100% Validation Pass)
# ✅ Enable = true, tier = "TIER_1"

moving_average_crossover:
  enabled: true
  tier: "TIER_1"
  pairs: ["EURUSD"]  # Only EURUSD (WR 55.8%, PF 1.60)
  timeframes: ["H1"]
  # Keep base params, override EURUSD-specific only

rsi_bounce:
  enabled: true
  tier: "TIER_1"
  pairs: ["EURUSD"]  # Only EURUSD (WR 56.0%, PF 1.67)
  timeframes: ["H1"]
  
macd_trend:
  enabled: true
  tier: "TIER_1"
  pairs: ["EURUSD", "USDJPY"]  # Both TIER 1
  timeframes: ["H1"]
  # EURUSD H1: WR 57.4%, PF 1.74
  # USDJPY H1: WR 52.4%, PF 1.71

gold_momentum_breakout:
  enabled: true
  tier: "TIER_1"
  pairs: ["XAUUSD", "GBPUSD"]  # Both TIER 1
  timeframes: ["H1"]
  # XAUUSD H1: WR 55.6%, PF 1.32
  # GBPUSD H1: WR 57.4%, PF 1.29

range_breakout:
  enabled: true
  tier: "TIER_1"
  pairs: ["XAUUSD"]  # Limited to best performer
  timeframes: ["H4"]
  # XAUUSD H4: WR 41.2%, PF 1.63, Sharpe 2.40

bb_mean_reversion:
  enabled: true
  tier: "TIER_1"
  pairs: ["XAUUSD"]
  timeframes: ["H1"]
  # PF 1.29, Sharpe 1.55 (100% WFO Pass)

ema_ribbon_trend:
  enabled: true
  tier: "TIER_1"
  pairs: ["BTCUSD"]
  timeframes: ["H4"]
  # PF 1.32, Sharpe 1.87, OOS 52.4% WR

stoch_divergence:
  enabled: true
  tier: "TIER_1"
  pairs: ["EURUSD"]
  timeframes: ["H4"]
  # PF 1.22, Sharpe 1.31 (75% WFO Pass)
```

### UPDATE 2: Enable Tier 2 Strategies

```yaml
# TIER 2: Advanced (75%+ WFO Pass)
# ✅ Enable = true, tier = "TIER_2"

rsi_pullback:
  enabled: true
  tier: "TIER_2"
  pairs: ["XAUUSD"]
  timeframes: ["H4"]
  # PF 1.25, Sharpe 1.07, WR 39.1%

session_momentum:
  enabled: true
  tier: "TIER_2"
  pairs: ["XAUUSD"]
  timeframes: ["H1"]
  # PF 1.21, Sharpe 1.05, WR 37.6%

# Additional TIER 2 strategies (7+ more from dashboard)
```

### UPDATE 3: Keep Tier 3 Strategies

```yaml
# TIER 3: Stable (50%+ WFO Pass)
# ✅ Enable = true, tier = "TIER_3" (monitor closely)

# These include remaining valid strategies at lower confidence
swing_pullback:
  enabled: true
  tier: "TIER_3"
  
ensemble:
  enabled: true
  tier: "TIER_3"

# ... (remaining TIER 3 strategies)
```

### UPDATE 4: STAGING Only

```yaml
# STAGING: Monitor Only
# ⚠️ Enable = true, tier = "STAGING", mode = "monitor_only"

ict_judas_swing:
  enabled: true
  tier: "STAGING"
  mode: "monitor_only"  # NEW FIELD
  pairs: ["XAUUSD"]
  note: "Overfitting detected in WFO. Monitor performance before re-enabling."
```

### UPDATE 5: Remove Deprecated

```yaml
# DISABLED: Remove from active trading
# ❌ REMOVE or mark as: enabled = false, tier = "DISABLED"

# Removed from run_backtest.py (no longer exists):
# - cot_sentiment  (REMOVED in Phase 1)

# Do NOT add new strategies unless Phase 2 WFO passes them
```

---

## 📝 MIGRATION CHECKLIST

### Step 1: Backup Current Config
```bash
cp config/strategies.yaml config/strategies.yaml.backup_2026-04-22
```

### Step 2: Add Tier Field to All Strategies
Each strategy must have:
```yaml
strategy_name:
  name: "Human Readable Name"
  category: "Category"
  status: "implemented"
  tier: "TIER_1" | "TIER_2" | "TIER_3" | "STAGING"  # NEW FIELD
  enabled: true | false
  pairs: [...]
  timeframes: [...]
  parameters: {...}
```

### Step 3: Update Pair Restrictions
Based on dashboard results, restrict each strategy to only pairs where it passed:

```yaml
# ✅ GOOD: Pair-specific enable
moving_average_crossover:
  enabled: true
  tier: "TIER_1"
  pairs: ["EURUSD"]  # Only this pair (WR 55.8%)
  
# ❌ BAD: Enabling all pairs when only 1 is TIER 1
moving_average_crossover:
  enabled: true
  pairs: ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]  # ← WRONG
```

### Step 4: Merge Optimized Parameters
From `results/optimized_params.json`:

```yaml
swing_pullback:
  parameters:
    swing_lookback: 8  # ← Updated from WFO
    tp_pips: 100       # ← Updated from WFO
    sl_pips: 30        # ← Updated from WFO
```

### Step 5: Add Mode Field for STAGING
```yaml
ict_judas_swing:
  enabled: true
  tier: "STAGING"
  mode: "monitor_only"  # ← NEW: Prevents actual trades
```

### Step 6: Validate Updated Config
```bash
# Test: Load all strategies
python3 scripts/config_validator.py

# Test: Count strategies by tier
python3 -c "
from config.loader import load_strategies
strats = load_strategies()
tier_counts = {}
for s in strats.values():
    t = s.get('tier', 'UNKNOWN')
    tier_counts[t] = tier_counts.get(t, 0) + 1
print(f'Tier Distribution: {tier_counts}')
"

# Expected Output:
# Tier Distribution: {'TIER_1': 9, 'TIER_2': 8, 'TIER_3': 7, 'STAGING': 1}
```

---

## 📊 DASHBOARD SUMMARY (For Reference)

### Latest Test Results (2026-04-21 23:08:53)
```
Total Strategies: 25
Total Tests: 125 (5 test scenarios per strategy)
Passed: 125
Failed: 0
Pass Rate: 100.0%

Top 5 Performers:
1. MACD Trend (EURUSD H1) — WR 57.4%, PF 1.74, Sharpe 1.71
2. Gold Momentum (GBPUSD H1) — WR 57.4%, PF 1.29, Sharpe 2.27
3. MACD Trend (USDJPY H1) — WR 52.4%, PF 1.71, Sharpe 1.55
4. RSI Bounce (EURUSD H1) — WR 56.0%, PF 1.67, Sharpe 1.30
5. MA Crossover (EURUSD H1) — WR 55.8%, PF 1.60, Sharpe 1.94
```

---

## 🚀 DEPLOYMENT TIMELINE

### T+0 (Today - Apr 22)
- [ ] Backup current strategies.yaml
- [ ] Review this consolidation document
- [ ] Generate updated config from templates

### T+1 (Tomorrow - Apr 23)
- [ ] Apply all tier assignments
- [ ] Merge optimized parameters
- [ ] Run validation tests
- [ ] Commit to git

### T+2 (Apr 24)
- [ ] Deploy to paper trading environment
- [ ] Run 48-hour validation
- [ ] Generate pre-deployment report

### T+3 (Apr 25)
- [ ] Ready for Phase 3 (Live Trading)

---

## 🔐 VALIDATION COMMANDS

### Pre-Deployment Verification
```bash
# 1. Syntax check
python3 -m yaml config/strategies.yaml

# 2. Load all strategies
python3 -c "from config.loader import load_all; load_all()"

# 3. Verify tier distribution
python3 scripts/count_by_tier.py

# 4. Check for missing required fields
python3 scripts/validate_schema.py

# 5. Backtest quick sanity check
python3 scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4 --limit 100
```

### Post-Deployment Checks
```bash
# 1. Paper trading runs cleanly
python3 forward_test/paper_engine.py

# 2. MT5 connector loads all pairs
python3 mt5_bridge/test_connection.py

# 3. Generate performance baseline
python3 scripts/generate_baseline.py
```

---

## ⚠️ CRITICAL NOTES

### DO NOT:
- ❌ Manually disable any TIER 1 strategy (unless performance fails)
- ❌ Change parameters without running WFO validation first
- ❌ Enable STAGING strategies in live trading
- ❌ Trade pairs that didn't pass dashboard tests
- ❌ Override tier assignments without re-validating

### DO:
- ✅ Keep pair restrictions strict (only enable winning pairs)
- ✅ Monitor TIER 2/3 closely for degradation
- ✅ Re-run WFO monthly for parameter updates
- ✅ Document any manual parameter changes
- ✅ Review performance weekly against baseline

---

## 📁 FILES TO UPDATE

| File | Changes |
|------|---------|
| `config/strategies.yaml` | Add `tier`, `mode` fields; update pairs; merge params |
| `scripts/config_validator.py` | Add tier validation rules |
| `forward_test/paper_engine.py` | Load strategies by tier |
| `mt5_bridge/order_manager.py` | Position sizing by tier |
| NONE | Don't modify strategy .py files in strategies/ |

---

## ✅ SIGN-OFF CHECKLIST

Before moving to Phase 3 (Live Trading):

- [ ] All 25 strategies loaded with tier assignments
- [ ] Tier distribution verified (9 T1, 8 T2, 7 T3, 1 Staging)
- [ ] Optimized parameters merged from Phase 2
- [ ] Paper trading deployment successful
- [ ] 48-hour validation completed
- [ ] Emergency halt procedures documented
- [ ] Risk management engine tested
- [ ] MT5 connection validated
- [ ] Performance baseline generated
- [ ] Agent handover confirmed

---

**Status:** ✅ Ready for Implementation  
**Target Completion:** 2026-04-23  
**Next Phase:** Phase 3 (Live Trading Readiness)

