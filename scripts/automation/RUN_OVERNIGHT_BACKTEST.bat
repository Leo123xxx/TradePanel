@echo off
REM ============================================================================
REM RUN_OVERNIGHT_BACKTEST.bat
REM TradePanel — Nightly real-data backtest + demotion gate (Mon-Fri @ 01:00)
REM ============================================================================
setlocal
cd /d "%~dp0..\.."

REM ── Guard: require venv ───────────────────────────────────────────────────
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo.
    echo [ERROR] venv not found. Run SETUP_VENV.bat first to create the environment.
    exit /b 1
)

echo.
echo [%DATE% %TIME%] TradePanel V3 - Overnight Backtest
echo.

python scripts\backtest\run_overnight_backtest.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Overnight backtest failed with code %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

echo.
echo [%DATE% %TIME%] Overnight backtest complete.
