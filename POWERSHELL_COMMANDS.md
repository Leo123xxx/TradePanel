# TradePanel Analytics - PowerShell Commands

Quick reference for checking analytics setup via PowerShell.

---

## Quick Start (Copy & Paste)

```powershell
# Navigate to TradePanel
cd F:\REPOS\leo123xxx\TradePanel

# Run verification script
powershell -ExecutionPolicy Bypass -File CHECK_ANALYTICS.ps1
```

---

## Manual Commands

### 1. Check if Analytics Files Exist

```powershell
# Check analytics module
Test-Path "F:\REPOS\leo123xxx\TradePanel\analytics\performance_calculator.py"
Test-Path "F:\REPOS\leo123xxx\TradePanel\analytics\__init__.py"
Test-Path "F:\REPOS\leo123xxx\TradePanel\webapp\api\router_analytics.py"
Test-Path "F:\REPOS\leo123xxx\TradePanel\webapp\main.py"

# List all files in analytics directory
Get-ChildItem "F:\REPOS\leo123xxx\TradePanel\analytics" -Recurse
```

---

### 2. Check Python Installation

```powershell
# Check Python version
python --version

# Check Python location
where python

# Check pip
pip --version

# List installed packages
pip list
```

---

### 3. Check Required Packages

```powershell
# Check pandas
python -c "import pandas; print(f'pandas: {pandas.__version__}')"

# Check numpy
python -c "import numpy; print(f'numpy: {numpy.__version__}')"

# Check psycopg2
python -c "import psycopg2; print('psycopg2: OK')"

# Check fastapi
python -c "import fastapi; print(f'fastapi: {fastapi.__version__}')"

# Check uvicorn
python -c "import uvicorn; print(f'uvicorn: {uvicorn.__version__}')"

# Check all at once
python -c "import pandas, numpy, psycopg2, fastapi, uvicorn; print('All required packages: OK')"
```

---

### 4. Test Analytics Module Import

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Simple import test
python -c "from analytics.performance_calculator import PerformanceCalculator; print('✓ Module imports OK')"

# More detailed test
python -c @"
from analytics.performance_calculator import PerformanceCalculator, PerformanceMetrics, generate_report
print('✓ PerformanceCalculator: OK')
print('✓ PerformanceMetrics: OK')
print('✓ generate_report: OK')
"@
```

---

### 5. Check API Server Status

```powershell
# Check if port 8000 is listening
netstat -ano | findstr :8000

# Try to connect to API health endpoint
Invoke-WebRequest -Uri "http://localhost:8000/api/analytics/health" -TimeoutSec 3

# If server not running, start it
cd F:\REPOS\leo123xxx\TradePanel
python main.py
```

---

### 6. Test Database Connection

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Check PostgreSQL is running
netstat -ano | findstr :5432

# Test database connection
python -c @"
from data.db_client import DBClient
db = DBClient()
result = db.execute_query('SELECT COUNT(*) FROM trades')
print(f'✓ Database connected')
print(f'✓ Total trades: {result[0][0]}')
"@

# Check what's in the database
python -c @"
from data.db_client import DBClient
db = DBClient()

# Count trades
trades = db.execute_query('SELECT COUNT(*) FROM trades')
print(f'Trades: {trades[0][0]}')

# Count strategies
strategies = db.execute_query('SELECT COUNT(*) FROM strategies')
print(f'Strategies: {strategies[0][0]}')

# Recent trades
recent = db.execute_query('SELECT pair, pnl, exit_time FROM trades ORDER BY exit_time DESC LIMIT 5')
print(f'Recent trades: {recent}')
"@
```

---

### 7. Test Analytics Calculation

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Calculate metrics for last 7 days
python -c @"
from analytics.performance_calculator import PerformanceCalculator
calc = PerformanceCalculator(lookback_days=7)
metrics = calc.calculate_all_metrics()

if metrics['account']:
    m = metrics['account']
    print(f'✓ Analytics working!')
    print(f'  Trades: {m.total_trades}')
    print(f'  Win Rate: {m.win_rate}%')
    print(f'  Sharpe: {m.sharpe_ratio}')
    print(f'  Profit Factor: {m.profit_factor}')
    print(f'  Max Drawdown: {m.max_drawdown_pct}%')
    print(f'  Net Profit: ${m.net_profit:,.2f}')
else:
    print('✓ Analytics working (no trades in last 7 days)')
"@

# Calculate for last 30 days
python -c @"
from analytics.performance_calculator import PerformanceCalculator
calc = PerformanceCalculator(lookback_days=30)
metrics = calc.calculate_all_metrics()
print(f'Account metrics: {metrics["account"]}')
print(f'By strategy: {list(metrics["by_strategy"].keys())}')
print(f'By asset: {list(metrics["by_asset"].keys())}')
"@

# Generate formatted report
python -m analytics.performance_calculator
```

---

### 8. Test API Endpoints (Server Must Be Running)

```powershell
# Health check
curl http://localhost:8000/api/analytics/health

