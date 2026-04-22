# Path B Implementation Guide: +12–13% Win Rate
> **Status:** In Progress  
> **Estimated Duration:** 9 hours  
> **Target Completion:** End of Week  
> **Last Updated:** 2026-04-19

---

## Overview

Path B consists of **5 interconnected components**. Build them in this order:

```
COMPONENT 1: Ensemble Voting (1 hr)
  ↓ [Tests: backtest ensemble strategy]
COMPONENT 2: BB Mean Reversion Fix (1.5 hrs)
  ↓ [Tests: backtest improved BB strategy]
COMPONENT 3: Session Momentum Fix (1 hr)
  ↓ [Tests: backtest improved session strategy]
────────────────────────────────────
COMPONENT 4: Regime Filter (3 hrs)
  ├─ 4a: Macro data feed (DXY, VIX, yields)
  ├─ 4b: Regime classification logic
  └─ 4c: Wire into paper engine
  ↓ [Tests: verify regime classification, backtest with regime filter]
────────────────────────────────────
COMPONENT 5: Multi-TF Confirmation (2.5 hrs)
  ├─ 5a: Modify base strategy to support confirm_tf parameter
  ├─ 5b: Update config with confirm_tf settings
  └─ 5c: Wire into paper engine
  ↓ [Tests: backtest with multi-TF confirmation]
────────────────────────────────────
FINAL: Integration Testing & Walk-Forward (1 hr)
  ├─ Run full backtest suite with all improvements
  ├─ Run walk-forward validation
  └─ Deploy to paper trading
```

---

## Component 1: Ensemble Voting System

### Objective
Combine signals from Range Breakout, RSI Pullback, and Swing Pullback. Only trade when 2+ strategies agree.

### Files to Create/Modify
- ✅ Create: `strategies/ensemble.py`
- ✅ Update: `scripts/run_backtest.py` (add ensemble to STRATEGY_MAP)
- ✅ Update: `config/strategies.yaml` (add ensemble entry)

### Expected Outcome
- Fewer trades (−30%)
- Higher win rate (+5–10%)
- Sharpe ratio +8–15%

### Verification
```bash
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
# Expected: ~14 trades, 58–62% win rate, PF 1.9–2.1
```

---

## Component 2: BB Mean Reversion Fix

