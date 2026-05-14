# TradePanel Daily Automation — Agent Schedule v2.0

Execute the TradePanel daily automation suite. All bash commands run in the Linux sandbox.

**System mode:** LIVE (config.yaml: `system.mode: live` — confirmed go-live 2026-05-10)

**Pass thresholds (single source of truth):** WR >= 70% AND Sharpe >= 2.0

**WFO OOS thresholds:** Sharpe >= 1.5 AND WR >= 65% AND Trades >= 10 per window

**Strategy portfolio:** 44 strategies across 18 pairs (expanded from 3 paper strategies at go-live)

---

## FULL SCHEDULE CONTEXT

| Job | SAST | UTC | Days |
|-----|------|-----|------|
| Data ingest | 02:05/08:05/14:05/20:05 | 00:05/06:05/12:05/18:05 | Daily |
| Signal outcome check | 01:00 | 23:00 prev | Daily |
| Overnight backtest | 04:00 | 02:00 | Mon–Fri |
| **This automation (Cowork)** | **06:04** | **04:04** | **Daily** |
| Scheduler readiness report | 06:04 | 04:04 | Daily (Telegram brief — complements this) |
| WFO bi-weekly | 05:00 | 03:00 | Wed+Sun |
| Daily summary (Telegram) | 20:00 | 18:00 | Daily |
| Weekly report (Telegram) | 10:00 Mon | 08:00 Mon | Weekly |
| Correlation check | 11:00 Mon | 09:00 Mon | Weekly |
| COT refresh | 23:00 | 21:00 | Friday |
| Yahoo history fill | 03:30 Sun | 01:30 Sun | Weekly |
| Weekly archive | 01:59 Fri | 23:59 Thu | Weekly |
| Account snapshot | every 15m | every 15m | Always |
| MT5 history sync | every 4h | every 4h | Always |
| DB cleanup | 02:30 Sun | 00:30 Sun | Weekly |

**Note:** The scheduler sends its own morning Telegram brief at 04:04 UTC via `_send_readiness_report`.
This Cowork automation runs at the same time and is the deeper analytical layer — it reads files,
calls APIs, writes the dashboard JSON, and surfaces anything requiring Leo's attention.

---

## STEP 0 — DETECT REPO PATH (always run first)

```bash
find /sessions -maxdepth 3 -name "TradePanel" -type d 2>/dev/null | grep -v ".git\|venv\|__pycache__" | head -1
```

Store this as REPO (e.g. `/sessions/awesome-stoic-allen/mnt/TradePanel`).
Use $REPO in place of any hardcoded path in every step below.

---

## STEP 1 — DETECT RUNTIME ENVIRONMENT & CONTAINER HEALTH

```bash
docker ps --format "{{.Names}}\t{{.Status}}\t{{.RunningFor}}" 2>/dev/null | grep tradepanel
```

**Expected containers (8 total in live stack):**

| Container | Purpose | Critical? |
|-----------|---------|-----------|
| `tradepanel-db` | PostgreSQL 16 | ✅ CRITICAL |
| `tradepanel-backend` | FastAPI :8000 | ✅ CRITICAL |
| `tradepanel-frontend` | React SPA :3000 (Nginx) | ⚠️ WARN if down |
| `tradepanel-scheduler` | APScheduler jobs | ✅ CRITICAL |
| `tradepanel-telegram` | Telegram bot | ✅ CRITICAL |
| `tradepanel-waha` | WhatsApp via WAHA :8025 | ⚠️ WARN if down |
| `tradepanel-db-backup` | DB backup daemon | ⚠️ WARN if down |
| `tradepanel-adminer` | DB admin UI :8090 | ℹ️ INFO only |

- If `tradepanel-backend` AND `tradepanel-scheduler` appear → **Docker mode**: execute via `docker exec`
- If `tradepanel-backend` is missing → **CRITICAL ALERT**: backend is down, no trades executing
- Otherwise → **File mode**: skip execution steps, read result files only

---

