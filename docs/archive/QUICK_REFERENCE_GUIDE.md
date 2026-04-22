# ⚡ QUICK REFERENCE GUIDE
**TradePanel Strategy Integration Project**  
**For:** Quick lookup during Phase 0–3 execution

---

## 📍 WHERE AM I?

**Current Status:** Phase 0 (Emergency Bot Stabilization) — Ready to start

**Next 48 Hours:**
```
Phase 0 (Today): Emergency Fixes (1–2 hours)
├─ Apply 4 critical bot fixes
├─ Test bot stability
└─ Go/No-Go for Phase 1A

Phase 1A (Days 1–2): Backtest Existing (6–8 hours)
├─ Test 10 existing strategies
├─ Assign tier ratings
└─ Document baseline
```

---

## 📚 DOCUMENT NAVIGATION

### Start Here (If New)
→ **PROJECT_RESTRUCTURE_SUMMARY.md** (this project's overview)

### For Planning & Strategy Details
→ **STRATEGY_INTEGRATION_&_TESTING_PLAN.md** (all 25 strategies, 4 phases)

### For Configuration Changes
→ **CONFIG_UPDATE_CHECKLIST.md** (45+ config updates needed)

### For Detailed Task Execution
→ **AGENT_STRATEGY_TESTING_TASK_LIST.md** (32 tasks, step-by-step)

### For Emergency Bot Fixes
→ **DIAGNOSTIC_REPORT.md** (Phase 0: 4 critical fixes)

### For Project Status
→ **MASTER_PROJECT_STATUS.md** (overall timeline + blockers)

---

## 🔴 PHASE 0: EMERGENCY FIXES (1–2 hours)

**Files to Modify:**

| File | Fix | Time | Status |
|------|-----|------|--------|
| `forward_test/paper_engine.py` | Signal deduplication tracking | 30 min | ⏳ Pending |
| `mt5_bridge/order_manager.py` | Order validation before MT5 | 20 min | ⏳ Pending |
| `forward_test/signal_checker.py` | Data freshness check | 15 min | ⏳ Pending |
| `mt5_bridge/connector.py` | Market watch symbol setup | 15 min | ⏳ Pending |

**Testing:**
```bash
python scripts/run_paper.py
# Expected: No "SIGNAL DETECTED" repeats, no "returned None" loops
```

**Go Criteria:**
- ✅ Bot runs 5+ minutes without errors
- ✅ No repeated signals on same bar
- ✅ Clear error messages (not silent failures)
- ✅ All 7 symbols in MT5 market watch

---

## 🟡 PHASE 1A: BACKTEST EXISTING (6–8 hours)

**Strategies to Test (10):**

```bash
# TIER 1 (Verify)
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy ema_ribbon_trend --pair BTCUSD --timeframe H4
python scripts/run_backtest.py --strategy crypto_rsi_extremes --pair BTCUSD --timeframe H4

# TIER 2 (Confirm)
python scripts/run_backtest.py --strategy ma_crossover --pair EURUSD --timeframe H1
python scripts/run_backtest.py --strategy rsi_bounce --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy stoch_divergence --pair EURUSD --timeframe H4
python scripts/run_backtest.py --strategy volatility_squeeze_breakout --pair BTCUSD --timeframe H4
```

**Expected Results:**
```
TIER 1 Strategies:
- Win Rate: 50–60%
- Profit Factor: 1.3–2.2
- Expected: 4–5 confirmed

TIER 2 Strategies:
- Win Rate: 45–50%
- Profit Factor: 1.1–1.3
- Expected: 4–5 to monitor

Baseline Average: WR ~52%, PF ~1.45
```

**Output:**
- tier_assignment_existing_10.csv
- tier_assignment_existing_10.md (rationale)

---

## 🟢 PHASE 1B: IMPLEMENT NEW (12–16 hours)

**15 New Strategies in 5 Groups:**

### Group 1: Institutional Flow (6 hours) — Quick Wins
```
1. Institutional Silver Bullet (SMC)      → 60–68% WR
2. ICT Judas Swing                       → 62–68% WR
3. Turtle Soup Liquidity Sweep           → 60–65% WR

Command:
python scripts/run_backtest.py --strategy institutional_silver_bullet --pair XAUUSD --timeframe M15
python scripts/run_backtest.py --strategy ict_judas_swing --pair GBPUSD --timeframe M15
python scripts/run_backtest.py --strategy turtle_soup_liquidity_sweep --pair XAUUSD --timeframe H1
```

### Group 2: Trend Following (5 hours) — Medium Priority
```
4. Dual EMA Momentum Continuity          → 45–55% WR
5. Triple MACD Momentum Scalping         → 55–62% WR
6. Dual EMA Fractal Breaker              → 48–54% WR
```

### Group 3: Mean Reversion (5 hours) — Quick Wins
```
7. Extreme Mean Reversion (RSI-2)        → 68–75% WR ⭐
8. VWAP Momentum Shift                   → 60–65% WR
9. Hikkake Inside Bar Trap               → 55–60% WR
```

### Group 4: Breakout/Session (4 hours) — Medium Priority
```
10. Opening Range Breakout (ORB)         → 50–56% WR
11. RVGI-CCI-SMA Confluence              → 52–58% WR
12. Volatility Contraction Breakout      → 40–50% WR
```

### Group 5: Advanced (3 hours) — Specialized
```
13. Statistical Arbitrage Spread (XAU/XAG) → 70–80% WR ⭐ (Pairs trade)
14. Naked Price Action (Engulfing)       → 50–55% WR
15. COT Sentiment Swing                  → 40–48% WR (Macro, FUTURE)
```

**Expected Outcome:**
- All 15 implemented and backtested
- 7 "Quick-Win" strategies (>60% WR or high PF)
- 3 "Specialized" strategies (pairs trading, macro)
- 5 "Medium-Priority" strategies (45–60% WR)

---

## 🔵 PHASE 2: WALK-FORWARD VALIDATION (8–10 hours)

**For All 25 Strategies:**

```bash
# Prepare walk-forward windows
python scripts/prepare_wfo_windows.py --windows 3 --is_pct 70 --oos_pct 20 --fwd_pct 10

# Run walk-forward test on each strategy
python scripts/run_walkforward.py --strategy range_breakout --windows 3
python scripts/run_walkforward.py --strategy institutional_silver_bullet --windows 3
... (repeat for all 25)

# Assign final tiers
python scripts/assign_strategy_tiers.py \
  --wfo_results wfo_results_all_25_strategies.csv \
  --output tier_assignment_final.csv
```

**Expected Tier Distribution:**

| Tier | Count | Status |
|------|-------|--------|
| TIER 1 | 8–12 | Enable for trading |
| TIER 2 | 10–12 | Monitor only |
| TIER 3 | 3–5 | Exclude |

**Update Configuration:**
```bash
# Edit config/strategies.yaml
# Set enabled: true for TIER 1 only
# Keep others disabled
```

---

## 🧪 PHASE 3: PAPER TRADING (2–4 weeks)

**Week 1–2: Live Signal Generation**
```bash
# Deploy and run
python scripts/run_paper.py --mode paper --verbose

# Monitor:
- Signal generation (no repeats)
- Order execution (clean fills)
- Telegram notifications
- P&L tracking
```

**Week 2–3: Stress Testing**
- Market gaps
- Low liquidity periods
- News spikes
- Crypto weekend trading

**Week 4: Final Report**
```
Check:
✓ Total trades match expectations
✓ Win rate within 20% of backtest
✓ Max drawdown < 15%
✓ Correlation between strategies < 0.6
✓ All regulatory requirements met
→ Go / No-Go for LIVE TRADING?
```

---

## 🎯 SUCCESS METRICS AT A GLANCE

### Phase 0 Success
- ✅ Bot stable 5+ min
- ✅ No retry loops
- ✅ Clear error messages

### Phase 1A Success
- ✅ 4–5 TIER 1 strategies confirmed
- ✅ Baseline documented (WR ~52%, PF ~1.45)

### Phase 1B Success
- ✅ 15 new strategies implemented
- ✅ 7 quick-wins identified (>60% WR)
- ✅ All backtested

### Phase 2 Success
- ✅ All 25 strategies walk-forward tested
- ✅ 8–12 strategies assigned TIER 1
- ✅ Configuration updated

### Phase 3 Success
- ✅ P&L within 20% of backtest
- ✅ Win rate: 55–65%
- ✅ Max drawdown: < 15%
- ✅ Ready for live trading

---

## 📊 THE 10%+ IMPROVEMENT FORMULA

**Where +10% comes from:**

```
Institutional Flow Strategies       (+3–5%)
  ↓ Liquidity sweeps, market structure, order flow
  
Mean Reversion Strategies           (+2–3%)
  ↓ RSI extremes, VWAP deviations, price action
  
Ensemble Voting                     (+1–2%)
  ↓ Reduce false signals: 2+ strategies agree
  
Regime Filtering (Path B)           (+2–3%)
  ↓ Only trade in favorable macro conditions
  
Multi-TF Confirmation (Path B)      (+1–2%)
  ↓ Confirm H1 signals with H4 structure
  
────────────────────────────────────────────
TOTAL EXPECTED BOOST               +9–15%
Conservative Target               +10% ✓
```

---

## 🚨 CRITICAL PATHS & BLOCKERS

```
Phase 0 (1–2h) ──→ MUST COMPLETE before Phase 1
    ↓
Phase 1A (6–8h) ──→ Validate existing 10
    ↓
Phase 1B (12–16h) ──→ Implement + test 15 new
    ↓
Phase 2 (8–10h) ──→ Walk-forward validation (all 25)
    ↓
Phase 3 (2–4w) ──→ Paper trading demo run
    ↓
Phase 4 ──→ LIVE TRADING (if all above pass)
```

**Blockers:**
- Phase 0 BLOCKS everything (bot must be stable)
- Phase 1A BLOCKS Phase 1B (need baseline)
- Phase 1B BLOCKS Phase 2 (need 15 implementations)
- Phase 2 BLOCKS Phase 3 (need tier assignments)
- Phase 3 BLOCKS Phase 4 (need 2–4 week validation)

---

## 🔧 COMMON QUICK FIXES

### Bot Keeps Failing on Same Signal
**Issue:** Signal deduplication not working  
**Fix:** Check `attempted_signals` dict in paper_engine.py  
**Verify:** `if signal_key in self.attempted_signals and ...`

### mt5.order_send Returns None
**Issue:** Order validation missing  
**Fix:** Add `_validate_order()` check in order_manager.py  
**Verify:** Symbol exists + lot size valid + liquidity > 0

### Data Looks Stale
**Issue:** No freshness check  
**Fix:** Add timestamp comparison in signal_checker.py  
**Verify:** `if time_diff > 1.5 * timeframe_minutes: print("WARNING")`

### Symbol Not Found in MT5
**Issue:** Market watch not configured  
**Fix:** Add symbol_select() calls in connector.py  
**Verify:** Check MT5 → Market Watch window

---

## 📞 HELP & ESCALATION

**Can't find something?**
1. Check AGENT_STRATEGY_TESTING_TASK_LIST.md (32 tasks in sequence)
2. Check STRATEGY_INTEGRATION_&_TESTING_PLAN.md (strategy details)
3. Check CONFIG_UPDATE_CHECKLIST.md (config requirements)
4. Check DIAGNOSTIC_REPORT.md (bot fixes)

**Got an error?**
- Check forward_test/ or mt5_bridge/ logs
- Verify config/strategies.yaml has strategy defined
- Verify config/config.yaml has pair/risk settings
- Check database connection string

**Ready to continue?**
- Phase 0 done? → Start Phase 1A
- Phase 1A done? → Start Phase 1B
- Phase 1B done? → Start Phase 2
- Phase 2 done? → Start Phase 3
- Phase 3 done? → Ready for LIVE!

---

## ✅ CHECKLIST: What You Should Have Done By Now

- [x] Read PROJECT_RESTRUCTURE_SUMMARY.md
- [x] Reviewed all 15 LeoDeX V2 strategy specs
- [x] Reviewed bot emergency fixes (Phase 0)
- [ ] **NEXT:** Approve Phase 0 to proceed
- [ ] Apply Phase 0 fixes (or assign to agent)
- [ ] Start Phase 1A backtesting

---

**Status:** ✅ **READY TO EXECUTE**

All documentation complete. Awaiting approval to proceed.

