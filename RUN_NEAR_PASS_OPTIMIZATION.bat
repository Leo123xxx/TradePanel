@echo off
REM
REM RUN_NEAR_PASS_OPTIMIZATION.bat
REM
REM Batch runner for near-pass candidate optimization suite.
REM This runs comprehensive parameter tuning on 8 strategies that are one metric away from PASS status.
REM

setlocal enabledelayedexpansion

echo ====================================================================
echo  NEAR-PASS STRATEGY OPTIMIZATION SUITE
echo ====================================================================
echo.

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)

echo [*] Virtual environment activated
echo.

REM Parse arguments
set "MODE=normal"
set "STRATEGY_FILTER="

if "%1"=="--quick" (
    set "MODE=quick"
    echo [*] Running in QUICK mode (fewer grid points)
) else if "%1"=="--extended" (
    set "MODE=extended"
    echo [*] Running in EXTENDED mode (comprehensive search)
) else if "%1"=="" (
    echo [*] Running in NORMAL mode
)

echo.
echo ====================================================================
echo  OPTIMIZATION STARTING
echo ====================================================================
echo.

REM Run the suite
if "%MODE%"=="quick" (
    python scripts\run_near_pass_suite.py --quick
) else if "%MODE%"=="extended" (
    python scripts\run_near_pass_suite.py --extended
) else (
    python scripts\run_near_pass_suite.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Optimization failed with exit code %errorlevel%
    exit /b 1
)

echo.
echo ====================================================================
echo  OPTIMIZATION COMPLETE
echo ====================================================================
echo.
echo Results available in:
echo   - results\optimization\near_pass_optimization.json (raw data)
echo   - results\optimization\near_pass_report.md (summary report)
echo.
pause
