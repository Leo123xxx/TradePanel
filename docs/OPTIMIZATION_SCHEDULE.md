# TradePanel — Monitoring & Optimization Schedule
> Living document. Update as strategies evolve and new tools are adopted.
> Last updated: 2026-04-25

---

## Daily Checks (5 min — spot-check automated outputs)

- [ ] APScheduler health: confirm 06:00/12:00/18:00/00:00 ingestion jobs ran (check logs)
- [ ] MT5 bridge: scan connection logs for reconnect events or data gaps
- [ ] Telegram bot: send `/status` — confirm live connection + last bar timestamp
- [ ] Overnight backtest report: check Pass/Review/Error counts vs yesterday
  - New PASS -> flag for paper trading consideration
  - PASS dropped to REVIEW -> investigate immediately (likely data or code regression)
- [ ] Review any open paper trades vs signal expectations

---

## Weekly Review (30 min — every Monday morning)

### Data Health
- [ ] Verify COT data updated: `SELECT MAX(report_date) FROM cot_data` (should be prior Friday)
  - If stale: `python data/cot_feed.py` manually
- [ ] DB row count check: `SELECT pair, timeframe, COUNT(*) FROM market_data GROUP BY 1,2 ORDER BY 1,2`
  - Confirm row counts growing at expected rate per pair/TF
- [ ] Check for zero-volume bars: run `data/cleaner.py` and review output

### Performance Review
- [ ] Compare this week's backtest Sharpe/WR/DD vs prior week for all PASS strategies
  - Flag any regression > 10% in Sharpe or WR
  - Check if market regime changed (trending -> ranging) and whether that explains it
- [ ] Review Telegram alert log for missed signals or connection drops
- [ ] Verify spread_pips in `config/config.yaml` vs actual broker spreads — update if drifted > 20%

### Strategy-Specific Weekly Watch
- [ ] **ORB EURUSD**: Is Sharpe still negative? Track trend — if no improvement in 4 weeks, remove EURUSD from ORB pair list
- [ ] **COT EURUSD/GBPUSD sells**: Track cumulative PnL on SELL signals separately — if negative for 8 weeks, consider disabling sell direction for FX
- [ ] **Stat Arb XAUUSD**: Check gold/silver spread ratio — if XAU/XAG ratio moves > 2 SD from historical mean, review stat_arb assumptions

---

## Monthly Deep Review (2-3 hours — first Saturday of each month)

### Full Strategy Audit
- [ ] Run backtest on ALL strategies including disabled/REVIEW ones — check if any improved
- [ ] For each REVIEW strategy closest to PASS threshold: identify one hypothesis to test
- [ ] Run isolated parameter test for each hypothesis (change one variable at a time)
- [ ] If improved: test on held-out period (last 6 months) to check for overfitting

### ORB Tuning Targets (as of 2026-04-25)
- [ ] EURUSD: test `tp_atr_mult=2.5`, `tp_atr_mult=3.0` — current 2.0 may be too tight for NY session
- [ ] EURUSD: test `vol_filter=1.0` (lower bar) — check if more signals improve WR
- [ ] XAGUSD: monitor Sharpe trend (was 1.84, dropped to 0.91 after session filter removal)

### COT Tuning Targets
- [ ] EURUSD: compare buy-only vs buy+sell Sharpe — decide whether sells should be disabled
- [ ] GBPUSD: same analysis
- [ ] XAUUSD: confirm EMA200 gate is still appropriate (check current gold trend vs 200-day)

### Config Updates
- [ ] Update `backtesting_usdzar_rate` to current USDZAR rate
- [ ] Update `backtesting_jpyzar_rate` to current JPYZAR rate
- [ ] Review pip values for any new pairs added

### Documentation
- [ ] Update TRADEPANEL_SKILLS.md with any new bugs found or architecture changes
- [ ] Add fixed bugs to "Known Bugs" section
- [ ] Update strategy status table with current Sharpe/WR/DD

---

## Quarterly Strategy Review (4-6 hours — first Saturday of Jan/Apr/Jul/Oct)

### Data Extension
- [ ] Ensure at least 2 extra months of OHLCV data since last quarterly review
- [ ] Check data quality: gaps, outliers, split-adjusted prices for indices
- [ ] Run `VACUUM ANALYZE` on PostgreSQL DB + check for table bloat

### Full Parameter Optimisation
- [ ] For each PASS strategy: run grid search +/- 20% on key params (tp_atr_mult, sl_atr_mult, ATR period)
- [ ] Validate on out-of-sample (hold out most recent 3 months)
- [ ] Document best params and rationale in strategy file header comment

