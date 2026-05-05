@echo off
REM ============================================================================
REM RUN_OVERNIGHT_BACKTEST.bat
REM TradePanel — Nightly real-data backtest + demotion gate (Mon-Fri @ 01:00)
REM Validates all enabled strategies on real market data.
REM Sends Telegram summary on completion.
REM Runtime: ~15-20 minutes.
REM ============================================================================
setlocal
cd /d "%~dp0"

REM ── Guard: require venv ───────────────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [ERROR] venv not found. Run SETUP_VENV.bat first to create the environment.
    echo         This is why you are seeing "No module named yaml/psycopg2" errors.
    exit /b 1
)
call venv\Scripts\activate.bat

echo.
echo [%DATE% %TIME%] TradePanel - Overnight Backtest
echo.

python scripts\run_overnight_backtest.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Overnight backtest failed with code %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

echo.
echo [%DATE% %TIME%] Overnight backtest complete.
