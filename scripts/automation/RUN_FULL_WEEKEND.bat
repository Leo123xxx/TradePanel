@echo off
REM ============================================================================
REM RUN_FULL_WEEKEND.bat
REM TradePanel V3 — Weekend deep maintenance
REM ============================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found.
    exit /b 1
)

echo.
echo ============================================================
echo   TradePanel V3 ^| Saturday Full Maintenance
echo   %DATE%  %TIME%
echo ============================================================

REM ── STEP 1: Data Update ───────────────────────────────────────────────────
echo.
echo [1/5] Updating market data from MT5...
python scripts\data\update_market_data.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Data update failed. Continuing...
)

REM ── STEP 2: Yahoo Finance CFD history fill ───────────────────────────────
echo.
echo [2/5] Filling CFD history from Yahoo Finance...
python scripts\data\pull_yahoo_history.py --d1-years 10
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Yahoo history fill failed. Continuing...
)

REM ── STEP 3: WFO — all strategies ─────────────────────────────────────────
echo.
echo [3/5] Running WFO on all enabled strategies...
python scripts\backtest\run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] WFO runner exited with errors.
)

REM ── STEP 4: V3 Near-Pass Optimization ─────────────────────────────────────
echo.
echo [4/5] Running V3 Parallel Near-Pass Optimization...
python scripts\backtest\optimization\optimize_near_pass.py --extended
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] V3 Optimization exited with errors.
)

REM ── STEP 5: Database Maintenance ──────────────────────────────────────────
echo.
echo [5/5] Performing DB cleanup and weekly archive...
python scripts\maintenance\weekly_archive.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Weekly archive failed.
)

echo.
echo ============================================================
echo   Saturday maintenance complete.
echo   Check results\reports\ for new validation and WFO summaries.
echo   %DATE%  %TIME%
echo ============================================================
echo.
pause
