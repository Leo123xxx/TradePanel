# Path B Implementation Progress

> **Status:** In Progress (Component 1 Complete)  
> **Last Updated:** 2026-04-19  
> **Target Completion:** End of Week (9 hours total)  
> **Completed:** 1.5 hours | **Remaining:** 7.5 hours

---

## ✅ COMPLETED: Component 1 — Ensemble Voting System (1 hr)

### What Was Done

1. ✅ **Created `strategies/ensemble.py`**
   - Implements EnsembleStrategy class inheriting from BaseStrategy
   - Combines signals from RangeBreakout, RSIPullback, SwingPullback
   - Voting mechanism: requires 2/3 strategies to agree on direction
   - Expected improvement: +5–10% win rate, -30% false signals

2. ✅ **Updated `scripts/run_backtest.py`**
   - Added import: `from strategies.ensemble import EnsembleStrategy`
   - Added to STRATEGY_MAP: `"ensemble": EnsembleStrategy`

3. ✅ **Updated `config/strategies.yaml`**
   - Added ensemble entry before crypto strategies
   - Set `enabled: true` for immediate deployment
   - Configured for all 5 FX/metals pairs + 2 crypto pairs
   - Timeframes: H1, H4, D1

### How to Test Component 1

```bash
# Syntax check
python -c "from strategies.ensemble import EnsembleStrategy; print('Ensemble import OK')"

# Quick test
cd F:\REPOS\leo123xxx\TradePanel
python strategies/ensemble.py
# Expected: "[ENSEMBLE] All tests passed ✓"

# Baseline backtest (no regime filter, no multi-TF yet)
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
# Expected: ~14–16 trades, 58–62% win rate, PF 1.9–2.1
```

### Expected Results After Component 1

| Metric | Current | After Ensemble | Improvement |
|--------|---------|-----------------|------------|
| Avg Win Rate | 52% | 57–58% | +5–6% |
| Profit Factor | 1.72 | 1.85–1.95 | +7–13% |
| Sharpe Ratio | ~4.5 | ~4.8–5.0 | +5–10% |
| False Signals | 100% | 70% | -30% |

---

## ⏳ NEXT: Component 2 — BB Mean Reversion Fix (1.5 hrs)

### Status: Ready to build

**File to modify:** `strategies/bb_mean_reversion.py`

**Current State:** Already has ADX < 22 guard + wider RSI zones (20–40, 60–80)

**Additional Fixes Needed:**

1. **Tighten RSI oversold threshold (20 → 25)**
   - Current: RSI between 20–40 for long
   - Better: RSI between 25–40 (filters more false reversions)
   - Location: Line 56, `"rsi_os_low": 25`

2. **Add volume spike confirmation**
   - Require: `volume > volume_avg * 1.3` before entering
   - Why: BB touch without volume = less reliable reversion
   - New parameter: `"vol_spike_mult": 1.3`

3. **Add market structure support check**
   - Check if BB lower is near a support level (within 30 pips)
   - Why: BB + support = higher probability reversion
   - Add: `find_support()` method to identify S/R levels

**Expected Result:** PF 0.69 → 1.25–1.35 (+30–50% improvement)

### Implementation Steps for Agent

```bash
# 1. Make a backup
cp strategies/bb_mean_reversion.py strategies/bb_mean_reversion.py.bak

# 2. Edit the file:
# - Line 56: Change rsi_os_low from 20 to 25
# - Add new parameter: "vol_spike_mult": 1.3
# - Add method to detect support levels
# - Require volume spike before entry

# 3. Test
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1
# Expected: 20–30 trades, 52–58% win rate, PF 1.25–1.35
```

---

## ⏳ NEXT: Component 3 — Session Momentum Fix (1 hr)

### Status: Ready to build

**File to modify:** `strategies/session_momentum.py`

**Current State:** Trades 13:00–17:00 UTC, no volume or session direction filters

**Fixes Needed:**

1. **Tighten trading window (13:00–17:00 → 13:30–15:30)**
   - 13:30 = NY 8:30 AM open (peak volume)
   - 15:30 = 2 PM London / 10 AM NY (overlap high)
   - Current window is too wide; more chop after 16:00
   - Location: `session_start_utc: 13.5`, `session_end_utc: 15.5`

2. **Add volume confirmation**
   - Require: `volume > volume_avg * 1.2`
   - Why: High-volume setups more reliable
   - New parameter: `"vol_threshold_mult": 1.2`

3. **Add previous session direction bias**
   - Check yesterday's close vs. open
   - If up yesterday → only take longs today
   - If down yesterday → only take shorts today
   - Why: Session momentum often continues from previous day
   - Add method: `get_session_direction(lookback_days=1)`

**Expected Result:** PF 0.99 → 1.20–1.30 (+15–25% improvement)

### Implementation Steps for Agent

```bash
# 1. Make a backup
cp strategies/session_momentum.py strategies/session_momentum.py.bak

# 2. Edit the file:
# - Change session_start_utc: 13 → 13.5
# - Change session_end_utc: 17 → 15.5
# - Add vol_threshold_mult: 1.2
# - Add previous session direction check

# 3. Test
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
# Expected: 8–12 trades, 52–56% win rate, PF 1.20–1.30
```

---

