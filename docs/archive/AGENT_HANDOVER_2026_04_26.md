# TradePanel — Agent Handover Task List
**Created:** 2026-04-26 | **Last updated:** 2026-04-27 (Session 4 — Final)  
**Purpose:** Structured task list tracking all issues resolved before live trading.  
**Current system mode:** `paper` (config/config.yaml → `system.mode: paper`)  
**Account:** Exness ZAR, R180,000 starting balance (~$10k USD)  
**Paper test window:** 2026-04-26 → 2026-05-10 (3 strategies: `stat_arb_gold_silver`, `moving_average_crossover`, `macd_trend`)

---

## Session 4 Summary (2026-04-27) — COMPLETE

All code-level tasks are complete. The system is now fully consolidated, scheduled, and ready for the paper trading evaluation period.

### What was built / fixed this session

| File | Purpose | Status |
|------|---------|--------|
| `scripts/update_market_data.py` | Incremental MT5 → DB data update (M1 pull + resample, all 7 pairs) | ✅ Done |
| `scripts/run_wfo_all.py` | Batch WFO for all 18 enabled strategies → `results/wfo_master_summary.md` | ✅ Done |
| `scripts/generate_agent_handover.py` | Auto-generates daily agent handover from WFO results, demotion tracker, overnight reports | ✅ Done |
| `RUN_WFO_AND_UPDATE.bat` | One-click: data update → WFO → open summary | ✅ Done |
| `RUN_DAILY_DATA_SYNC.bat` | Lightweight daily data sync (Mon–Fri + Sun @ 00:30) | ✅ Done |
| `RUN_OVERNIGHT_BACKTEST.bat` | Overnight backtest runner (Mon–Fri @ 01:00) | ✅ Done |
| `RUN_FULL_WEEKEND.bat` | Full Saturday deep maintenance: data + WFO + optimizer + handover gen | ✅ Done |
| `SCHEDULE_SETUP.bat` | Registers 5 Windows Task Scheduler tasks (run once as Admin) | ✅ Done |
| `data/resampler.py` | Added `resample_and_store()` (was missing — caused ERROR on every TF resample) | ✅ Done |
| `data/ingestion.py` | Added M30/H2/H12/W1 to RESAMPLE_TIMEFRAMES; fixed duplicate gap print | ✅ Done |
| `data/cleaner.py` | Added H2/H12/W1 to TIMEFRAME_DELTAS for gap checker | ✅ Done |
| `config/strategies.yaml` | Repaired truncated file (was cut off at line 840); added 4 missing strategy stubs | ✅ Done |
| `notifications/router.py` | Fixed `get_mode()` bug; added 5 new methods (wfo, demotion, data, toggle, morning brief) | ✅ Done |
| `notifications/telegram_bot.py` | Added /wfo /demotion /data /enable /disable commands; 08:00 morning push | ✅ Done |
| `archive/legacy_scripts/` | 19 legacy/duplicate scripts archived | ✅ Done |
| `archive/legacy_bat/` | 4 old bat files archived | ✅ Done |

---

## How to Run (Live Machine)

### Automated Schedule (runs itself after SCHEDULE_SETUP.bat)

| Day | Time | Task | What runs |
|-----|------|------|-----------|
| Mon–Fri, Sun | 00:30 | TRADEPANEL_DATA_SYNC | `RUN_DAILY_DATA_SYNC.bat` — incremental M1 pull + resample |
| Mon–Fri | 01:00 | TRADEPANEL_OVERNIGHT | `RUN_OVERNIGHT_BACKTEST.bat` — overnight backtest + demotion check |
| Monday | 01:30 | TRADEPANEL_WFO_MON | `RUN_WFO_AND_UPDATE.bat` — data + full WFO |
| Wednesday | 01:30 | TRADEPANEL_WFO_WED | `RUN_WFO_AND_UPDATE.bat` — data + full WFO |
| Saturday | 01:30 | TRADEPANEL_WEEKEND | `RUN_FULL_WEEKEND.bat` — data + WFO + optimizer + handover gen |

### One-click manual runs

```batch
RUN_WFO_AND_UPDATE.bat          # Data sync + full WFO + open summary
RUN_DAILY_DATA_SYNC.bat         # Data only (quick)
RUN_OVERNIGHT_BACKTEST.bat      # Overnight backtest only
RUN_FULL_WEEKEND.bat            # Full deep maintenance
```

### Step-by-step (manual control)

```bash
# Update market data (incremental, all 7 pairs, M1 + all TFs)
python scripts/update_market_data.py

# Run WFO on all 18 enabled strategies
python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20

# Re-run a single strategy WFO
python scripts/run_wfo_all.py --strategy moving_average_crossover

# Generate agent handover doc
python scripts/generate_agent_handover.py
```

