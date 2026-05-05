@echo off
REM ============================================================================
REM RUN_FULL_WEEKEND.bat
REM TradePanel — Saturday deep maintenance (Saturday @ 01:30)
REM
REM Step 1: Update market data from MT5          (~2 min)
REM Step 2: Walk-Forward Optimisation — all 18   (~60 min)
REM Step 3: Parameter optimizer — all strategies (~60 min)
REM Step 4: Generate agent handover report       (~1 min)
REM
REM Total runtime: ~2-3 hours
REM ============================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

echo.
echo ============================================================
echo   TradePanel ^| Saturday Full Maintenance
echo   %DATE%  %TIME%
echo ============================================================

REM ── STEP 1: Data Update ───────────────────────────────────────────────────
echo.
echo [1/4] Updating market data from MT5...
python scripts\update_market_data.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Data update failed (code %ERRORLEVEL%). Continuing with existing data.
)

REM ── STEP 2: WFO — all strategies ─────────────────────────────────────────
echo.
echo [2/4] Running WFO on all enabled strategies...
python scripts\run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] WFO runner exited with errors. Check output above.
)

REM ── STEP 3: Parameter Optimizer ──────────────────────────────────────────
echo.
echo [3/4] Running parameter optimizer on all enabled strategies...
python scripts\param_optimizer.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Param optimizer exited with errors. Check output above.
)

REM ── STEP 4: Generate agent handover ──────────────────────────────────────
echo.
echo [4/4] Generating agent handover report...
python scripts\generate_agent_handover.py
if %ERRORLEVEL% NEQ 0 (
    echo  [WARNING] Handover generator failed. Check output above.
)

echo.
echo ============================================================
echo   Saturday maintenance complete.
echo   Results:
echo     WFO      : results\wfo_master_summary.md
echo     Handover : results\agent_handover_%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%.md
echo   %DATE%  %TIME%
echo ============================================================
echo.

REM Open handover report
for /f "tokens=1-3 delims=/" %%a in ("%DATE%") do set YMD=%%c%%b%%a
if exist "results\agent_handover_%YMD%.md" (
    start "" "results\agent_handover_%YMD%.md"
)
pause
