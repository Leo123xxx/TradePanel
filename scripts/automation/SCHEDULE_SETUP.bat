@echo off
REM ============================================================================
REM SCHEDULE_SETUP.bat
REM TradePanel V3 — One-click Windows Task Scheduler registration
REM ============================================================================
setlocal
cd /d "%~dp0..\.."
set PROJECT=%cd%

REM ── Handle /delete flag ───────────────────────────────────────────────────
if /i "%1"=="/delete" goto DELETE_TASKS

REM ── Verify running as Administrator ───────────────────────────────────────
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: This script must be run as Administrator.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   TradePanel V3 — Task Scheduler Setup
echo   Project: %PROJECT%
echo ============================================================
echo.

REM ── 1. Daily data sync ───────────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_DATA_SYNC" /tr "%PROJECT%\scripts\automation\RUN_DAILY_DATA_SYNC.bat" ^
    /sc weekly /d MON,TUE,WED,THU,FRI,SUN /st 00:30 /f /rl highest
echo [OK] TRADEPANEL_DATA_SYNC  — Mon-Fri + Sun @ 00:30

REM ── 2. Overnight backtest ────────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_OVERNIGHT" /tr "%PROJECT%\scripts\automation\RUN_OVERNIGHT_BACKTEST.bat" ^
    /sc weekly /d MON,TUE,WED,THU,FRI /st 01:00 /f /rl highest
echo [OK] TRADEPANEL_OVERNIGHT  — Mon-Fri @ 01:00

REM ── 3. WFO Monday ────────────────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_WFO_MON" /tr "%PROJECT%\scripts\automation\RUN_WFO_AND_UPDATE.bat" ^
    /sc weekly /d MON /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WFO_MON    — Monday @ 01:30

REM ── 4. WFO Wednesday ─────────────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_WFO_WED" /tr "%PROJECT%\scripts\automation\RUN_WFO_AND_UPDATE.bat" ^
    /sc weekly /d WED /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WFO_WED    — Wednesday @ 01:30

REM ── 5. Full weekend maintenance ──────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_WEEKEND" /tr "%PROJECT%\scripts\automation\RUN_FULL_WEEKEND.bat" ^
    /sc weekly /d SAT /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WEEKEND    — Saturday @ 01:30

echo.
echo [OK] All V3 tasks registered.
echo.
pause
exit /b 0

:DELETE_TASKS
echo Removing all TRADEPANEL_ scheduled tasks...
for %%t in (TRADEPANEL_DATA_SYNC TRADEPANEL_OVERNIGHT TRADEPANEL_WFO_MON TRADEPANEL_WFO_WED TRADEPANEL_WEEKEND) do (
    schtasks /delete /tn "%%t" /f >nul 2>&1 && echo   [REMOVED] %%t || echo   [NOT FOUND] %%t
)
echo Done.
pause