---

## Active Timeframes (as of Session 4)

All 9 derived timeframes are now populated from M1:

| TF | Resample Rule | Use |
|----|--------------|-----|
| M5 | 5min | Short-term signal confirmation |
| M15 | 15min | ORB, session momentum |
| M30 | 30min | VWAP momentum combos |
| H1 | h | Primary strategy timeframe |
| H2 | 2h | Bridges H1/H4; 2-session cycles |
| H4 | 4h | Swing entries |
| H12 | 12h | Half-day context; fills H4→D1 gap |
| D1 | D | Daily trend / COT |
| W1 | W | Weekly macro / COT strategy |

---

## Telegram Bot Commands (updated Session 4)

| Command | What it does |
|---------|-------------|
| `/status` | Account balance, equity, drawdown |
| `/positions` | Open positions |
| `/trades` | Recent trade history |
| `/pnl` | P&L summary |
| `/signals` | Current strategy signals |
| `/backtest` | Last overnight backtest result |
| `/mode` | Active strategies (reads `enabled: true` in yaml) |
| `/report` | Full daily report |
| `/health` | System health check |
| `/pause` | Pause all trading |
| `/resume` | Resume trading |
| `/risk` | Current risk parameters |
| `/drawdown` | Drawdown details |
| `/correlation` | Correlation matrix |
| `/wfo` | **NEW** — WFO pass/fail summary from wfo_master_summary.md |
| `/demotion` | **NEW** — Demotion tracker: consecutive fail counts per strategy |
| `/data` | **NEW** — Market data coverage: latest bar per pair/TF, staleness flag |
| `/enable <name>` | **NEW** — Enable a strategy in strategies.yaml |
| `/disable <name>` | **NEW** — Disable a strategy in strategies.yaml |
| `/help` | Full command list |

**Morning push:** Bot sends a morning brief at 08:00 daily (account status + overnight backtest summary).

---

## WFO Configs (all 18 strategies)

| Strategy | Combo 1 | Combo 2 |
|----------|---------|---------|
| moving_average_crossover | EURUSD H1 | GBPUSD H4 |
| rsi_bounce | EURUSD H1 | XAUUSD H4 |
| gold_momentum_breakout | XAUUSD H4 | GBPUSD H4 |
| macd_trend | EURUSD H1 | USDJPY H4 |
| range_breakout | XAUUSD H4 | EURUSD H1 |
| bb_mean_reversion | XAUUSD H4 | EURUSD H1 |
| stoch_divergence | EURUSD H1 | USDJPY H4 |
| stat_arb_gold_silver | XAUUSD H4 | XAUUSD D1 |
| ema_ribbon_trend | XAUUSD H4 | BTCUSD H4 |
| cot_sentiment | XAUUSD D1 | EURUSD D1 |
| session_momentum | XAUUSD H1 | GBPUSD M30 |
| turtle_soup | EURUSD H4 | XAUUSD D1 |
| dual_ema_momentum | XAUUSD H4 | EURUSD H1 |
| dual_ema_fractal | EURUSD H1 | XAUUSD H4 |
| vwap_momentum | EURUSD M30 | XAUUSD H1 |
| hikkake_trap | XAUUSD H4 | EURUSD H1 |
| orb | XAGUSD M15 | EURUSD M15 |
| rvgi_cci_confluence | EURUSD H1 | GBPUSD H4 |

---

## Go-Live Acceptance Criteria (review on 2026-05-10)

From `config/strategies.yaml` header:

- Forward test WR >= 90% of backtest WR
- Forward test Sharpe >= 0.8
- No more than 3 consecutive losing days
- Max drawdown in forward test < 12%

**After forward test passes:** set `system.mode: live` in `config/config.yaml` and re-enable all 18 strategies.

---

## Completion Checklist (all sessions)

> Last audited: 2026-04-27 — Session 4 Final

