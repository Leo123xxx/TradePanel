# Scheduled Task Update — Pending Manual Apply

**When:** Generated 2026-05-01 by daily automation run  
**Why:** Docker containers confirmed running on host. Sandbox can't reach Docker socket,  
but all Python packages are now installed directly in the sandbox (matching `docker/requirements.docker.txt`).  
The task prompt needs to be updated to stop false "Docker offline" alerts and to run Python directly.

## How to apply

Open a regular (non-scheduled) Claude session and say:
> "Update the daily-tradepanel-automation scheduled task with the prompt below"

Then paste the prompt from the section below.

Alternatively, you can edit the task directly in the Claude desktop app under Scheduled Tasks.

---

## Updated SKILL.md content

```
---
name: daily-tradepanel-automation
description: Daily TradePanel health check, validation, and dashboard report — runs Python directly in the sandbox (packages match Docker image)
---

Execute the TradePanel daily automation suite. All bash commands run in the Linux sandbox.

## STEP 0 — RESOLVE REPO PATH

The session name changes each run. Resolve the repo path dynamically:

\```bash
REPO=$(find /sessions -maxdepth 3 -type d -name "leo123xxx--TradePanel" 2>/dev/null | head -1)
echo "REPO=$REPO"
\```

Use `$REPO` for all subsequent paths.

## STEP 1 — RUNTIME MODE

The sandbox has no Docker socket — always use Direct Python mode. All required packages
(pyyaml, psycopg2-binary, python-telegram-bot, pandas, numpy, scipy, fastapi, pydantic,
apscheduler, yfinance, requests, tradingview_screener) are installed in the sandbox Python
environment and match docker/requirements.docker.txt.

Set MODE=direct for the log entry.

## STEP 2 — RUN DAILY VALIDATION

\```bash
cd "$REPO" && python3 scripts/daily_validation_suite.py --quick 2>&1 | tail -60
\```

Extract from output: total strategies, pass count, fail count, pass rate, any WARN or FAIL entries.

## STEP 3 — CHECK LATEST VALIDATION RESULTS

\```bash
ls -lt "$REPO/results/daily_validation/" | head -15
\```

Read the newest dashboard_*.json. Also read the validation log:

\```bash
tail -80 "$REPO/results/validation_daily.log" 2>/dev/null
\```

## STEP 4 — READ LATEST RECOMMENDATIONS REPORT

This is the most important step for actionable intelligence. Read the most recent recommendations file:

\```bash
ls -lt "$REPO/results/recommendations/" 2>/dev/null | head -5
\```

Then read the latest *_recommendations.md file in full. Summarise:
- Any regressions (PASS → REVIEW) — flag immediately
- Any new PASSes — highlight positively
- Top 3 near-PASS candidates and their recommended actions
- Any P1 critical issues (zero-trades bugs, deeply negative Sharpe)
- Any removal queue entries

## STEP 5 — CHECK SYSTEM HEALTH

\```bash
grep -E "ERROR|CRITICAL" "$REPO/logs/main.log" 2>/dev/null | tail -15
tail -5 "$REPO/logs/telegram_bot.log" 2>/dev/null
\```

Note: Docker container status is not checked from the sandbox — Docker runs on the host.

## STEP 6 — CHECK OVERNIGHT BACKTEST

\```bash
ls -lt "$REPO/results/overnight/" | head -5
\```

Read the most recent backtest report. Flag if older than 48 hours.

## STEP 7 — WRITE DASHBOARD JSON

Write to $REPO/results/daily_validation/dashboard_[YYYYMMDD_HHMMSS].json with runtime_mode: "direct".

## STEP 8 — ALERT ON ISSUES

Flag if:
- Any regressions in the recommendations report
- Pass rate < 10%
- More than 3 ERROR entries in main.log in the last 24 hours
- Overnight backtest report older than 48 hours
- Any P1 critical issues

Do NOT alert on Docker containers not running — Docker is on the host, not in the sandbox.

## STEP 9 — WRITE SUMMARY LOG ENTRY

Append to $REPO/results/validation_daily.log:
[YYYY-MM-DD HH:MM UTC] MODE=direct | PASS=n/total | RECO_DATE=YYYYMMDD | REGRESSIONS=n | STATUS=OK|WARN|ALERT

## CONSTRAINTS
- Never execute live trades or modify strategy parameters
- Never delete result files; keep last 7 days minimum
- All timestamps in UTC
- If all result files are older than 48 hours, set STATUS=STALE
- Complete within 10 minutes
```
