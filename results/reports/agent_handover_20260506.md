# TradePanel — Agent Handover Document
**Date:** 2026-05-06  
**Generated from:** `results/overnight/20260506_backtest_report.md` + `results/recommendations/20260506_recommendations.md`  
**System mode:** Paper trading (ZAR-denominated, Exness MT5)  
**Account base currency:** ZAR — all P&L converts via live USDZAR tick (fallback: 18.50)

---

## 1. System Snapshot

| Metric | Value |
|--------|-------|
| Total strategy/pair combos tested | 148 |
| ✅ PASS | 35 (24%) |
| 🔄 REVIEW | 90 (61%) |
| ❌ ERROR / SKIP | 23 (16%) |
| Active pairs | 18 (expanded 2026-04-30) |
| System mode | Paper |

The overnight backtest pipeline is running. No live capital is at risk. All actions below are diagnostic or config changes.

---

## 2. Immediate Actions — Escalation Queue

These strategies have hit the consecutive-fail threshold and require a decision **before the next overnight run**.

| Priority | Strategy | Pair | TF | Sharpe | Consecutive Fails | Action Required |
|----------|----------|------|----|--------|-------------------|-----------------|
| 🔴 ESCALATE | macd_trend | EURUSD | H4 | -2.48 | 6 | Disable in `strategies.yaml` or diagnose signal logic |
| 🔴 ESCALATE | cot_sentiment | GBPUSD | D1 | 0.03 | 6 | No edge — disable or full rework |
| 🔴 ESCALATE | cot_sentiment | USDJPY | D1 | -5.13 | 6 | Disable — 50.6% max drawdown, no edge |
| 🟡 WATCH | orb | EURUSD | M15 | -4.87 | 1 | 26 days to deadline — monitor closely |

**What "ESCALATE" means:** The demotion tracker has flagged these as having 6 consecutive overnight fails. The rule is: either disable the pair/TF combination in `config/strategies.yaml`, or perform a root-cause investigation and explicitly reset the fail counter.

**Recommended action for ESCALATE items:**
1. Open `config/strategies.yaml`
2. Find each strategy's entry under its pair list
3. Set `enabled: false` for the specific pair/TF, or remove it from the `pairs` list
4. Document the reason in a comment

---

## 3. Confirmed PASS Strategies (35 combos — do not touch)