| # | Task | Priority | Status | Notes |
|---|------|----------|--------|-------|
| 1.1 | Disable all 6 M1/M5 scalpers in strategies.yaml | CRITICAL | ✅ DONE | Moved to `disabled_pending_review`; `enabled: false` on each |
| 1.2 | Root-cause scalper optimizer/real-data mismatch | CRITICAL | ✅ DONE | Optimizer ran M5 synthetic; backtest ran M1 real. Fixed: `SCALPER_MIN_TF_MINS=5` guard in `param_optimizer.py` |
| 2.1 | Fix range_breakout drawdown (XAUUSD H4/D1) | CRITICAL | ✅ DONE | D1 removed from timeframes; XAUUSD `sl_atr_mult: 0.7` override applied |
| 2.2 | Fix dual_ema_fractal drawdown (XAUUSD D1) | CRITICAL | ✅ DONE | XAUUSD override: `tp_atr_mult=3.0`, `sl_atr_mult=0.8` |
| 3.1 | Diagnose dual_ema_fractal 0/3 WFO failure | CRITICAL | ✅ DONE | Confirmed 0/3 on EURUSD H1. Demoted to Tier 2 in `strategies.yaml` |
| 3.2 | WFO for all active strategies | CRITICAL | ✅ DONE | `scripts/run_wfo_all.py` created — batch runs all 18 enabled strategies |
| 4.1 | Ingest M30/H2/H12/W1 data for all pairs | CRITICAL | ✅ DONE | All 4 TFs added to `RESAMPLE_TIMEFRAMES` in `data/ingestion.py`; resample rules added to `_get_resample_rule()` |
| 4.2 | Fix `resample_and_store()` missing method bug | CRITICAL | ✅ DONE | Method was entirely absent from `DataResampler`; added — was writing to wrong table too |
| 5.1 | DB ThreadedConnectionPool + retry wrapper | HIGH | ✅ DONE | `ThreadedConnectionPool(2,20)` + 3-attempt backoff (2s/4s/8s) in `data/db_client.py` |
| 5.2 | Log rotation (RotatingFileHandler) | HIGH | ✅ DONE | `RotatingFileHandler(10MB, 5 backups)` on all log files |
| 5.3 | Weekly correlation check (was monthly) | HIGH | ✅ DONE | `scheduler/jobs.py` → `CronTrigger(day_of_week="mon", hour=9)` |
| 5.4 | WFO auto-demotion gate | HIGH | ✅ DONE | File-based tracker in `run_overnight_backtest.py`. 5 consecutive days WR < 50% → auto-demote. State in `results/demotion_tracker.json` |
| 6.1 | Enable use_multi_tf_confirmation | HIGH | ✅ DONE | `config.yaml` → `use_multi_tf_confirmation: true` |
| 7.1 | Telegram ALLOWED_CHAT_IDS whitelist | HIGH | ✅ DONE | `@auth_required` on all handlers; `ALLOWED_CHAT_IDS` from `.env` |
| 8.1 | Paper trading — 3 strategies only | HIGH | ✅ DONE | 15 strategies paused; active: `stat_arb_gold_silver`, `moving_average_crossover`, `macd_trend` |
| 8.2 | Go-live acceptance criteria documented | HIGH | ✅ DONE | See criteria in `config/strategies.yaml` header and above |
| 9.1 | Re-optimize or disable rsi_pullback | MEDIUM | ✅ DONE | `enabled: false` in `strategies.yaml` (54.5% WR below 60% threshold) |
| 10.1 | Add results/logs to .gitignore | MEDIUM | ✅ DONE | `results/overnight/`, `results/daily_validation/*.json/.csv` active exclusions |
| 11 | Create batch WFO runner for all strategies | HIGH | ✅ DONE | `scripts/run_wfo_all.py` — reads yaml, name-translates, runs all 18, writes summary |
| 12 | Create market data updater script | HIGH | ✅ DONE | `scripts/update_market_data.py` — wraps `data/ingestion.py`, incremental sync |
| 13 | Create one-click Windows batch runner | MEDIUM | ✅ DONE | `RUN_WFO_AND_UPDATE.bat` — data update → WFO → open summary |
| 14 | Create full automated schedule | HIGH | ✅ DONE | 5 Task Scheduler tasks via `SCHEDULE_SETUP.bat`; daily sync, overnight backtest, Mon/Wed WFO, Sat deep maintenance |
| 15 | Consolidate scripts (archive legacy/duplicates) | MEDIUM | ✅ DONE | 19 scripts → `archive/legacy_scripts/`, 4 bat files → `archive/legacy_bat/` |
| 16 | Telegram bot — new commands + morning push | HIGH | ✅ DONE | `/wfo /demotion /data /enable /disable`; 08:00 daily push; `get_mode()` bug fixed |
| 17 | Auto-generate agent handover script | MEDIUM | ✅ DONE | `scripts/generate_agent_handover.py` — reads all results, writes prioritised action list |
| 18 | Fix `get_mode()` stale `active:` list bug | HIGH | ✅ DONE | Router now iterates strategy defs checking `enabled: True` directly |
| 19 | Repair truncated `config/strategies.yaml` | CRITICAL | ✅ DONE | File was cut at line 840; completed `triple_macd_scalping` + added 3 missing disabled stubs |

---

## Remaining Actions (Live Machine Only)

