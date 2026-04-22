# ✅ CONFIG UPDATE CHECKLIST
**Project:** TradePanel LeoDeX V2 Integration  
**Last Updated:** 2026-04-20  
**Status:** Planning → Implementation  
**Total Updates Required:** 45+ config entries

---

## 📋 Overview

This checklist tracks all configuration updates needed to support 15 new LeoDeX V2 strategies across your project. Updates are organized by:
1. **config/strategies.yaml** — Parameter definitions for all 25 strategies
2. **config/config.yaml** — Global trading pairs, risk management, scheduler
3. **Database & Logging** — Trade logging for strategy validation
4. **Regulatory Compliance** — FSCA (South Africa) & SARS tax reporting

---

## 🔴 PHASE 0: CRITICAL FIXES (Already planned in DIAGNOSTIC_REPORT.md)

### Files to Update for Bot Stabilization
- [ ] `forward_test/paper_engine.py` — Add signal deduplication tracking
- [ ] `mt5_bridge/order_manager.py` — Add order validation before MT5.order_send()
- [ ] `forward_test/signal_checker.py` — Add data freshness checks
- [ ] `mt5_bridge/connector.py` — Add market watch symbol selection on connect

**Status:** Not yet applied  
**Blocker:** Phase 0 must complete before strategy testing

---

## 🟡 SECTION 1: config/strategies.yaml UPDATES

### New Strategies to Add (15)

#### Group 1: Institutional Flow Strategies

- [ ] **1. Institutional Silver Bullet (SMC)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    institutional_silver_bullet:
      name: "Institutional Silver Bullet (SMC)"
      category: "Institutional Flow"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["XAUUSD", "GBPUSD", "EURUSD"]
      timeframes: ["M15", "M5"]
      parameters:
        liquidity_sweep_pips: 10
        market_structure_shift: true
        fair_value_gap_retracement: true
        atr_period: 14
        tp_rr_mult: 3.0
        sl_atr_mult: 1.0
      pair_overrides:
        XAUUSD:
          liquidity_sweep_pips: 20  # Gold needs wider sweep detection
        GBPUSD:
          liquidity_sweep_pips: 15
    ```

- [ ] **2. ICT Judas Swing (London Trap)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    ict_judas_swing:
      name: "ICT Judas Swing (London Trap)"
      category: "Institutional Flow"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["GBPUSD", "EURUSD"]
      timeframes: ["M15"]
      parameters:
        asian_range_lookback: 5
        fake_breakout_detection: true
        choch_confirmation_min: 1  # 1-min CHoCH (Change of Character)
        atr_period: 14
        tp_rr_mult: 3.5
        sl_atr_mult: 1.0
      pair_overrides:
        GBPUSD:
          asian_range_lookback: 6  # GBP Asian range slightly longer
    ```

- [ ] **3. Turtle Soup Liquidity Sweep**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    turtle_soup_liquidity_sweep:
      name: "Turtle Soup Liquidity Sweep"
      category: "Institutional Flow"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["XAUUSD", "BTCUSD"]
      timeframes: ["M15", "H1"]
      parameters:
        old_level_lookback: 20  # Untouched levels > 20 periods
        sweep_threshold_pips: 15  # Sweep 10-20 pips beyond level
        close_inside_range: true
        atr_period: 14
        tp_rr_mult: 3.0
        sl_atr_mult: 1.0
      pair_overrides:
        XAUUSD:
          sweep_threshold_pips: 25
        BTCUSD:
          sweep_threshold_pips: 50  # BTC needs larger absolute sweep
    ```

#### Group 2: Trend Following & Momentum

- [ ] **4. Dual EMA Momentum Continuity**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    dual_ema_momentum:
      name: "Dual EMA Momentum Continuity"
      category: "Trend Following"
      status: implemented
      regime: ["TRENDING", "ANY"]
      enabled: true
      pairs: ["BTCUSD", "ETHUSD", "EURUSD"]
      timeframes: ["H1", "H4"]
      parameters:
        fast_ema: 10
        slow_ema: 50
        adx_min: 25
        engulfing_confirmation: true
        atr_period: 14
        tp_atr_mult: 4.0
        sl_atr_mult: 1.5
      pair_overrides:
        BTCUSD:
          tp_atr_mult: 5.0  # BTC runs further
        EURUSD:
          adx_min: 22
    ```

