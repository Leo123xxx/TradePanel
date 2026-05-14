@echo off
REM ============================================================================
REM RUN_DAILY_DATA_SYNC.bat
REM TradePanel V3 - Modular Daily Data Ingestion
REM ============================================================================
setlocal
cd /d "%~dp0..\.."

REM ── Detect Python ─────────────────────────────────────────────────────────
if exist "%~dp0..\..\venv\Scripts\python.exe" (
    set PY_EXE="%~dp0..\..\venv\Scripts\python.exe"
) else if exist "%~dp0..\..\.venv\Scripts\python.exe" (
    set PY_EXE="%~dp0..\..\.venv\Scripts\python.exe"
) else (
    set PY_EXE=python
)

echo.
echo ============================================================
echo   TradePanel V3 — Daily Data Sync
echo ============================================================
echo.

echo [1/3] Pulling new history from Yahoo Finance...
%PY_EXE% -m scripts.data.pull_yahoo_history

echo [2/3] Updating MT5 Market Data...
%PY_EXE% -m scripts.data.update_market_data

echo [3/3] Refreshing Parquet Cache...
%PY_EXE% -m scripts.data.refresh_parquet_cache

echo.
echo [OK] Daily sync complete.
echo.
pause
