@echo off
REM tail_logs.bat — View real-time logs
setlocal enabledelayedexpansion

set TRADEPANEL_DIR=%~dp0
cd /d "%TRADEPANEL_DIR%.."

if not exist "logs" (
    echo ERROR: logs directory not found
    pause
    exit /b 1
)

:menu
echo.
echo ========================================
echo TradePanel Log Viewer
echo ========================================
echo.
echo Select log to view:
echo   1. Main log (main.log)
echo   2. Dashboard log
echo   3. Telegram bot log
echo   4. All logs (list only)
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto log_main
if "%choice%"=="2" goto log_dash
if "%choice%"=="3" goto log_tele
if "%choice%"=="4" goto log_all
if "%choice%"=="5" goto log_exit

echo Invalid choice. Try again.
goto menu

:log_main
echo.
echo Showing main.log (last 50 lines):
echo ========================================
if exist "logs\main.log" (
    powershell -NoProfile -Command "Get-Content -Path 'logs\main.log' -Tail 50"
) else (
    echo main.log not found
)
goto menu

:log_dash
echo.
echo Showing dashboard.log (last 50 lines):
echo ========================================
if exist "logs\dashboard.log" (
    powershell -NoProfile -Command "Get-Content -Path 'logs\dashboard.log' -Tail 50"
) else (
    echo dashboard.log not found
)
goto menu

:log_tele
echo.
echo Showing telegram_bot.log (last 50 lines):
echo ========================================
if exist "logs\telegram_bot.log" (
    powershell -NoProfile -Command "Get-Content -Path 'logs\telegram_bot.log' -Tail 50"
) else (
    echo telegram_bot.log not found
)
goto menu

:log_all
echo.
echo Showing ALL log files:
echo ========================================
dir /b "logs\*.log"
echo.
echo Use options 1-3 to view specific logs.
goto menu

:log_exit
exit /b 0
