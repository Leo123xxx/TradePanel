@echo off
REM test_health.bat — Run TradePanel health check and validation

setlocal enabledelayedexpansion
set TRADEPANEL_DIR=%~dp0
cd /d %TRADEPANEL_DIR%

echo.
echo ========================================
echo TradePanel System Test
echo ========================================
echo.

REM Test 1: Health Check
echo [1/3] Running Health Check...
echo.
python main.py --mode health
if errorlevel 1 (
    echo.
    echo ERROR: Health check failed
    pause
    exit /b 1
)

REM Test 2: Validation
echo.
echo [2/3] Running Validation Suite...
echo This may take 2-3 minutes...
echo.
python main.py --mode validate
if errorlevel 1 (
    echo.
    echo ERROR: Validation failed
    pause
    exit /b 1
)

REM Test 3: Dashboard Check
echo.
echo [3/3] Checking Dashboard...
python -c "from fastapi import FastAPI; print('OK: FastAPI available')" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: FastAPI not installed
    echo Install with: pip install fastapi uvicorn
) else (
    echo OK: FastAPI available
)

echo.
echo ========================================
echo All Tests Passed!
echo ========================================
echo.
echo Next steps:
echo   1. Start services: start_all.bat
echo   2. View dashboard: http://localhost:5000
echo   3. Test telegram: Send /status to your bot
echo.
pause
