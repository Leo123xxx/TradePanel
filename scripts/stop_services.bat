@echo off
REM stop_services.bat — Stop all TradePanel services

setlocal enabledelayedexpansion
set TRADEPANEL_DIR=%~dp0..
cd /d %TRADEPANEL_DIR%

echo.
echo ========================================
echo Stopping TradePanel Services
echo ========================================
echo.

REM Kill Python processes related to TradePanel
echo Stopping Dashboard...
taskkill /F /FI "WINDOWTITLE eq TradePanel Dashboard" >nul 2>&1

echo Stopping Telegram Bot...
taskkill /F /FI "WINDOWTITLE eq TradePanel Telegram Bot" >nul 2>&1

echo Stopping MT5 Bridge...
taskkill /F /IM pythonw.exe /FI "COMMANDLINE eq *api_server.py*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq TradePanel MT5 Bridge" >nul 2>&1

REM Kill main.py and dashboard.py processes
taskkill /F /IM python.exe /FI "COMMANDLINE eq *main.py*" >nul 2>&1
taskkill /F /IM python.exe /FI "COMMANDLINE eq *dashboard.py*" >nul 2>&1

echo.
echo ========================================
echo Services Stopped
echo ========================================
echo.
echo To restart services, run: start_all.bat
echo.
pause
