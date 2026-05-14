@echo off
REM ============================================================================
REM trade.bat - V3 Modular Management CLI for TradePanel
REM ============================================================================
setlocal enabledelayedexpansion

set CMD=%1
set ARG2=%2

if "%CMD%"=="" goto USAGE
if "%CMD%"=="help" goto USAGE

REM ── Detect Python ─────────────────────────────────────────────────────────
if exist "%~dp0venv\Scripts\python.exe" (
    set PY_EXE="%~dp0venv\Scripts\python.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set PY_EXE="%~dp0.venv\Scripts\python.exe"
) else (
    set PY_EXE=python
)

REM ── COMMANDS ───────────────────────────────────────────────────────────────

if /i "%CMD%"=="start"      goto START
if /i "%CMD%"=="stop"       goto STOP
if /i "%CMD%"=="restart"    goto RESTART
if /i "%CMD%"=="status"     goto STATUS
if /i "%CMD%"=="logs"       goto LOGS
if /i "%CMD%"=="rebuild"    goto REBUILD
if /i "%CMD%"=="backtest"   goto BACKTEST
if /i "%CMD%"=="sync"       goto SYNC
if /i "%CMD%"=="v3-sync"    goto SYNC
if /i "%CMD%"=="backup"     goto BACKUP
if /i "%CMD%"=="wfo"        goto WFO
if /i "%CMD%"=="v3-opt"     goto V3_OPT
if /i "%CMD%"=="monitor"    goto MONITOR
if /i "%CMD%"=="cleanup"    goto CLEANUP

echo Unknown command: %CMD%
goto USAGE

:START
echo Starting all TradePanel services...
call "%~dp0scripts\automation\START_DOCKER.bat"
goto END

:STOP
echo Stopping all TradePanel services...
call "%~dp0scripts\automation\stop_services.bat"
call "%~dp0scripts\automation\START_DOCKER.bat" /stop
goto END

:RESTART
echo Restarting all TradePanel services...
call "%~dp0scripts\automation\stop_services.bat"
call "%~dp0scripts\automation\START_DOCKER.bat" /stop
call "%~dp0scripts\automation\START_DOCKER.bat"
goto END

:STATUS
call "%~dp0scripts\automation\START_DOCKER.bat" /status
goto END

:LOGS
call "%~dp0scripts\automation\tail_logs.bat"
goto END

:REBUILD
echo Rebuilding and restarting TradePanel...
call "%~dp0scripts\automation\START_DOCKER.bat" /rebuild
goto END

:BACKTEST
if "%ARG2%"=="" (
    echo Usage: trade.bat backtest ^<strategy_name^> [pair] [timeframe]
    exit /b 1
)
set BT_PAIR=%3
if "!BT_PAIR!"=="" set BT_PAIR=XAUUSD
set BT_TF=%4
if "!BT_TF!"=="" set BT_TF=H1

echo Running backtest: %ARG2% on !BT_PAIR! !BT_TF!...
%PY_EXE% -m scripts.backtest.run_backtest --strategy %ARG2% --pair !BT_PAIR! --timeframe !BT_TF!
goto END

:SYNC
echo Running daily data sync (Modular)...
call "%~dp0scripts\automation\RUN_DAILY_DATA_SYNC.bat"
goto END

:BACKUP
echo Triggering manual database backup...
docker exec tradepanel-db-backup /app/scripts/maintenance/db_backup.sh
goto END

:WFO
echo Starting Walk-Forward Optimization suite...
docker exec -it tradepanel-backend python scripts/backtest/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
goto END

:V3_OPT
echo Starting Parallel V3 Optimization...
%PY_EXE% -m scripts.backtest.optimization.optimize_near_pass --extended
goto END

:MONITOR
echo Launching Observability Stack (Grafana/Prometheus)...
echo [INFO] This requires docker-compose.observability.yml to be present.
docker-compose -f docker-compose.observability.yml up -d
goto END

:CLEANUP
echo Running V3 System Cleanup...
%PY_EXE% -m scripts.maintenance.cleanup_and_backup
goto END

:USAGE
echo.
echo TradePanel Management CLI (Version 3)
echo =====================================
echo.
echo Usage: trade.bat ^<command^> [args]
echo.
echo Core Commands:
echo   start      - Start all services (Docker + MT5 Bridge)
echo   stop       - Stop all services
echo   restart    - Restart all services
echo   status     - Show container status
echo   logs       - Tail all service logs
echo   rebuild    - Force rebuild and restart containers
echo.
echo V3 Advanced Commands:
echo   v3-sync    - Run daily data sync (Modular and Optimized)
echo   v3-opt     - Run Parallel Near-Pass Optimization Suite
echo   monitor    - Launch Grafana/Prometheus Observability Stack
echo   cleanup    - Perform DB maintenance and log rotation
echo.
echo Strategy Commands:
echo   backtest   - Run a backtest (e.g. trade.bat backtest rsi_bounce XAUUSD H1)
echo   wfo        - Run full Walk-Forward Optimization suite
echo   backup     - Trigger a manual database backup
echo.
goto END

:END
exit /b 0
