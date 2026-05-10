---
name: daily-tradepanel-automation
description: Daily TradePanel health check — account P&L, signals, backtest results, WFO, COT freshness, removal countdown, Telegram health
---

Execute the TradePanel daily automation suite. All bash commands run in the Linux sandbox.

**Pass thresholds (single source of truth):** WR >= 70% AND Sharpe >= 2.0

---

## STEP 0 — DETECT REPO PATH (always run first)

```bash
find /sessions -maxdepth 3 -name "leo123xxx--TradePanel" -type d 2>/dev/null | head -1
```

Store this as REPO (e.g. `/sessions/peaceful-happy-shannon/mnt/leo123xxx--TradePanel`).
Use $REPO in place of any hardcoded path in every step below.

---

## STEP 1 — DETECT RUNTIME ENVIRONMENT

```bash
docker ps --format "{{.Names}}" 2>/dev/null | grep -E "tradepanel-(backend|scheduler)" | head -5
```

- If `tradepanel-backend` or `tradepanel-scheduler` appear → **Docker mode**: run Python commands via `docker exec tradepanel-backend python ...`
- Otherwise → **File mode**: skip execution, read result files only.

---

## STEP 2 — RUN DAILY VALIDATION (Docker mode only)

```bash
docker exec tradepanel-backend python scripts/daily_validation_suite.py --quick 2>&1 | tail -60
```

File mode: skip, proceed to Step 3.

---

## STEP 3 — CHECK LATEST VALIDATION RESULTS

```bash
ls -lt $REPO/results/daily_validation/ | head -10
tail -80 $REPO/results/validation_daily.log 2>/dev/null
```

Read the newest `visualization_*.json`. Extract: total strategies, pass count, fail count, pass rate, WARN/FAIL entries, last run timestamp.

---

## STEP 4 — READ LATEST RECOMMENDATIONS REPORT

```bash
ls -lt $REPO/results/recommendations/ | head -5
```

Read the latest `*_recommendations.md` in full. Summarise:
- **Regressions** (PASS → REVIEW) — flag immediately, these need same-session action
- **New PASSes** — highlight (WR >= 70% AND Sharpe >= 2.0)
- **Near-PASS** (Sharpe >= 1.2) — top 3 candidates with exact blocker
- **P1 critical** — Sharpe < 0 or MaxDD > 20% — disable these today
- **Removal queue** — any strategy with consecutive_fails >= 6

If the directory is empty, note that the engine generates its first report after the next overnight backtest.

---

## STEP 5 — CHECK LIVE ACCOUNT STATUS

Call the dashboard API (if Docker mode):

```bash
curl -s http://localhost:8000/api/accounts 2>/dev/null
curl -s "http://localhost:8000/api/accounts/1/kpis?lookback_days=1" 2>/dev/null
```

Extract and report:
- Current balance (ZAR)
- Today's net P&L (ZAR) and % of balance
- Daily drawdown % — alert if > 10%, CRITICAL if > 15%
- Open position count
- Win rate for the day

File mode: read the most recent `dashboard_*.json` in `results/daily_validation/` for last known values.

---

## STEP 6 — CHECK SIGNAL TAKE RATE

```bash
curl -s "http://localhost:8000/api/papertrades/signals?lookback_hours=24&limit=200" 2>/dev/null
```

Calculate and report:
- Total signals fired in last 24h
- Taken count (triggered_trade_id IS NOT NULL) and take rate %
- Breakdown by strategy (top 5 most active)
- **Alert if take rate < 20%** — could indicate MT5 execution failing silently or risk manager blocking all entries

File mode: read signals from DB result files if available, or note as unavailable.

---

## STEP 7 — CHECK OPEN POSITIONS

```bash
curl -s "http://localhost:8000/api/papertrades/trades?status=OPENED&limit=20" 2>/dev/null
```

List any open positions: pair, direction, entry price, lot size, strategy, time open.
Note if any position has been open > 48h (possible stale/stuck trade).

---

## STEP 8 — CHECK SYSTEM HEALTH + TELEGRAM BOT

```bash
# Recent errors
grep -E "ERROR|CRITICAL|EXCEPTION" $REPO/logs/main.log 2>/dev/null | tail -15

# Docker container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}" 2>/dev/null | grep tradepanel

# Telegram bot last activity
tail -10 $REPO/logs/telegram_bot.log 2>/dev/null
```

**Telegram health check**: Look for any log entry in `telegram_bot.log` within the last 24 hours.
- If last entry > 24h ago → **ALERT: Telegram bot may be offline — trade alerts not reaching Leo**
- If log is empty or missing → note as unknown

---

## STEP 9 — CHECK OVERNIGHT BACKTEST

```bash
ls -lt $REPO/results/overnight/ | head -5
```