## ⏳ THEN: Component 4 — Regime Filter (3 hrs)

### Status: Design complete, ready for implementation

**Three Sub-Components:**

#### 4a: Macro Data Feed (1 hr)
- Create: `data/macro_feed.py`
- Pull DXY, VIX, 10Y real yields daily
- APIs: Alpha Vantage (free), FRED (free), Yahoo Finance (free)
- Add API keys to `.env`

#### 4b: Regime Classifier (1 hr)
- Create: `risk/regime_classifier.py`
- Classify: Risk-Off (LONG_BIAS), Risk-On (SHORT_BIAS), Transition (NEUTRAL)
- Logic: DXY > MA + Yields > MA + VIX > 15 = RISK_OFF

#### 4c: Wire into Paper Engine (1 hr)
- Update: `forward_test/paper_engine.py`
- Before trade execution: check regime bias
- If RISK_OFF: only allow longs
- If RISK_ON: only allow shorts
- If NEUTRAL: reduce position size or skip

**Expected Result:** +15–20% win rate across all strategies

---

## ⏳ THEN: Component 5 — Multi-TF Confirmation (2.5 hrs)

### Status: Design complete, ready for implementation

**Three Sub-Components:**

#### 5a: Modify Base Strategy (0.75 hr)
- Update: `strategies/base_strategy.py`
- Add `self.confirm_tf` parameter
- Add method: `_get_confirm_signal()`

#### 5b: Update Config (0.5 hr)
- Update: `config/strategies.yaml`
- Add per-strategy: `confirm_timeframe: H4` or `D1`
- Add: `confirm_threshold: ema_crossover` or `trend_dir`

#### 5c: Wire into Paper Engine (0.75 hr)
- Update: `forward_test/paper_engine.py`
- Load confirm_tf settings per strategy
- Before executing trade: verify confirmation from higher TF

**Expected Result:** +8–12% win rate, -20–30% false signals

---

## Integration Testing (1 hr)

After all 5 components complete:

```bash
# Full backtest suite
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1

# With regime filter
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4 --regime-filter

# With multi-TF confirmation
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H1 --confirm-tf H4
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H1 --confirm-tf H4

# Walk-forward validation
python scripts/run_walk_forward.py --strategy ensemble --pair XAUUSD --timeframe H4
```

---

## Summary: What Agent Should Do Next

### IMMEDIATE (Next 2.5 hours)

**Component 2 — BB Mean Reversion Fix:**
```bash
# 1. Edit strategies/bb_mean_reversion.py:
#    - rsi_os_low: 20 → 25
#    - Add vol_spike_mult: 1.3
#    - Add volume spike check in signal generation
#    - Add support level detection

# 2. Test
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1

# 3. Verify: PF 0.69 → 1.25+, Win Rate 48–52% → 52–58%
```

**Component 3 — Session Momentum Fix:**
```bash
# 1. Edit strategies/session_momentum.py:
#    - session_start_utc: 13 → 13.5
#    - session_end_utc: 17 → 15.5
#    - Add vol_threshold_mult: 1.2
#    - Add previous session direction bias

# 2. Test
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1

# 3. Verify: PF 0.99 → 1.20+, Win Rate → 52–56%
```

### THEN (Next 5.5 hours)

- Component 4: Regime Filter (3 hrs)
- Component 5: Multi-TF Confirmation (2.5 hrs)
- Integration Testing (1 hr)

---

## Verification Checklist

After each component, run:

```bash
✓ Syntax check: ast.parse() on modified files
✓ Import test: python -c "from module import Class"
✓ Backtest: single strategy run
✓ Expected results match numbers above
✓ No errors in log output
✓ Trade count reasonable (not 0, not >100)
✓ Win rate trend positive
✓ Profit Factor > 1.0
```

---

## Files Status

| File | Status | Component |
|------|--------|-----------|
| `strategies/ensemble.py` | ✅ Created | 1 |
| `scripts/run_backtest.py` | ✅ Updated | 1 |
| `config/strategies.yaml` | ✅ Updated | 1 |
| `strategies/bb_mean_reversion.py` | ⏳ To modify | 2 |
| `strategies/session_momentum.py` | ⏳ To modify | 3 |
| `data/macro_feed.py` | ⏳ To create | 4a |
| `risk/regime_classifier.py` | ⏳ To create | 4b |
| `forward_test/paper_engine.py` | ⏳ To update | 4c, 5c |
| `strategies/base_strategy.py` | ⏳ To update | 5a |
| `config/strategies.yaml` | ⏳ To update (add confirm_tf) | 5b |

---

## Time Budget

| Component | Estimate | Actual | Status |
|-----------|----------|--------|--------|
| 1: Ensemble | 1 hr | ✅ 1 hr | Complete |
| 2: BB Fix | 1.5 hrs | ⏳ Pending | Next |
| 3: Session Fix | 1 hr | ⏳ Pending | Next |
| 4: Regime Filter | 3 hrs | ⏳ Pending | Later |
| 5: Multi-TF | 2.5 hrs | ⏳ Pending | Later |
| Integration | 1 hr | ⏳ Pending | Final |
| **Total** | **9 hrs** | **1 hr done** | **8 hrs left** |

---

**Ready for Components 2–3? Agent should proceed with BB Mean Reversion and Session Momentum fixes.**

