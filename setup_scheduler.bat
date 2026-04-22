@echo off
REM setup_scheduler.bat — Setup Windows Task Scheduler for TradePanel automation

setlocal enabledelayedexpansion
set TRADEPANEL_DIR=%~dp0
cd /d %TRADEPANEL_DIR%

echo.
echo ========================================
echo TradePanel Windows Task Scheduler Setup
echo ========================================
echo.
echo This will create automated tasks for:
echo   1. Daily paper trading (1:00 AM UTC)
echo   2. Health check every 6 hours
echo   3. Telegram bot (startup)
echo   4. Dashboard (startup)
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script requires Administrator privileges
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Get Python path
for /f "delims=" %%A in ('where python') do set PYTHON_PATH=%%A
if "%PYTHON_PATH%"=="" (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo Using Python: %PYTHON_PATH%
echo Working Directory: %TRADEPANEL_DIR%
echo.

REM Create Task 1: Daily Paper Trading at 1:00 AM UTC
echo Creating Task 1: Daily Paper Trading...
schtasks /create /tn "TradePanel - Paper Trading" /tr "%PYTHON_PATH% \"%TRADEPANEL_DIR%main.py\" --mode paper-trade --quiet" /sc daily /st 01:00 /f
if %errorlevel% equ 0 (
    echo OK: Task created: Daily Paper Trading (1:00 AM UTC)
) else (
    echo ! Task may already exist or error occurred
)

REM Create Task 2: Health Check every 6 hours
echo Creating Task 2: Health Check (every 6 hours)...
schtasks /create /tn "TradePanel - Health Check" /tr "%PYTHON_PATH% \"%TRADEPANEL_DIR%main.py\" --mode health --quiet" /sc hourly /mo 6 /f
if %errorlevel% equ 0 (
    echo OK: Task created: Health Check
) else (
    echo ! Task may already exist or error occurred
)

REM Create Task 3: Telegram Bot at Startup
echo Creating Task 3: Telegram Bot (at startup)...
schtasks /create /tn "TradePanel - Telegram Bot" /tr "%PYTHON_PATH% \"%TRADEPANEL_DIR%main.py\" --mode telegram --quiet" /sc onstart /delay 0000:30 /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo OK: Task created: Telegram Bot
) else (
    echo ! Task may already exist or error occurred
)

REM Create Task 4: Dashboard at Startup
echo Creating Task 4: Dashboard (at startup)...
schtasks /create /tn "TradePanel - Dashboard" /tr "%PYTHON_PATH% \"%TRADEPANEL_DIR%dashboard.py\" --port 5000" /sc onstart /delay 0000:45 /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo OK: Task created: Dashboard
) else (
    echo ! Task may already exist or error occurred
)

echo.
echo ========================================
echo Task Scheduler Setup Complete
echo ========================================
echo.
echo Created tasks:
schtasks /query /tn "TradePanel*" /fo list
echo.
echo To manage tasks:
echo   View:   schtasks /query /tn "TradePanel*"
echo   Run:    schtasks /run /tn "TradePanel - Paper Trading"
echo   Delete: schtasks /delete /tn "TradePanel - Paper Trading" /f
echo.
pause