## STEP 2 — SYSTEM HEALTH CHECK (replaces old manual checks)

```bash
curl -s http://localhost:8000/api/health 2>/dev/null
```

This single endpoint covers three subsystems:
- **postgresql**: live DB query status (READY / OFFLINE)
- **mt5_bridge**: based on HEARTBEAT rows in `bot_health` table (ONLINE if < 5 min ago)
- **event_bus**: FastAPI EventBus listener running flag

Also check the circuit breaker state — a paused circuit breaker means zero trades are firing:

```bash
curl -s "http://localhost:8000/api/backtests/overnight/status" 2>/dev/null
docker exec tradepanel-backend python -c "
from data.db_client import DBClient
db = DBClient()
rows = db.execute_query(\"SELECT status, message, timestamp FROM bot_health WHERE event_type='CIRCUIT_BREAKER' ORDER BY timestamp DESC LIMIT 1\")
if rows: print('CB_STATUS:', rows[0][0], '|', rows[0][1], '| at', rows[0][2])
else: print('CB_STATUS: NO_ENTRY (normal)')
" 2>/dev/null
```

**CRITICAL alert if CB status = 'PAUSED'** — trading is halted, requires `/resume` Telegram command or manual DB clear.

File mode: skip execution, proceed to Step 3.

---

## STEP 3 — RUN DAILY VALIDATION (Docker mode only)

```bash
docker exec tradepanel-backend python scripts/daily_validation_suite.py --quick 2>&1 | tail -60
```

File mode: skip, proceed to Step 4.

---

## STEP 4 — CHECK LATEST VALIDATION RESULTS

```bash
ls -lt $REPO/results/daily_validation/ | head -10
tail -80 $REPO/results/validation_daily.log 2>/dev/null
```

Read the newest `dashboard_*.json`. Extract: total strategies, pass count, fail count, pass rate, WARN/FAIL entries, last run timestamp.

---

## STEP 5 — READ LATEST RECOMMENDATIONS REPORT

```bash
ls -lt $REPO/results/recommendations/ | head -5
```

Read the latest `*_recommendations.md` in full. Summarise:

- **Regressions** (PASS → REVIEW) — flag immediately, these need same-session action
- **New PASSes** — highlight (WR >= 70% AND Sharpe >= 2.0)
- **WFO Validation Status section** — note which strategies are WFO PASS vs WFO FAIL vs WFO ERROR
- **Near-PASS** (Sharpe >= 1.2) — top 3 candidates with exact blocker
- **P1 critical** — Sharpe < 0 or MaxDD > 20% — disable these today
- **Removal queue** — any strategy with consecutive_fails >= 6

If the directory is empty or the latest report is > 7 days old, note that — the engine generates a new report after each overnight backtest via `_run_recommendations()`.

---

## STEP 6 — LIVE ACCOUNT STATUS

Call the dashboard API (Docker mode):

```bash
curl -s http://localhost:8000/api/accounts 2>/dev/null
curl -s "http://localhost:8000/api/accounts/1/kpis?lookback_days=1" 2>/dev/null
```

Also check the Prometheus metrics endpoint for a fast account pulse:

```bash
curl -s http://localhost:8000/api/metrics 2>/dev/null | grep -E "tradepanel_account_(equity|balance|drawdown|floating)"
```

Check account_metrics table freshness (updated every 15 min by account_snapshot job):

```bash
docker exec tradepanel-backend python -c "
from data.db_client import DBClient
from datetime import datetime
db = DBClient()
rows = db.execute_query('SELECT timestamp, equity, balance, drawdown_pct, active_positions FROM account_metrics ORDER BY timestamp DESC LIMIT 1')
if rows:
    age_mins = (datetime.now() - rows[0][0]).total_seconds() / 60
    print(f'Last snapshot: {rows[0][0]} | Age: {age_mins:.1f} min | Equity: {rows[0][1]} | Balance: {rows[0][2]} | DD: {rows[0][3]}% | Positions: {rows[0][4]}')
else:
    print('NO account_metrics rows — snapshot job may not have run yet')
" 2>/dev/null
```

