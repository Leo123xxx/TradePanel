# TradePanel — Master Project Status
## Check Gate #1 — May 2026

**Last Updated:** 2026-05-12  
**System Mode:** Paper Trading (live MT5, ZAR-denominated, Exness)  
**Overall Completion:** ~72% toward live trading  
**Next Gate:** Go-live approval (paper test sustained ≥ 2 weeks)

---

## Executive Summary

TradePanel has progressed from a broken bot in crisis mode (April 20, ~15% complete) to a stable, automated paper-trading platform running 35 confirmed strategies across 18 pairs on a live MT5 demo account. The May 6 overnight report produced 35 PASS, 90 REVIEW, and 23 ERROR combos out of 148 total — a meaningful result set with clear next actions. The system is structurally sound. The remaining work is strategy quality improvement, infrastructure hardening, and the 2–4 week paper run required before any live capital deployment.

---

## Phase Completion Summary

| Phase | Name | Target | Status | Completion |
|-------|------|--------|--------|------------|
| 0 | Crisis stabilisation — fix bot retry loop | 2026-04-20 | ✅ DONE | 100% |
| 1A | Path B quick wins — Ensemble, BB, Session Momentum | 2026-04-22 | ✅ DONE | 100% |
| 1B | Infrastructure — venv rebuild, Docker, DB migrations | 2026-05-05 | ✅ DONE | 100% |
| 2A | Paper trading live — 35 PASS strategies running | 2026-05-06 | ✅ DONE | 100% |
| 2B | Path B medium wins — Regime filter, Multi-TF | 2026-05-12 | 🟡 IN PROGRESS | 60% |
| 3A | Strategy quality — disable ESCALATE, tune Near-PASS | 2026-05-19 | 🟡 IN PROGRESS | 20% |
| 3B | Infrastructure hardening — observability, Kafka stream | TBD | ⏳ PLANNED | 0% |
| 4 | 2–4 week sustained paper run | TBD | ⏳ PLANNED | 0% |
| 5 | Live trading — go/no-go decision | TBD | ⏳ PLANNED | 0% |

---

## What Has Been Built (Confirmed Complete)

### Core Engine
- ✅ Backtesting engine (`backtesting/engine.py`) — runs full OHLCV backtests against historical data from 2019
- ✅ Walk-forward optimisation (`backtesting/walk_forward.py`) — rolling window validation to prevent overfitting
- ✅ Paper trading engine (`forward_test/paper_engine.py`) — live signal detection, order routing, deduplication
- ✅ Signal checker (`forward_test/signal_checker.py`) — per-bar signal evaluation with freshness check
- ✅ Risk manager (`risk/manager.py`) — 1% risk per trade, 20% circuit breaker
- ✅ Regime classifier (`risk/regime_classifier.py`) — macro regime detection (trend/range/volatile)

### MT5 Bridge
- ✅ Connector (`mt5_bridge/connector.py`) — connects to MT5, adds all symbols to market watch on boot
- ✅ Order manager (`mt5_bridge/order_manager.py`) — validates orders before send, magic number assignment
- ✅ Data feed (`mt5_bridge/data_feed.py`) — historical pull + incremental latest-bars sync to PostgreSQL

### Data Pipeline
- ✅ Market data ingestion (`data/ingestion.py`) — OHLCV from MT5 into PostgreSQL
- ✅ COT feed (`data/cot_feed.py`) — Commitment of Traders sentiment data
- ✅ Macro feed (`data/macro_feed.py`) — macro context for regime classification
- ✅ DB client (`data/db_client.py`) — pooled connections, batch inserts
- ✅ Resampler (`data/resampler.py`) — M1 bars resampled to higher timeframes

### Strategies (35 PASS as of 2026-05-06)
35 active strategy/pair/TF combos confirmed passing (Sharpe ≥ 1.0, WR ≥ 60%, MaxDD ≤ 20%). Full list in `results/overnight/20260506_backtest_report.md`.

Top performers:
- `stat_arb_gold_silver` XAUUSD H4/H1 — Sharpe 3.39–4.66, PF 2.06–3.16
- `ema_ribbon_trend` AAPL/USTEC/US500/MSFT H4 — Sharpe 3.17–10.18
- `macd_trend` USDJPY H4, USTEC H4, GBPJPY H4 — Sharpe 3.41–6.34
- `gold_momentum_breakout` XAUUSD/US500/AAPL/MSFT H4 — Sharpe 0.91–5.38
- `range_breakout` XAUUSD H4, USOIL H4 — Sharpe 2.34–4.76
- `rsi_pullback` XAUUSD/GBPUSD/EURUSD/XAGUSD H4 — Sharpe 2.23–3.09
- `hikkake_trap` XAUUSD H4 — Sharpe 4.58

