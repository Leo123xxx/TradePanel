@echo off
REM ============================================================================
REM RUN_NEAR_PASS_OPTIMIZATION.bat
REM V3 Batch runner for near-pass candidate optimization suite.
REM ============================================================================
setlocal enabledelayedexpansion

echo ====================================================================
echo  NEAR-PASS STRATEGY OPTIMIZATION SUITE (V3 Modular)
echo ====================================================================
echo.

REM Activate virtual environment
if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat"
) else if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat"
)

REM Parse arguments
set "MODE=normal"
if "%1"=="--quick" set "MODE=quick"
if "%1"=="--extended" set "MODE=extended"

echo [*] Mode: %MODE%
echo.

REM Run the suite
if "%MODE%"=="quick" (
    python scripts\backtest\run_near_pass_suite.py --quick
) else if "%MODE%"=="extended" (
    python scripts\backtest\run_near_pass_suite.py --extended
) else (
    python scripts\backtest\run_near_pass_suite.py
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
echo   - results\data\near_pass_optimization.json
echo   - results\reports\near_pass_report.md
echo.
pause