| Priority | Action | Command | When |
|----------|--------|---------|------|
| 🔴 HIGH | Activate Windows Task Scheduler (run ONCE as Administrator) | `Right-click SCHEDULE_SETUP.bat → Run as administrator` | Now |
| 🔴 HIGH | Review `results/wfo_master_summary.md` after WFO completes — demote any strategy with < 70% WFO pass rate | Manual review | After WFO finishes |
| 🟡 HIGH | Run generate_agent_handover.py after WFO to get a structured action list | `python scripts/generate_agent_handover.py` | After WFO finishes |
| 🟢 MEDIUM | Commit all changes to git | `git add -A && git commit -m "feat: session4 — schedule, consolidation, telegram improvements, timeframe expansion"` | Anytime |
| 🟢 MEDIUM | On 2026-05-10: review forward test results and flip to live if criteria met | Set `system.mode: live` in config.yaml | 2026-05-10 |

---

## Active Script Inventory (post-consolidation)

### scripts/ (20 files — all active)
```
run_wfo_all.py              — Batch WFO runner for all 18 strategies
update_market_data.py       — Incremental data sync from MT5
generate_agent_handover.py  — Auto-generates handover doc from results
run_walk_forward.py         — Single strategy WFO (used by run_wfo_all.py)
run_overnight_backtest.py   — Overnight backtest + demotion check
run_backtest.py             — Manual single backtest runner
param_optimizer.py          — Strategy parameter optimizer
run_paper_trading.py        — Paper trading entry point
generate_daily_report.py    — Daily report generator
generate_correlation.py     — Correlation matrix generator
validate_data.py            — Data validation runner
check_strategy_health.py    — Strategy health checker
export_results.py           — Results exporter
monitor_positions.py        — Live position monitor
send_morning_brief.py       — Manual morning brief trigger
run_stat_arb.py             — Stat-arb specific runner
run_cot.py                  — COT strategy runner
run_vwap.py                 — VWAP strategy runner
check_mt5_connection.py     — MT5 connection checker
reset_paper_balance.py      — Paper balance reset utility
```

### Batch files (9 active, 4 archived)
```
RUN_WFO_AND_UPDATE.bat      — Manual: data + WFO + open summary
RUN_DAILY_DATA_SYNC.bat     — Scheduled @ 00:30 Mon-Fri,Sun
RUN_OVERNIGHT_BACKTEST.bat  — Scheduled @ 01:00 Mon-Fri
RUN_FULL_WEEKEND.bat        — Scheduled @ 01:30 Saturday
SCHEDULE_SETUP.bat          — One-time Admin: registers all 5 Task Scheduler tasks
START_PAPER_TRADING.bat     — Start paper trading session
START_TELEGRAM_BOT.bat      — Start Telegram bot
START_SCHEDULER.bat         — Start APScheduler
STOP_ALL.bat                — Kill all running TradePanel processes
```

---

## Critical Reminder — File Editing on This Machine

**Windows/Linux mount causes .py file truncation** when using text editors or tools that write via the mount.  
Always write Python files via bash heredoc:

```bash
cat > scripts/my_script.py << 'PYEOF'
...python content...
PYEOF
touch scripts/my_script.py   # bust .pyc cache
```

---

## Architecture Quick Reference

```
TradePanel/
├── config/
│   ├── config.yaml             — System config (mode: paper/live, risk, MT5 settings)
│   └── strategies.yaml         — All 24 strategies (18 enabled, 6 disabled)
├── data/
│   ├── ingestion.py            — Full historical pull + resample pipeline
│   ├── resampler.py            — M1 → M5/M15/M30/H1/H2/H4/H12/D1/W1
│   ├── cleaner.py              — Gap detection, OHLC integrity, zero-volume
│   └── db_client.py            — PostgreSQL pool + retry (ThreadedConnectionPool)
├── mt5_bridge/
│   ├── connector.py            — MT5 connect/disconnect
│   └── data_feed.py            — pull_historical_data(), pull_latest_bars(), get_data_range()
├── strategies/                 — 24 strategy modules
├── backtesting/                — Backtest engine + WFO (WalkForwardOptimizer)
├── notifications/
│   ├── router.py               — Data fetching for all bot commands
│   └── telegram_bot.py         — Command handlers + 08:00 morning push
├── scheduler/
│   └── jobs.py                 — APScheduler jobs (data sync, overnight, correlation)
├── scripts/                    — 20 active scripts
├── results/
│   ├── wfo_master_summary.md   — Latest WFO results (written by run_wfo_all.py)
│   ├── demotion_tracker.json   — Per-strategy consecutive fail counts
│   └── overnight/              — Daily backtest reports (.gitignored)
├── archive/
│   ├── legacy_scripts/         — 19 archived scripts
│   └── legacy_bat/             — 4 archived bat files
└── *.bat                       — 9 active batch runners
```
