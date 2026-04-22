@echo off
REM tail_logs.bat — View real-time logs

setlocal enabledelayedexpansion
set TRADEPANEL_DIR=%~dp0
cd /d %TRADEPANEL_DIR%

echo.
echo ========================================
echo TradePanel Log Viewer
echo ========================================
echo.

if not exist "logs" (
    echo ERROR: logs directory not found
    pause
    exit /b 1
)

:menu
echo.
echo Select log to view:
echo   1. Main log (main.py)
echo   2. Dashboard log
echo   3. Telegram bot log
echo   4. All logs (main)
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Showing main.log (last 50 lines):
    echo ========================================
    if exist "logs\main.log" (
        powershell -NoProfile -Command "Get-Content -Path 'logs\main.log' -Tail 50"
    ) else (
        echo main.log not found
    )
) else if "%choice%"=="2" (
    echo.
    echo Showing dashboard.log (last 50 lines):
    echo ========================================
    if exist "logs\dashboard.log" (
        powershell -NoProfile -Command "Get-Content -Path 'logs\dashboard.log' -Tail 50"
    ) else (
        echo dashboard.log not found
    )
) else if "%choice%"=="3" (
    echo.
    echo Showing telegram bot logs:
    echo ========================================
    if exist "logs\telegram_bot.log" (
        powershell -NoProfile -Command "Get-Content -Path 'logs\telegram_bot.log' -Tail 50"
    ) else (
        echo telegram_bot.log not found
    )
) else if "%choice%"=="4" (
    echo.
    echo Showing ALL logs:
    echo ========================================
    dir /b "logs\*.log"
    echo.
    echo All log files listed. Use options 1-3 to view specific logs.
) else if "%choice%"=="5" (
    exit /b 0
) else (
    echo Invalid choice. Try again.
)

goto menu
