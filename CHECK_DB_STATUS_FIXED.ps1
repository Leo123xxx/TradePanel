#!/usr/bin/env pwsh
<#
.SYNOPSIS
Check database status and backtest results
Explains why dashboard shows 3 PASS vs backtest showed 35 PASS
#>

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  DATABASE STATUS CHECK - Backtest Results Analysis                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL container is running
Write-Host "[1] Checking PostgreSQL container..." -ForegroundColor Yellow
$container = docker ps | Select-String "tradepanel-db"

if ($container) {
    Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
} else {
    Write-Host "✗ PostgreSQL container not found - cannot check database" -ForegroundColor Red
    Write-Host "  Run: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Query 1: Count of backtest records by status
Write-Host "`n[2] Backtest Records by Status..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

$query = "SELECT status, COUNT(*) as count FROM backtests GROUP BY status ORDER BY count DESC;"

try {
    Write-Host "Querying database..." -ForegroundColor Gray
    $result = docker exec tradepanel-db psql -U postgres -d tradepanel -c $query 2>&1

    if ($result) {
        Write-Host $result -ForegroundColor Gray
    } else {
        Write-Host "⚠ No data returned from query" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Error executing query: $_" -ForegroundColor Red
}

# Query 2: Total count
Write-Host "`n[3] Total Backtest Records..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

$query2 = "SELECT COUNT(*) as total_records FROM backtests;"

try {
    Write-Host "Counting all records..." -ForegroundColor Gray
    $result2 = docker exec tradepanel-db psql -U postgres -d tradepanel -c $query2 2>&1
    Write-Host $result2 -ForegroundColor Cyan
} catch {
    Write-Host "✗ Error counting records: $_" -ForegroundColor Red
}

# Query 3: Latest backtest timestamp
Write-Host "`n[4] Latest Backtest Date..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

$query3 = "SELECT MAX(created_at) as latest_backtest FROM backtests;"

try {
    Write-Host "Checking latest backtest..." -ForegroundColor Gray
    $result3 = docker exec tradepanel-db psql -U postgres -d tradepanel -c $query3 2>&1
    Write-Host $result3 -ForegroundColor Cyan
    Write-Host "Expected: 2026-05-05 or later (from last successful backtest)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Error querying date: $_" -ForegroundColor Red
}

# Query 4: Check paper_trades
Write-Host "`n[5] Paper Trading Activity (Today)..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

$query4 = "SELECT COUNT(*) as total_paper_trades FROM paper_trades WHERE created_at >= CURRENT_DATE;"

try {
    Write-Host "Checking paper trades..." -ForegroundColor Gray
    $result4 = docker exec tradepanel-db psql -U postgres -d tradepanel -c $query4 2>&1
    Write-Host $result4 -ForegroundColor Cyan
} catch {
    Write-Host "✗ Error querying paper trades: $_" -ForegroundColor Red
}

# Summary
Write-Host "`n[6] INTERPRETATION" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

Write-Host @"
Expected Results (from May 5, 2026 backtest):
  • Total Records: 148 combos (23 strategies × ~6 pairs each)
  • Status PASS: 35 combos ✓
  • Status REVIEW: 90 combos
  • Status ERROR: 23 combos

What the results above tell you:

  IF Total = 148 AND PASS = 35:
    ✓ Database has CORRECT data from May 5 backtest
    ✓ Dashboard is applying a filter (check the UI)
    ✓ All strategies and pairs are properly configured

  IF Total = 84 AND PASS = 3:
    ✗ Database has OLD/STALE data from earlier failed backtest
    ✗ Need to clear old records before continuing

  IF Total = 0:
    ✗ No backtest data in database at all
    ✗ Backtest results never saved to DB

Paper Trades = 0:
  This is NORMAL if paper mode just started (wait 4-6 hours for trades)
  Check Telegram for signals being detected
"@ -ForegroundColor Gray

Write-Host "`n[7] IF YOU NEED TO FIX IT" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Yellow

Write-Host @"
If you see OLD data (3 PASS instead of 35):

  # Delete old backtest records from before May 5
  docker exec tradepanel-db psql -U postgres -d tradepanel -c `
    "DELETE FROM backtests WHERE created_at < '2026-05-05';"

  # Then restart backend
  docker restart tradepanel-backend

After that, go to http://localhost:3000 and refresh the dashboard
"@ -ForegroundColor Cyan

Write-Host "`n✅ Diagnostic complete. Review results above.`n" -ForegroundColor Cyan
