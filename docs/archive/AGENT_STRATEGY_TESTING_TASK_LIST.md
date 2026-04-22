# 🎯 AGENT STRATEGY TESTING TASK LIST
**Project:** TradePanel LeoDeX V2 Strategy Integration & Testing  
**Date:** 2026-04-20  
**Assigned Agent:** (To be assigned)  
**Total Tasks:** 32  
**Estimated Duration:** 4–6 weeks (including 2–4 week demo)

---

## 📌 QUICK START FOR AGENT

**Your Role:** Execute the TradePanel strategy integration and testing project step-by-step.

**What You'll Do:**
1. Apply 4 emergency bot fixes (Phase 0) — 1–2 hours
2. Validate 10 existing strategies (Phase 1A) — 6–8 hours
3. Implement 15 new LeoDeX V2 strategies (Phase 1B) — 12–16 hours
4. Run walk-forward validation (Phase 2) — 8–10 hours
5. Monitor paper trading (Phase 3) — 2–4 weeks

**Success Metric:** 10%+ improvement in aggregate win rate/profit factor across 25-strategy ensemble

**Key Documents to Read First:**
1. **STRATEGY_INTEGRATION_&_TESTING_PLAN.md** — Overview & strategy groups
2. **CONFIG_UPDATE_CHECKLIST.md** — All config changes needed
3. **DIAGNOSTIC_REPORT.md** — Phase 0 bot fixes
4. **MASTER_PROJECT_STATUS.md** — Project timeline & phases

---

## 🔴 PHASE 0: EMERGENCY BOT STABILIZATION (1–2 hours)

**Status:** 🔴 BLOCKING — Must complete before strategy testing  
**Blocker:** Live bot in retry loop  
**Success Criteria:** Bot runs stable for 5+ minutes without error loop

### TASK 0.0: Apply Signal Deduplication Fix
**File:** `forward_test/paper_engine.py`  
**Time:** 30 minutes  
**Instructions:** See DIAGNOSTIC_REPORT.md → "Fix 1: Signal Deduplication"

**What to Do:**
1. Add `self.attempted_signals = {}` dict to PaperEngine.__init__()
2. Before executing order, check if signal key already attempted on this bar
3. Track attempted signals by (strat_name, symbol, timeframe) + bar_time
4. Skip execution if already attempted; mark as done after execution

**Testing:**
```bash
python scripts/run_paper.py
# Watch console for signal deduplication:
# ✓ "Already attempted on this bar, skipping"
# ✓ No repeated "SIGNAL DETECTED" for same bar/strategy
```

**Expected Outcome:** Same signal not repeated on same bar ✅

---

### TASK 0.1: Apply Order Validation Fix
**File:** `mt5_bridge/order_manager.py`  
**Time:** 20 minutes  
**Instructions:** See DIAGNOSTIC_REPORT.md → "Fix 2: Order Validation"

**What to Do:**
1. Add `_validate_order(symbol, direction, lot)` method to OrderManager
2. Check: Symbol exists via `mt5.symbol_info(symbol)`
3. Check: Lot size within `symbol_info.volume_min/max`
4. Check: Symbol has liquidity (trade_tick_value > 0)
5. Return True if valid; raise ValueError with clear message if not

**Testing:**
```bash
python scripts/run_paper.py
# Watch for clear error messages:
# ✓ "Order validation failed: Symbol XAUUSD not in market watch"
# ✓ "Lot 2.5 outside [0.01, 1.0]"
# ✓ No more "mt5.order_send returned None" loops
```

**Expected Outcome:** Clear error messages on order failure ✅

---

### TASK 0.2: Apply Data Freshness Check
**File:** `forward_test/signal_checker.py`  
**Time:** 15 minutes  
**Instructions:** See DIAGNOSTIC_REPORT.md → "Fix 3: Data Freshness Check"

