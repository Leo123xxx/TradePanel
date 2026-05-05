# TradePanel — Agent Handover: Docker Containerisation
**Created:** 2026-04-28 | **Session:** 6 — Docker Migration
**Supersedes:** AGENT_HANDOVER_2026_04_28.md (Session 5)
**Status:** PLANNING COMPLETE — Ready for execution

---

## Mission

Migrate the entire TradePanel system from ad-hoc Windows services + Task Scheduler
into a single `docker compose up --build` that:
- Starts all services (backend, frontend, scheduler, Telegram bot, WhatsApp, DB)
- Creates the full database schema on first run (zero manual SQL steps)
- Replaces all 9 Windows Task Scheduler jobs with in-container APScheduler
- Adds WhatsApp notifications via WAHA (self-hosted)
- Exposes a Windows-native MT5 bridge on port 8001 (MetaTrader5 cannot run in Linux)

After this migration, setup on any machine = clone repo + add .env + `docker compose up --build`.

---

## Critical Rule (unchanged)

**NEVER use the Write/Edit tools to modify .py files on this machine.**
The Windows/Linux mount truncates files with non-ASCII bytes.
Always write Python files via bash heredoc or python3 -c open().write().

---

## Pre-Flight: Stop Everything First

Before writing any code, agent must confirm these are stopped/disabled:
1. Disable all 9 Task Scheduler tasks under "Task Scheduler Library":
   - TradePanel - Dashboard
   - TradePanel - Health Check
   - TradePanel - Paper Trading
   - TradePanel - Telegram Bot
   - TRADEPANEL_DATA_SYNC
   - TRADEPANEL_OVERNIGHT
   - TRADEPANEL_WEEKEND
   - TRADEPANEL_WFO_MON
   - TRADEPANEL_WFO_WED
2. Stop running uvicorn backend (Ctrl+C or kill the process)
3. Stop Telegram bot process if running separately
4. Leave Windows PostgreSQL running until Docker DB is confirmed healthy,
   then stop the Windows PostgreSQL service

**DO NOT stop MT5 terminal** — it must stay running on Windows at all times.

---

## Port Map (all ports 8000–8100)

| Port | Service            | Notes                                      |
|------|--------------------|--------------------------------------------|
| 8000 | FastAPI backend    | API + WebSocket (/api/ws/logs)             |
| 8001 | MT5 bridge         | Windows-native only, NOT in Docker         |
| 8025 | WAHA               | WhatsApp HTTP API (remapped from 3000)     |
| 8080 | Frontend           | nginx serving React build                  |
| 8090 | Adminer            | DB admin UI (browser-based)                |
| 5433 | PostgreSQL         | Host-exposed for tooling; internal = 5432  |

---

## Final Docker Architecture

```
docker-compose.yml
├── db            postgres:16           port 5433:5432
├── backend       python:3.11-slim      port 8000:8000
├── frontend      nginx:alpine          port 8080:80
├── telegram-bot  python:3.11-slim      (no exposed port)
├── scheduler     python:3.11-slim      (no exposed port)
├── waha          devlikeapro/waha-plus port 8025:3000
└── adminer       adminer               port 8090:8080

MT5 bridge: Windows-native FastAPI at port 8001 (starts via start_mt5_bridge.bat)
```

All Python services share a common Dockerfile (docker/Dockerfile.python).
Frontend uses a two-stage build: node:20-alpine builds React, nginx:alpine serves dist.

---

## Volume / Persistence Strategy

Named volumes (survive container destroy/recreate):
- `postgres_data`   — all database tables and data
- `waha_sessions`   — WAHA WhatsApp session (avoids re-scanning QR after restart)

Bind mounts (files on disk, user-editable, survive everything):
- `./config`    → /app/config    — config.yaml, strategies.yaml
- `./results`   → /app/results   — backtest results, daily validation, WFO output
- `./logs`      → /app/logs      — all application logs
- `./data`      → /app/data      — market data cache, COT cache, macro cache
- `./scripts`   → /app/scripts   — migration scripts (read-only reference)
- `./.env`      → read by Docker via env_file directive

---

## Environment Variable Changes for Docker

The .env file stays unchanged. docker-compose.yml overrides two keys per service
(DB_HOST and DB_PORT) so containers reach the db service by its Docker DNS name.
The Windows MT5 bridge still uses the original .env values if it needs them.

