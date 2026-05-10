@echo off
REM TradePanel Test Runner
REM Sets up proper environment and runs pytest

setlocal enabledelayedexpansion

REM Activate venv
call venv\Scripts\activate.bat

REM Set PYTHONPATH to project root
set PYTHONPATH=%CD%

REM Run pytest from project root
echo [*] Running pytest from: %CD%
echo [*] PYTHONPATH: %PYTHONPATH%
echo.

python -m pytest tests\ -v --tb=short

echo.
echo Test run complete!
pause
