# 🎯 STRATEGY INTEGRATION & TESTING PLAN
**Project: TradePanel LeoDeX V2 Integration**  
**Date Created:** 2026-04-20  
**Status:** Planning Phase  
**Total Strategies:** 25 (10 Existing + 15 New LeoDeX V2)  
**Goal:** +10% success rate improvement through comprehensive testing & validation

---

## 📊 EXECUTIVE SUMMARY

This document outlines a structured approach to integrating and testing 15 new LeoDeX V2 strategies alongside 10 existing strategies. The plan prioritizes:

1. **Phase 0:** Emergency bot stabilization (4 critical fixes)
2. **Phase 1A:** Test existing 10 strategies in backtesting framework
3. **Phase 1B:** Implement & test 15 new LeoDeX V2 strategies
4. **Phase 2:** Strategy tier assignment based on walk-forward validation
5. **Phase 3:** Resume paper trading with validated strategy suite
6. **Target:** 10%+ success rate boost across the complete strategy portfolio

**Total Estimated Time:** 3–4 weeks (Phase 0–2), then 2–4 weeks demo run

---

## 🔴 PHASE 0: EMERGENCY BOT STABILIZATION (1–2 hours)

**Status:** 🔴 BLOCKING — Must complete before strategy testing  
**Blocker:** Live bot in retry loop due to stale signals + order validation  

### Critical Fixes Required

| # | Issue | File | Fix | Time |
|---|-------|------|-----|------|
| 1 | Stale signal repetition | `forward_test/paper_engine.py` | Track attempted signals by timestamp | 30 min |
| 2 | Order validation missing | `mt5_bridge/order_manager.py` | Validate symbol/lot/liquidity | 20 min |
| 3 | Data freshness unchecked | `forward_test/signal_checker.py` | Warn if data > timeframe old | 15 min |
| 4 | No market watch setup | `mt5_bridge/connector.py` | Add symbols to market watch on connect | 15 min |

**Success Criteria:**
- ✅ Same signal not repeated on same bar
- ✅ Orders execute OR fail with clear error (not return None)
- ✅ No infinite retry loop
- ✅ All symbols in MT5 market watch
- ✅ Bot runs stable for >5 minutes without error spam

**After Phase 0 Complete:** Proceed to Phase 1A

---

## 📈 PHASE 1A: EXISTING STRATEGY VALIDATION (6–8 hours)

**Status:** ⏳ Queued (Blocked by Phase 0)  
**Objective:** Baseline all 10 existing strategies before adding new ones

### Existing Strategies to Validate

| # | Strategy | Category | Status | Pair(s) | TF | Expected PF | Priority |
|---|----------|----------|--------|---------|----|-----------  |----------|
| 1 | Range Breakout | Breakout | Implemented | XAUUSD, EURUSD, GBPUSD | H4, D1 | ~1.44 | TIER 1 |
| 2 | RSI Pullback | Hybrid | Implemented | XAUUSD, EURUSD, USDJPY | H4, D1 | ~1.52 | TIER 1 |
| 3 | Swing Pullback | Price Action | Implemented | XAUUSD, GBPUSD | H4, D1 | ~2.21 | TIER 1 |
| 4 | EMA Ribbon Trend | Trend Following | Implemented | BTCUSD, ETHUSD, XAUUSD | H4, D1 | ~1.8 | TIER 1 (Crypto) |
| 5 | Crypto RSI Extremes | Mean Reversion | Implemented | BTCUSD, ETHUSD, XAUUSD | H4, D1 | ~1.6 | TIER 1 (Crypto) |
| 6 | MA Crossover | Trend Following | Implemented | XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD | H1, H4, D1 | ~1.2 | TIER 2 |
| 7 | RSI Bounce | Mean Reversion | Implemented | XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD | M15, H1 | ~1.3 | TIER 2 |
| 8 | Session Momentum | Session-Based | Implemented | XAUUSD, GBPUSD, EURUSD | H1 | ~1.4 | TIER 2 |
| 9 | Stoch Divergence | Divergence | Implemented | XAUUSD, EURUSD, USDJPY | H4, D1 | ~1.25 | TIER 2 |
| 10 | Volatility Squeeze Breakout | Breakout | Implemented | BTCUSD, ETHUSD, XAUUSD | H4, D1 | ~1.5 | TIER 2 |