Extract and report:
- Current balance and equity (ZAR)
- Floating P&L (ZAR) and realised P&L today (ZAR)
- Daily drawdown % — **WARN if > 10%, CRITICAL if > 15%**
- Open position count
- **ALERT if account_metrics last snapshot > 30 min old** (snapshot job may be stuck)

File mode: read the most recent `dashboard_*.json` in `results/daily_validation/` for last known values.

---

## STEP 7 — CHECK SIGNAL TAKE RATE

```bash
curl -s "http://localhost:8000/api/papertrades/signals?lookback_hours=24&limit=200" 2>/dev/null
```

Calculate and report:
- Total signals fired in last 24h
- Taken count (signal_taken = true) and take rate %
- Breakdown by account (use account_name field)
- Breakdown by strategy (top 5 most active)
- **Alert if take rate < 20%** — could indicate MT5 execution failing silently, circuit breaker active, or risk manager blocking all entries

Note: The `/api/papertrades/` prefix is retained even in live mode (historical naming convention).

File mode: note as unavailable if API unreachable.

---

## STEP 8 — CHECK OPEN POSITIONS

```bash
curl -s "http://localhost:8000/api/papertrades/trades?status=OPENED&limit=20" 2>/dev/null
```

List any open positions: pair, direction, entry price, lot size, strategy, time open.
Note if any position has been open > 48h (possible stale/stuck trade).

---

## STEP 9 — SYSTEM HEALTH: TELEGRAM + WHATSAPP + EVENT BUS

```bash
# Telegram bot last activity
tail -10 $REPO/logs/telegram_bot.log 2>/dev/null

# WhatsApp (WAHA) session status
curl -s http://localhost:8025/api/sessions/default 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('WAHA status:', d.get('status','UNKNOWN'), '| engine:', d.get('engine',{}).get('state','?'))" 2>/dev/null

# WhatsApp router health
curl -s http://localhost:8000/api/whatsapp/status 2>/dev/null

# Recent errors
grep -E "ERROR|CRITICAL|EXCEPTION" $REPO/logs/main.log 2>/dev/null | tail -15
```

**Telegram health check:**
- Last entry > 24h ago → **CRITICAL: Telegram bot may be offline — trade alerts not reaching Leo**
- Log empty or missing → note as unknown

**WhatsApp health check (NEW):**
- WAHA session status should be `WORKING`
- If `STOPPED` or `FAILED` → **WARN: WhatsApp notifications offline**
- Note: WhatsApp is the secondary notification channel (Telegram is primary)

**Event bus** is confirmed via `/api/health` response (Step 2). A non-running event bus means circuit breaker events won't propagate — flag as CRITICAL.

---

## STEP 10 — CHECK OVERNIGHT BACKTEST

```bash
ls -lt $REPO/results/overnight/ | head -5
```

Read the most recent `*_backtest_report.md` (canon daily file — not test/variant files). Note:
- PASS count, REVIEW count, ERROR count, date
- **Alert if PASS count < 15** (healthy 44-strategy portfolio should produce 15+ passes at 70% WR / Sharpe 2.0)
- **Alert if report > 48h old** (backtest may have failed silently — Mon–Fri only)
- **Alert if ERROR count > 5**

Also check via API:
```bash
curl -s "http://localhost:8000/api/backtests/overnight/status" 2>/dev/null
```

---

## STEP 11 — CHECK WFO RESULTS

```bash
ls -lt $REPO/results/wfo/ | head -5
head -60 $REPO/results/wfo_master_summary.md 2>/dev/null
```

Also check live WFO status from DB:
```bash
curl -s http://localhost:8000/api/wfo/status 2>/dev/null
```