- [ ] **5. Triple MACD Momentum Scalping**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    triple_macd_momentum:
      name: "Triple MACD Momentum Scalping"
      category: "Momentum Scalping"
      status: implemented
      regime: ["TRENDING", "ANY"]
      enabled: true
      pairs: ["XAUUSD", "BTCUSD"]
      timeframes: ["M5"]
      parameters:
        layer_c_ma_period: 200  # Macro trend filter
        layer_b_ma_period: 50   # Intraday trend
        layer_a_macd_fast: 12   # Scalp trigger
        layer_a_macd_slow: 26
        layer_a_macd_signal: 9
        zero_line_cross: true
        atr_period: 14
        tp_rr_mult: 3.0
        sl_atr_mult: 1.0
      pair_overrides:
        XAUUSD:
          layer_c_ma_period: 180
    ```

- [ ] **6. Dual EMA Fractal Breaker**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    dual_ema_fractal_breaker:
      name: "Dual EMA Fractal Breaker"
      category: "Trend Following"
      status: implemented
      regime: ["TRENDING"]
      enabled: true
      pairs: ["USDJPY", "EURUSD"]
      timeframes: ["H1"]
      parameters:
        trend_ema: 200
        fractal_ema: 14
        bill_williams_lookback: 5
        buy_stop_offset_pips: 1
        atr_period: 14
        tp_rr_mult: 3.0
        sl_atr_mult: 1.0
      pair_overrides:
        USDJPY:
          fractal_ema: 13
    ```

#### Group 3: Mean Reversion & Countertrend

- [ ] **7. Extreme Mean Reversion (RSI-2)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    extreme_mean_reversion:
      name: "Extreme Mean Reversion (RSI-2)"
      category: "Mean Reversion"
      status: implemented
      regime: ["RANGING", "ANY"]
      enabled: true
      pairs: ["EURUSD", "USDJPY"]
      timeframes: ["D1", "H4"]
      parameters:
        sma_period: 200
        rsi_period: 2
        rsi_extreme: 10  # RSI < 10 = oversold
        bb_period: 20
        bb_deviation: 2.0
        bb_lower_bound: true
        atr_period: 14
        tp_rr_mult: 2.0
        sl_atr_mult: 1.5
      pair_overrides:
        EURUSD:
          rsi_extreme: 12
        USDJPY:
          rsi_extreme: 8
    ```

- [ ] **8. VWAP Momentum Shift**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    vwap_momentum_shift:
      name: "VWAP Momentum Shift"
      category: "Mean Reversion"
      status: implemented
      regime: ["RANGING", "ANY"]
      enabled: true
      pairs: ["ETHUSD", "XAGUSD"]
      timeframes: ["M15", "M30"]
      parameters:
        vwap_lookback: 20
        std_dev_extreme: 2.0  # Price > 2σ from VWAP
        reversal_pattern: true  # Pin bar / Engulfing
        atr_period: 14
        tp_rr_mult: 2.5
        sl_atr_mult: 1.5
      pair_overrides:
        ETHUSD:
          std_dev_extreme: 2.2
        XAGUSD:
          std_dev_extreme: 1.8  # Silver is tighter
    ```