### Phase 1A Execution Plan

**STEP 1A-1: Run Full Backtest Suite (Existing Strategies)**
```bash
# Test each Tier-1 strategy on primary pairs
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4

# Test crypto strategies
python scripts/run_backtest.py --strategy ema_ribbon_trend --pair BTCUSD --timeframe H4
python scripts/run_backtest.py --strategy crypto_rsi_extremes --pair BTCUSD --timeframe H4

# Expected: Win rates 50–80%, Profit factors 1.2–2.2+
```

**STEP 1A-2: Walk-Forward Validation (Each Strategy)**
- Split data: 70% IS / 20% OOS / 10% FWD
- Verify profit factors don't degrade on OOS/FWD
- Flag any strategies with PF < 1.0 or win rate < 45%

**STEP 1A-3: Tier Assignment**
- **TIER 1 (Keep):** PF ≥ 1.3, Win Rate ≥ 50%, Stable across OOS/FWD
- **TIER 2 (Monitor):** PF 1.1–1.29, Acceptable but less stable
- **TIER 3 (Exclude):** PF < 1.1 or Win Rate < 45%

**Expected Outcome:**
- Confirm existing Tier-1 strategies
- Identify any that should be excluded
- Baseline performance before integrating new strategies

---

## 🚀 PHASE 1B: LEDEDX V2 STRATEGY IMPLEMENTATION (12–16 hours)

**Status:** ⏳ Queued (After Phase 1A)  
**Objective:** Integrate, implement, and validate 15 new LeoDeX V2 strategies

### 15 New LeoDeX V2 Strategies

#### Group 1: Institutional Flow Strategies (3 strategies) — 6 hours

| # | Strategy | Entry Logic | Assets | TF | Expected WR | Priority |
|---|----------|-------------|--------|----|-----------  |----------|
| 1 | **Institutional Silver Bullet (SMC)** | Liquidity sweep + MSS + FVG retracement | XAUUSD, GBPUSD, EURUSD | M15/M5 | 60–68% | QUICK WIN |
| 2 | **ICT Judas Swing** | Fake breakout trap + 1min CHoCH | GBPUSD, EURUSD | M15 | 62–68% | QUICK WIN |
| 3 | **Turtle Soup Liquidity Sweep** | Old levels swept + retail stops triggered + close retest | XAUUSD, BTCUSD | M15, H1 | 60–65% | QUICK WIN |

**Implementation Time:** 2 hours each (total 6h)  
**Key Concepts:** Market structure, liquidity pools, order blocks, fair value gaps  
**Success Metric:** >60% win rate, >3:1 avg RR

---

#### Group 2: Trend Following & Momentum (3 strategies) — 5 hours

| # | Strategy | Entry Logic | Assets | TF | Expected WR | Priority |
|---|----------|-------------|--------|----|-----------  |----------|
| 4 | **Dual EMA Momentum Continuity** | Fast EMA cross Slow + ADX>25 + engulfing | BTCUSD, ETHUSD, EURUSD | H1, H4 | 45–55% | MEDIUM |
| 5 | **Triple MACD Momentum Scalping** | Layer alignment (C→B→A) + zero-line cross | XAUUSD, BTCUSD | M5 | 55–62% | MEDIUM |
| 6 | **Dual EMA Fractal Breaker** | Price > 200 EMA + Bill Williams fractal breakout | USDJPY, EURUSD | H1 | 48–54% | MEDIUM |

**Implementation Time:** 1.5–2 hours each (total 5h)  
**Key Concepts:** EMA ribbons, MACD divergence, Bill Williams fractals  
**Success Metric:** >45% win rate, >2.5:1 avg RR

---