These are working. No parameter changes needed. Paper trading should continue as-is.

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|----------|------|----|------|-----|--------|--------|--------|----|
| gold_momentum_breakout | NVDA | H4 | T1 | 100.0 | 14.97 | 0.0 | 4 | 999 |
| vwap_momentum | US500 | M15 | T2 | 100.0 | 50.00 | 0.0 | 2 | 999 |
| bb_squeeze_scalp | USDJPY | M15 | T2 | 87.5 | 15.17 | 0.1 | 8 | 7.80 |
| ema_ribbon_trend | AAPL | H4 | T1 | 86.7 | 10.18 | 0.3 | 15 | 5.49 |
| ema_ribbon_trend | ETHUSD | H4 | T1 | 75.8 | 2.32 | 0.1 | 33 | 1.51 |
| macd_trend | USDJPY | H4 | T1 | 73.7 | 6.34 | 0.8 | 19 | 2.60 |
| ema_ribbon_trend | USTEC | H4 | T1 | 72.2 | 7.96 | 0.3 | 18 | 3.72 |
| stat_arb_gold_silver | XAUUSD | H4 | T1 | 70.8 | 4.66 | 6.2 | 247 | 3.16 |
| ema_ribbon_trend | US500 | H4 | T1 | 70.6 | 8.29 | 0.1 | 17 | 3.36 |
| macd_trend | USTEC | H4 | T1 | 67.7 | 3.77 | 0.3 | 34 | 1.77 |
| gold_momentum_breakout | AAPL | H4 | T1 | 66.7 | 4.77 | 0.4 | 21 | 2.12 |
| ema_ribbon_trend | MSFT | H4 | T1 | 66.7 | 3.17 | 1.1 | 9 | 1.60 |
| stat_arb_gold_silver | XAUUSD | H1 | T1 | 64.3 | 3.39 | 5.8 | 957 | 2.06 |
| gold_momentum_breakout | XAUUSD | H4 | T1 | 63.9 | 5.38 | 4.3 | 72 | 3.01 |
| gold_momentum_breakout | US500 | H4 | T1 | 62.8 | 3.97 | 0.1 | 43 | 1.86 |
| ema_ribbon_trend | AMD | H4 | T1 | 62.5 | 0.87 | 0.8 | 8 | 1.14 |
| ma_crossover | USDJPY | H4 | T1 | 61.5 | 3.19 | 2.6 | 39 | 1.58 |
| bb_squeeze_scalp | USTEC | M15 | T2 | 61.1 | 0.93 | 0.1 | 18 | 1.14 |
| range_breakout | XAUUSD | H4 | T1 | 60.8 | 4.76 | 9.5 | 97 | 2.65 |
| gold_momentum_breakout | MSFT | H4 | T1 | 60.0 | 0.91 | 0.9 | 10 | 1.16 |
| rsi_pullback | XAUUSD | H4 | T2 | 60.0 | 2.80 | 8.2 | 55 | 1.73 |
| rvgi_cci_confluence | EURUSD | H4 | T2 | 59.8 | 1.63 | 2.2 | 82 | 1.29 |
| dual_ema_momentum | USTEC | H4 | T2 | 59.6 | 1.17 | 0.6 | 52 | 1.19 |
| rsi_pullback | GBPUSD | H4 | T2 | 58.3 | 2.93 | 1.5 | 36 | 1.54 |
| dual_ema_fractal | USDCAD | H4 | T1 | 58.2 | 1.18 | 1.6 | 110 | 1.19 |
| rsi_pullback | EURUSD | H4 | T2 | 58.1 | 2.23 | 1.4 | 43 | 1.38 |
| macd_trend | GBPJPY | H4 | T1 | 57.1 | 3.41 | 2.1 | 35 | 1.68 |
| macd_trend | USDJPY | H1 | T1 | 57.0 | 2.17 | 1.0 | 79 | 1.39 |
| dual_ema_fractal | XAUUSD | H4 | T1 | 55.1 | 1.78 | 8.4 | 107 | 1.32 |
| ema_ribbon_trend | XAUUSD | H4 | T1 | 54.5 | 3.06 | 2.6 | 11 | 1.79 |
| rsi_pullback | XAGUSD | H4 | T2 | 54.2 | 3.09 | 9.5 | 59 | 3.42 |
| dual_ema_momentum | XAUUSD | H4 | T2 | 54.0 | 1.98 | 7.2 | 37 | 1.43 |
| range_breakout | USOIL | H4 | T1 | 52.5 | 2.34 | 8.2 | 118 | 1.44 |
| gold_momentum_breakout | USTEC | H4 | T1 | 52.4 | 1.21 | 0.6 | 42 | 1.20 |
| hikkake_trap | XAUUSD | H4 | T2 | 51.9 | 4.58 | 6.7 | 54 | 2.16 |

> ⚠️ **Note:** `gold_momentum_breakout NVDA H4` and `vwap_momentum US500 M15` show extremely high Sharpe/PF with only 4 and 2 trades respectively. These should be considered statistically unreliable — do not promote to live without more trade history.

---

## 4. Near-PASS Candidates — Prioritise for Tuning

These have real potential but are blocked on one or two metrics. Tune these before anything else.

| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker | Suggested Fix |
|----------|------|----|--------|-----|-----|---------|---------------|
| session_momentum | XAUUSD | H1 | 1.254 | 35.6 | 13.6 | WR needs +24.4pp | Tighten entry filter — increase ADX min or add session-time gate |
| session_momentum | GBPJPY | H1 | 1.226 | 37.1 | 2.6 | WR needs +22.9pp | Same as above — entry quality is the blocker |
| range_breakout | US500 | H4 | 0.683 | 53.9 | 0.6 | Sharpe +0.32 + WR +6.1pp | Small improvements needed — try tightening ATR filter |
| dual_ema_momentum | XAUUSD | H1 | 0.657 | 51.9 | 8.4 | Sharpe +0.34 + WR +8.1pp | Add trend confirmation (higher TF bias check) |
| session_momentum | GBPUSD | H1 | 0.631 | 35.6 | 2.8 | Sharpe +0.37 + WR +24.4pp | Entry quality — same fix as XAUUSD/GBPJPY |

**How to action:**
- Run `python scripts/run_opt_single.py --strategy session_momentum --pair XAUUSD --tf H1` to start parameter search
- Focus on `adx_min`, `session_filter`, and `tp_atr_mult` parameters first

---

## 5. Priority Task List

### P1 — Diagnose & Pause (53 losing combinations)

The following strategy/pair/TF combos are actively losing money. **Do not tune yet — diagnose the signal logic first.**

For every P1 item, the standard diagnostic checklist is:
1. Check entry condition direction (is the signal inverted?)
2. Verify spread/commission is being applied correctly
3. Check data alignment (SAST vs UTC timezone issue)
4. If none of the above: reduce lot size or disable the combination

**Top P1 items by severity (worst Sharpe first):**

| Strategy | Pair | TF | Sharpe | WR% | Key Issue |
|----------|------|----|--------|-----|-----------|
| bb_squeeze_scalp | EURUSD | M15 | -20.15 | 7.7% | Near-zero WR — likely inverted signal |
| bb_squeeze_scalp | GBPUSD | M15 | -18.38 | 14.3% | Same as above — 7 trades only |
| rsi_extremes_scalp | USDJPY | M15 | -6.77 | 23.8% | Very low WR — check signal direction |
| rsi_extremes_scalp | GBPJPY | M15 | -6.43 | 46.0% | Near-threshold WR, Sharpe very negative |
| ema_ribbon_trend | NVDA | H4 | -6.33 | 40.0% | Only 10 trades — extend window first |
| bb_squeeze_scalp | AUDUSD | M15 | -6.94 | 44.8% | Directional bias LONG — disable SHORTs |
| rsi_extremes_scalp | GBPUSD | M15 | -5.70 | 37.9% | Directional bias SHORT — disable LONGs |
| rsi_extremes_scalp | AUDUSD | M15 | -5.33 | 45.2% | Directional bias SHORT — disable LONGs |
| ma_crossover | USDCAD | H4 | -5.32 | 48.5% | WR near threshold, Sharpe very negative |
| cot_sentiment | USDJPY | D1 | -5.14 | 36.1% | 50.6% max drawdown — stop immediately |
| stat_arb_gold_silver | XAUUSD | M15 | -1.24 | 46.0% | 186.7% max drawdown — critical risk issue |

> 🚨 **Critical:** `stat_arb_gold_silver XAUUSD M15` has a 186.7% max drawdown. Even in paper mode, this indicates a position sizing or calculation bug. Investigate `risk/` module for this specific combo before the next run.

**Full P1 list (all 53 combos) is in:** `results/recommendations/20260506_recommendations.md` → Appendix table.

---

### P2 — Extend Backtest Window (11 combos with insufficient trades)

These have fewer than 10 trades — statistics are unreliable. Do not tune. Instead:
- Extend the backtest window (increase `lookback_days` in `config/strategies.yaml`)
- Or relax entry filters to generate more signals