- [ ] **9. Hikkake Inside Bar Trap**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    hikkake_inside_bar:
      name: "Hikkake Inside Bar Trap"
      category: "Price Action"
      status: implemented
      regime: ["RANGING"]
      enabled: true
      pairs: ["BTCUSD", "ETHUSD"]
      timeframes: ["H4", "D1"]
      parameters:
        inside_bar_lookback: 2
        breakout_reversal_candles: 3  # Reversal must occur within 3 candles
        atr_period: 14
        tp_rr_mult: 3.0
        sl_atr_mult: 1.0
      pair_overrides:
        BTCUSD:
          tp_rr_mult: 4.0
    ```

#### Group 4: Breakout & Session-Based

- [ ] **10. Opening Range Breakout (ORB)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    opening_range_breakout:
      name: "Opening Range Breakout (ORB)"
      category: "Breakout"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["GBPUSD", "EURUSD"]
      timeframes: ["M15"]
      parameters:
        opening_hour_utc: 8  # Frankfurt opens at 08:00 UTC
        range_period_bars: 60  # First hour = 4 x M15 = 4 bars
        breakout_close_requirement: true
        atr_period: 14
        tp_range_mult: 3.0  # TP = 3x opening range
        sl_buffer_pips: 10
      pair_overrides:
        GBPUSD:
          opening_hour_utc: 8
        EURUSD:
          opening_hour_utc: 8
    ```

- [ ] **11. RVGI-CCI-SMA Confluence**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    rvgi_cci_sma:
      name: "RVGI-CCI-SMA Confluence"
      category: "Confluence"
      status: implemented
      regime: ["TRENDING"]
      enabled: true
      pairs: ["GBPUSD", "USDJPY"]
      timeframes: ["H1"]
      parameters:
        rvgi_period: 10
        cci_period: 20
        cci_oversold: -100  # CCI < -100 = entry condition
        sma_period: 30
        fractal_lookback: 2
        atr_period: 14
        tp_rr_mult: 3.5
        sl_atr_mult: 1.0
      pair_overrides:
        USDJPY:
          cci_oversold: -90
    ```

- [ ] **12. Volatility Contraction Breakout**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    volatility_contraction_breakout:
      name: "Volatility Contraction Breakout"
      category: "Breakout"
      status: implemented
      regime: ["ANY"]
      enabled: false  # Tier 2 - enable after validation
      pairs: ["USDJPY", "ETHUSD"]
      timeframes: ["D1"]
      parameters:
        contraction_days: 4  # 3-4 consecutive decreasing ranges
        contraction_threshold_pct: 0.02  # Daily range must decrease by 2%
        volume_spike_mult: 1.5
        atr_period: 14
        tp_atr_mult: 4.0
        sl_atr_mult: 1.5
      pair_overrides:
        ETHUSD:
          tp_atr_mult: 5.0
    ```

#### Group 5: Advanced & Statistical

- [ ] **13. Statistical Arbitrage Spread (XAU/XAG)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    statistical_arbitrage_spread:
      name: "Statistical Arbitrage Spread (Gold/Silver Ratio)"
      category: "Pairs Trading"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["XAUUSD", "XAGUSD"]  # Pairs trading
      timeframes: ["H4", "D1"]
      parameters:
        zscore_window: 20
        zscore_entry_threshold: 2.0  # Z-score > 2.0 = entry
        zscore_exit_threshold: 0.0   # Exit at mean (Z=0)
        correlation_min: 0.7
        atr_period: 14
        tp_rr_mult: 2.0
      notes: >
        This is a pairs trading strategy. Two simultaneous trades:
        - When Z-score > 2.0: Short XAUUSD + Long XAGUSD
        - Exit both when Z-score reverts to mean
    ```

- [ ] **14. Naked Price Action (Engulfing)**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    naked_price_action:
      name: "Naked Price Action (Engulfing at S&R)"
      category: "Price Action"
      status: implemented
      regime: ["ANY"]
      enabled: true
      pairs: ["EURUSD", "GBPUSD", "XAUUSD"]
      timeframes: ["D1", "H4"]
      parameters:
        sr_lookback: 50  # Identify S/R over last 50 periods
        engulfing_confirmation: true
        body_size_min_pct: 0.7  # Body must be 70% of range
        atr_period: 14
        tp_rr_mult: 4.0
        sl_buffer_pips: 5  # Tight SL (5 pips above engulfing high)
      pair_overrides:
        XAUUSD:
          tp_rr_mult: 3.0
          sl_buffer_pips: 10  # Gold volatility needs wider buffer
    ```

