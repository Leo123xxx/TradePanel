@echo off
REM ============================================================================
REM SCHEDULE_SETUP.bat
REM TradePanel — One-click Windows Task Scheduler registration
REM
REM Run this ONCE as Administrator to register all scheduled tasks.
REM All tasks run under the current user account.
REM
REM Schedule created:
REM   TRADEPANEL_DATA_SYNC        Mon-Fri + Sun @ 00:30  (daily data top-up)
REM   TRADEPANEL_OVERNIGHT        Mon-Fri       @ 01:00  (nightly backtest)
REM   TRADEPANEL_WFO_MON          Monday        @ 01:30  (weekly WFO)
REM   TRADEPANEL_WFO_WED          Wednesday     @ 01:30  (mid-week WFO)
REM   TRADEPANEL_WEEKEND          Saturday      @ 01:30  (full maintenance)
REM
REM To remove all tasks: run with argument /delete
REM   SCHEDULE_SETUP.bat /delete
REM ============================================================================
setlocal
cd /d "%~dp0"
set PROJECT=%~dp0

REM ── Handle /delete flag ───────────────────────────────────────────────────
if /i "%1"=="/delete" goto DELETE_TASKS

REM ── Verify running as Administrator ───────────────────────────────────────
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: This script must be run as Administrator.
    echo Right-click SCHEDULE_SETUP.bat and choose "Run as administrator".
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   TradePanel — Task Scheduler Setup
echo   Project: %PROJECT%
echo ============================================================
echo.

REM ── 1. Daily data sync: Mon-Fri @ 00:30 ──────────────────────────────────
schtasks /create /tn "TRADEPANEL_DATA_SYNC" /tr "%PROJECT%RUN_DAILY_DATA_SYNC.bat" ^
    /sc weekly /d MON,TUE,WED,THU,FRI,SUN /st 00:30 /f /rl highest
echo [OK] TRADEPANEL_DATA_SYNC  — Mon-Fri + Sun @ 00:30

REM ── 2. Overnight backtest: Mon-Fri @ 01:00 ────────────────────────────────
schtasks /create /tn "TRADEPANEL_OVERNIGHT" /tr "%PROJECT%RUN_OVERNIGHT_BACKTEST.bat" ^
    /sc weekly /d MON,TUE,WED,THU,FRI /st 01:00 /f /rl highest
echo [OK] TRADEPANEL_OVERNIGHT  — Mon-Fri @ 01:00

REM ── 3. WFO Monday @ 01:30 ────────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_WFO_MON" /tr "%PROJECT%RUN_WFO_AND_UPDATE.bat" ^
    /sc weekly /d MON /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WFO_MON    — Monday @ 01:30

REM ── 4. WFO Wednesday @ 01:30 ─────────────────────────────────────────────
schtasks /create /tn "TRADEPANEL_WFO_WED" /tr "%PROJECT%RUN_WFO_AND_UPDATE.bat" ^
    /sc weekly /d WED /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WFO_WED    — Wednesday @ 01:30

REM ── 5. Full weekend maintenance: Saturday @ 01:30 ─────────────────────────
schtasks /create /tn "TRADEPANEL_WEEKEND" /tr "%PROJECT%RUN_FULL_WEEKEND.bat" ^
    /sc weekly /d SAT /st 01:30 /f /rl highest
echo [OK] TRADEPANEL_WEEKEND    — Saturday @ 01:30

echo.
echo ============================================================
echo   All tasks registered. Verify in Task Scheduler:
echo   Start -> Task Scheduler -> Task Scheduler Library
echo   Look for tasks prefixed with TRADEPANEL_
echo.
echo   To remove all tasks run:  SCHEDULE_SETUP.bat /delete
echo ============================================================
echo.
pause
exit /b 0

REM ── Delete all tasks ──────────────────────────────────────────────────────
:DELETE_TASKS
echo Removing all TRADEPANEL_ scheduled tasks...
for %%t in (TRADEPANEL_DATA_SYNC TRADEPANEL_OVERNIGHT TRADEPANEL_WFO_MON TRADEPANEL_WFO_WED TRADEPANEL_WEEKEND) do (
    schtasks /delete /tn "%%t" /f >nul 2>&1 && echo   [REMOVED] %%t || echo   [NOT FOUND] %%t
)
echo Done.
pause
