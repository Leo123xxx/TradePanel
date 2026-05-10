# 📚 TradePanel Command Library & Cheat Sheet

This document serves as the central reference for all commands needed to operate, maintain, and validate the TradePanel system.

---

## 🚀 1. Unified Management (Recommended)
The `trade.bat` script is the primary entry point for managing the entire stack.

| Command | Description |
| :--- | :--- |
| `.\trade.bat start` | Start all services (Docker Stack + MT5 Bridge) |
| `.\trade.bat stop` | Stop all services safely |
| `.\trade.bat status` | Check the health of all containers |
| `.\trade.bat logs` | Tail all service logs in real-time |
| `.\trade.bat rebuild` | Force a rebuild of Docker images and restart |
| `.\trade.bat sync` | Run the daily market data sync |
| `.\trade.bat backtest <strategy> [pair] [tf]` | Run a quick backtest for a specific combo |
| `.\trade.bat backup` | Trigger a manual dual-cloud (R2/S3) backup |
| `.\trade.bat wfo` | Run the full Walk-Forward Optimization suite |

---

## 🏗️ 2. Environment Setup & Maintenance
Run these when setting up a new environment or after major updates.

### One-Time Setup
```bat
REM Initialize virtual environment and install all dependencies
.\scripts\SETUP_VENV.bat

REM Initialize the database schema
.\venv\Scripts\python scripts/setup_db.py
```

### Dependency & Env Fixes
```bat
REM Fix missing YAML/Telegram modules (Common Fix)
.\venv\Scripts\pip install pyyaml python-telegram-bot

REM Verify environment health
.\venv\Scripts\python scripts/check_env.py
.\venv\Scripts\python scripts/check_dependencies.py
```

---

## 📊 3. Market Data Management
Commands to keep your local database in sync with MT5.

| Task | Command |
| :--- | :--- |
| **Quick Sync** | `.\venv\Scripts\python scripts/update_market_data.py` |
| **Check Gaps** | `.\venv\Scripts\python scripts/pull_deep_history.py --check-only` |
| **Fill Gaps** | `.\venv\Scripts\python scripts/pull_deep_history.py --pairs GBPJPY AUDUSD USDCAD` |
| **Full Backfill** | `.\venv\Scripts\python scripts/pull_deep_history.py --start 2019-01-01` |
| **Account Sync** | `.\venv\Scripts\python scripts/sync_mt5_account.py` |

---

## 💾 4. Backup & Infrastructure
The system uses a dedicated backup container to ensure data integrity across Cloudflare R2 and AWS S3.

| Task | Command |
| :--- | :--- |
| **Manual Backup** | `.\trade.bat backup` |
| **Check Backups** | Telegram `/backups` or `ls .\backups\` |
| **Status Check** | `docker-compose ps db-backup` |
| **View Logs** | `docker logs tradepanel-db-backup` |

**Automated Schedules:**
- **Database Backup**: Daily @ `00:05 UTC` (Market Rollover)
- **Overnight Backtest**: Daily @ `02:00 UTC` (Mon-Fri)
- **WFO Master Suite**: Bi-Weekly @ `03:00 UTC` (Wed, Sun)
- **Morning Brief**: Daily @ `08:00 Local` (Telegram Push)

---

## 🧪 5. Backtesting & Optimization
Run these to validate strategy performance.

### Single Backtest (Fast)
```bat
.\venv\Scripts\python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
```

### Overnight Batch Run
```bat
REM Run all Tier 1 combos (Fastest batch)
.\venv\Scripts\python scripts/run_overnight_backtest.py --tier 1 --no-telegram

REM Full run with custom suffix for reports
.\venv\Scripts\python scripts/run_overnight_backtest.py --suffix _post_tune_20260508
```

### Walk Forward Optimization (WFO)
```bat
REM Run WFO for a specific strategy
.\venv\Scripts\python scripts/run_wfo_all.py --strategy stat_arb_gold_silver

REM Full WFO suite (takes 30-90 mins)
.\venv\Scripts\python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
```

---

## ✅ 5. Validation & Health Checks
Use these to "End and Validate" your work before a deployment or weekend.

### System Validation
```bat
REM Run the full health + validation suite (Recommended before 'End')
.\scripts\test_health.bat

REM Run the Daily Validation Suite (Deep strategy check)
.\venv\Scripts\python scripts/daily_validation_suite.py --full
```

### Configuration Validation
```bat
REM Check strategies.yaml for schema errors or missing fields
.\venv\Scripts\python scripts/config_validator.py config/strategies.yaml
```

### Database Status
```powershell
REM Detailed check of DB connectivity and table counts
powershell -ExecutionPolicy Bypass -File .\CHECK_DB_STATUS_FIXED.ps1
```

---

## 🐳 6. Docker Stack Control
Direct control over the containerized infrastructure.

| Action | Command |
| :--- | :--- |
| **Start Stack** | `docker-compose up -d` |
| **Stop Stack** | `docker-compose down` |
| **View Backend Logs** | `docker logs -f tradepanel-backend` |
| **Prune Volumes** | `docker system prune -a --volumes` (CAUTION: Deletes DB data) |

---

## 🛠️ 7. Troubleshooting & Cleanup
| Issue | Command |
| :--- | :--- |
| **Encoding Errors** | Fix `scripts/run_wfo_all.py` to use `encoding='utf-8'` in `open()` calls. |
| **Stale Logs/Docs** | `bash scripts/CLEANUP_OLD_DOCS.sh` |
| **MT5 Connection** | Ensure MT5 is running AND `.\scripts\start_mt5_bridge.bat` is active. |

---

## 🏁 8. Recommended "End of Work" Workflow
When finishing a session, follow these steps to ensure everything is stable:

1.  **Validate Health**: Run `.\scripts\test_health.bat`.
2.  **Verify Backup**: Run `.\trade.bat backup` to ensure latest data is off-site.
3.  **Check Telegram**: Verify no critical alerts in the last hour.
4.  **Git Commit**: `git add . && git commit -m "Master WFO State: Finalized Alpha Injection and Remote Backups"`

---
*Last Updated: 2026-05-09*