- [ ] **15. COT Sentiment Swing**
  - **File:** `config/strategies.yaml`
  - **Add entry:**
    ```yaml
    cot_sentiment_swing:
      name: "COT Sentiment Swing (Macro)"
      category: "Macro Sentiment"
      status: implemented
      regime: ["ANY"]
      enabled: false  # Tier 2 - requires external COT data feed
      pairs: ["XAUUSD", "XAGUSD", "USDJPY"]
      timeframes: ["D1", "Weekly"]
      parameters:
        cot_source: "cftc"  # CFTC Commitment of Traders
        commercial_net_extreme: true  # Commercial hedging at extreme
        non_commercial_extreme: true  # Non-commercial (spec) at opposite extreme
        d1_break_of_structure: true
        atr_period: 14
        tp_rr_mult: 5.0  # Long-term swings have high reward
        sl_atr_mult: 3.0  # But wider stops
      notes: >
        Requires external COT data feed. Currently not available in Phase 1.
        Mark as FUTURE ENHANCEMENT for Phase 2 macro integration.
    ```

---

### Update Existing Strategy Entries in strategies.yaml

- [ ] **Ensemble Strategy** — Already exists; verify:
  ```yaml
  ensemble:
    sub_strategies:
      - range_breakout
      - rsi_pullback
      - swing_pullback
    # Verify these three are still Tier-1 after Phase 1A validation
  ```

- [ ] **BB Mean Reversion** — Currently Tier 3 (PF 0.69); verify after Phase 1B
  - May need parameter tuning (Component 2 in PATH_B_IMPLEMENTATION.md)
  - If PF improves to >1.1, move to Tier 2

- [ ] **Session Momentum** — Currently Tier 2; verify after Phase 1B
  - May need parameter tuning (Component 3 in PATH_B_IMPLEMENTATION.md)
  - If PF improves to >1.2, consider promoting to Tier 1 for crypto

---

## 🟢 SECTION 2: config/config.yaml UPDATES

### Global Trading Pairs — Verify All Assets

- [ ] Confirm all 7 trading pairs are enabled:
  - [ ] XAUUSD (Gold) — spread_pips: 5.0 ✓
  - [ ] EURUSD (EUR/USD) — spread_pips: 1.0 ✓
  - [ ] GBPUSD (GBP/USD) — spread_pips: 1.5 ✓
  - [ ] USDJPY (USD/JPY) — spread_pips: 1.0 ✓
  - [ ] XAGUSD (Silver) — spread_pips: 6.0 ✓
  - [ ] BTCUSD (Bitcoin) — spread_pips: 50.0 ✓
  - [ ] ETHUSD (Ethereum) — spread_pips: 5.0 ✓

### Risk Management Settings

- [ ] `risk_per_trade_pct` — Verify: 2.0% ✓
- [ ] `max_lot_size` — Verify: 1.0 ✓
- [ ] `max_concurrent_positions` — Verify: 5 ✓
- [ ] `max_spread_pips` — Verify: 5.0 ✓
- [ ] `strategy_correlation_threshold` — Verify: 0.7 ✓
- [ ] `use_macro_regime_filter` — Set to: `true` (for Path B, Phase 2)

### Add New Risk Settings for 25-Strategy Ensemble

- [ ] Add strategy-specific position sizing:
  ```yaml
  strategy_risk_overrides:
    institutional_silver_bullet:
      max_concurrent: 1  # Only one institutional trade at a time
      max_lot_size: 0.5  # Tighter position size for new strategy
    statistical_arbitrage_spread:
      is_pairs_trade: true
      max_concurrent: 1  # One pair trade only
  ```

