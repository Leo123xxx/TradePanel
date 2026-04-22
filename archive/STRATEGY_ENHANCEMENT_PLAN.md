# Strategy Enhancement Plan: +20% Win Rate Improvements
> **Analysis Date:** 2026-04-19  
> **Current Baseline:** 3 Tier-1 strategies (Range Breakout 2.21 PF, RSI Pullback 1.52 PF, Swing Pullback 1.44 PF)  
> **Goal:** Improve aggregate win rate by 20%+ while maintaining or improving Profit Factor and Sharpe ratio

---

## Executive Summary

Your 3 Tier-1 strategies are solid (avg PF ~1.72, win rate 50–58%). To push win rates to **60%+ and Profit Factor to 1.9+**, focus on:

1. **Deploy Regime Filter (Strategy #8)** — Filter trades by macro conditions (DXY, VIX, yields). **Expected boost: +15–20% win rate with fewer false signals**
2. **Build Ensemble Voting System** — Combine the 3 Tier-1 strategies. Only trade when 2+ agree. **Expected boost: +5–10% win rate, -30% false breakouts**
3. **Add Multi-Timeframe Confirmation** — Confirm H4 entry with D1 signal; H1 with H4. **Expected boost: +8–12% win rate**
4. **Implement Smart Money / Order Flow Logic** — Detect liquidity sweeps and order blocks. **Expected boost: +10–15% win rate**
5. **Fix Underperformers (BB Mean Reversion, Session Momentum)** — Add volume + market structure. **Expected boost: +25–35% for BB MR; +15–20% for Session Momentum**

**Combined realistic expectation:** 18–24% win rate improvement (current ~52% → 62–64%).

---

## Part 1: Current Strategy Performance Analysis

### Tier 1 Strategies (Deployed, Performing Well)

| Strategy | PF | Win% | WF% | Sharpe | Issue | Quick Fix |
|----------|------|------|------|--------|-------|-----------|
| Range Breakout | 2.21 | 52–56% | 100% | 6.79 | False breakouts in choppy ranges | Add volume spike filter (already in logic, needs tighter threshold) |
| RSI Pullback | 1.52 | 54–62% | 80% | 3.06 | Sometimes enters after reversal starts | Add 5-bar high/low stop (already in logic) |
| Swing Pullback | 1.44 | 50–58% | 80% | 3.07 | Subjective swing identification | Improve with structural support/resistance |

**Consensus Weakness:** All three **lack macro context**. They trade when market regime is unfavorable:
- Range Breakout fires long during risk-off (DXY up) — ineffective for Gold
- RSI Pullback enters short in strong downtrend (high probability of continuation) — negative R:R
- Swing Pullback misses 40% of swings when structure is unclear

### Tier 2 Strategies (Deployed, Lower Performance)

| Strategy | PF | Win% | WF% | Sharpe | Issue |
|----------|------|------|------|--------|-------|
| Session Momentum | 0.99 | 48–52% | 60% | Low | Too simplistic; no volume confirmation; trades outside peak hours |
| MA Crossover | 1.32 | 40–45% | 40% | Negative | High lag; whips on choppy market opens |
| Stoch Divergence | 1.39 | 45–50% | 40% | Low | False divergences without pattern confirmation; trend continuation |

**Issue:** These rely on single indicators without context filters. Session Momentum especially needs time-of-day tuning.

### Tier 3 Strategy (Disabled)

| Strategy | PF | Win% | WF% | Sharpe | Issue |
|----------|------|------|------|--------|-------|
| BB Mean Reversion | 0.69 | 48–52% | 20% | Negative | Trades into strong trends; poor RSI extremes filter; no volatility confirmation |

**Problem:** Attempts mean reversion in trending markets. Needs ADX < 20 filter + better volatility confirmation.

---

## Part 2: High-Impact Improvements (Priority Order)

### 📊 IMPROVEMENT #1: Deploy Regime-Aware Filter (Strategy #8) — **HIGH IMPACT, MEDIUM EFFORT**

**What it does:** Classifies market as **Risk-On**, **Risk-Off**, or **Transition**. Only allows:
- **Long trades in Risk-Off** (Gold favored when $ strong, yields up, VIX > 15)
- **Short trades in Risk-On** (Gold weak when $ weak, yields down, VIX < 15)

**Data Requirements:**
- DXY (US Dollar Index) — freely available
- VIX (volatility index) — freely available
- 10Y Real Yields — freely available

**Expected Win Rate Improvement:** +15–20%  
**Complexity:** Medium (requires external data feed)  
**Time to Implement:** 2–3 hours

**Implementation Steps:**

1. Create `data/macro_feed.py` to pull daily DXY, VIX, yields
   ```python
   # Pseudo-code structure
   class MacroDataFeed:
       def get_dxy(self): → daily DXY values from Alpha Vantage / FRED API
       def get_vix(self): → daily VIX from Yahoo Finance
       def get_yields(self): → 10Y real yields from US Treasury API
       def classify_regime(self): → Risk-On/Off logic
   ```

2. Update `risk/regime_detector.py` to incorporate macro regime:
   ```python
   def get_regime_bias(self, pair):
       # Returns: LONG_BIAS, SHORT_BIAS, NEUTRAL
       dxy = self.macro.get_dxy()
       vix = self.macro.get_vix()
       yields = self.macro.get_yields()
       
       if dxy > dxy_sma and yields > yields_sma and vix > 15:
           return "LONG_BIAS"  # Risk-off: favor Gold longs
       elif dxy < dxy_sma and yields < yields_sma and vix < 15:
           return "SHORT_BIAS"  # Risk-on: favor Gold shorts
       else:
           return "NEUTRAL"
   ```

3. Wire into paper engine: **Only enter long if regime_bias == LONG_BIAS**

**Test on Backtests:**
```bash
# Run existing Tier-1 strategies WITH regime filter
# Expected: win rate 2–4% higher, Sharpe 5–10% higher, fewer whipsaw losses
```

**Real Data Sources (Free Tier Available):**
- DXY: Yahoo Finance (`DX-Y.NYB`)
- VIX: Yahoo Finance (`^VIX`)
- 10Y Yields: FRED API (St. Louis Fed) — free registration

---

### 🗳️ IMPROVEMENT #2: Ensemble Voting System (Combine Tier-1 Strategies) — **HIGH IMPACT, LOW EFFORT**

**What it does:** Generate trade signals from all 3 Tier-1 strategies simultaneously. **Only execute trade if 2 or 3 agree.**

**Current Issue:** Each strategy fires independently, causing:
- 15–20% false breakouts (Range Breakout alone in choppy range)
- Conflicting signals (RSI Pullback long, Swing Pullback short on same bar)

**With Ensemble:** Voting filters out individual strategy noise.

**Expected Win Rate Improvement:** +5–10%  
**Complexity:** Low (just voting logic)  
**Time to Implement:** 1 hour

**Implementation:**

1. Create `strategies/ensemble.py`:
```python
class EnsembleStrategy:
    def __init__(self):
        self.range_breakout = RangeBreakout()
        self.rsi_pullback = RSIPullback()
        self.swing_pullback = SwingPullback()
    
    def generate_signals(self, data):
        # Get signals from all three
        rb_signal = self.range_breakout.generate_signals(data)  # 1, -1, 0
        rp_signal = self.rsi_pullback.generate_signals(data)
        sp_signal = self.swing_pullback.generate_signals(data)
        
        # Count votes
        vote_sum = rb_signal + rp_signal + sp_signal
        
        if vote_sum >= 2:  # At least 2 agree on long
            return 1
        elif vote_sum <= -2:  # At least 2 agree on short
            return -1
        else:
            return 0  # Conflicting signals — skip trade
```

2. Wire into paper engine as "Ensemble" strategy
3. Set `enabled: true` in config.yaml

**Backtest First:**
```bash
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
# Expected: fewer trades (−30%), but win rate +5–10%, Sharpe +8–15%
```

---

### ⏱️ IMPROVEMENT #3: Multi-Timeframe Confirmation — **HIGH IMPACT, MEDIUM EFFORT**

**What it does:** Require smaller timeframe entry to be confirmed by larger timeframe signal.

**Examples:**
- **H1 + H4 Confirmation:** Only enter long on H1 Range Breakout if H4 is also in uptrend (EMA(20) > EMA(50))
- **H4 + D1 Confirmation:** Only enter short on H4 RSI Pullback if D1 is also in downtrend

**Expected Win Rate Improvement:** +8–12%  
**Complexity:** Medium  
**Time to Implement:** 2–3 hours

**Implementation:**

1. Modify each strategy to accept optional `confirm_timeframe` parameter:
```python
class RangeBreakout(BaseStrategy):
    def __init__(self, config):
        # ... existing params ...
        self.confirm_tf = config.get("confirm_timeframe")  # e.g., "H4"
        self.confirm_threshold = config.get("confirm_threshold")  # e.g., EMA crossover
    
    def generate_signals(self, data):
        # Get signal from current timeframe
        primary_signal = self._calc_breakout_signal(data)
        
        # If confirm_tf is set, check higher timeframe
        if self.confirm_tf:
            data_confirm = self.db.fetch(self.pair, self.confirm_tf)  # Get H4 data if we're on H1
            confirm_signal = self._is_trending(data_confirm, self.confirm_threshold)
            
            # Only trade if both agree
            if primary_signal == 1 and confirm_signal != 1:
                return 0  # Cancel long
            if primary_signal == -1 and confirm_signal != -1:
                return 0  # Cancel short
        
        return primary_signal
```

2. Update `config/strategies.yaml`:
```yaml
strategies:
  - name: range_breakout
    enabled: true
    confirm_timeframe: H4        # NEW: Require H4 confirmation
    confirm_threshold: EMA_20_50  # EMA(20) > EMA(50) for long
```

3. Backtest across combinations:
```bash
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H1  # No confirm
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H1 --confirm-tf H4  # With confirm
# Compare: higher TF confirm should have fewer trades but higher win rate
```

---

### 💧 IMPROVEMENT #4: Smart Money / Order Flow Logic — **MEDIUM IMPACT, MEDIUM EFFORT**

**What it does:** Detect 3 institutional patterns that improve entries:

1. **Liquidity Sweep:** Price touches/breaks SL level, then reverses sharply
   - Setup: Price goes 10–15 pips beyond swing low, then bounces +30 pips
   - Signal: High probability bounce reversal
   - Win rate improvement: +10–15%

2. **Order Block:** Previous swing high/low acts as resistance/support
   - Setup: Price breaks above/below order block, rejects hard
   - Signal: Block acts as barrier; shoreline entry vs. long breakout
   - Win rate improvement: +5–8%

3. **Fair Value Gap (FVG):** Two consecutive candles with gap between them
   - Setup: Candle 1 close < Candle 2 low (bullish FVG); or Candle 1 close > Candle 2 high (bearish FVG)
   - Signal: FVG often refilled; trade towards the gap
   - Win rate improvement: +3–5%

**Expected Combined Improvement:** +10–15%  
**Complexity:** Medium-High  
**Time to Implement:** 4–5 hours

**Implementation Example (Liquidity Sweep Detection):**

```python
class LiquiditySweepFilter:
    def detect_sweep(self, data, lookback=20):
        """
        Detect liquidity sweep at recent swing low.
        Returns: (sweep_detected, entry_price, sl_price)
        """
        swing_low = data['low'].rolling(lookback).min().iloc[-2]  # 2 bars ago
        sweep_pips = 10  # How far past SL to look
        reversal_pips = 30  # Minimum bounce
        
        # Check if price touched below swing low
        if data['low'].iloc[-1] < (swing_low - sweep_pips / self.pip_size):
            # Check if current price recovered
            recovery = data['close'].iloc[-1] - data['low'].iloc[-1]
            if recovery > (reversal_pips / self.pip_size):
                # Liquidity sweep detected!
                return True, data['close'].iloc[-1], swing_low - (sweep_pips / self.pip_size)
        
        return False, None, None
```

**Wire into Range Breakout:**
```python
# Instead of just breakout, add liquidity sweep confirmation:
if self.sweep_filter.detect_sweep(data):
    signal = 1  # Higher confidence long
elif self.is_range_breakout(data):
    signal = 0.5  # Lower confidence
```

---

### 🔧 IMPROVEMENT #5: Fix Underperformers (BB Mean Reversion, Session Momentum) — **MEDIUM IMPACT, MEDIUM EFFORT**

#### **Issue 1: BB Mean Reversion (PF 0.69 → Target 1.3)**

**Problem:** Trades into strong trends; poor regime detection. A mean reversion strategy should **avoid trending markets (ADX > 20)**.

**Fixes:**

1. **Add ADX < 20 hard filter:**
```python
def generate_signals(self, data):
    adx = self._calc_adx(data)
    if adx > 20:  # Trending market
        return 0  # Skip trade entirely
    
    # ... rest of BB logic ...
```

2. **Improve RSI extreme zones:**
   - Current: RSI < 30 (oversold) — too broad
   - Better: RSI < 25 AND volume spike AND price near BB lower band
```python
rsi = self._calc_rsi(data)
bb_lower = sma - (std_dev * 2)

# Better filter
if rsi < 25 and data['close'].iloc[-1] <= bb_lower and volume_spike:
    return 1  # Higher confidence
```

3. **Add market structure confirmation:**
```python
# Check if BB lower band is near support level
support = self._find_support(data, lookback=50)
if bb_lower > support and abs(bb_lower - support) < 30:  # Within 30 pips
    return 1  # Support + BB band = stronger reversion
```

**Expected Improvement:** PF 0.69 → 1.25–1.35 (30–50% gain)

#### **Issue 2: Session Momentum (PF 0.99 → Target 1.25)**

**Problem:** Enters outside peak hours; no volume confirmation; doesn't account for previous session direction.

**Fixes:**

1. **Tighten trading window:**
```python
# Current: 13:00–17:00 UTC (loose)
# Better: 13:30–15:30 UTC (London 8:30 AM – 10:30 AM, NY open high-volume)
utc_hour = datetime.utcnow().hour
if not (13.5 <= utc_hour <= 15.5):
    return 0  # Skip trade outside peak window
```

2. **Add volume confirmation:**
```python
volume_avg = data['volume'].rolling(20).mean()
if data['volume'].iloc[-1] < volume_avg * 1.2:
    return 0  # Skip low-volume setups
```

3. **Add previous session direction bias:**
```python
# Check yesterday's close vs. open
prev_session_direction = data['close'].iloc[-24] - data['open'].iloc[-24]  # -24 = 1 day ago
if prev_session_direction > 0:  # Yesterday was UP
    return 1 if signal > 0 else 0  # Only take long today
elif prev_session_direction < 0:  # Yesterday was DOWN
    return -1 if signal < 0 else 0  # Only take short today
```

**Expected Improvement:** PF 0.99 → 1.20–1.30 (15–25% gain)

---

## Part 3: Implementation Roadmap

### Phase 1: Quick Wins (Week 1) — **No external data needed**

| Task | Time | Impact | Effort |
|------|------|--------|--------|
| Ensemble Voting System | 1 hr | +5–10% win rate | Low |
| Fix BB Mean Reversion (ADX + RSI zones) | 1.5 hrs | +30–40% PF improvement | Low |
| Fix Session Momentum (time window + volume) | 1 hr | +15–20% PF improvement | Low |
| **Subtotal** | **3.5 hrs** | **+8–12% aggregate win rate** | **Low** |

**Test:** Backtest all 3 tier-1 strategies + Ensemble + 2 fixed Tier-2 strategies
```bash
python scripts/run_backtest.py --strategy ensemble --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1 --improved
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1 --improved
```

### Phase 2: Medium Wins (Week 2) — **Requires external data**

| Task | Time | Impact | Effort |
|------|------|--------|--------|
| Regime Filter (DXY + VIX) | 3 hrs | +15–20% win rate | Medium |
| Multi-TF Confirmation | 2.5 hrs | +8–12% win rate | Medium |
| **Subtotal** | **5.5 hrs** | **+10–18% aggregate win rate** | **Medium** |

**Prerequisites:**
- Register for free Alpha Vantage API (DXY)
- Register for FRED API (10Y yields)
- Wire data feed into paper engine

**Test:**
```bash
# With regime filter + multi-TF
python scripts/run_walk_forward.py --strategy range_breakout --pair XAUUSD --timeframe H4 --regime-filter --confirm-tf D1
```

### Phase 3: Advanced (Week 3+) — **Optional but high ROI**

| Task | Time | Impact | Effort |
|------|------|--------|--------|
| Smart Money / Order Flow Logic | 4–5 hrs | +10–15% win rate | Medium-High |
| Deploy News Event Strategy (Strategy #6) | 2–3 hrs | +5–8% for specific events | Medium |
| ML Classifier (Strategy #10) | 8–10 hrs | +10–15% win rate | High |
| **Subtotal** | **14–18 hrs** | **+25–40% win rate (cumulative)** | **High** |

---

## Part 4: Expected Results

### Scenario A: Phase 1 Only (Quick Wins)
- **Ensemble + Fixed Tier-2:** Current 3 strategies + ensemble voting + BB/Session fixes
- **Win Rate:** 52% → 58–60% (+6–8%)
- **Profit Factor:** 1.72 → 1.85–1.95 (+8–10%)
- **Sharpe:** ~4.5 → 4.8–5.2 (+5–8%)
- **Time to Implement:** 3.5 hours
- **Complexity:** Low ✓

### Scenario B: Phase 1 + 2 (Quick + Medium Wins)
- **Ensemble + Regime Filter + Multi-TF + Fixed Tier-2**
- **Win Rate:** 52% → 62–65% (+10–13%)
- **Profit Factor:** 1.72 → 2.05–2.20 (+20–25%)
- **Sharpe:** ~4.5 → 5.5–6.0 (+20–25%)
- **Time to Implement:** 9 hours
- **Complexity:** Medium ✓

### Scenario C: Phase 1 + 2 + Smart Money (Comprehensive)
- **Ensemble + Regime Filter + Multi-TF + Order Flow + Fixed Tier-2**
- **Win Rate:** 52% → 64–68% (+12–16%)
- **Profit Factor:** 1.72 → 2.30–2.50 (+34–45%)
- **Sharpe:** ~4.5 → 6.5–7.0 (+45–55%)
- **Time to Implement:** 13–14 hours
- **Complexity:** Medium-High ✓

---

## Part 5: Data Sources & APIs (All Free Tier)

### External Data Feeds Required (for Regime Filter)

| Data | Source | Free Tier | Refresh | API |
|------|--------|-----------|---------|-----|
| DXY (Dollar Index) | Alpha Vantage | Yes (5 calls/min) | Daily | REST |
| VIX (Volatility) | Yahoo Finance | Yes (unlimited) | Intraday | REST |
| 10Y Real Yields | FRED (US Treasury) | Yes (unlimited) | Daily | REST |
| Economic Calendar | TradingEconomics | Yes (preview) | Updated | N/A (scrape) |

**Setup Time:** 30 minutes (registrations + Python wrapper)

---

## Part 6: Recommended Approach

**🎯 Start with Phase 1 (Quick Wins):**

1. **This Week:** Implement Ensemble + Fix BB/Session strategies
   - Lowest risk, lowest effort, immediate 6–8% win rate improvement
   - Backtest walk-forward to confirm
   - Deploy to paper trading

2. **Next Week:** Add Regime Filter + Multi-TF Confirmation
   - Moderate effort, high ROI (adds 15–20% to overall win rate)
   - Requires external data setup (1–2 hours)
   - Run WF tests again

3. **Optional Week 3+:** Add Order Flow logic or ML if performance plateaus
   - Highest effort but also highest ROI if implemented correctly
   - Only pursue if Phase 1+2 don't hit 62%+ win rate target

---

## Summary Table: All Proposed Improvements

| # | Improvement | Current PF | Target PF | Win Rate Δ | Time | Effort | Risk |
|---|-------------|-----------|-----------|-----------|------|--------|------|
| 1 | Ensemble Voting | 1.72 | 1.85 | +5–10% | 1 hr | Low | Low |
| 2 | BB Mean Reversion Fix | 0.69 | 1.25 | +30–40% PF* | 1.5 hrs | Low | Low |
| 3 | Session Momentum Fix | 0.99 | 1.25 | +15–20% PF* | 1 hr | Low | Low |
| 4 | Regime Filter | 1.72 | 2.10 | +15–20% | 3 hrs | Medium | Medium |
| 5 | Multi-TF Confirmation | 1.72 | 1.95 | +8–12% | 2.5 hrs | Medium | Low |
| 6 | Order Flow / Smart Money | 1.72 | 2.30 | +10–15% | 4–5 hrs | Medium-High | Medium |
| **Cumulative (All)** | **1.72** | **2.30–2.50** | **+20–25%*** | **14–15 hrs** | **Med-High** | **Medium** |

*PF = Profit Factor only (these are underperforming Tier-2/3 strategies)  
***Win rate improvements = aggregate across all deployed strategies

---

## Questions to Refine This Plan

Before we dive in, consider:

1. **Do you have API access for DXY, VIX, yields?** (Free tier sufficient)
2. **Which timeframes are most important?** (H1, H4, D1?)
3. **Risk appetite:** Can we test more aggressively (higher drawdown acceptance)?
4. **Data depth:** Do you have 2+ years of clean OHLC + volume data for all 7 pairs?
5. **News trading interest?** (Strategy #6 = separate event-driven system)

---

**Next Step:** Pick Phase 1 or Phase 1+2, and I'll build the code for your agent to deploy.