**What to Do:**
1. In `get_signal()` method, check data age
2. Compare latest_time (from df) vs current_time (datetime.utcnow())
3. If time_diff > 1.5 × timeframe_minutes, print WARNING
4. Continue signal generation (don't block)

**Testing:**
```bash
python scripts/run_paper.py
# Watch for warnings when data is stale:
# ✓ "WARNING: Data is 450 seconds old (>5min)"
# ✓ No blocking of signal generation
```

**Expected Outcome:** Data freshness logged/warned ✅

---

### TASK 0.3: Apply Market Watch Symbol Setup
**File:** `mt5_bridge/connector.py`  
**Time:** 15 minutes  
**Instructions:** See DIAGNOSTIC_REPORT.md → "Fix 4: Market Watch Setup"

**What to Do:**
1. In `connect()` method, after MT5 initialization
2. Add all required symbols to market watch via `mt5.symbol_select(symbol, True)`
3. Required symbols: `["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]`
4. Log warning if any symbol fails to select

**Testing:**
```bash
python scripts/run_paper.py
# Verify in MT5 Market Watch window:
# ✓ All 7 symbols appear in MT5 Market Watch
# ✓ No "Symbol not in market watch" errors
```

**Expected Outcome:** All symbols in market watch on connect ✅

---

### TASK 0.4: Verify Phase 0 Completion
**Time:** 10 minutes  
**Success Criteria:**

- [ ] Bot runs 5+ minutes without error loop
- [ ] Same signal not repeated on same bar
- [ ] Orders execute OR fail with clear error message
- [ ] No "mt5.order_send returned None" loops
- [ ] All 7 symbols in MT5 market watch
- [ ] Data freshness warnings logged when applicable

**Report:** Create brief summary showing all 4 fixes applied + test results

**Go/No-Go Decision:** Proceed to Phase 1A only if ALL criteria met ✅

---

## 📈 PHASE 1A: VALIDATE EXISTING STRATEGIES (6–8 hours)

**Status:** ⏳ Queued (After Phase 0)  
**Objective:** Baseline all 10 existing strategies before adding new ones  
**Success Criteria:** Tier-1 strategies confirmed; exclusions identified

### TASK 1A.0: Prepare Backtest Environment
**Time:** 30 minutes  
**Checklist:**

- [ ] Verify data exists for all 7 trading pairs (6+ years for FX, 4+ for crypto)
- [ ] Run data validation:
  ```bash
  python scripts/validate_data.py --pair XAUUSD --timeframes M5,H1,H4,D1
  python scripts/validate_data.py --pair BTCUSD --start 2021-01-01
  ```
- [ ] Confirm backtesting database is clean
- [ ] Set backtesting parameters: 70% IS / 20% OOS / 10% FWD
- [ ] Verify all strategy files exist and are importable

**Exit Criteria:**
- ✓ All data validations pass
- ✓ Backtesting engine runs without errors on single strategy

---

### TASK 1A.1: Backtest Range Breakout Strategy
**Time:** 30 minutes  
**Instructions:**

```bash
# Test on primary pair
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4

# Expected output:
# Total Trades: 12-18
# Win Rate: 50-56%
# Profit Factor: 1.40-1.50
# Expected Tier: TIER 1 (confirm)
```

**Document Results:** Create backtest_results_range_breakout.txt showing:
- Total trades
- Win rate
- Profit factor
- Largest win / largest loss
- Sharpe ratio

**Decision:** Keep as Tier 1? YES/NO/MODIFY

---

### TASK 1A.2: Backtest RSI Pullback Strategy
**Time:** 30 minutes

```bash
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4
# Expected: WR 48-54%, PF 1.45-1.60
```

**Decision:** Keep as Tier 1? YES/NO/MODIFY

---

### TASK 1A.3: Backtest Swing Pullback Strategy
**Time:** 30 minutes

```bash
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4
# Expected: WR 52-60%, PF 2.0-2.5 (best performer)
```

**Decision:** Keep as Tier 1? YES/NO/MODIFY

---

### TASK 1A.4: Backtest EMA Ribbon Trend (Crypto)
**Time:** 30 minutes

```bash
python scripts/run_backtest.py --strategy ema_ribbon_trend --pair BTCUSD --timeframe H4
# Expected: WR 45-55%, PF 1.6-1.9
```

**Decision:** Keep as Tier 1 for crypto? YES/NO/MODIFY

---

### TASK 1A.5: Backtest Crypto RSI Extremes
**Time:** 30 minutes

```bash
python scripts/run_backtest.py --strategy crypto_rsi_extremes --pair BTCUSD --timeframe H4
# Expected: WR 50-60%, PF 1.4-1.7
```

**Decision:** Keep as Tier 1 for crypto? YES/NO/MODIFY

---

### TASK 1A.6: Backtest Tier-2 Strategies (Quick Pass)
**Time:** 2 hours (10 min each)  
**Strategies to quick-test:**

```bash
# Test each for baseline confirmation
python scripts/run_backtest.py --strategy ma_crossover --pair EURUSD --timeframe H1
python scripts/run_backtest.py --strategy rsi_bounce --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy stoch_divergence --pair EURUSD --timeframe H4
python scripts/run_backtest.py --strategy volatility_squeeze_breakout --pair BTCUSD --timeframe H4
```

**Document:** Create tier_assignment_existing_10.csv showing strategy name, win rate, profit factor, tier assignment

---

### TASK 1A.7: Generate Tier Assignment Report
**Time:** 30 minutes  
**Output:** tier_assignment_existing_10.md

**Template:**
```
# Existing Strategies — Phase 1A Tier Assignment

| Strategy | Pair | Timeframe | Trades | Win Rate | PF | Sharpe | Tier |
|----------|------|-----------|--------|----------|----|---------|----|
| Range Breakout | XAUUSD | H4 | 15 | 54% | 1.45 | 2.3 | TIER 1 |
| RSI Pullback | XAUUSD | H4 | 12 | 50% | 1.52 | 2.1 | TIER 1 |
...
```

**Success Metric:** 3–5 strategies confirmed as Tier 1; clear rationale for each

---

## 🚀 PHASE 1B: IMPLEMENT & TEST 15 NEW LEDEDX V2 STRATEGIES (12–16 hours)

**Status:** ⏳ Queued (After Phase 1A)  
**Objective:** Implement, integrate, and validate 15 new strategies  
**Key Concept:** Implement in groups; backtest each group after coding

### TASK 1B-G1.0: Implement Institutional Silver Bullet (SMC)
**Time:** 2 hours  
**File:** `strategies/institutional_silver_bullet.py`

**Template to Follow:**
```python
from strategies.base_strategy import BaseStrategy
import pandas as pd
import numpy as np

class InstitutionalSilverBulletStrategy(BaseStrategy):
    def __init__(self, config=None):
        params = config or {}
        super().__init__(
            name="institutional_silver_bullet",
            category="Institutional Flow",
            params=params,
            regime=["ANY"],
            timeframes=["M15", "M5"],
            pairs=['XAUUSD', 'GBPUSD', 'EURUSD']
        )
    
    def generate_signals(self, data):
        # 1. Detect liquidity sweep (10-20 pips beyond level)
        # 2. Identify market structure shift (MSS)
        # 3. Wait for fair value gap (FVG) retracement
        # 4. Enter on retracement close
        # Entry signal: 1 (long) or -1 (short)
        pass
```

**Key Entry Logic:**
- Detect liquidity sweep during London/NY killzones (03:00-10:00 EST)
- Identify strong MSS with displacement
- Enter on retracement to newly formed FVG
- TP at next major liquidity pool (min 3:1 RR)
- SL 1 ATR beyond order block

**Testing:**
```bash
python scripts/run_backtest.py --strategy institutional_silver_bullet --pair XAUUSD --timeframe M15
# Expected: 60-68% win rate, 3.0+ avg RR
```

**Success Criteria:** Strategy runs without errors; backtest shows >50% win rate

---

### TASK 1B-G1.1: Implement ICT Judas Swing
**Time:** 2 hours  
**File:** `strategies/ict_judas_swing.py`

**Key Entry Logic:**
- Identify Asian Range consolidation (5 bars lookback)
- Watch for fake breakout at London Open (08:00 UTC)
- Detect 1-minute CHoCH (Change of Character)
- Enter opposite the fake breakout once CHoCH confirmed
- TP at opposite side of Asian Range (min 3:1 RR)
- SL just beyond Judas Swing wick

**Testing:**
```bash
python scripts/run_backtest.py --strategy ict_judas_swing --pair GBPUSD --timeframe M15
# Expected: 62-68% win rate, 3.5+ avg RR
```

---

### TASK 1B-G1.2: Implement Turtle Soup Liquidity Sweep
**Time:** 2 hours  
**File:** `strategies/turtle_soup_liquidity_sweep.py`

**Key Entry Logic:**
- Identify old highs/lows untouched for >20 periods
- Watch for price to sweep these levels 10-20 pips
- Detect retail stop triggering
- Close back inside range and enter
- TP at opposing liquidity pool
- SL 1 ATR beyond sweep wick

**Testing:**
```bash
python scripts/run_backtest.py --strategy turtle_soup_liquidity_sweep --pair XAUUSD --timeframe H1
# Expected: 60-65% win rate, 3.0+ avg RR
```

**Group 1 Completion Check:**
- [ ] All 3 strategies implemented
- [ ] All 3 strategies backtest >50% win rate
- [ ] All 3 ready for walk-forward validation

---

### TASK 1B-G2.0: Implement Dual EMA Momentum Continuity
**Time:** 1.5 hours  
**File:** `strategies/dual_ema_momentum.py`

**Key Entry Logic:**
- Fast EMA (10) crosses Slow EMA (50)
- ADX(14) must be > 25 (trending)
- Enter on pullback into EMA "Value Zone"
- Confirm with engulfing candle
- Trail stop using 2x ATR
- No fixed TP; ride the macro trend until EMA cross reverses

**Testing:**
```bash
python scripts/run_backtest.py --strategy dual_ema_momentum --pair BTCUSD --timeframe H4
# Expected: 45-55% win rate, 4.0+ avg RR
```

---

### TASK 1B-G2.1: Implement Triple MACD Momentum Scalping
**Time:** 2 hours  
**File:** `strategies/triple_macd_momentum.py`

**Key Entry Logic:**
- Layer C (200 SMA): Macro trend filter
- Layer B (50 SMA): Intraday trend alignment
- Layer A (MACD 12/26/9): Scalp trigger
- Enter when all 3 layers align AND Layer A crosses zero line
- TP at 3:1 RR
- SL just below recent swing low
- Close if Layer A reverses before target

**Testing:**
```bash
python scripts/run_backtest.py --strategy triple_macd_momentum --pair XAUUSD --timeframe M5
# Expected: 55-62% win rate, 3.0+ avg RR
```

---

### TASK 1B-G2.2: Implement Dual EMA Fractal Breaker
**Time:** 1.5 hours  
**File:** `strategies/dual_ema_fractal_breaker.py`

**Key Entry Logic:**
- Price > 200 EMA (Uptrend confirmation)
- Bill Williams 'Up Fractal' forms near 14 EMA
- Place buy-stop 1 pip above Fractal high
- TP at 3:1 RR
- SL at most recent 'Down Fractal'

**Testing:**
```bash
python scripts/run_backtest.py --strategy dual_ema_fractal_breaker --pair EURUSD --timeframe H1
# Expected: 48-54% win rate, 3.0+ avg RR
```

**Group 2 Completion Check:**
- [ ] All 3 strategies implemented
- [ ] All 3 strategies backtest >40% win rate
- [ ] All 3 ready for walk-forward validation

---

### TASK 1B-G3.0: Implement Extreme Mean Reversion (RSI-2)
**Time:** 1.5 hours  
**File:** `strategies/extreme_mean_reversion.py`

**Key Entry Logic:**
- Price > 200 SMA (Uptrend bias)
- RSI(2) drops < 10 (extreme oversold)
- Price drops below Lower Bollinger Band (20, 2)
- Enter Long on close
- TP at 20 SMA (middle band)
- SL 1.5x ATR below entry wick

**Testing:**
```bash
python scripts/run_backtest.py --strategy extreme_mean_reversion --pair EURUSD --timeframe H4
# Expected: 68-75% win rate, 2.0-3.0 avg RR
```

---

### TASK 1B-G3.1: Implement VWAP Momentum Shift
**Time:** 1.5 hours  
**File:** `strategies/vwap_momentum_shift.py`

**Key Entry Logic:**
- Price deviates strongly from daily VWAP (hitting 2nd standard deviation)
- Wait for reversal candlestick pattern (Pin bar / Engulfing)
- Enter back toward VWAP baseline
- TP at VWAP baseline
- SL 1.5x ATR beyond extreme deviation wick

**Testing:**
```bash
python scripts/run_backtest.py --strategy vwap_momentum_shift --pair ETHUSD --timeframe M15
# Expected: 60-65% win rate, 2.5-3.0 avg RR
```

---

### TASK 1B-G3.2: Implement Hikkake Inside Bar Trap
**Time:** 1.5 hours  
**File:** `strategies/hikkake_inside_bar.py`

**Key Entry Logic:**
- Identify Inside Bar (price range inside previous bar)
- Price breaks out of Inside Bar
- Traps retail traders
- If price reverses within 3 candles, enter opposite direction
- TP at next major swing structure (3:1 RR)
- SL at extreme of trap candle

**Testing:**
```bash
python scripts/run_backtest.py --strategy hikkake_inside_bar --pair BTCUSD --timeframe H4
# Expected: 55-60% win rate, 3.0+ avg RR
```

**Group 3 Completion Check:**
- [ ] All 3 strategies implemented
- [ ] All 3 strategies backtest >50% win rate
- [ ] All 3 ready for walk-forward validation

---

### TASK 1B-G4.0: Implement Opening Range Breakout (ORB)
**Time:** 1 hour  
**File:** `strategies/opening_range_breakout.py`

**Key Entry Logic:**
- Define high/low range of first Frankfurt session hour (08:00-09:00 UTC)
- Wait for candle to close decisively outside range
- Enter on immediate retest of broken boundary
- TP = 3x opening range
- SL at midpoint of opening range

**Testing:**
```bash
python scripts/run_backtest.py --strategy opening_range_breakout --pair GBPUSD --timeframe M15
# Expected: 50-56% win rate, 3.0+ avg RR
```

---

### TASK 1B-G4.1: Implement RVGI-CCI-SMA Confluence
**Time:** 1.5 hours  
**File:** `strategies/rvgi_cci_sma.py`

**Key Entry Logic:**
- Triple alignment required:
  1. RVGI (Relative Vigor Index) crosses up
  2. CCI rises from < -100 (oversold)
  3. Price below 30 SMA but breaking local fractal high
- TP at next H4 structural resistance
- SL strictly below swing low

**Testing:**
```bash
python scripts/run_backtest.py --strategy rvgi_cci_sma --pair GBPUSD --timeframe H1
# Expected: 52-58% win rate, 3.5+ avg RR
```

---

### TASK 1B-G4.2: Implement Volatility Contraction Breakout
**Time:** 1 hour  
**File:** `strategies/volatility_contraction_breakout.py`

**Key Entry Logic:**
- Look for 3-4 consecutive days of decreasing daily ranges
- Wait for high-volume breakout from contraction zone
- Trail stop using low of previous day's candle
- No fixed TP; capture volatility expansion

**Testing:**
```bash
python scripts/run_backtest.py --strategy volatility_contraction_breakout --pair USDJPY --timeframe D1
# Expected: 40-50% win rate, 4.0+ avg RR
```

**Group 4 Completion Check:**
- [ ] All 3 strategies implemented
- [ ] All 3 strategies backtest >40% win rate
- [ ] All 3 ready for walk-forward validation

---

### TASK 1B-G5.0: Implement Statistical Arbitrage Spread (XAU/XAG)
**Time:** 1 hour  
**File:** `strategies/statistical_arbitrage_spread.py`

**Key Entry Logic:**
- Calculate Z-Score of XAU/XAG price ratio
- When Z-Score > 2.0 (Gold overpriced vs Silver):
  - SHORT XAUUSD + LONG XAGUSD simultaneously
- Exit both positions when Z-Score reverts to 0 (mean)
- Expected PF > 1.6

**Testing:**
```bash
python scripts/run_backtest.py --strategy statistical_arbitrage_spread --pair XAUUSD,XAGUSD --timeframe H4
# Expected: 70-80% win rate, PF > 1.6
# Note: This is a pairs trade — two trades open simultaneously
```

---

### TASK 1B-G5.1: Implement Naked Price Action (Engulfing)
**Time:** 1 hour  
**File:** `strategies/naked_price_action.py`

**Key Entry Logic:**
- Strip indicators; identify clean D1 Support/Resistance levels
- Look for massive Bullish/Bearish Engulfing candle
- Candlebody must be >70% of range to qualify
- Enters on rejection of S/R zone
- TP at next Daily zone (4:1 RR expected)
- SL: 5 pips above/below engulfing candle
- Move stop to break-even at 1:1

**Testing:**
```bash
python scripts/run_backtest.py --strategy naked_price_action --pair EURUSD --timeframe D1
# Expected: 50-55% win rate, 4.0+ avg RR
```

---

### TASK 1B-G5.2: Implement COT Sentiment Swing
**Time:** 1 hour  
**File:** `strategies/cot_sentiment_swing.py`

**Key Entry Logic:**
- Use weekly Commitment of Traders (COT) report
- When Commercial hedging hits extreme (e.g., massive net longs on Silver)
- AND non-commercials heavily short (opposite position)
- Wait for D1 bullish break of structure to enter
- Hold for multi-week/month swings
- SL below macro swing low (3x ATR)
- Expected 1:5.0 to 1:10.0 RR

**Note:** COT data may not be available yet. Mark as "Future" if external feed required.

**Testing:**
```bash
# If COT data available:
python scripts/run_backtest.py --strategy cot_sentiment_swing --pair XAUUSD --timeframe D1
# Expected: 40-48% win rate, 5.0+ avg RR
```

**Group 5 Completion Check:**
- [ ] All 3 strategies implemented
- [ ] All 3 strategies backtested (COT may be "Future")
- [ ] All 3 ready for walk-forward validation

---

### TASK 1B.F: Generate Phase 1B Completion Report
**Time:** 1 hour  
**Output:** phase_1b_implementation_summary.md

**Report Contents:**
```
# Phase 1B — Implementation Summary

## Group 1: Institutional Flow (3/3)
- Institutional Silver Bullet: ✓ Implemented, WR 62%, PF 1.8
- ICT Judas Swing: ✓ Implemented, WR 65%, PF 2.1
- Turtle Soup Liquidity: ✓ Implemented, WR 61%, PF 1.7

## Group 2: Trend Following (3/3)
...

## Summary Statistics
- Total Strategies Implemented: 15
- Average Win Rate: 57%
- Average Profit Factor: 1.68
- Quick-Win Strategies (>60% WR): 7
- Strategies Ready for Walk-Forward: 15

## Issues & Notes
- [Any blockers or special considerations]
```

**Success Metric:** All 15 strategies implemented and backtested

---

## 📊 PHASE 2: WALK-FORWARD VALIDATION & TIER ASSIGNMENT (8–10 hours)

**Status:** ⏳ Queued (After Phase 1B)  
**Objective:** Validate all 25 strategies through walk-forward testing

### TASK 2.0: Prepare Walk-Forward Test Windows
**Time:** 1 hour

**Define 3 Walk-Forward Windows:**
- Window 1 (2022–2023): 70% IS / 20% OOS / 10% FWD
- Window 2 (2023–2024): 70% IS / 20% OOS / 10% FWD
- Window 3 (2024–2026): 70% IS / 20% OOS / 10% FWD

**Script:**
```bash
python scripts/prepare_wfo_windows.py \
  --windows 3 \
  --is_pct 70 \
  --oos_pct 20 \
  --fwd_pct 10
```

---

### TASK 2.1: Run Walk-Forward Validation (All 25 Strategies)
**Time:** 6 hours (15 min per strategy average)

**For Each Strategy (Existing + New):**
1. Run WFO with 3 windows
2. Track IS, OOS, and FWD profit factors
3. Flag if OOS PF degrades >20% from IS (overfitting)
4. Calculate aggregate metrics

**Batch Script:**
```bash
for strategy in range_breakout rsi_pullback swing_pullback \
                ema_ribbon_trend crypto_rsi_extremes \
                institutional_silver_bullet ict_judas_swing turtle_soup \
                dual_ema_momentum triple_macd_momentum dual_ema_fractal \
                extreme_mean_reversion vwap_momentum_shift hikkake_inside_bar \
                opening_range_breakout rvgi_cci_sma volatility_contraction \
                statistical_arbitrage_spread naked_price_action cot_sentiment; do
  echo "WFO: $strategy"
  python scripts/run_walkforward.py --strategy $strategy --windows 3
done
```

**Document Results:** Create wfo_results_all_25_strategies.csv

---

### TASK 2.2: Assign Strategy Tiers
**Time:** 1.5 hours

**Tier Criteria:**
| Tier | Win Rate | PF | Sharpe | Action |
|------|----------|----|---------|----|
| TIER 1 | ≥50% | ≥1.3 | ≥2.5 | Enable, use in trading |
| TIER 2 | 45–49% | 1.1–1.29 | 2.0–2.49 | Monitor, optional |
| TIER 3 | <45% | <1.1 | <2.0 | Disable, review later |

**Script to Generate Tier Report:**
```bash
python scripts/assign_strategy_tiers.py \
  --wfo_results wfo_results_all_25_strategies.csv \
  --output tier_assignment_final.csv
```

**Expected Distribution:**
- TIER 1: 8–12 strategies (including 3–5 institutional/mean-reversion)
- TIER 2: 10–12 strategies
- TIER 3: 3–5 strategies

---

### TASK 2.3: Create Final Configuration Matrix
**Time:** 1.5 hours

**Output:** tier_assignment_final.md + updated strategies.yaml

**Update config/strategies.yaml:**
- Set `enabled: true` for all TIER 1 strategies
- Set `enabled: false` for TIER 2/3 strategies
- Add pair-specific overrides based on WFO results
- Document any parameter changes needed

**Example:**
```yaml
# Update to strategies.yaml after WFO validation

# TIER 1 — Enable immediately
range_breakout:
  enabled: true
  # ...

institutional_silver_bullet:
  enabled: true
  # Adjust parameters if needed based on WFO results
  # ...

# TIER 2 — Monitor
ma_crossover:
  enabled: false  # Disable until validation complete
  # ...

# TIER 3 — Exclude
bb_mean_reversion:
  enabled: false  # Excluded; PF < 1.1 on OOS
  # ...
```

---

### TASK 2.4: Generate Phase 2 Final Report
**Time:** 1 hour

**Output:** phase_2_walkforward_summary.md

**Report Contents:**
```
# Phase 2 — Walk-Forward Validation Summary

## Tier Assignment (25 Strategies)

### TIER 1 (Approved for Trading) — [X] Strategies
- [Strategy Name]: WR 55%, PF 1.45, Sharpe 2.4
- ...

### TIER 2 (Monitor) — [X] Strategies
- ...

### TIER 3 (Excluded) — [X] Strategies
- ...

## Key Findings
- [Any strategies that degraded heavily on OOS?]
- [Any surprising wins/failures?]
- [Recommended ensemble configuration]

## Next Step
Proceed to Phase 3: Paper Trading Deployment
```

**Success Criteria:**
- ✓ All 25 strategies have WFO results
- ✓ Tier assignments made and documented
- ✓ Final configuration matrix updated
- ✓ Ready for paper trading deployment

---

## 🧪 PHASE 3: PAPER TRADING DEPLOYMENT (2–4 weeks)

**Status:** ⏳ Queued (After Phase 2)  
**Objective:** Validate Tier-1 ensemble in live market conditions

### TASK 3.0: Deploy Tier-1 Ensemble to Paper Trading
**Time:** 2 hours

**What to Deploy:**
- All TIER 1 strategies (expected 8–12 strategies)
- Risk per trade: 2.0% account balance
- Max concurrent positions: 5 across all strategies
- Update config/config.yaml to enable all TIER 1 strategies

**Steps:**
1. Update config/config.yaml active_strategies list
2. Verify all required strategies are imported in scripts/run_paper.py
3. Start paper trading engine:
   ```bash
   python scripts/run_paper.py --mode paper --verbose
   ```

---

### TASK 3.1: Monitor Live Signal Generation (Week 1–2)
**Time:** Continuous (2+ hours per week)

**Weekly Checks:**
- [ ] No error loops or stale signals
- [ ] Orders execute cleanly
- [ ] Telegram notifications work
- [ ] P&L tracking is accurate
- [ ] No positions exceed max concurrent limit
- [ ] Correlations between strategies stay <0.6

**Report:** Create paper_trading_week1_summary.txt

---

### TASK 3.2: Stress Test (Week 2–3)
**Time:** Observation + logging

**Stress Test Scenarios:**
- [ ] Market gaps (verify order handling)
- [ ] Low liquidity periods
- [ ] News announcements (high volatility)
- [ ] Weekend crypto trading
- [ ] Drawdown management (<15% threshold)

**Log:** paper_trading_week2_summary.txt

---

### TASK 3.3: Final Paper Trading Report (Week 4)
**Time:** 2 hours

**Output:** phase_3_paper_trading_final_report.md

**Content:**
```
# Phase 3 — Paper Trading Final Report

## Performance Summary
- Total Trades: [X]
- Win Rate: [X]%
- Total P&L: $[X]
- Sharpe Ratio: [X]
- Max Drawdown: [X]%

## Strategy Performance Breakdown
| Strategy | Trades | WR | PnL | Notes |
|----------|--------|----|----|--------|
| Range Breakout | 8 | 62% | +$450 | Solid, as expected |
...

## Issues Encountered
- [Any problems?]
- [Fixes applied?]
- [Ready for live trading?]

## Recommendations
- [Are all TIER 1 strategies performing as expected?]
- [Any exclusions or adjustments needed?]
- [Risk management holding up?]
- [Go / No-Go for LIVE TRADING?]
```

**Success Criteria for Go-Live:**
- ✓ No error loops or crashes
- ✓ P&L within 20% of backtest expectations
- ✓ Max drawdown < 15%
- ✓ All regulatory requirements met
- ✓ No correlation above 0.6 between strategies
- ✓ Data freshness maintained
- ✓ Telegram notifications working

---

## 📋 ADDITIONAL SUPPORT TASKS

### TASK A.0: Create Master Strategy Documentation
**Time:** 2 hours  
**Output:** All 25 strategies documented in a single reference file

**Content:**
```
# All 25 Strategies — Master Reference

## Existing Strategies (10)
1. Range Breakout — Breakout strategy on consolidation zones
...

## New LeoDeX V2 Strategies (15)
1. Institutional Silver Bullet — SMC-based institutional entry
...

Each entry should include:
- Entry logic (1–2 paragraphs)
- Assets & timeframes
- Expected win rate & R:R
- Key parameters
- Special considerations
```

---

### TASK A.1: Create Test Results Archive
**Time:** 1 hour  
**Purpose:** Preserve all backtest/WFO results for future reference

**Files to Archive:**
- All backtest results (Phase 1A & 1B)
- Walk-forward validation results (Phase 2)
- Paper trading logs (Phase 3)
- Configuration snapshots at each phase

**Location:** `results/phase1a_backtest_results/`, etc.

---

### TASK A.2: Update MASTER_PROJECT_STATUS.md
**Time:** 2 hours  
**When:** After each phase completion

**Update with:**
- Current phase completion %
- Key findings
- Any blockers or decisions
- Timeline adjustments

---

## ✅ FINAL CHECKLIST

### Phase 0 Complete
- [ ] Signal deduplication working
- [ ] Order validation in place
- [ ] Data freshness monitored
- [ ] All symbols in market watch
- [ ] Bot stable for 5+ minutes

### Phase 1A Complete
- [ ] All 10 existing strategies backtested
- [ ] Tier assignments made
- [ ] Baseline performance documented

### Phase 1B Complete
- [ ] All 15 new strategies implemented
- [ ] All 15 backtested
- [ ] Quick-win strategies identified
- [ ] No critical errors in any strategy

### Phase 2 Complete
- [ ] Walk-forward validation complete (all 25)
- [ ] Final tier assignments
- [ ] Configuration updated
- [ ] Ready for paper trading

### Phase 3 Complete
- [ ] 2–4 weeks of live paper trading data
- [ ] P&L matches expectations
- [ ] Risk limits maintained
- [ ] Go/No-Go decision for live trading

---

## 🎯 SUCCESS METRICS

| Metric | Target | Status |
|--------|--------|--------|
| **Phase 0 Completion** | 1–2 hours | ⏳ Pending |
| **Phase 1A Completion** | 6–8 hours | ⏳ Pending |
| **Phase 1B Completion** | 12–16 hours | ⏳ Pending |
| **Phase 2 Completion** | 8–10 hours | ⏳ Pending |
| **Tier-1 Strategies** | 8–12 strategies | ⏳ Pending |
| **Aggregate Win Rate** | 55–65% | ⏳ Pending |
| **Aggregate Profit Factor** | 1.60–1.75 | ⏳ Pending |
| **Win Rate Improvement** | +10% min | ⏳ Target |
| **Phase 3 Duration** | 2–4 weeks | ⏳ Pending |
| **Live Trading Ready** | 4–6 weeks | ⏳ Target |

---

## 📞 SUPPORT & ESCALATION

**If Stuck:**
1. Check the **STRATEGY_INTEGRATION_&_TESTING_PLAN.md** for overall strategy
2. Check **CONFIG_UPDATE_CHECKLIST.md** for config requirements
3. Check **DIAGNOSTIC_REPORT.md** for Phase 0 fixes
4. Review **PATH_B_IMPLEMENTATION.md** for enhancement context

**Questions?**
- Strategy logic: Check uploaded `stragy_prompts_2.txt`
- Config structure: Review `config/strategies.yaml` examples
- Backtest parameters: Review `config/config.yaml` backtesting section
- Error messages: Check `forward_test/` and `mt5_bridge/` logs

---

**Next Step:** Get approval to proceed with Phase 0 emergency fixes, then execute Phase 1A–3 sequentially.

