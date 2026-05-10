@echo off
REM ============================================================================
REM SETUP_VENV.bat
REM TradePanel — Create Python virtual environment and install all dependencies.
REM
REM Run this ONCE after cloning, or any time you see:
REM   "No module named 'yaml'"
REM   "No module named 'psycopg2'"
REM   "No module named 'telegram'"
REM
REM Usage:
REM   SETUP_VENV.bat            — create venv + install requirements
REM   SETUP_VENV.bat /upgrade   — re-install / upgrade all packages
REM   SETUP_VENV.bat /delete    — remove venv (run setup again to rebuild)
REM ============================================================================
setlocal
cd /d "%~dp0.."

REM ── Handle /delete ────────────────────────────────────────────────────────
if /i "%1"=="/delete" goto DELETE_VENV

REM ── Check Python ──────────────────────────────────────────────────────────
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python not found in PATH.
    echo Install Python 3.12 from https://python.org and try again.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo Python found: %PYVER%

REM ── Create venv if it doesn't exist ───────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create venv. Check your Python installation.
        pause
        exit /b 1
    )
    echo [OK] venv created.
) else (
    echo [OK] venv already exists.
)

REM ── Activate ──────────────────────────────────────────────────────────────
call venv\Scripts\activate.bat

REM ── Check Python Version ──────────────────────────────────────────────────
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_FULL_VER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PY_FULL_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)
echo Detected Python version: %PY_MAJOR%.%PY_MINOR%

if %PY_MAJOR% GEQ 3 (
    if %PY_MINOR% GEQ 14 (
        echo.
        echo [!] WARNING: You are using Python %PY_MAJOR%.%PY_MINOR%.
        echo This is an experimental version. We have updated requirements.txt 
        echo to include 2026-compatible wheels for %PY_MAJOR%.%PY_MINOR%.
        echo.
    )
)

REM ── Upgrade pip silently ──────────────────────────────────────────────────
echo.
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM ── Install requirements ──────────────────────────────────────────────────
echo.
echo Installing requirements from requirements.txt...
echo (This may take 2-3 minutes on first run)
echo.
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Some packages failed to install.
    echo Check the errors above. 
    echo TIP: If psycopg2-binary fails with "pg_config not found", 
    echo ensure you have the latest 2026 versions in requirements.txt.
    pause
    exit /b 1
)

REM ── Quick smoke test ──────────────────────────────────────────────────────
echo.
echo Running dependency smoke test...
python -c "import yaml, psycopg2, telegram, pandas, apscheduler, dotenv, yfinance; print('[OK] All core packages imported successfully')"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARN: Smoke test failed — some packages may not have installed correctly.
    echo Check errors above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Setup complete!
echo   venv is ready at: %~dp0venv
echo.
echo   All scheduled tasks (TRADEPANEL_OVERNIGHT etc.) will now
echo   use this venv automatically.
echo.
echo   To activate manually:
echo     call venv\Scripts\activate.bat
echo.
echo   To start all services:
echo     start_all.bat      (native: dashboard + telegram bot)
echo     START_DOCKER.bat   (Docker stack: full backend + scheduler)
echo ============================================================
echo.
pause
exit /b 0

REM ── Delete venv ───────────────────────────────────────────────────────────
:DELETE_VENV
echo Removing venv...
if exist "venv" (
    rmdir /s /q venv
    echo [OK] venv removed. Run SETUP_VENV.bat to rebuild.
) else (
    echo [NOT FOUND] No venv directory found.
)
pause
exit /b 0