#### Group 3: Mean Reversion & Countertrend (3 strategies) — 5 hours

| # | Strategy | Entry Logic | Assets | TF | Expected WR | Priority |
|---|----------|-------------|--------|----|-----------  |----------|
| 7 | **Extreme Mean Reversion (RSI-2)** | Price > 200SMA + RSI<10 + below Lower BB | EURUSD, USDJPY | D1, H4 | 68–75% | QUICK WIN |
| 8 | **VWAP Momentum Shift** | Price deviates from VWAP 2σ + reversal pattern | ETHUSD, XAGUSD | M15, M30 | 60–65% | QUICK WIN |
| 9 | **Hikkake Inside Bar Trap** | Inside bar formed + price breaks out + reverses within 3 candles | BTCUSD, ETHUSD | H4, D1 | 55–60% | MEDIUM |

**Implementation Time:** 1.5–2 hours each (total 5h)  
**Key Concepts:** RSI extremes, Bollinger Bands, VWAP, price action patterns  
**Success Metric:** >55% win rate, >2.0:1 avg RR

---

#### Group 4: Breakout & Session-Based (3 strategies) — 4 hours

| # | Strategy | Entry Logic | Assets | TF | Expected WR | Priority |
|---|----------|-------------|--------|----|-----------  |----------|
| 10 | **Opening Range Breakout (ORB)** | Define opening hour range + close outside + retest entry | GBPUSD, EURUSD | M15 | 50–56% | QUICK WIN |
| 11 | **RVGI-CCI-SMA Confluence** | RVGI cross up + CCI >-100 + Price below SMA30 | GBPUSD, USDJPY | H1 | 52–58% | MEDIUM |
| 12 | **Volatility Contraction Breakout** | 3–4 days decreasing range + high-volume breakout | USDJPY, ETHUSD | D1 | 40–50% | LOWER |

**Implementation Time:** 1–1.5 hours each (total 4h)  
**Key Concepts:** Session times, opening ranges, volume analysis, volatility metrics  
**Success Metric:** >45% win rate, >2.5:1 avg RR

---

#### Group 5: Advanced & Statistical (3 strategies) — 3 hours

| # | Strategy | Entry Logic | Assets | TF | Expected WR | Priority |
|---|----------|-------------|--------|----|-----------  |----------|
| 13 | **Statistical Arbitrage Spread (XAU/XAG)** | Z-Score XAU/XAG > 2.0 (gold overpriced) + mean reversion | XAUUSD vs XAGUSD | H4, D1 | 70–80% | QUICK WIN |
| 14 | **Naked Price Action (Engulfing)** | Strip indicators + D1 S/R + massive engulfing rejection | EURUSD, GBPUSD, XAUUSD | D1, H4 | 50–55% | MEDIUM |
| 15 | **COT Sentiment Swing** | Commercial hedging extreme (COT) + D1 break of structure | XAUUSD, XAGUSD, USDJPY | Weekly/D1 | 40–48% | MEDIUM |

**Implementation Time:** 1 hour each (total 3h)  
**Key Concepts:** Correlation, COT data, price action, mean reversion  
**Success Metric:** Varies by strategy; arbitrage should have PF > 1.6

---

### Phase 1B Execution Plan

**STEP 1B-1: Implement Group 1 (Institutional Flow) — 6 hours**
- Institutional Silver Bullet: Create entry/exit logic for liquidity sweeps + FVG
- ICT Judas Swing: Implement Asian range consolidation + fake breakout detection
- Turtle Soup Liquidity Sweep: Identify old liquidity levels + sweep detection
- Backtest each: Expected >60% win rate on primary pairs

**STEP 1B-2: Implement Group 2 (Trend/Momentum) — 5 hours**
- Dual EMA Momentum: Fast/slow EMA crossover + ADX + engulfing confirmation
- Triple MACD Momentum Scalping: Multi-layer MACD alignment detection
- Dual EMA Fractal Breaker: Bill Williams fractal implementation
- Backtest each: Expected >45% win rate

