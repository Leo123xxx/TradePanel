# TradePanel Quick Commands Cheat Sheet

Fastest way to get common tasks done.

---

## Start Everything (New Terminal Windows)

### Terminal 1: API Server
```powershell
# Windows
cd F:\REPOS\leo123xxx\TradePanel
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload

# Linux
cd ~/repos/leo123xxx/TradePanel
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Trading Bot
```powershell
# Windows
cd F:\REPOS\leo123xxx\TradePanel
python main.py --mode paper-trade

# Linux
cd ~/repos/leo123xxx/TradePanel
python main.py --mode paper-trade
```

---

## Test Everything

| Task | Command |
|------|---------|
| API Health | `curl http://localhost:8000/api/analytics/health` |
| Analytics Summary | `curl "http://localhost:8000/api/analytics/summary?lookback_days=30"` |
| Performance Report | `python -m analytics.performance_calculator` |
| Database OK? | `python -c "from data.db_client import DBClient; DBClient()"` |

---

## Common Tasks

| Task | Windows | Linux |
|------|---------|-------|
| **View Config** | `code config/config.yaml` | `nano config/config.yaml` |
| **View Logs** | `Get-Content logs/main.log -Tail 50` | `tail -50 logs/main.log` |
| **Watch Logs** | `Get-Content logs/main.log -Wait` | `tail -f logs/main.log` |
| **Backtest** | `python main.py --mode backtest` | `python main.py --mode backtest` |
| **Validate** | `python main.py --mode validate` | `python main.py --mode validate` |
| **Kill API** | `Get-Process python \| Stop-Process` | `pkill -f uvicorn` |
| **Kill Bot** | `Get-Process python \| Stop-Process` | `pkill -f main.py` |
| **List trades** | `curl "http://localhost:8000/api/data"` | `curl "http://localhost:8000/api/data"` |

---

## API Endpoints (All accept `?lookback_days=30`)

```
Summary:       curl http://localhost:8000/api/analytics/summary
Strategy:      curl http://localhost:8000/api/analytics/by-strategy
Asset:         curl http://localhost:8000/api/analytics/by-asset
Daily:         curl http://localhost:8000/api/analytics/daily
Heatmap:       curl http://localhost:8000/api/analytics/heatmap
Correlation:   curl http://localhost:8000/api/analytics/correlation
Dashboard:     curl http://localhost:8000/api/analytics/dashboard
```

---

## Shortcuts for Your Shell

### PowerShell (add to profile or create functions)
```powershell
function api { python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload }
function bot { python main.py --mode paper-trade }
function logs { Get-Content logs/main.log -Wait }
function report { python -m analytics.performance_calculator }
function test-api { curl http://localhost:8000/api/analytics/health }
function start-all { api & bot }
```

### Bash (add to ~/.bashrc)
```bash
alias api='python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000'
alias bot='python main.py --mode paper-trade'
alias logs='tail -f logs/main.log'
alias report='python -m analytics.performance_calculator'
alias test-api='curl http://localhost:8000/api/analytics/health'
```

---

## File Locations

```
Config:        config/config.yaml
Strategies:    config/strategies.yaml
Logs:          logs/main.log
Analytics:     analytics/performance_calculator.py
API:           webapp/main.py
Database:      PostgreSQL on localhost:5432
```

---

## Status Check Script

### Windows PowerShell
```powershell
Write-Host "=== TradePanel Status ===" -ForegroundColor Cyan

# 1. Check ports
"Port 8000 (API):" 
netstat -ano | findstr :8000 | Out-Null
if ($?) { Write-Host "  ✓ Running" -ForegroundColor Green } else { Write-Host "  ✗ Not running" -ForegroundColor Red }

"Port 5432 (DB):"
netstat -ano | findstr :5432 | Out-Null
if ($?) { Write-Host "  ✓ Running" -ForegroundColor Green } else { Write-Host "  ✗ Not running" -ForegroundColor Red }

# 2. Test API
"API Health:"
try {
    $result = curl http://localhost:8000/api/analytics/health -UseBasicParsing -ErrorAction Stop
    Write-Host "  ✓ OK" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error" -ForegroundColor Red
}

# 3. Test database
"Database:"
try {
    python -c "from data.db_client import DBClient; DBClient().execute_query('SELECT 1')" 2>$null
    Write-Host "  ✓ Connected" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error" -ForegroundColor Red
}
```

### Linux Bash
```bash
echo "=== TradePanel Status ==="

# 1. Check ports
echo -n "Port 8000 (API): "
lsof -i :8000 > /dev/null 2>&1 && echo "✓ Running" || echo "✗ Not running"

echo -n "Port 5432 (DB): "
lsof -i :5432 > /dev/null 2>&1 && echo "✓ Running" || echo "✗ Not running"

# 2. Test API
echo -n "API Health: "
curl -s http://localhost:8000/api/analytics/health > /dev/null && echo "✓ OK" || echo "✗ Error"

# 3. Test database
echo -n "Database: "
python -c "from data.db_client import DBClient; DBClient().execute_query('SELECT 1')" 2>/dev/null && echo "✓ Connected" || echo "✗ Error"
```

---

## Emergency Fixes

| Problem | Fix |
|---------|-----|
| API won't start | Check port 8000: `netstat -ano \| findstr :8000` |
| Bot crashes | View logs: `tail -f logs/main.log` |
| DB connection fails | Restart PostgreSQL or check localhost:5432 |
| Memory leak | Kill Python: `pkill python` and restart |
| Port stuck | Force kill: `netstat -ano \| findstr :8000` then `taskkill /PID xxxx /F` |

---

## 30-Second Setup

```powershell
# Windows - Run ONCE to set up
cd F:\REPOS\leo123xxx\TradePanel
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# Linux - Run ONCE to set up
cd ~/repos/leo123xxx/TradePanel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Daily Startup (30 seconds)

**Terminal 1:**
```
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2:**
```
python main.py --mode paper-trade
```

**Check Health:**
```
curl http://localhost:8000/api/analytics/health
```

Done! ✓

---

**Print this page for your desk!**
