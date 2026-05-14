Execute the TradePanel daily automation suite. All bash commands run in the Linux sandbox.



**Pass thresholds (single source of truth):** WR >= 70% AND Sharpe >= 2.0

**WFO OOS thresholds:** Sharpe >= 1.5 AND WR >= 65% AND Trades >= 10 per window



## SCHEDULE CONTEXT

This task runs at 06:04 SAST (04:04 UTC) daily — after the overnight backtest completes (~04:00–05:30 SAST Mon–Fri). Active results window = last 3 days.



| Job | SAST | UTC | Days |

|-----|------|-----|------|

| Data ingest | 02:05/08:05/14:05/20:05 | 00:05/06:05/12:05/18:05 | Daily |

| Signal outcome check | 01:00 | 23:00 prev | Daily |

| Overnight backtest | 04:00 | 02:00 | Mon–Fri |

| **This automation** | **06:04** | **04:04** | **Daily** |

| WFO bi-weekly | 05:00 | 03:00 | Wed+Sun |

| COT refresh | 23:00 | 21:00 | Friday |

| DB cleanup | 02:30 | 00:30 | Sunday |



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



Read the newest `dashboard_*.json`. Extract: total strategies, pass count, fail count, pass rate, WARN/FAIL entries, last run timestamp.



---



## STEP 4 — READ LATEST RECOMMENDATIONS REPORT



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

- Taken count (signal_taken = true) and take rate %

- Breakdown by account (use account_name field)

- Breakdown by strategy (top 5 most active)

- **Alert if take rate < 20%** — could indicate MT5 execution failing silently or risk manager blocking all entries



Note: Each signal includes account_name and account_type showing which account executed the trade. Untaken signals show account_name = "—".



File mode: note as unavailable if API unreachable.



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



Read the most recent `*_backtest_report.md` (canon daily file — not test/variant files). Note:

- PASS count, REVIEW count, ERROR count, date

- **Alert if PASS count < 15** (at 70% WR / Sharpe 2.0, a healthy system should produce 15+ passes)

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

head -60 $REPO/results/wfo_master_summary.md 2>/dev/null

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



## STEP 11 — CHECK COT DATA FRESHNESS



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



**Alert if COT data is more than 8 days old** — cot_sentiment strategy fires on stale data. COT releases every Friday 15:30 EST; auto-refresh job runs Friday 21:00 UTC.



---



## STEP 12 — CHECK REMOVAL COUNTDOWN



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



## STEP 13 — WRITE DASHBOARD JSON



Write to: `$REPO/results/daily_validation/dashboard_[YYYYMMDD_HHMMSS].json`



Structure:

```json

{

  "last_update": "<ISO timestamp UTC>",

  "runtime_mode": "docker|file",

  "pass_thresholds": { "win_rate_pct": 70.0, "sharpe": 2.0 },

  "wfo_thresholds": { "oos_win_rate_pct": 65.0, "oos_sharpe": 1.5, "min_trades": 10, "min_window_pass_pct": 70.0 },

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

    "age_days": null,

    "wfo_pass_count": null,

    "wfo_fail_count": null,

    "wfo_error_count": null,

    "validated_strategies": []

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

| Any strategy in RED removal zone (consecutive_fails >= 6) | WARN |

| Docker containers expected but not running | CRITICAL |

| More than 5 ERROR entries in main.log (24h) | WARN |

| Any position open > 48h | WARN |

| WFO last run > 14 days old | WARN |

| Any overnight PASS strategy has WFO FAIL verdict | WARN |



---



## STEP 15 — WRITE SUMMARY LOG ENTRY



Append to: `$REPO/results/validation_daily.log`



```

[YYYY-MM-DD HH:MM UTC] MODE=docker|file | PASS=n/total | BAL=Rn | PNL=Rn | SIG_TAKE=n% | RECO_DATE=YYYYMMDD | REGRESSIONS=n | WFO=ok|stale|n_pass | TELEGRAM=ok|stale | COT=ok|stale | STATUS=OK|WARN|ALERT|CRITICAL

```



---



## CONSTRAINTS



- Never execute live trades or modify strategy parameters or config files

- Never delete result files during automation; active working window = last 3 days

- All timestamps in UTC; display in SAST (UTC+2) for Leo's readability

- If Docker is unavailable and all result files older than 48 hours → STATUS=STALE

- Complete within 12 minutes

- Repo mount path changes each session — always detect via Step 0, never hardcode

- WFO runs automatically Wed + Sun 03:00 UTC via `wfo_biweekly` job in docker_jobs.py — do not trigger manually unless > 14 days stale