Override in every Python service's environment block:
```yaml
environment:
  - DB_HOST=db
  - DB_PORT=5432
  - MT5_BRIDGE_URL=http://host.docker.internal:8001
  - WAHA_URL=http://waha:3000
```

New .env keys to add (agent adds these to the bottom of .env):
```
MT5_BRIDGE_URL=http://host.docker.internal:8001
WAHA_URL=http://waha:3000
WAHA_API_KEY=tradepanel_secret
WHATSAPP_PHONE=           # user's WhatsApp number e.g. 27821234567
```

---

## Files to Create

### 1. db/init/01_schema.sql
Consolidate ALL table creation into one idempotent SQL file.
Source: scripts/setup_db.py (11 tables), scripts/migrate_account_profiles.sql,
        scripts/migrate_backtest_runs.sql
Tables required (all CREATE TABLE IF NOT EXISTS):
  strategies, backtest_runs, signals, trades, positions, bot_health,
  daily_summary, commands, market_data, regime_log, cot_data,
  account_profiles, wfo_runs (if not already present)

After all tables: seed account_profiles with ON CONFLICT DO NOTHING:
  (1, 'Demo Account',  'DEMO',  'MetaTrader 5', 'USD', 10000.00)
  (2, 'Live Account',  'LIVE',  'MetaTrader 5', 'USD', 10000.00)
  (3, 'Paper Account', 'PAPER', 'MetaTrader 5', 'USD', 10000.00)

Add index: CREATE INDEX IF NOT EXISTS idx_trades_account_id ON trades(account_id);
Add trigger: set_account_updated_at() on account_profiles (from migrate_account_profiles.sql)