- [ ] Add per-pair correlation checks:
  ```yaml
  pair_correlation_limits:
    XAUUSD_XAGUSD: 0.75  # High correlation — reduce concurrent trades
    BTCUSD_ETHUSD: 0.90  # Very high correlation — no simultaneous trades
  ```

### Update Scheduler Settings

- [ ] `signal_check_interval_sec` — Change from 900 to 600 (10 min checks for faster strategies)
- [ ] Add new signal deduplication timer:
  ```yaml
  scheduler:
    signal_dedup_timeout_sec: 300  # 5 min — signals older than this are forgotten
  ```

---

## 🔵 SECTION 3: DATABASE & LOGGING UPDATES

### Trade Logging Schema

- [ ] Verify PostgreSQL schema includes:
  ```sql
  CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100),
    asset_pair VARCHAR(10),
    timeframe VARCHAR(10),
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    entry_price FLOAT,
    exit_price FLOAT,
    direction INT,  -- 1=long, -1=short
    lot_size FLOAT,
    profit_loss FLOAT,
    win BOOLEAN,
    signal_bars JSONB,  -- For signal debugging
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```

- [ ] Add columns for new strategies:
  ```sql
  ALTER TABLE trades ADD COLUMN IF NOT EXISTS strategy_category VARCHAR(50);
  ALTER TABLE trades ADD COLUMN IF NOT EXISTS regime_type VARCHAR(50);
  ALTER TABLE trades ADD COLUMN IF NOT EXISTS entry_signal_strength FLOAT;
  ```

- [ ] Create performance view:
  ```sql
  CREATE MATERIALIZED VIEW strategy_performance AS
  SELECT 
    strategy_name,
    COUNT(*) as total_trades,
    SUM(CASE WHEN win THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as win_rate,
    SUM(profit_loss) as total_pnl,
    AVG(profit_loss) as avg_trade_pnl
  FROM trades
  GROUP BY strategy_name;
  ```

---

## 🟣 SECTION 4: REGULATORY COMPLIANCE UPDATES

### South African FSCA Compliance

- [ ] Add FSCA leverage limits to config:
  ```yaml
  regulatory:
    jurisdiction: "South Africa"
    fsca_max_leverage: 20  # Max 20:1 leverage for retail
    fsca_check_enabled: true
    flag_excess_leverage: true  # Alert if leverage > 20:1
  ```

- [ ] Verify all trading pairs comply with FSCA:
  - [ ] XAUUSD — leverage_limit: 20 ✓
  - [ ] EURUSD — leverage_limit: 30 ✓ (FX pairs can be higher)
  - [ ] BTCUSD — leverage_limit: 2 ⚠️ (Crypto is restricted)
  - [ ] ETHUSD — leverage_limit: 2 ⚠️ (Crypto is restricted)

### SARS Capital Gains Tax Reporting

- [ ] Add SARS logging:
  ```yaml
  tax_reporting:
    enabled: true
    jurisdiction: "ZA"
    report_schedule_day: "january_1"  # Annual SARS report
    output_format: "eighth_schedule"  # SARS Eighth Schedule format
    include_swap_costs: true
    include_commissions: true
  ```

- [ ] Create tax report generation:
  ```sql
  -- SQL query to generate SARS-compliant trade report
  SELECT
    EXTRACT(YEAR FROM exit_time) as tax_year,
    asset_pair,
    COUNT(*) as num_trades,
    SUM(profit_loss) as net_gain_loss,
    SUM(CASE WHEN direction = 1 THEN profit_loss ELSE 0 END) as long_pnl,
    SUM(CASE WHEN direction = -1 THEN profit_loss ELSE 0 END) as short_pnl
  FROM trades
  GROUP BY tax_year, asset_pair;
  ```

---

## 📊 SECTION 5: TEST DATA & VALIDATION

### Backtest Data Requirements