### Notifications & UI
- ✅ Telegram bot (`scripts/start_telegram_bot.py`) — trade alerts, signal notifications
- ✅ React dashboard (`webapp/frontend/`) — equity curve, positions, trade history
- ✅ FastAPI backend (`webapp/api/`) — REST endpoints for dashboard
- ✅ Scheduler (`scheduler/`) — 11 automated background jobs (daily backtest, data sync, etc.)

### Infrastructure
- ✅ Docker compose — PostgreSQL + backend + scheduler + frontend
- ✅ Python venv rebuilt (Python 3.14.3, 40+ packages)
- ✅ Config system — `config/config.yaml` (18 pairs, per-pair cost model) + `config/strategies.yaml`
- ✅ Overnight backtest pipeline — automated nightly runs generating `results/overnight/YYYYMMDD_backtest_report.md`
- ✅ Recommendation engine — produces `results/recommendations/YYYYMMDD_recommendations.md` with tuning hints
- ✅ Demotion tracker — flags strategies at ≥6 consecutive fails for escalation

---

## What Is In Progress

### Phase 2B — Path B Medium Wins (60% done)
- ✅ Regime classifier exists and is wired in `risk/regime_classifier.py`
- ⏳ Multi-timeframe confirmation not fully wired into paper engine
- ⏳ Regime filter not yet gating scalping strategies (crypto/M15 pairs)

**Target:** Reduce false signals by 15–20% by adding regime + multi-TF gates to the paper engine signal checker.

### Phase 3A — Strategy Quality Sprint (20% done)
From the 2026-05-06 recommendations, the immediate task list is:

**Escalations to action now:**
- Disable `macd_trend` EURUSD H4 (6 consecutive fails, Sharpe -2.48)
- Disable `cot_sentiment` GBPUSD D1 (6 consecutive fails)
- Disable `cot_sentiment` USDJPY D1 (6 consecutive fails, 50.6% max drawdown)

**Directional bias quick fixes (13 combos) — disable the losing direction in `strategies.yaml`:**
- `hikkake_trap` GBPUSD H4: disable LONG
- `dual_ema_momentum` US500 H4: disable SHORT
- `ma_crossover` GBPUSD H4: disable LONG
- `macd_trend` US500 H4: disable SHORT
- `orb` GBPUSD/EURUSD M15: disable SHORT
- Full list in `results/agent_handover_20260506.md` Section 6

**Near-PASS tuning (P3 — 5 combos):**
- `session_momentum` XAUUSD/GBPJPY/GBPUSD H1 — tighten entry filter (ADX min up + session gate)
- `range_breakout` US500 H4 — ATR filter + TP mult
- `dual_ema_momentum` XAUUSD H1 — add higher-TF bias check

**Critical bug to investigate:**
- `stat_arb_gold_silver` XAUUSD M15 — 186.7% max drawdown (likely position sizing bug in `risk/manager.py` for this combo)

---

## What Is Planned (Not Started)

### Phase 3B — Infrastructure Hardening

#### 3B-1: Apache Kafka Live Stream Integration
Replace the current poll-based data model with a streaming architecture for near-real-time paper trading signals. Full design in `docs/guides/KAFKA_INTEGRATION_PLAN.md`.

**Current latency:** ~60 seconds (scheduler heartbeat interval)  
**Target latency after Kafka:** < 5 seconds tick-to-signal

Key components:
- MT5 tick producer → `kafka/producer.py`
- OHLCV aggregator (M1 candle builder from ticks) → `kafka/aggregator.py`
- Strategy signal consumer → `kafka/signal_consumer.py`
- PostgreSQL sync consumer (replaces `data/ingestion.py` in live mode) → `kafka/db_sink.py`

#### 3B-2: Observability Stack (from `docs/v3/OBSERVABILITY.md`)
- Prometheus metrics exporter on paper engine
- Grafana dashboards for strategy P&L, signal latency, order fill rate
- Alerting on circuit breaker triggers, MT5 disconnects, data staleness

#### 3B-3: V3 Script Modularisation (from `docs/v3/ORCHESTRATION_V3.md`)
- Migrate to `scripts/core/`, `scripts/automation/`, `scripts/data/`, `scripts/backtest/` structure
- Shared libraries in `scripts/lib/` (logger, db_client, config_loader)
- Parquet caching for backtest data
- Parallel WFO runner

### Phase 4 — Roadmap Items (from `docs/archive/v2_roadmap.md`)
- Auto-tiering: WFO results automatically synced to `strategies.yaml` weekly
- Kelly Criterion position sizing (adaptive, replaces fixed 1% per trade)
- Correlation matrix engine (prevent cluster trades — max 0.8 correlation between concurrent positions)
- HFT data resampling (M1 → H1/H4 aggregation in `ohlc_high_res` table)
- CI/CD pipeline (backtest on every Git push, fail build if Tier 1 PF < 1.0)