### 2. docker/Dockerfile.python
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```
Note: MetaTrader5 must NOT be in requirements.txt for Docker.
Create docker/requirements.docker.txt that excludes MetaTrader5.
All other packages from requirements.txt should be included.

### 3. docker/Dockerfile.frontend
Two-stage build:
  Stage 1 (node:20-alpine): cd webapp/frontend && npm ci && npm run build
  Stage 2 (nginx:alpine): copy dist → /usr/share/nginx/html, copy nginx.conf

### 4. docker/nginx.conf
Serve React SPA with:
- Root /usr/share/nginx/html
- try_files $uri $uri/ /index.html (SPA routing)
- Proxy /api/ → http://backend:8000/api/
- Proxy /ws/ → http://backend:8000/ws/ (WebSocket upgrade headers)

### 5. docker-compose.yml (full replacement)
Replace the existing minimal docker-compose.yml with the full version
covering all 6 services + volumes + bind mounts as specified above.
Use `restart: unless-stopped` on all services.
Add `depends_on: db: condition: service_healthy` on all Python services.
Add healthcheck to db service:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s, timeout: 5s, retries: 5

### 6. mt5_bridge/api_server.py  (Windows-native, runs outside Docker)
Lightweight FastAPI server that wraps MT5Connector.
Endpoints:
  GET  /health                — returns {status: ok, mt5_connected: bool}
  GET  /account               — returns MT5 account info (balance, equity, etc.)
  GET  /tick/{symbol}         — returns latest tick for symbol
  GET  /rates/{symbol}/{tf}   — returns last N bars as JSON
  POST /order                 — place order (used by paper_engine in paper mode)
  GET  /positions             — open positions

Start command (Windows): python mt5_bridge/api_server.py
Or via: start_mt5_bridge.bat (create this bat file)

### 7. start_mt5_bridge.bat  (Windows, repo root)
```bat
@echo off
cd /d F:\REPOS\leo123xxx\TradePanel
python mt5_bridge/api_server.py
pause
```

### 8. scheduler/docker_jobs.py  (NEW — Docker version of scheduler/jobs.py)
Copy of scheduler/jobs.py but:
- Remove `import MetaTrader5 as mt5` and all direct MT5 calls
- Replace MT5 calls with HTTP requests to os.getenv("MT5_BRIDGE_URL")
- Use httpx or requests for all MT5 bridge calls
- Keep all APScheduler job registrations (11 jobs)
- Entry point: python -m scheduler.docker_jobs

### 9. notifications/whatsapp_bot.py  (NEW)
WAHA client for WhatsApp notifications.
WAHA API base: os.getenv("WAHA_URL", "http://waha:3000")
Methods to implement:
  send_message(phone, text) — POST /api/sendText
  send_alert(text)          — calls send_message with WHATSAPP_PHONE from env
Use same message templates as Telegram (notifications/templates.py).
Wire into notifications/router.py alongside TelegramBot:
  if whatsapp_enabled: await whatsapp_bot.send_alert(msg)

### 10. webapp/api/router_whatsapp.py  (NEW)
Two endpoints:
  GET  /api/whatsapp/status  — returns WAHA session status (connected/disconnected)
  POST /api/whatsapp/qr      — triggers QR code refresh if session lost
Add to webapp/main.py router includes.

### 11. webapp/frontend/src/App.jsx  (MODIFY)
Add WhatsApp status card to the sidebar (alongside existing TELEGRAM BOT card).
Polls GET /api/whatsapp/status every 30s.
Shows: session status (CONNECTED/DISCONNECTED), phone number, QR link if disconnected.

### 12. .dockerignore  (NEW)
```
__pycache__
*.pyc
.git
node_modules
results/
logs/
*.log
backups/
```

---

## Files to Modify

### scheduler/jobs.py
Currently imports MetaTrader5 directly at line 6.
Must not be broken for Windows-side usage.
Solution: add try/except around MT5 import; if ImportError, set MT5_AVAILABLE=False
and fall back to HTTP bridge calls. This makes the file work on both Windows and Linux.

### forward_test/paper_engine.py
Currently calls connector.connect() and mt5.* directly.
Add MT5_BRIDGE_URL fallback: if MetaTrader5 not available, use HTTP bridge.
New method: _get_tick_via_bridge(symbol) → GET MT5_BRIDGE_URL/tick/{symbol}
New method: _get_rates_via_bridge(symbol, tf, n) → GET MT5_BRIDGE_URL/rates/{symbol}/{tf}

### data/db_client.py
Check it reads DB_HOST/DB_PORT from env — it should already do this.
Verify no hardcoded 127.0.0.1 or 5433.

### webapp/main.py
Add router_whatsapp include (after router_telegram).

### notifications/router.py
Add WhatsApp notification alongside Telegram sends.

---

## WebSocket 403 Fix (already in source, not in dist)

The source (webapp/frontend/src/App.jsx line 1048) already has the correct URL:
  ws://localhost:8000/api/ws/logs
The 403s are from the old dist being served.
The Docker frontend build does a clean npm run build — this is automatically fixed.
No source change needed here.

---

## Verification Steps (agent must run these before closing)

1. `docker compose build` — all 6 images build without error
2. `docker compose up -d` — all containers start
3. `docker compose ps` — all show "healthy" or "running"
4. `curl http://localhost:8000/health` — backend returns 200
5. `curl http://localhost:8000/api/accounts` — returns 3 account profiles
6. `curl http://localhost:8080` — frontend loads (200)
7. `curl http://localhost:8025/api/sessions` — WAHA running
8. `curl http://localhost:8090` — Adminer loads
9. `docker compose logs scheduler` — no import errors, jobs registered
10. `docker compose logs telegram-bot` — bot started, polling
11. WebSocket test: open browser to localhost:8080, check Logs tab — no 403

---

## WAHA First-Run Setup (user must do this once after docker compose up)

1. Open http://localhost:8025 in browser
2. Go to Sessions → Create session named "default"
3. Scan the QR code with WhatsApp on your phone
4. Session status changes to CONNECTED
5. This state is persisted in the waha_sessions volume — no re-scan needed after restart

---

## What Windows Still Runs (outside Docker)

| Component       | How to start                    | Notes                           |
|-----------------|---------------------------------|---------------------------------|
| MT5 terminal    | Open MetaTrader 5 manually      | Must be running for live data   |
| MT5 bridge API  | Double-click start_mt5_bridge.bat | Exposes MT5 data to containers |

Everything else runs in Docker.

---

## Go-Live Decision (unchanged from Session 5)

Paper test window: 2026-04-26 to 2026-05-10
On 2026-05-10: review forward test results and flip config/config.yaml:
  system.mode: live
The Docker setup does not change this workflow — config is a bind mount.

---

## Open Items After Docker Migration

| Priority | Item                                    |
|----------|-----------------------------------------|
| HIGH     | WAHA QR scan (one-time, user action)    |
| MEDIUM   | Review 3 PASS WFO strategies for paper  |
| MEDIUM   | Go-live decision on 2026-05-10          |
| LOW      | WebSocket reconnect countdown in UI     |