Read the most recent `*_backtest_report.md`. Note:
- PASS count, REVIEW count, ERROR count, date
- **Alert if PASS count < 15** (threshold: at 70% WR / Sharpe 2.0, healthy system should produce 15+ passes)
- **Alert if report > 48h old** (backtest may have failed silently)
- **Alert if ERROR count > 5**

Also check:
```bash
curl -s "http://localhost:8000/api/backtests/overnight/status" 2>/dev/null
```

---

## STEP 10 — CHECK WFO RESULTS

```bash
ls -lt $REPO/results/wfo/ | head -5
cat $REPO/results/wfo_master_summary.md 2>/dev/null | head -60
```

Summarise the most recent WFO run:
- Which strategies have WFO-validated results?
- Flag any strategy where live/paper WR is diverging >10pp from backtest WR
- Note date of last WFO run — alert if > 14 days old (WFO should run at least biweekly)

---

## STEP 11 — CHECK COT DATA FRESHNESS

```bash
# Check when COT data was last updated in DB (Docker mode)
docker exec tradepanel-backend python -c "
from data.db_client import DBClient
db = DBClient()
rows = db.execute_query('SELECT MAX(report_date) FROM cot_data')
print('Latest COT report_date:', rows[0][0] if rows else 'NO DATA')
" 2>/dev/null
```

File mode alternative — check COT feed log:
```bash
grep -i "cot\|COT" $REPO/logs/main.log 2>/dev/null | tail -5
```

**Alert if COT data is more than 8 days old** — cot_sentiment strategy will be firing on stale positioning data. COT releases every Friday at 15:30 EST; the auto-refresh job runs Friday 21:00 UTC.

---

## STEP 12 — CHECK REMOVAL COUNTDOWN

```bash
cat $REPO/results/demotion_tracker.json 2>/dev/null
```

Parse the JSON. For each entry:
- Calculate days until removal deadline (if `deadline` field exists)
- **Flag RED** if <= 7 days remaining
- **Flag AMBER** if <= 14 days remaining
- Show consecutive_fails count for any strategy with >= 4 fails

Also check `recommendations.md` removal queue section for strategies at ESCALATE level.

---

## STEP 13 — WRITE DASHBOARD JSON

Write to: `$REPO/results/daily_validation/dashboard_[YYYYMMDD_HHMMSS].json`

```json
{
  "last_update": "<ISO timestamp UTC>",
  "runtime_mode": "docker|file",
  "pass_thresholds": { "win_rate_pct": 70.0, "sharpe": 2.0 },
  "account": {
    "balance_zar": null,
    "daily_pnl_zar": null,
    "daily_drawdown_pct": null,
    "open_positions": null
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
  "system_health": {
    "docker_containers_up": [],
    "errors_last_24h": null,
    "telegram_bot_active": null,
    "telegram_last_message_age_hours": null
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
    "age_days": null
  },
  "cot_data": {
    "latest_report_date": null,
    "age_days": null,
    "is_stale": null
  },
  "removal_countdown": {
    "red_zone": [],
    "amber_zone": []
  },
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

## STEP 14 — ALERT ON ISSUES

Flag clearly (and include in the `alerts` array) if any of these are true:

| Condition | Severity |
|-----------|----------|
| Any regressions in recommendations report | WARN |
| PASS count < 15 in overnight backtest | WARN |
| Overnight backtest report older than 48 hours | WARN |
| Any P1 critical issues (Sharpe < 0, MaxDD > 20%) | CRITICAL |
| Signal take rate < 20% | WARN |
| Daily drawdown > 10% | WARN |
| Daily drawdown > 15% | CRITICAL |
| Telegram bot last message > 24h ago | CRITICAL |
| COT data older than 8 days | WARN |
| Any strategy in RED removal zone (< 7 days) | WARN |
| Docker containers expected but not running | CRITICAL |
| More than 5 ERROR entries in main.log (24h) | WARN |
| Any position open > 48h | WARN |

---

## STEP 15 — WRITE SUMMARY LOG ENTRY

Append to: `$REPO/results/validation_daily.log`

```
[YYYY-MM-DD HH:MM UTC] MODE=docker|file | PASS=n/total | BAL=Rn | PNL=Rn | SIG_TAKE=n% | RECO_DATE=YYYYMMDD | REGRESSIONS=n | TELEGRAM=ok|stale | COT=ok|stale | STATUS=OK|WARN|ALERT|CRITICAL
```

---

## CONSTRAINTS

- Never execute live trades or modify strategy parameters or config files
- Never delete result files; keep last 14 days minimum
- All timestamps in UTC; display in SAST (UTC+2) for Leo's readability
- If Docker is unavailable and all result files are older than 48 hours → STATUS=STALE
- Complete within 12 minutes
- Repo mount path changes each session — always detect via Step 0, never hardcode
