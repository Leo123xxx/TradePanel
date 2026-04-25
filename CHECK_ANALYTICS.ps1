# TradePanel Analytics Verification Script
# PowerShell commands to check analytics setup

Write-Host "================================" -ForegroundColor Cyan
Write-Host "TradePanel Analytics Check" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# 1. Check if files exist
Write-Host "1. CHECKING FILES EXIST..." -ForegroundColor Yellow
$files = @(
    "analytics\performance_calculator.py",
    "analytics\__init__.py",
    "analytics\README.md",
    "webapp\api\router_analytics.py",
    "webapp\main.py"
)

foreach ($file in $files) {
    $path = "F:\REPOS\leo123xxx\TradePanel\$file"
    if (Test-Path $path) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (MISSING)" -ForegroundColor Red
    }
}

Write-Host ""

# 2. Check Python installation
Write-Host "2. CHECKING PYTHON..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
}

Write-Host ""

# 3. Check required packages
Write-Host "3. CHECKING PYTHON PACKAGES..." -ForegroundColor Yellow
$packages = @("pandas", "numpy", "psycopg2", "fastapi", "uvicorn")

foreach ($pkg in $packages) {
    try {
        python -c "import $pkg; print('')" 2>$null
        Write-Host "  ✓ $pkg" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ $pkg (NOT INSTALLED)" -ForegroundColor Red
    }
}

Write-Host ""

# 4. Try to import the analytics module
Write-Host "4. TESTING MODULE IMPORT..." -ForegroundColor Yellow
$importTest = @"
try:
    from analytics.performance_calculator import PerformanceCalculator, PerformanceMetrics
    print('OK')
except ImportError as e:
    print(f'ERROR: {e}')
except Exception as e:
    print(f'ERROR: {e}')
"@

$result = python -c $importTest 2>&1
if ($result -eq "OK") {
    Write-Host "  ✓ Module imports successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ Module import failed: $result" -ForegroundColor Red
}

Write-Host ""

# 5. Check if API server is running
Write-Host "5. CHECKING API SERVER STATUS..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/analytics/health" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ API Server is RUNNING (port 8000)" -ForegroundColor Green
    }
} catch {
    Write-Host "  ✗ API Server NOT RUNNING (port 8000)" -ForegroundColor Red
    Write-Host "    Run: python main.py" -ForegroundColor Yellow
}

Write-Host ""

# 6. Test database connection
Write-Host "6. TESTING DATABASE CONNECTION..." -ForegroundColor Yellow
$dbTest = @"
try:
    from data.db_client import DBClient
    db = DBClient()
    result = db.execute_query("SELECT COUNT(*) FROM trades")
    if result:
        count = result[0][0]
        print(f'OK:{count}')
    else:
        print('EMPTY')
except Exception as e:
    print(f'ERROR: {str(e)[:80]}')
"@

$result = python -c $dbTest 2>&1
if ($result.StartsWith("OK:")) {
    $tradeCount = $result.Split(":")[1]
    Write-Host "  ✓ Database connected" -ForegroundColor Green
    Write-Host "    Total trades in DB: $tradeCount" -ForegroundColor Cyan
} elseif ($result -eq "EMPTY") {
    Write-Host "  ✓ Database connected (no trades yet)" -ForegroundColor Yellow
} else {
    Write-Host "  ✗ Database error: $result" -ForegroundColor Red
}

Write-Host ""

# 7. Test analytics calculation (if DB has trades)
Write-Host "7. TESTING ANALYTICS CALCULATION..." -ForegroundColor Yellow
$analyticsTest = @"
try:
    from analytics.performance_calculator import PerformanceCalculator
    calc = PerformanceCalculator(lookback_days=7)
    metrics = calc.calculate_all_metrics()

    if metrics['account']:
        m = metrics['account']
        print(f'OK:{m.total_trades}:{m.win_rate}:{m.sharpe_ratio}')
    else:
        print('NO_TRADES')
except Exception as e:
    print(f'ERROR: {str(e)[:80]}')
"@

$result = python -c $analyticsTest 2>&1
if ($result.StartsWith("OK:")) {
    $parts = $result.Split(":")
    $trades = $parts[1]
    $wr = $parts[2]
    $sharpe = $parts[3]
    Write-Host "  ✓ Analytics working!" -ForegroundColor Green
    Write-Host "    Trades: $trades, Win Rate: $wr%, Sharpe: $sharpe" -ForegroundColor Cyan
} elseif ($result -eq "NO_TRADES") {
    Write-Host "  ✓ Analytics working (no trades in last 7 days)" -ForegroundColor Yellow
} else {
    Write-Host "  ✗ Analytics error: $result" -ForegroundColor Red
}

Write-Host ""

# 8. Summary
Write-Host "================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IF API SERVER IS NOT RUNNING:" -ForegroundColor Yellow
Write-Host "  cd F:\REPOS\leo123xxx\TradePanel" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "THEN TEST API ENDPOINTS:" -ForegroundColor Yellow
Write-Host "  curl http://localhost:8000/api/analytics/summary?lookback_days=30" -ForegroundColor Cyan
Write-Host "  curl http://localhost:8000/api/analytics/dashboard?lookback_days=30" -ForegroundColor Cyan
Write-Host ""
Write-Host "GENERATE REPORT:" -ForegroundColor Yellow
Write-Host "  python -m analytics.performance_calculator" -ForegroundColor Cyan
Write-Host ""