| Strategy | Pair | TF | Trades | Current Issue |
|----------|------|----|--------|---------------|
| rsi_bounce | XAUUSD | H4 | 1 | Window too short |
| stoch_divergence | GBPUSD | H4 | 1 | Window too short |
| stoch_divergence | GBPJPY | H4 | 1 | Window too short |
| stoch_divergence | AUDUSD | H4 | 1 | Window too short |
| stoch_divergence | XAUUSD | H4 | 8 | Extend window |
| gold_momentum_breakout | AMD | H4 | 1 | Window too short |
| vwap_momentum | GBPJPY | M15 | 1 | Window too short |
| vwap_momentum | BTCUSD | M15 | 1 | Window too short |
| ma_crossover | EURUSD | D1 | 6 | Extend window |
| crypto_rsi_extremes | BTCUSD | D1 | 7 | Extend window |
| crypto_rsi_extremes | ETHUSD | D1 | 8 | Extend window |

---

### P3 — Near-PASS Tuning (8 combos)

Good Sharpe, blocked on WR or marginal edge. Worth investigating this sprint.

| Strategy | Pair | TF | Sharpe | WR% | Recommended Action |
|----------|------|----|--------|-----|--------------------|
| session_momentum | XAUUSD | H1 | 1.254 | 35.6 | Tighten entry — ADX min up, add session gate |
| session_momentum | GBPJPY | H1 | 1.226 | 37.1 | Same |
| range_breakout | US500 | H4 | 0.683 | 53.9 | ATR filter + TP mult |
| dual_ema_momentum | XAUUSD | H1 | 0.657 | 51.9 | Add higher-TF bias check |
| session_momentum | GBPUSD | H1 | 0.631 | 35.6 | Tighten entry |
| hikkake_trap | US500 | H4 | 0.609 | 39.3 | Tighten entry — WR needs +20.7pp |
| hikkake_trap | GBPJPY | H4 | 0.325 | 36.7 | Low WR but PF 1.05 — trend-follower behaviour, monitor |
| cot_sentiment | GBPUSD | D1 | 0.026 | 48.8 | Marginal — check long vs short win rate split |

---

### P4 — Monitor / Investigate Trade Duration (16 combos)

These are in the Sharpe -0.85 to +0.31 range with reasonable WR. The main investigation question is: **are trades closing too quickly?** Short-duration trades may be hitting TP/SL on noise rather than signal.

For each: run `python scripts/run_backtest.py --strategy <name> --pair <pair> --tf <tf> --debug-duration` and check `avg_trade_duration`.

| Strategy | Pair | TF | Sharpe | WR% | Note |
|----------|------|----|--------|-----|------|
| dual_ema_fractal | EURUSD | H4 | 0.305 | 52.0 | Check trade duration |
| range_breakout | EURUSD | H4 | 0.297 | 54.4 | Check trade duration |
| ema_ribbon_trend | BTCUSD | H4 | 0.263 | 59.0 | Near-pass WR |
| dual_ema_fractal | XAUUSD | H1 | 0.144 | 52.1 | Check trade duration |
| rsi_pullback | USDJPY | H4 | 0.143 | 57.5 | Check trade duration |
| bb_squeeze_scalp | GBPJPY | M15 | 0.119 | 59.1 | Very close to WR pass |
| rvgi_cci_confluence | GBPJPY | H4 | 0.041 | 51.4 | Check trade duration |
| cot_sentiment | EURUSD | D1 | -0.033 | 48.3 | Check trade duration |
| turtle_soup | XAUUSD | H4 | -0.142 | 57.6 | Check trade duration |
| bb_squeeze_scalp | XAUUSD | M15 | -0.278 | 38.5 | No edge — disable if no improvement |
| ma_crossover | AUDUSD | H4 | -0.285 | 56.5 | Check trade duration |
| ma_crossover | GBPJPY | H4 | -0.330 | 46.3 | Check trade duration |
| turtle_soup | ETHUSD | H4 | -0.445 | 50.0 | Check trade duration |
| dual_ema_fractal | GBPUSD | H4 | -0.749 | 51.6 | Check trade duration |
| gold_momentum_breakout | XAUUSD | H1 | -0.781 | 49.8 | Check trade duration |
| turtle_soup | GBPUSD | H4 | -0.817 | 51.2 | Check trade duration |

---

## 6. Directional Bias Flags