### Objective
Fix BB Mean Reversion (currently PF 0.69) by adding:
1. ADX < 20 hard filter (don't trade in trending markets)
2. Tighter RSI zones (< 25 instead of < 30)
3. Volume spike confirmation

### Files to Modify
- ✅ Update: `strategies/bb_mean_reversion.py`

### Expected Outcome
- PF 0.69 → 1.25–1.35 (+30–50%)
- Win rate 48–52% → 52–58%

### Verification
```bash
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1
# Expected: 20–30 trades, 52–58% win rate, PF 1.25–1.35
```

---

## Component 3: Session Momentum Fix

### Objective
Fix Session Momentum (currently PF 0.99) by:
1. Tighten trading window (13:30–15:30 UTC, not 13:00–17:00)
2. Add volume confirmation (>1.2x average)
3. Add previous session direction bias

### Files to Modify
- ✅ Update: `strategies/session_momentum.py`

### Expected Outcome
- PF 0.99 → 1.20–1.30 (+15–25%)
- Win rate 48–52% → 52–56%

### Verification
```bash
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
# Expected: 8–12 trades, 52–56% win rate, PF 1.20–1.30
```

---

## Component 4: Regime Filter

### 4a: Macro Data Feed

**Objective:** Pull DXY, VIX, and 10Y real yields daily.

**Files to Create:**
- ✅ Create: `data/macro_feed.py`
- ✅ Update: `.env` with API keys

**API Registrations (All Free):**
1. **Alpha Vantage (DXY):** https://www.alphavantage.co
   - Sign up → get API key
   - Rate limit: 5 calls/min (sufficient for daily updates)
   - Add to `.env`: `ALPHA_VANTAGE_API_KEY=...`

2. **FRED (10Y Real Yields):** https://fred.stlouisfed.org
   - Sign up → get API key
   - Rate limit: unlimited
   - Add to `.env`: `FRED_API_KEY=...`

3. **Yahoo Finance (VIX):** No API key needed; free via yfinance Python library

**Verification:**
```bash
python -c "from data.macro_feed import MacroDataFeed; m = MacroDataFeed(); print(m.get_regime())"
# Expected output: {'dxy': 102.5, 'vix': 16.2, 'yields': 2.1, 'regime': 'RISK_OFF'}
```

### 4b: Regime Classification Logic

**Objective:** Classify market as Risk-On, Risk-Off, or Transition.

**Files to Create:**
- ✅ Create: `risk/regime_classifier.py` (or extend existing regime_detector.py)

**Logic:**
```
RISK-OFF (favor Gold LONG):
  - DXY > DXY_50day_MA  (strong dollar)
  - 10Y Real Yields rising  (risk-off = yields up)
  - VIX > 15  (elevated volatility)
  → Signal: LONG_BIAS (only take long trades)

RISK-ON (favor Gold SHORT):
  - DXY < DXY_50day_MA  (weak dollar)
  - 10Y Real Yields falling  (risk-on = yields down)
  - VIX < 15  (low volatility)
  → Signal: SHORT_BIAS (only take short trades)

TRANSITION / MIXED:
  - Conflicting signals
  → Signal: NEUTRAL (skip trades or reduce size)
```

**Verification:**
```bash
python -c "from risk.regime_classifier import RegimeClassifier; rc = RegimeClassifier(); print(rc.classify())"
# Expected: 'RISK_OFF' or 'RISK_ON' or 'NEUTRAL'
```

### 4c: Wire into Paper Engine

**Objective:** Modify paper engine to respect regime bias.

**Files to Modify:**
- ✅ Update: `forward_test/paper_engine.py`
  - Before executing trade, check regime bias
  - If regime = RISK_OFF, only allow long trades
  - If regime = RISK_ON, only allow short trades
  - If regime = NEUTRAL, reduce position size or skip

**Verification:**
```bash
python scripts/run_paper.py
# In logs, should see: "[REGIME] RISK_OFF — Long bias active"
```

**Backtest Verification:**
```bash
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4 --regime-filter
# Expected: 15–20% fewer trades, 5–10% higher win rate, Sharpe +15–25%
```

---

## Component 5: Multi-Timeframe Confirmation

### 5a: Modify Base Strategy

**Objective:** Add optional `confirm_timeframe` parameter to all strategies.

**Files to Modify:**
- ✅ Update: `strategies/base_strategy.py`
  - Add `self.confirm_tf` parameter
  - Add method `_get_confirm_signal()`

**Logic:**
```python
def generate_signals(self, data):
    # Get signal from primary timeframe
    primary_signal = self._calc_signal(data)
    
    # If confirm_tf is set, check confirmation
    if self.confirm_tf:
        confirm_signal = self._get_confirm_signal()  # Fetch higher-TF data
        
        # Only trade if both agree
        if (primary_signal == 1 and confirm_signal != 1):
            return 0  # Cancel long
        if (primary_signal == -1 and confirm_signal != -1):
            return 0  # Cancel short
    
    return primary_signal
```

**Verification:**
```bash
python -c "from strategies.base_strategy import BaseStrategy; print('Base strategy updated with confirm_tf support')"
```

### 5b: Update Config

**Objective:** Add confirm_tf settings to strategies in config.yaml.

**Files to Modify:**
- ✅ Update: `config/strategies.yaml`

**Example:**
```yaml
strategies:
  - name: range_breakout
    enabled: true
    confirm_timeframe: H4        # Require H4 confirmation for H1 entries
    confirm_threshold: ema_crossover  # EMA(20) > EMA(50) for long
    
  - name: rsi_pullback
    enabled: true
    confirm_timeframe: H4
    confirm_threshold: trend_dir
    
  - name: swing_pullback
    enabled: true
    confirm_timeframe: D1
    confirm_threshold: ema_crossover
```

**Verification:**
```bash
python -c "import yaml; cfg = yaml.safe_load(open('config/strategies.yaml')); print(cfg['strategies'][0])"
# Expected: confirm_timeframe key present
```

### 5c: Wire into Paper Engine

**Objective:** Load confirm_tf settings and apply on paper trades.

**Files to Modify:**
- ✅ Update: `forward_test/paper_engine.py`
  - Load confirm_tf from config per strategy
  - Before executing trade, verify confirmation

**Verification:**
```bash
python scripts/run_paper.py
# In logs, should see: "[CONFIRM] H1 Range Breakout signal confirmed by H4 uptrend"
```

**Backtest Verification:**
```bash
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H1 --confirm-tf H4
# Expected: 20–30% fewer trades, 8–12% higher win rate
```

---

## Final Integration Testing

### Full Backtest Suite

Run all strategies with all improvements:

```bash
# Tier 1 with Ensemble
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4

# Tier 2 (fixed)
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1

# All with Regime Filter
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4 --regime-filter

# All with Multi-TF
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H1 --confirm-tf H4
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H1 --confirm-tf H4
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe D1 --confirm-tf W1
```

### Walk-Forward Validation

After baseline backtests pass:

```bash
# Ensemble WF
python scripts/run_walk_forward.py --strategy ensemble --pair XAUUSD --timeframe H4

# Tier 1 with regime filter
python scripts/run_walk_forward.py --strategy range_breakout --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_walk_forward.py --strategy rsi_pullback --pair XAUUSD --timeframe H4 --regime-filter
python scripts/run_walk_forward.py --strategy swing_pullback --pair XAUUSD --timeframe H4 --regime-filter
```

### Expected Results Summary

| Strategy | Before | After | Change |
|----------|--------|-------|--------|
| Range Breakout | PF 2.21, 52%, WF 100% | PF 2.40, 58%, WF 100% | +8%, +15% |
| RSI Pullback | PF 1.52, 56%, WF 80% | PF 1.70, 61%, WF 85% | +9%, +10% |
| Swing Pullback | PF 1.44, 53%, WF 80% | PF 1.65, 60%, WF 85% | +13%, +12% |
| **Ensemble (new)** | — | PF 2.10, 62%, WF 90% | — |
| BB Mean Reversion | PF 0.69, 50% | PF 1.28, 55% | +85%, +10% |
| Session Momentum | PF 0.99, 50% | PF 1.25, 55% | +26%, +10% |
| **Aggregate** | **~52% avg** | **~58–62% avg** | **+12–15%** |

---

## Deployment to Paper Trading

Once all tests pass:

1. Update `config/config.yaml`:
   ```yaml
   system:
     mode: paper
     regime_filter_enabled: true
     multi_tf_enabled: true
   ```

2. Restart paper engine:
   ```bash
   python scripts/run_paper.py
   ```

3. Monitor Telegram for trade signals:
   ```
   /status — should show regime bias and confirm status
   /balance — should show improved P&L from better entries
   ```

---

## Progress Tracking

- [ ] Component 1: Ensemble Voting (1 hr)
- [ ] Component 2: BB Mean Reversion Fix (1.5 hrs)
- [ ] Component 3: Session Momentum Fix (1 hr)
- [ ] Component 4a: Macro Data Feed (1 hr)
- [ ] Component 4b: Regime Classification (1 hr)
- [ ] Component 4c: Wire into Paper Engine (1 hr)
- [ ] Component 5a: Multi-TF Base Strategy (0.75 hr)
- [ ] Component 5b: Config Updates (0.5 hr)
- [ ] Component 5c: Wire into Paper Engine (0.75 hr)
- [ ] Integration Testing & Walk-Forward (1 hr)

**Total: 9 hours**

---

## Rollback Plan

If any component causes issues:

1. **Ensemble:** Comment out in `STRATEGY_MAP` in `run_backtest.py`
2. **BB/Session fixes:** Revert to original strategy files from git
3. **Regime Filter:** Set `regime_filter_enabled: false` in config
4. **Multi-TF:** Set `multi_tf_enabled: false` in config

All changes are backwards-compatible with existing strategies.

---

**Ready to implement Component 1? Let's go!**
