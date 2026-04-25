# Quick Check Commands

## Run Everything at Once

```powershell
cd F:\REPOS\leo123xxx\TradePanel
powershell -ExecutionPolicy Bypass -File CHECK_ANALYTICS.ps1
```

---

## Individual Quick Checks

### Check Files Exist (5 seconds)
```powershell
ls analytics\performance_calculator.py
ls webapp\api\router_analytics.py
```

### Check Module Imports (3 seconds)
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -c "from analytics import PerformanceCalculator; print('✓ OK')"
```

### Check Database Connection (5 seconds)
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -c "from data.db_client import DBClient; db = DBClient(); print('✓ Connected')"
```

### Check API Server (2 seconds)
```powershell
curl http://localhost:8000/api/analytics/health
```

### Run Analytics & Get Report (10 seconds)
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -m analytics.performance_calculator
```

---

## If API Server Not Running

```powershell
cd F:\REPOS\leo123xxx\TradePanel
python main.py
```

Then in another PowerShell window:

```powershell
# Test the API
curl http://localhost:8000/api/analytics/summary?lookback_days=30
```

---

## View Full Documentation

- **POWERSHELL_COMMANDS.md** — All available commands with examples
- **analytics/README.md** — API endpoint reference
- **analytics/DASHBOARD_EXAMPLE.md** — Frontend implementation guide
- **ANALYTICS_IMPLEMENTATION.md** — Complete implementation details

---

## Status Indicators

✓ = Working  
✗ = Problem  
⚠ = Warning

Examples:
- ✓ Database connected → Everything OK
- ✗ API Server NOT RUNNING → Run `python main.py`
- ⚠ No trades in last 7 days → Try longer lookback period