- [ ] Verify data availability for all 7 pairs:
  - [ ] XAUUSD — 6+ years history (M5 minimum) ✓
  - [ ] EURUSD — 6+ years history ✓
  - [ ] GBPUSD — 6+ years history ✓
  - [ ] USDJPY — 6+ years history ✓
  - [ ] XAGUSD — 6+ years history ✓
  - [ ] BTCUSD — 4+ years history (since 2021-01-01) ⚠️
  - [ ] ETHUSD — 4+ years history ✓

- [ ] Download missing data:
  ```bash
  python scripts/download_historical_data.py --pair BTCUSD --start 2021-01-01 --timeframes M5,M15,H1,H4,D1
  ```

### Walk-Forward Test Windows

- [ ] Define 3 walk-forward windows:
  - [ ] Window 1 (2022–2023): 70% IS / 20% OOS / 10% FWD
  - [ ] Window 2 (2023–2024): 70% IS / 20% OOS / 10% FWD
  - [ ] Window 3 (2024–2026): 70% IS / 20% OOS / 10% FWD

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 0 (Before Any Strategy Testing)
- [ ] Apply 4 emergency bot fixes (see DIAGNOSTIC_REPORT.md)
- [ ] Verify bot runs 5+ minutes without error loop
- [ ] Test signal deduplication with single strategy

### Phase 1A (Validate Existing 10 Strategies)
- [ ] Add existing 10 strategies to strategies.yaml (if not already)
- [ ] Run full backtest suite (6–8 hours)
- [ ] Assign tier ratings (Tier 1/2/3)
- [ ] Document baseline performance

### Phase 1B (Implement 15 New Strategies)
- [ ] Add all 15 new strategies to strategies.yaml ✓ (This checklist)
- [ ] Create Python implementations for each strategy
- [ ] Run individual backtests (12–16 hours)
- [ ] Identify quick-win strategies

### Phase 2 (Walk-Forward Validation)
- [ ] Run walk-forward tests for all 25 strategies
- [ ] Re-assign tiers based on OOS/FWD performance
- [ ] Create ensemble configuration for Tier-1 strategies
- [ ] Update config files with final parameters

### Phase 3 (Paper Trading Deployment)
- [ ] Deploy Tier-1 ensemble to paper trading
- [ ] Monitor live signal generation
- [ ] Verify Telegram notifications
- [ ] Track 2–4 weeks of live P&L

---

## 📝 NOTES & SPECIAL CONSIDERATIONS

### FSCA Compliance Notes
- Crypto pairs (BTCUSD, ETHUSD) have strict South African leverage limits (2:1)
- Must flag any positions exceeding FSCA limits
- Keep copies of all FSCA regulatory documentation

### Pairs Trading Considerations
- Statistical Arbitrage (Strategy 13) requires TWO simultaneous trades
- Config system must support correlated position tracking
- Correlation between XAUUSD and XAGUSD is ~0.75 (high) — this is intentional

### Data Quality Notes
- BTCUSD has only 4+ years of available data (crypto is newer)
- Backtest window for BTCUSD may be shorter than FX pairs
- Use resampling if historical tick data is unavailable

### Future Enhancement (Phase 2)
- COT Sentiment Swing (Strategy 15) requires external data feed
- Mark as "Future" for now; implement in Phase 2 when macro data available
- Will enable higher-timeframe macro-based trading

---

## 🎯 SUMMARY TABLE

| Section | Status | Updates Needed | Blocker |
|---------|--------|----------------|---------|
| Phase 0 Fixes | ⏳ Pending | Apply 4 emergency fixes | YES |
| New Strategies (1–15) | 📋 Ready | Add to strategies.yaml | NO |
| Global Config | ✓ Verified | Minor updates only | NO |
| Database Schema | ✓ Verified | Add new columns | NO |
| FSCA Compliance | ✓ Verified | Add compliance checks | NO |
| SARS Tax Reporting | ⏳ Pending | Implement after Phase 1 | NO |
| Test Data | ⏳ Verify | Download BTCUSD history | NO |

---

**Next Step:** After Phase 0 completion, proceed with Phase 1A validation of existing 10 strategies, then Phase 1B implementation of 15 new strategies.

