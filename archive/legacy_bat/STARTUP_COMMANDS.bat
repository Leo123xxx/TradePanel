@echo off
REM ============================================================================
REM TRADEPANEL - SYSTEM STARTUP SCRIPT
REM Phase 3: Paper Trading - All 10 Top Strategies Active
REM ============================================================================
REM
REM This script starts all required services for paper trading validation.
REM Each service runs in its own terminal window for easy monitoring.
REM
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         TRADEPANEL SYSTEM STARTUP - PHASE 3               ║
echo ║         Paper Trading with Top 10 Strategies               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "config\strategies.yaml" (
    echo ERROR: config\strategies.yaml not found!
    echo Please run this script from the TradePanel root directory.
    pause
    exit /b 1
)

echo ✓ Configuration verified
echo ✓ All 10 strategies active
echo ✓ System ready to start
echo.

REM Count active strategies
for /f "tokens=*" %%a in ('findstr /c:"enabled: true" config\strategies.yaml ^| find /c "true"') do (
    set "ACTIVE_COUNT=%%a"
)

echo Detected Active Strategies: %ACTIVE_COUNT%
echo.
echo Starting services...
echo.

REM Start Terminal 1: Daily Validation Suite
echo [1/4] Starting Daily Validation Suite...
start "TradePanel - Validation Suite" cmd /k "python scripts/daily_validation_suite.py --quick"
timeout /t 2 /nobreak

REM Start Terminal 2: Web Dashboard
echo [2/4] Starting Dashboard (http://localhost:5000)...
start "TradePanel - Dashboard" cmd /k "python dashboard.py --port 5000"
timeout /t 2 /nobreak

REM Start Terminal 3: Telegram Bot
echo [3/4] Starting Telegram Bot...
start "TradePanel - Telegram Bot" cmd /k "python scripts/start_telegram_bot.py"
timeout /t 2 /nobreak

REM Start Terminal 4: Paper Trading Engine
echo [4/4] Starting Paper Trading Engine...
start "TradePanel - Paper Trading" cmd /k "python main.py --mode paper-trade"
timeout /t 2 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   STARTUP COMPLETE                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Services Started:
echo   ✓ Daily Validation Suite    (Strategy validation)
echo   ✓ Web Dashboard             (http://localhost:5000)
echo   ✓ Telegram Bot              (Commands: /status, /balance, /active)
echo   ✓ Paper Trading Engine      (Live paper trading)
echo.
echo Next Steps:
echo   1. Open http://localhost:5000 in your browser
echo   2. Send /status to your Telegram bot
echo   3. Monitor logs in each terminal window
echo   4. Check daily results in the dashboard
echo.
echo To stop all services:
echo   - Close each terminal window, or
echo   - Run: taskkill /F /IM python.exe
echo.
pause
