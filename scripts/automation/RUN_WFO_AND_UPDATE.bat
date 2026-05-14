@echo off
REM ============================================================================
REM RUN_WFO_AND_UPDATE.bat
REM TradePanel V3 — One-click: Update market data + Run WFO on all strategies
REM ============================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

echo.
echo ============================================================
echo   TradePanel V3 ^| WFO + Data Update Runner
echo   %DATE%  %TIME%
echo ============================================================
echo.

REM ── Activate virtual environment ──────────────────────────────────────────
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found.
    exit /b 1
)

echo.
echo [1/3] Updating market data from MT5...
python scripts\data\update_market_data.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Market data update failed. Continuing...
)

echo.
echo [2/3] Filling CFD history from Yahoo Finance...
python scripts\data\pull_yahoo_history.py --d1-years 10
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Yahoo history fill failed. Continuing...
)

echo.
echo [3/3] Walk-Forward Optimisation - all strategies...
python scripts\backtest\run_wfo_all.py --n_windows 5 --is_pct 0.70 --oos_pct 0.30
if %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] WFO runner failed.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  All done!
echo  WFO results : results\reports\wfo_master_summary.md
echo  %DATE%  %TIME%
echo ============================================================
echo.

if exist "results\reports\wfo_master_summary.md" (
    start "" "results\reports\wfo_master_summary.md"
)

pause