**STEP 1B-3: Implement Group 3 (Mean Reversion) — 5 hours**
- Extreme Mean Reversion: RSI-2 + Bollinger Band extreme detection
- VWAP Momentum Shift: VWAP deviation + reversal candlestick patterns
- Hikkake Inside Bar Trap: Inside bar + breakout + reversal logic
- Backtest each: Expected >55% win rate

**STEP 1B-4: Implement Group 4 (Breakout/Session) — 4 hours**
- Opening Range Breakout: Define session opening range + breakout detection
- RVGI-CCI-SMA Confluence: Indicator confluence detection
- Volatility Contraction Breakout: Volatility contraction + breakout logic
- Backtest each: Expected >40% win rate minimum

**STEP 1B-5: Implement Group 5 (Advanced) — 3 hours**
- Statistical Arbitrage: Z-score calculation on currency pairs
- Naked Price Action: Strip-chart engulfing detection on D1
- COT Sentiment Swing: COT data integration + macro bias
- Backtest each: Expected variable win rates

**Expected Outcome:**
- 15 new strategies implemented and backtested
- Quick-win strategies identified (Institutional Flow, Mean Reversion)
- Medium-priority strategies ready for further optimization
- Foundation for 10%+ success rate improvement

---

## 📊 PHASE 2: STRATEGY TIER ASSIGNMENT & WALK-FORWARD VALIDATION (8–10 hours)

**Status:** ⏳ Queued (After Phase 1B)  
**Objective:** Validate all 25 strategies through walk-forward testing and assign tiers

### Walk-Forward Validation Sequence

**For Each Strategy:**
1. **In-Sample (70%):** Optimize parameters
2. **Out-of-Sample (20%):** Verify no overfitting (profit factor should not degrade >20%)
3. **Forward Test (10%):** Most recent data — real performance estimate

**Tier Assignment Criteria:**

| Tier | Win Rate | Profit Factor | Sharpe | Status | Action |
|------|----------|---------------|--------|--------|--------|
| **TIER 1** | ≥50% | ≥1.3 | ≥2.5 | Approved | Enable immediately |
| **TIER 2** | 45–49% | 1.1–1.29 | 2.0–2.49 | Monitor | Enable after baseline confirmation |
| **TIER 3** | <45% | <1.1 | <2.0 | Excluded | Disabled; revisit later |

### Expected Distribution

Based on LeoDeX V2 specifications:
- **TIER 1:** 8–10 strategies (Institutional, Mean Reversion, Some Trend)
- **TIER 2:** 10–12 strategies (Trend, Session-based, Breakout)
- **TIER 3:** 3–5 strategies (Low-performing, high-complexity)

### Phase 2 Output

**Tier-1 Strategy Ensemble:**
- Combination of best-performing strategies across asset classes
- Ready for paper trading deployment
- Expected aggregate win rate: 55–65%

**Configuration Matrix:**
- Per-strategy enabled/disabled flags
- Per-pair parameter overrides
- Per-timeframe risk settings

---

## 🧪 PHASE 3: PAPER TRADING & DEMO RUN (2–4 weeks)

**Status:** ⏳ Queued (After Phase 2)  
**Objective:** Validate Tier-1 strategies in live market conditions

### Paper Trading Validation

**Week 1–2:**
- Deploy Tier-1 strategies to paper trading account
- Monitor live signal generation and order execution
- Track P&L, drawdowns, correlation between strategies
- Verify Telegram notifications work correctly
- Check data freshness and signal deduplication

**Week 3–4:**
- Stress test with different market regimes
- Verify position sizing and risk limits
- Test edge cases (gaps, limit moves, low liquidity)
- Prepare live trading deployment checklist

**Success Criteria:**
- ✅ No error loops or stale signals
- ✅ Orders execute cleanly with clear error messages
- ✅ P&L matches backtest expectations (within 20%)
- ✅ Drawdown stays within risk limits (<15%)
- ✅ Correlation between strategies <0.6 (diversification)
- ✅ All regulatory requirements met (FSCA, SARS)