Summarise the most recent WFO run:
- Which strategies have WFO PASS (OOS Sharpe >= 1.5, WR >= 65%, Trades >= 10, >= 70% of windows passing)?
- Which strategies have WFO FAIL — flag these: do NOT promote to live even if overnight backtest says PASS
- Note date of last WFO run — **alert if > 14 days old** (WFO runs automatically Wed + Sun at 03:00 UTC via `wfo_biweekly` job)

**If WFO is stale or broken, trigger manually (Docker mode only):**
```bash
# Full suite — all enabled strategies (~30-90 min):
docker exec tradepanel-backend python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20

# Single strategy (faster, for spot-checking):
docker exec tradepanel-backend python scripts/run_wfo_all.py --strategy stat_arb_gold_silver

# With more windows for high-trade-count strategies:
docker exec tradepanel-backend python scripts/run_wfo_all.py --n_windows 5 --is_pct 0.70 --oos_pct 0.20
```

**WFO interpretation:**
- **WFO PASS** = OOS validated → safe to increase lot size or promote to live
- **WFO FAIL** = Fails OOS gate → treat as REVIEW regardless of overnight backtest status
- **WFO ERROR** = Missing data or deps (yaml/psycopg2) → re-run manually after fixing deps
- OOS Sharpe < 0 on any window → strategy may be overfit; diagnose before enabling
- 0 OOS trades → data gap or strategy too restrictive; check pair data freshness

---

## STEP 12 — CHECK STRATEGY INTELLIGENCE

```bash
curl -s "http://localhost:8000/api/intelligence/best-strategies?limit=15" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
if isinstance(data, list):
    for s in data[:5]:
        print(f\"{s.get('strategy','?')} | {s.get('symbol','?')} | Maturity: {s.get('maturity',0)} | Sharpe: {s.get('sharpe',0):.2f} | WR: {s.get('win_rate',0):.1f}%\")
else:
    print(data)
" 2>/dev/null
```

Report:
- Top 5 strategies by maturity score and Sharpe
- Note if `strategy_intelligence` table is empty (will use WFO fallback — normal for first run)
- Flag any strategy with maturity score > 10 but Sharpe < 1.0 (degrading performer, review tweaks)

---

## STEP 13 — CHECK COT DATA FRESHNESS

```bash
docker exec tradepanel-backend python -c "
from data.db_client import DBClient
db = DBClient()
rows = db.execute_query('SELECT MAX(report_date) FROM cot_data')
print('Latest COT report_date:', rows[0][0] if rows else 'NO DATA')
" 2>/dev/null
```

File mode alternative:
```bash
grep -i "cot" $REPO/logs/main.log 2>/dev/null | tail -5
```

**Alert if COT data is more than 8 days old** — `cot_sentiment` strategy fires on stale data. COT releases every Friday 15:30 EST; auto-refresh job runs Friday 21:00 UTC via `cot_refresh`.

---

## STEP 14 — CHECK REMOVAL COUNTDOWN

```bash
python3 -c "
import json
with open('$REPO/results/demotion_tracker.json') as f:
    data = json.load(f)
high = {k:v for k,v in data.items() if v.get('consecutive_fails',0) >= 4}
import json; print(json.dumps(high, indent=2))
print(f'Total tracked: {len(data)} | Fails>=4: {len(high)} | Fails>=6: {len({k:v for k,v in data.items() if v.get(\"consecutive_fails\",0)>=6})}')
" 2>/dev/null
```

For each entry:
- **Flag RED** if consecutive_fails >= 6 (ESCALATE — disable this combo)
- **Flag AMBER** if consecutive_fails >= 4 (WATCH — tune or investigate)
- Show strategy, pair, TF, fail count, and latest win_rate from history

Also check `recommendations.md` removal queue section for strategies at ESCALATE level.

---

## STEP 15 — WEEKLY JOBS AUDIT (run Monday only, or if flagged stale)

Check the status of weekly jobs that don't produce daily results files:

