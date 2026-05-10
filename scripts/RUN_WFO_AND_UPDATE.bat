@echo off
REM ============================================================================
REM RUN_WFO_AND_UPDATE.bat
REM TradePanel — One-click: Update market data + Run WFO on all strategies
REM
REM Step 1: Update market data from MT5  (incremental — tops up to latest bars)
REM Step 2: Run Walk-Forward Optimisation on all enabled strategies
REM Step 3: Open the WFO summary report
REM
REM Requirements:
REM   - MT5 terminal running and logged in  (needed for Step 1 data pull)
REM   - PostgreSQL running                  (for DB access)
REM   - Python environment with all deps    (venv\Scripts\activate or system Python)
REM
REM Output:
REM   results\wfo_master_summary.md         (WFO results table + per-window detail)
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   TradePanel ^| WFO + Data Update Runner
echo   %DATE%  %TIME%
echo ============================================================
echo.

REM ── Set working directory to project root (where this .bat lives) ──────────
cd /d "%~dp0.."

REM ── Activate virtual environment if present ────────────────────────────────
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found.
    exit /b 1
)
echo [setup] venv activated.

echo.
echo ============================================================
echo  STEP 1 of 2: Updating market data from MT5
echo  Pairs: XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD, BTCUSD, ETHUSD,
echo         GBPJPY, AUDUSD, USDCAD, USDZAR, USOIL, US500, USTEC,
echo         NVDA, AMD, MSFT, AAPL (18 total)
echo  Mode : Incremental (only pulls bars newer than DB)
echo  NOTE : MT5 terminal must be running and logged in.
echo ============================================================
echo.

python scripts\update_market_data.py
set DATA_EXIT=%ERRORLEVEL%

if %DATA_EXIT% NEQ 0 (
    echo.
    echo  [WARNING] Market data update exited with code %DATA_EXIT%.
    echo  Check MT5 connection. WFO will proceed using existing DB data.
    echo.
) else (
    echo.
    echo  [OK] Market data update complete.
    echo.
)

echo.
echo ============================================================
echo  STEP 2 of 3: Yahoo Finance CFD history fill
echo  Pairs  : NVDA, AMD, MSFT, AAPL, US500, USTEC, USOIL
echo  H1     : up to 729 days  (resampled to H1/H2/H4)
echo  D1     : 10 years of daily bars
echo  NOTE   : No MT5 needed. ON CONFLICT DO NOTHING - safe to re-run.
echo ============================================================
echo.

python scripts\pull_yahoo_history.py --d1-years 10
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [WARNING] Yahoo history fill exited with errors. WFO will proceed using existing data.
    echo.
) else (
    echo.
    echo  [OK] Yahoo history fill complete.
    echo.
)

echo.
echo ============================================================
echo  STEP 3 of 3: Walk-Forward Optimisation - all strategies
echo  Config : 5 windows ^| IS=70%% ^| OOS=30%%
echo  Pairs  : All 18 pairs across active strategies
echo  Combos : ~60 runs (multi-pair validation)
echo  ETA    : 45-120 minutes depending on data size
echo ============================================================
echo.

python scripts\run_wfo_all.py --n_windows 5 --is_pct 0.70 --oos_pct 0.30
set WFO_EXIT=%ERRORLEVEL%

if %WFO_EXIT% NEQ 0 (
    echo.
    echo  [ERROR] WFO runner exited with code %WFO_EXIT%.
    echo  Check the output above for details.
    echo.
    pause
    exit /b %WFO_EXIT%
)

echo.
echo ============================================================
echo  All done!
echo.
echo  Market data : updated (or used existing if MT5 unavailable)
echo  Yahoo fill  : CFD history topped up (NVDA/AMD/MSFT/AAPL/US500/USTEC/USOIL)
echo  WFO results : results\wfo_master_summary.md
echo.
echo  %DATE%  %TIME%
echo ============================================================
echo.

REM ── Open the summary report in the default markdown viewer / notepad ────────
if exist "results\wfo_master_summary.md" (
    echo Opening results\wfo_master_summary.md ...
    start "" "results\wfo_master_summary.md"
)

pause