---

## 🎯 SUCCESS METRICS & 10% BOOST TARGET

### Current Baseline (From 10 Existing Strategies)
- **Average Win Rate:** 52% (estimate)
- **Average Profit Factor:** 1.45
- **Average Sharpe Ratio:** 2.1

### Target After Integration (25 Strategy Ensemble)
- **Average Win Rate:** 57–60% (+5–8%)
- **Average Profit Factor:** 1.60–1.75 (+10–15%)
- **Average Sharpe Ratio:** 2.4–2.7 (+15–20%)

### How to Achieve 10% Boost

| Lever | Contribution | How |
|-------|-------------|-----|
| Institutional Flow Strategies (+3–5%) | Add 3 high-accuracy entry strategies | Liquidity sweeps + market structure |
| Mean Reversion Strategies (+2–3%) | Add counter-trend entry confirmation | RSI extremes + VWAP deviations |
| Ensemble Voting (+1–2%) | Combine Tier-1 signals, reduce false signals | Vote on 2+ strategy agreement |
| Regime Filtering (+2–3%) | Filter trades by macro regime (USD, VIX, yields) | Only trade in favorable regimes |
| Multi-TF Confirmation (+1–2%) | Confirm intraday signals on higher timeframes | H1 signal confirmed by H4 structure |

**Total Expected Boost:** +9–15% (conservative target: +10%)

---

## 📋 CONFIGURATION UPDATES REQUIRED

See **CONFIG_UPDATE_CHECKLIST.md** for complete list of:
- New parameters for each of 15 LeoDeX V2 strategies
- Pair-specific overrides (spread, slippage, pip value)
- Regulatory compliance settings (FSCA, SARS)
- Risk management adjustments

---

## ⏱️ OVERALL TIMELINE

```
NOW (2026-04-20):
Phase 0: CRISIS MODE (1–2h)
  └─ 4 emergency fixes to paper engine + order manager
  └─ Success: Bot stable, no retry loops

Week 1:
Phase 1A: Validate Existing Strategies (6–8h)
  └─ Backtest + WFO all 10 existing strategies
  └─ Success: Tier-1 confirmed, exclusions identified

Week 1–2:
Phase 1B: Implement LeoDeX V2 Strategies (12–16h)
  └─ Implement + backtest 15 new strategies by group
  └─ Success: Quick-win strategies identified, ready for validation

Week 2–3:
Phase 2: Walk-Forward Validation (8–10h)
  └─ Tier assignment for all 25 strategies
  └─ Success: 8–12 Tier-1 strategies ready for deployment

Week 3–6:
Phase 3: Paper Trading Demo (2–4 weeks)
  └─ Live validation of Tier-1 ensemble
  └─ Success: Ready for live trading if P&L meets targets

Week 6+:
Phase 4: LIVE TRADING (if Phase 3 passes)
  └─ Deploy to live account with 0.1% of capital
  └─ Monitor correlations, drawdowns, regulatory compliance
```

**Total Duration:** 4–6 weeks to live trading (including 2–4 week demo)

---

## ✅ NEXT ACTIONS

1. **Approve Phase 0 fixes** → Assign to agent or apply manually
2. **Prepare test data** → Ensure MT5 has 6+ years history for each asset
3. **Review strategy specs** → Verify LeoDeX V2 strategies match your risk profile
4. **Configure database** → Set up trade logging for Phase 1 validation
5. **Create agent task list** → (See AGENT_STRATEGY_TESTING_TASK_LIST.md)

---

## 📁 Supporting Documentation

- **DIAGNOSTIC_REPORT.md** — Phase 0 emergency fixes (bot stabilization)
- **MASTER_PROJECT_STATUS.md** — Overall project phases and timeline
- **PATH_B_IMPLEMENTATION.md** — Path B enhancement details (Components 2–5)
- **CONFIG_UPDATE_CHECKLIST.md** — All config files that need updates
- **AGENT_STRATEGY_TESTING_TASK_LIST.md** — Detailed agent task queue