# Get account summary
curl "http://localhost:8000/api/analytics/summary?lookback_days=30"

# Get performance by strategy
curl "http://localhost:8000/api/analytics/by-strategy?lookback_days=30"

# Get performance by asset
curl "http://localhost:8000/api/analytics/by-asset?lookback_days=30"

# Get daily P&L
curl "http://localhost:8000/api/analytics/daily?lookback_days=30"

# Get heatmap
curl "http://localhost:8000/api/analytics/heatmap?lookback_days=30"

# Get complete dashboard data
curl "http://localhost:8000/api/analytics/dashboard?lookback_days=30"

# Save response to file
curl "http://localhost:8000/api/analytics/summary?lookback_days=30" -OutFile analytics_summary.json
Get-Content analytics_summary.json | ConvertFrom-Json | Format-Table
```

---

### 9. Test with Different Lookback Periods

```powershell
# Last 7 days
curl "http://localhost:8000/api/analytics/summary?lookback_days=7"

# Last 30 days
curl "http://localhost:8000/api/analytics/summary?lookback_days=30"

# Last 90 days
curl "http://localhost:8000/api/analytics/summary?lookback_days=90"

# Last year
curl "http://localhost:8000/api/analytics/summary?lookback_days=365"
```

---

### 10. Check File Contents

```powershell
# Check if __init__.py is correct
Get-Content "F:\REPOS\leo123xxx\TradePanel\analytics\__init__.py"

# Check file sizes
Get-ChildItem "F:\REPOS\leo123xxx\TradePanel\analytics" | Select-Object Name, Length

# Check for null bytes
(Get-Content "F:\REPOS\leo123xxx\TradePanel\analytics\performance_calculator.py" -Encoding Byte | Where-Object {$_ -eq 0}).Count

# Should return 0 (no null bytes)
```

---

### 11. Start the API Server

```powershell
# Navigate to TradePanel
cd F:\REPOS\leo123xxx\TradePanel

# Option 1: Run with python directly
python main.py

# Option 2: Run with uvicorn
uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload

# Option 3: Run in new terminal
Start-Process powershell -ArgumentList "cd F:\REPOS\leo123xxx\TradePanel; python main.py"
```

---

### 12. Comprehensive Health Check

```powershell
cd F:\REPOS\leo123xxx\TradePanel

Write-Host "=== TradePanel Analytics Health Check ===" -ForegroundColor Cyan

# 1. Files
Write-Host "`n1. Checking files..." -ForegroundColor Yellow
$files = @(
    "analytics\performance_calculator.py",
    "analytics\__init__.py",
    "webapp\api\router_analytics.py"
)
foreach ($f in $files) {
    if (Test-Path $f) { Write-Host "  ✓ $f" -ForegroundColor Green }
    else { Write-Host "  ✗ $f" -ForegroundColor Red }
}

# 2. Python
Write-Host "`n2. Python version:" -ForegroundColor Yellow
python --version

# 3. Module import
Write-Host "`n3. Testing module import..." -ForegroundColor Yellow
python -c "from analytics.performance_calculator import PerformanceCalculator; print('  ✓ OK')" 2>&1

# 4. Database
Write-Host "`n4. Testing database..." -ForegroundColor Yellow
python -c @"
from data.db_client import DBClient
db = DBClient()
result = db.execute_query('SELECT COUNT(*) FROM trades')
print(f'  ✓ Trades in DB: {result[0][0]}')
"@ 2>&1

# 5. API Server
Write-Host "`n5. API Server status:" -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://localhost:8000/api/analytics/health" -TimeoutSec 2 -ErrorAction Stop | Out-Null
    Write-Host "  ✓ Running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Not running (start with: python main.py)" -ForegroundColor Red
}

Write-Host "`n=== Health Check Complete ===" -ForegroundColor Cyan
```

---

## Troubleshooting

### If psycopg2 import fails
```powershell
# Install PostgreSQL driver
pip install psycopg2-binary
```

### If pandas/numpy missing
```powershell
# Install data science packages
pip install pandas numpy
```

### If fastapi/uvicorn missing
```powershell
# Install web framework
pip install fastapi uvicorn
```

### If database won't connect
```powershell
# Check PostgreSQL is running
netstat -ano | findstr :5432

# Test connection directly
python -c "import psycopg2; conn = psycopg2.connect(dbname='trading_platform'); print('✓ Connected')"
```

### If API port is already in use
```powershell
# Kill process on port 8000
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process -Force

# Or use different port
uvicorn webapp.main:app --host 0.0.0.0 --port 8001
```

---

## Sample Output

If everything works, you should see:

```
✓ Files exist
✓ Python: Python 3.10.x
✓ Module imports OK
✓ Database connected (1250 trades)
✓ Analytics working! Trades: 125, Win Rate: 52.4%, Sharpe: 1.32
✓ API Server running on port 8000
✓ All endpoints accessible
```

---

**Last Updated:** April 24, 2026  
**Version:** 1.0