```bash
# Yahoo history fill — last run Sunday 01:30 UTC
grep -i "yahoo\|history fill" $REPO/logs/main.log 2>/dev/null | tail -5

# Correlation check — last run Monday 09:00 UTC
grep -i "correlation\|Strategy Correlation" $REPO/logs/main.log 2>/dev/null | tail -5

# Weekly archive — last run Thursday 23:59 UTC
grep -i "weekly.*archiv\|archiv.*complet" $REPO/logs/main.log 2>/dev/null | tail -3

# DB backup container log
docker logs tradepanel-db-backup --tail 5 2>/dev/null
```

- **Alert if correlation warning was sent** (strategy pairs > 0.85 correlation) — may need portfolio rebalance
- **Alert if db-backup container last log > 24h old** — backup job may have silently failed

---

## STEP 16 — WRITE DASHBOARD JSON

Write to: `$REPO/results/daily_validation/dashboard_[YYYYMMDD_HHMMSS].json`

Structure:
```json
{
  "last_update": "<ISO timestamp UTC>",
  "runtime_mode": "docker|file",
  "system_mode": "live",
  "pass_thresholds": { "win_rate_pct": 70.0, "sharpe": 2.0 },
  "wfo_thresholds": { "oos_win_rate_pct": 65.0, "oos_sharpe": 1.5, "min_trades": 10, "min_window_pass_pct": 70.0 },
  "system_health": {
    "docker_containers_up": [],
    "docker_containers_missing": [],
    "postgresql": null,
    "mt5_bridge": null,
    "event_bus": null,
    "circuit_breaker_status": null,
    "circuit_breaker_message": null,
    "errors_last_24h": null
  },
  "notifications": {
    "telegram_bot_active": null,
    "telegram_last_message_age_hours": null,
    "whatsapp_waha_status": null,
    "whatsapp_session_state": null
  },
  "account": {
    "balance_zar": null,
    "equity_zar": null,
    "floating_pnl_zar": null,
    "realized_pnl_today_zar": null,
    "daily_drawdown_pct": null,
    "open_positions": null,
    "margin_level_pct": null,
    "account_metrics_age_mins": null
  },
  "signals": {
    "total_24h": null,
    "taken_24h": null,
    "take_rate_pct": null
  },
  "validation_summary": {
    "total_strategies": null,
    "passed": null,
    "failed": null,
    "pass_rate": null
  },
  "overnight_backtest": {
    "last_run_date": null,
    "pass_count": null,
    "review_count": null,
    "error_count": null,
    "report_age_hours": null
  },
  "wfo": {
    "last_run_date": null,
    "age_days": null,
    "wfo_pass_count": null,
    "wfo_fail_count": null,
    "wfo_error_count": null,
    "validated_strategies": []
  },
  "strategy_intelligence": {
    "top_strategies": [],
    "table_populated": null
  },
  "cot_data": { "latest_report_date": null, "age_days": null, "is_stale": null },
  "removal_countdown": { "red_zone": [], "amber_zone": [], "total_tracked": null },
  "recommendations": {
    "report_date": null,
    "regressions": null,
    "improvements": null,
    "near_pass_count": null,
    "p1_critical_count": null,
    "removal_queue_count": null
  },
  "alerts": []
}
```

---

## STEP 17 — ALERT ON ISSUES

Flag clearly (and include in the `alerts` array) if any of these are true:

| Condition | Severity |
|-----------|----------|
| Circuit breaker status = PAUSED | CRITICAL |
| Any regressions in recommendations report | WARN |
| PASS count < 15 in overnight backtest | WARN |
| Overnight backtest report older than 48 hours (weekday) | WARN |
| Any P1 critical issues (Sharpe < 0, MaxDD > 20%) | CRITICAL |
| Signal take rate < 20% | WARN |
| Daily drawdown > 10% | WARN |
| Daily drawdown > 15% | CRITICAL |
| Telegram bot last message > 24h ago | CRITICAL |
| WhatsApp WAHA session not WORKING | WARN |
| COT data older than 8 days | WARN |
| Any strategy in RED removal zone (consecutive_fails >= 6) | WARN |
| tradepanel-backend or tradepanel-scheduler containers down | CRITICAL |
| tradepanel-telegram container down | CRITICAL |
| tradepanel-waha container down | WARN |
| tradepanel-db-backup container down | WARN |
| Event bus not running (from /api/health) | CRITICAL |
| MT5 bridge status OFFLINE (from /api/health) | CRITICAL |
| PostgreSQL status not READY (from /api/health) | CRITICAL |
| account_metrics last snapshot > 30 min old | WARN |
| More than 5 ERROR entries in main.log (24h) | WARN |
| Any position open > 48h | WARN |
| WFO last run > 14 days old | WARN |
| Any overnight PASS strategy has WFO FAIL verdict | WARN |
| Strategy correlation alert logged (pair > 0.85) | WARN |