### Market Regime Assessment
Review current macro environment and adjust strategy weights accordingly:

| Regime | Favoured Strategies | Action |
|---|---|---|
| Gold trending up | XAUUSD trend, Stat Arb | Maintain or increase XAUUSD exposure |
| Gold ranging | Stat Arb (mean reversion) | Reduce trend strategy lot sizes |
| High FX volatility (VIX > 25) | Reduce all FX entries | Widen TP multiples; reduce position size |
| USD strength cycle | USDJPY momentum | COT SELL signals on FX pairs more likely |
| Low volatility | ORB less reliable | Widen TP or pause ORB; range strategies better |
| FOMC week | All pairs | Check spread guard is calibrated; consider pausing entries on announcement day |

### Technology Review
- [ ] `pip show MetaTrader5` — check for new API version; test upgrade in dev first
- [ ] Check CFTC COT data format: `python data/cot_feed.py` — if parse errors, inspect raw CFTC file format
- [ ] Telegram Bot API: check @BotFather for deprecation notices on bot API version in use
- [ ] `pip list --outdated` — review pandas/numpy major version updates; test in dev before upgrading
- [ ] PostgreSQL: `pg_dump` full backup before any schema changes

### New Strategy Ideas Evaluation
Generate 1-2 ideas per quarter based on what's working in markets:
- If gold in strong trend: EMA crossover or MACD on XAUUSD D1
- If mean reversion regime: Bollinger Band strategies on EURUSD or GBPUSD H4
- If volatility expanding: Breakout strategies on indices (if pairs added)
- If new data source added: Evaluate whether it improves signal quality for existing strategies

---

## Optimization Loop Template (Monthly Cycle)

```
1. OBSERVE    Run overnight backtest -> collect Pass/Review/Error counts and metrics
2. IDENTIFY   Pick 2-3 REVIEW strategies closest to PASS threshold (best Sharpe in REVIEW)
3. DIAGNOSE   Read strategy code + check signal count, WR breakdown by direction,
              drawdown timing (is it correlated with specific market events?)
4. HYPOTHESIZE Form 1-2 parameter change hypotheses max — avoid overfitting trap
5. TEST       Run isolated backtest on that pair/strategy/parameter only
6. VALIDATE   If improved: test on held-out period (last 6 months separate from training)
7. DEPLOY     Update params in run_overnight_backtest.py; add comment explaining why
8. DOCUMENT   Update TRADEPANEL_SKILLS.md and this file with findings
9. MONITOR    Watch paper-trading signals for 2 weeks before enabling on live account
```

---

## Tools & Integrations Roadmap

Evaluate in priority order — one integration per quarter max to keep system stable:

| Tool | Purpose | Priority | Notes |
|---|---|---|---|
| Economic calendar API | Pause trading around high-impact news (FOMC, NFP, CPI) | HIGH | Forex Factory or Investing.com API; prevents holding trades through shock events |
| Grafana dashboard | PostgreSQL -> live equity curve, trade log, signal count visualization | HIGH | Replaces manual DB queries; makes regime changes visible at a glance |
| TradingView webhooks | Pipe Pine Script alerts into TradePanel as optional signal confirmation | MEDIUM | Adds independent confirmation layer without replacing existing logic |
| Broker direct API | Fallback if MT5 bridge becomes unreliable | MEDIUM | OANDA v20 REST or Interactive Brokers API; implement as parallel bridge |
| pg_dump automation | Nightly DB backup to local or cloud storage | MEDIUM | Add to APScheduler; protect against DB corruption |
| Slack/Discord | Alternative to Telegram if project scales to team | LOW | Telegram is fine for solo use |
| QuantLib | Rigorous option-adjusted spreads if expanding to derivatives | LOW | Only needed if adding options strategies |

---

## Regression Watchlist (review every week)

Strategies to monitor closely — these have known instabilities:

| Strategy | Pair | Watch For |
|---|---|---|
| ORB | EURUSD M15 | Sharpe improving trend or not? Remove if still negative at 2026-06-01 |
| ORB | XAGUSD M15 | Sharpe trend since session filter removal (was 1.84, now 0.91) |
| COT Sentiment | EURUSD D1 | SELL signal cumulative PnL — disable sells if negative after 8 weeks |
| COT Sentiment | GBPUSD D1 | Same as EURUSD — monitor sell direction separately |
| Session Momentum | GBPUSD H1 | Near-pass — test partial TP disabled |

---

*End of OPTIMIZATION_SCHEDULE.md*
