@echo off
REM ============================================================================
REM trade.bat - Unified Management CLI for TradePanel
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

if /i "%CMD%"=="start"   goto START
if /i "%CMD%"=="stop"    goto STOP
if /i "%CMD%"=="restart" goto RESTART
if /i "%CMD%"=="status"  goto STATUS
if /i "%CMD%"=="logs"    goto LOGS
if /i "%CMD%"=="rebuild" goto REBUILD
if /i "%CMD%"=="backtest" goto BACKTEST
if /i "%CMD%"=="sync"    goto SYNC
if /i "%CMD%"=="backup"  goto BACKUP
if /i "%CMD%"=="wfo"     goto WFO

echo Unknown command: %CMD%
goto USAGE

:START
echo Starting all TradePanel services...
call "%~dp0scripts\START_DOCKER.bat"
goto END

:STOP
echo Stopping all TradePanel services...
call "%~dp0scripts\stop_services.bat"
call "%~dp0scripts\START_DOCKER.bat" /stop
goto END

:RESTART
echo Restarting all TradePanel services...
call "%~dp0scripts\stop_services.bat"
call "%~dp0scripts\START_DOCKER.bat" /stop
call "%~dp0scripts\START_DOCKER.bat"
goto END

:STATUS
call "%~dp0scripts\START_DOCKER.bat" /status
goto END

:LOGS
call "%~dp0scripts\tail_logs.bat"
goto END

:REBUILD
echo Rebuilding and restarting TradePanel...
call "%~dp0scripts\START_DOCKER.bat" /rebuild
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
%PY_EXE% -m scripts.run_backtest --strategy %ARG2% --pair !BT_PAIR! --timeframe !BT_TF!
goto END

:SYNC
echo Running daily data sync...
call "%~dp0scripts\RUN_DAILY_DATA_SYNC.bat"
goto END

:BACKUP
echo Triggering manual database backup...
docker exec tradepanel-db-backup /app/scripts/db_backup.sh
goto END

:WFO
echo Starting Walk-Forward Optimization suite...
docker exec -it tradepanel-backend python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
goto END

:USAGE
echo.
echo TradePanel Management CLI
echo.
echo Usage: trade.bat ^<command^> [args]
echo.
echo Commands:
echo   start     Start all services (Docker + MT5 Bridge)
echo   stop      Stop all services
echo   restart   Restart all services
echo   status    Show container status
echo   logs      Tail all service logs
echo   rebuild   Force rebuild and restart containers
echo   sync      Run daily data sync
echo   backtest  Run a backtest (e.g. trade.bat backtest dual_ema_fractal EURUSD H1)
echo   backup    Trigger a manual dual-cloud backup
echo   wfo       Run full Walk-Forward Optimization suite
echo.
goto END

:END
exit /b 0
