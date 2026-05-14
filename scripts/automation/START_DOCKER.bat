@echo off
REM ============================================================================
REM START_DOCKER.bat
REM TradePanel — Start (or restart) the full Docker stack.
REM
REM Services started:
REM   tradepanel-db        PostgreSQL 16.6  (port 5433)
REM   tradepanel-backend   FastAPI backend  (port 8000)
REM   tradepanel-frontend  React/Nginx      (port 3000)
REM   tradepanel-telegram  Telegram bot
REM   tradepanel-scheduler APScheduler (overnight backtests, data sync)
REM   tradepanel-waha      WhatsApp bridge  (port 8025)
REM   tradepanel-adminer   DB admin UI      (port 8090)
REM
REM Usage:
REM   START_DOCKER.bat           — start all containers
REM   START_DOCKER.bat /rebuild  — force image rebuild then start
REM   START_DOCKER.bat /stop     — stop all containers
REM   START_DOCKER.bat /status   — show container status
REM ============================================================================
setlocal
cd /d "%~dp0..\.."

REM ── Check Docker is available ─────────────────────────────────────────────
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker is not running or not installed.
    echo Start Docker Desktop and try again.
    pause
    exit /b 1
)

REM ── Handle flags ──────────────────────────────────────────────────────────
if /i "%1"=="/stop"   goto STOP_CONTAINERS
if /i "%1"=="/status" goto SHOW_STATUS
if /i "%1"=="/rebuild" goto REBUILD

REM ── Check MT5 Bridge (Dependency) ──────────────────────────────────────────
echo Checking MT5 Bridge status...
netstat -ano | findstr :8001 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] MT5 Bridge is NOT running on port 8001.
    echo     Starting it now in background mode...
    call scripts\automation\start_mt5_bridge.bat /background
    echo     Waiting for bridge to initialize...
    timeout /t 5 /nobreak >nul
) else (
    echo [OK] MT5 Bridge is already running.
)

REM ── Default: start ────────────────────────────────────────────────────────
:START
echo.
echo ============================================================
echo   TradePanel — Starting Docker Stack
echo ============================================================
echo.
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: docker-compose up failed.
    echo Check Docker Desktop and docker-compose.yml.
    pause
    exit /b 1
)
goto WAIT_AND_STATUS

REM ── Rebuild images then start ──────────────────────────────────────────────
:REBUILD
echo.
echo ============================================================
echo   TradePanel — Rebuilding images + Starting Docker Stack
echo ============================================================
echo.

REM ── Check MT5 Bridge (Dependency) ──────────────────────────────────────────
echo Checking MT5 Bridge status...
netstat -ano | findstr :8001 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] MT5 Bridge is NOT running on port 8001.
    echo     Starting it now in background mode...
    call scripts\automation\start_mt5_bridge.bat /background
    timeout /t 5 /nobreak >nul
)
docker-compose build --no-cache
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed. Check Dockerfile and requirements.
    pause
    exit /b 1
)
docker-compose up -d
goto WAIT_AND_STATUS

REM ── Wait for DB health then print status ──────────────────────────────────
:WAIT_AND_STATUS
echo.
echo Waiting for database to become healthy...
set /a ATTEMPTS=0
:WAIT_LOOP
timeout /t 3 /nobreak >nul
docker exec tradepanel-db pg_isready -U postgres >nul 2>&1
if %ERRORLEVEL% EQU 0 goto DB_READY
set /a ATTEMPTS+=1
if %ATTEMPTS% GEQ 15 (
    echo WARN: DB not ready after 45s — check tradepanel-db logs.
    goto SHOW_STATUS
)
echo   Waiting... (%ATTEMPTS%/15)
goto WAIT_LOOP

:DB_READY
echo [OK] Database is healthy.

:SHOW_STATUS
echo.
echo ============================================================
echo   Container Status
echo ============================================================
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=tradepanel"
echo.
echo ============================================================
echo   Service URLs
echo ============================================================
echo   Backend API:   http://localhost:8000
echo   Frontend:      http://localhost:3000
echo   DB Admin:      http://localhost:8090
echo   Waha (WA):     http://localhost:8025
echo.
echo   Logs:   docker logs tradepanel-scheduler -f
echo           docker logs tradepanel-backend -f
echo.
goto END

REM ── Stop all containers ───────────────────────────────────────────────────
:STOP_CONTAINERS
echo.
echo Stopping TradePanel containers...
docker-compose down
echo [OK] All containers stopped.

:END
echo.
pause
exit /b 0