---

## STEP 18 — WRITE SUMMARY LOG ENTRY

Append to: `$REPO/results/validation_daily.log`

```
[YYYY-MM-DD HH:MM UTC] MODE=docker|file | PASS=n/total | BAL=Rn | EQ=Rn | DD=n% | PNL=Rn | SIG_TAKE=n% | RECO_DATE=YYYYMMDD | REGRESSIONS=n | WFO=ok|stale|n_pass | TG=ok|stale | WA=ok|offline | CB=normal|PAUSED | COT=ok|stale | STATUS=OK|WARN|ALERT|CRITICAL
```

---

## STEP 19 — AI RECOMMENDATIONS (run every session)

After completing all checks, synthesise findings and provide **3–5 actionable recommendations** in priority order. Consider:

1. **Strategy promotions / demotions** — based on combined overnight backtest + WFO verdict. Never promote a WFO FAIL to higher lot size.
2. **Lot size adjustments** — if a strategy is WFO PASS and has >= 10 consecutive live wins, flag it as a candidate for lot increase.
3. **Data freshness issues** — stale COT, Yahoo history, or missing account_metrics snapshots can degrade signal quality.
4. **Notification channel redundancy** — if either Telegram or WhatsApp is offline, flag urgently (both channels must be working for 24/7 live trading).
5. **Circuit breaker hygiene** — if CB was triggered and reset, review the triggering drawdown event and confirm root cause before the next session.
6. **Correlation risk** — if the weekly correlation check flagged pairs > 0.85, suggest which strategy to reduce lot size on to reduce portfolio overlap.
7. **New strategy candidates** — if strategy_intelligence shows a strategy with maturity >= 5, Sharpe >= 2.0, WR >= 70%, and WFO PASS, it is a promotion candidate.

---

## CONSTRAINTS

- **Never execute live trades or modify strategy parameters or config files**
- Never delete result files during automation; active working window = last 3 days
- All timestamps in UTC; display in SAST (UTC+2) for Leo's readability
- If Docker is unavailable and all result files older than 48 hours → STATUS=STALE
- Complete within 12 minutes
- Repo mount path changes each session — always detect via Step 0, never hardcode
- WFO runs automatically Wed + Sun 03:00 UTC via `wfo_biweekly` job in docker_jobs.py — do not trigger manually unless > 14 days stale
- The scheduler sends its own morning Telegram brief (`_send_readiness_report`) at the same 04:04 UTC time — this Cowork automation is the deeper analytical layer and should not duplicate that message
- Traefik `gateway_net` is an external Docker network — if the web UI is unreachable but backend API responds on :8000, the Traefik gateway may be down (out of scope to fix, but flag it)
- Account currency is ZAR; all P&L and balance figures must be displayed in ZAR (not USD)
- In live mode, `mode='PAPER'` queries in the DB still apply (the trades table uses PAPER/LIVE/DEMO mode column — live bot trades may be tagged PAPER in legacy rows; include both)

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-04-28 | Initial schedule — paper trading, 3 strategies, 2 containers |
| v2.0 | 2026-05-13 | Live mode; 8-container stack; WhatsApp/WAHA; circuit breaker; event bus; account_metrics; strategy intelligence; 44 strategies; Prometheus metrics; weekly jobs audit; AI recommendations step |