### Phase 5 — Paper Run → Live Decision
**Criteria to proceed to live:**
- ≥ 14 days stable paper trading
- Forward test WR ≥ 90% of backtest WR (target: ≥ 63%)
- Max drawdown < 12% in paper mode
- Telegram alerts delivering within 1 minute
- Dashboard equity curve updating in real-time
- Zero Python exceptions in logs during test period
- Circuit breaker confirmed functional (20% DD trigger)
- All magic numbers appearing on MT5 orders
- ESCALATE strategies resolved (disabled or rehabilitated)

---

## Current Metrics Snapshot (as of 2026-05-06)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| PASS combos | 35 / 148 (24%) | 40+ | 🟡 Close |
| REVIEW combos | 90 / 148 (61%) | < 50% | 🔴 Work needed |
| ERROR / SKIP | 23 / 148 (16%) | < 10% | 🟡 Improving |
| System mode | Paper | Paper → Live | ✅ Correct |
| Overnight pipeline | Running nightly | Running | ✅ OK |
| Max drawdown (best PASS) | 0.0–9.5% | < 20% | ✅ OK |
| Best Sharpe (reliable) | 4.66 (stat_arb_gold_silver H4) | > 1.0 | ✅ Strong |
| Escalation queue | 3 strategies | 0 | 🔴 Needs action |
| Near-PASS candidates | 5 combos | 0 (promote all) | 🟡 Actionable |

---

## Risk & Blockers

| Risk | Severity | Mitigation |
|------|----------|------------|
| stat_arb_gold_silver M15 — 186.7% DD | 🔴 High | Investigate `risk/manager.py` position sizing for this combo immediately |
| 3 ESCALATE strategies still active | 🔴 High | Disable in `strategies.yaml` before next overnight run |
| Poll-based data has 60s latency | 🟡 Medium | Phase 3B Kafka integration (reduces to < 5s) |
| Multi-TF confirmation not fully wired | 🟡 Medium | Complete Phase 2B wiring in paper engine |
| venv and .venv both present | 🟡 Low | Verify which is active; remove the stale one |
| Dashboard showing stale backtest data | 🟡 Low | Clear old DB records, restart backend |
| Low trade count on crypto D1 | 🟢 Low | Extend backtest window, not a live risk |

---

## Recommended Sprint Order (Next 2 Weeks)

**Week 1 (2026-05-12 to 2026-05-19) — Strategy Quality**
1. Disable 3 ESCALATE strategies in `strategies.yaml`
2. Investigate stat_arb_gold_silver M15 drawdown bug
3. Apply 13 directional bias fixes (disable losing direction per combo)
4. Run P3 optimisation on 5 Near-PASS session_momentum combos
5. Complete Phase 2B: wire multi-TF confirmation into paper engine

**Week 2 (2026-05-19 to 2026-05-26) — Infrastructure & Observation**
1. Begin Phase 3B-1: Kafka integration design + MT5 tick producer prototype
2. Set up Prometheus/Grafana observability stack
3. Monitor paper trading metrics daily (WR, DD, signal count)
4. Extend backtest windows for 11 P2 combos with < 10 trades

**Week 3–4 (2026-05-26 onwards) — Paper Run & Go-Live Gate**
1. Sustained paper trading observation
2. Weekly performance review against go-live criteria
3. Go/no-go decision on live trading
4. If approved: change `mode: paper` → `mode: live` in `config.yaml`

---

## File Reference Map

| Document | Location | Purpose |
|----------|----------|---------|
| This file | `docs/core/MASTER_PROJECT_STATUS.md` | Primary check gate document |
| Agent handover (May 6) | `results/agent_handover_20260506.md` | Detailed task list from overnight report |
| Latest recommendations | `results/recommendations/20260506_recommendations.md` | Full tuning hints |
| Latest backtest report | `results/overnight/20260506_backtest_report.md` | Raw overnight results |
| Strategy config | `config/strategies.yaml` | Enable/disable strategies and parameters |
| System config | `config/config.yaml` | Pairs, risk settings, system mode |
| Kafka integration plan | `docs/guides/KAFKA_INTEGRATION_PLAN.md` | Streaming architecture (new) |
| V3 orchestration | `docs/v3/ORCHESTRATION_V3.md` | Script modularisation plan |
| Roadmap (Phase 4–5) | `docs/archive/v2_roadmap.md` | Kelly, correlation matrix, CI/CD |
| Architecture | `docs/core/ARCHITECTURE.md` | System architecture overview |

---

*Check Gate #1 — 2026-05-12. Next review at go-live decision or 2026-06-01, whichever comes first.*
