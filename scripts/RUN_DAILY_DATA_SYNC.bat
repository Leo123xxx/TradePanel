@echo off
REM ============================================================================
REM RUN_DAILY_DATA_SYNC.bat
REM TradePanel — Quick incremental data sync (Mon-Fri @ 00:30, Sun @ 21:00)
REM Pulls latest M1 bars from MT5 and resamples to all timeframes.
REM Runtime: ~2 minutes.
REM ============================================================================
setlocal
cd /d "%~dp0.."

REM ── Guard: require venv ───────────────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [ERROR] venv not found. Run SETUP_VENV.bat first to create the environment.
    echo         This is why you are seeing "No module named yaml/psycopg2" errors.
    exit /b 1
)
call venv\Scripts\activate.bat

echo.
echo [%DATE% %TIME%] TradePanel - Daily Data Sync
echo.

python scripts\update_market_data.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Data sync failed with code %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

echo.
echo [%DATE% %TIME%] Data sync complete.
