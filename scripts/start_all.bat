@echo off
REM start_all.bat — Start all TradePanel services
REM This script starts the dashboard, telegram bot, and optionally runs the daily cycle

setlocal enabledelayedexpansion
set TRADEPANEL_DIR=%~dp0
cd /d %TRADEPANEL_DIR%

echo.
echo ========================================
echo TradePanel Service Startup
echo ========================================
echo.

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
if not exist "results" mkdir results

REM Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ or add it to your PATH
    pause
    exit /b 1
)

echo [%date% %time%] Starting TradePanel services...

REM Start Dashboard in background
echo.
echo Starting Dashboard on port 5000...
start "TradePanel Dashboard" cmd /k python dashboard.py --port 5000
timeout /t 3 /nobreak

REM Start Telegram Bot in background
echo Starting Telegram Bot...
start "TradePanel Telegram Bot" cmd /k python main.py --mode telegram --quiet
timeout /t 2 /nobreak

REM Run daily cycle (optional - comment out if not needed)
REM echo.
REM echo Running daily paper trading cycle...
REM python main.py --mode paper-trade

echo.
echo ========================================
echo Services Started Successfully
echo ========================================
echo.
echo Dashboard:     http://localhost:5000
echo Telegram Bot:  Running (check logs/main.log)
echo.
echo To view logs, run: tail_logs.bat
echo To stop services, run: stop_services.bat
echo.
pause