Several strategies show strong directional skew — one side is winning, the other is dragging the stats down. These are quick wins: disable the losing direction in `strategies.yaml`.

| Strategy | Pair | TF | Bias | Action |
|----------|------|----|------|--------|
| hikkake_trap | GBPUSD | H4 | SHORT (44%) >> LONG (24%) | Disable LONG trades |
| dual_ema_momentum | US500 | H4 | LONG (55%) >> SHORT (38%) | Disable SHORT trades |
| ma_crossover | GBPUSD | H4 | SHORT (58%) >> LONG (35%) | Disable LONG trades |
| dual_ema_momentum | EURUSD | H4 | LONG (50%) >> SHORT (35%) | Disable SHORT trades |
| hikkake_trap | USOIL | H4 | LONG (41%) >> SHORT (11%) | Disable SHORT trades |
| macd_trend | US500 | H4 | LONG (70%) >> SHORT (33%) | Disable SHORT trades |
| orb | GBPUSD | M15 | LONG (56%) >> SHORT (40%) | Disable SHORT trades |
| orb | EURUSD | M15 | LONG (50%) >> SHORT (35%) | Disable SHORT trades |
| turtle_soup | GBPJPY | H4 | LONG (51%) >> SHORT (24%) | Disable SHORT trades |
| bb_squeeze_scalp | AUDUSD | M15 | LONG (56%) >> SHORT (27%) | Disable SHORT trades |
| rsi_extremes_scalp | GBPUSD | M15 | SHORT (53%) >> LONG (21%) | Disable LONG trades |
| rsi_extremes_scalp | AUDUSD | M15 | SHORT (53%) >> LONG (39%) | Disable LONG trades |
| ma_crossover | GBPUSD | H1 | LONG (52%) >> SHORT (36%) | Disable SHORT trades |

---

## 7. Known Data / Config Issues

- **stat_arb_gold_silver XAUUSD M15:** 186.7% max drawdown is a likely bug — investigate before next run
- **Timezone alignment:** Multiple strategies flagged for potential SAST vs UTC data misalignment — verify `data/ingestion.py` is converting correctly
- **Low trade count on crypto D1:** `BTCUSD D1` and `ETHUSD D1` have only 7–8 trades. Extend backtest window or the sample is too thin to evaluate
- **Two virtual environments exist** (`.venv/` and `venv/`) — confirm which is active; stale dependencies in the wrong env could affect results
- **`D:\Trade_training_data`** appears as a directory inside the repo (likely a symlink or Windows junction) — verify this is intentional and not a stray path

---

## 8. Suggested Sprint Order for Next Session

1. **Disable ESCALATE strategies** in `strategies.yaml` (macd_trend EURUSD H4, cot_sentiment GBPUSD D1, cot_sentiment USDJPY D1)
2. **Investigate stat_arb_gold_silver XAUUSD M15** — the 186.7% drawdown is a bug, not a feature
3. **Apply directional bias fixes** (Section 6) — quick config changes, high impact
4. **Run P3 optimization** on session_momentum (XAUUSD, GBPJPY, GBPUSD H1)
5. **Extend backtest windows** for P2 combos with < 10 trades
6. **Diagnose bb_squeeze_scalp EURUSD M15** — Sharpe -20 with 7.7% WR is almost certainly a signal direction bug
7. **Investigate P4 trade durations** to identify TP/SL noise issues

---

## 9. Reference

| Resource | Path |
|----------|------|
| Overnight backtest report | `results/overnight/20260506_backtest_report.md` |
| Full recommendations | `results/recommendations/20260506_recommendations.md` |
| Strategy config | `config/strategies.yaml` |
| System config | `config/config.yaml` |
| Demotion tracker | `results/demotion_tracker.json` |
| Backtest runner | `scripts/run_backtest.py` |
| Single optimization | `scripts/run_opt_single.py` |
| WFO runner | `scripts/run_walk_forward.py` |
| This handover | `results/agent_handover_20260506.md` |

---

*End of handover — next session should begin at Section 8, Step 1.*
