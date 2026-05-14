@echo off
title TradePanel MT5 Bridge
REM ==============================================
REM TradePanel MT5 Bridge - Startup
REM ==============================================

setlocal
cd /d "%~dp0..\.."

echo.
echo [1/2] Verifying dependencies...

REM Use venv if it exists
if exist "venv\Scripts\python.exe" (
    set PY_EXE=.\venv\Scripts\python.exe
    set PYW_EXE=.\venv\Scripts\pythonw.exe
) else (
    set PY_EXE=python
    set PYW_EXE=pythonw
)

%PY_EXE% -m pip install -q fastapi uvicorn pydantic pandas MetaTrader5 python-dotenv pyyaml

if /i "%1"=="/background" (
    echo [OK] Starting MT5 Bridge in background mode...
    start "" %PYW_EXE% mt5_bridge/api_server.py
    exit /b 0
)

echo.
echo [2/2] Starting the MT5 API Server on port 8001...
echo.
%PY_EXE% mt5_bridge/api_server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: MT5 Bridge failed to start. 
    echo Ensure MetaTrader 5 terminal is installed and logged in.
    pause
)
