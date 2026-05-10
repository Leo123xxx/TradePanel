#!/usr/bin/env pwsh

Write-Host "DATABASE STATUS CHECK - Why Dashboard Data Differs from Backtest" -ForegroundColor Cyan

# Check if PostgreSQL container is running
Write-Host "[1] Checking PostgreSQL container..." -ForegroundColor Yellow
$container = docker ps | Select-String "tradepanel-db"

if ($container) {
    Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
} else {
    Write-Host "✗ PostgreSQL container not found - cannot check database" -ForegroundColor Red
    exit 1
}

# Query 1: Count of backtest records by status
Write-Host "`n[2] Backtest Records by Status..." -ForegroundColor Yellow
$query = "SELECT status, COUNT(*) as count FROM backtest_runs GROUP BY status ORDER BY count DESC;"

try {
    $result = docker exec -it tradepanel-db psql -U postgres -d trading_platform -c $query 2>&1 | Select-String -Pattern "PASS|REVIEW|ERROR|status|count" -Context 0
    if ($result) { Write-Host $result -ForegroundColor Gray } else { Write-Host "⚠ No data returned from query" -ForegroundColor Yellow }
} catch {
    Write-Host "✗ Error executing query: $_" -ForegroundColor Red
}

# Query 2: Total count of backtest records
Write-Host "`n[3] Total Backtest Records..." -ForegroundColor Yellow
$query2 = "SELECT COUNT(*) as total_records FROM backtest_runs;"

try {
    $result2 = docker exec -it tradepanel-db psql -U postgres -d trading_platform -c $query2 2>&1 | Select-String -Pattern "\d+"
    if ($result2) { Write-Host "Total backtest records in database: $result2" -ForegroundColor Cyan }
} catch {
    Write-Host "✗ Error counting records: $_" -ForegroundColor Red
}

# Query 3: Latest backtest timestamp
Write-Host "`n[4] Latest Backtest Date..." -ForegroundColor Yellow
$query3 = "SELECT MAX(created_at) as latest_backtest FROM backtest_runs;"

try {
    $result3 = docker exec -it tradepanel-db psql -U postgres -d trading_platform -c $query3 2>&1 | Select-String -Pattern "\d{4}-\d{2}-\d{2}"
    if ($result3) {
        Write-Host "Latest backtest: $result3" -ForegroundColor Cyan
        Write-Host "Expected: 2026-05-05 (from last successful backtest)" -ForegroundColor Gray
    } else {
        Write-Host "⚠ Could not determine latest backtest date" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Error querying date: $_" -ForegroundColor Red
}

# Query 4: Check paper_trades (if paper mode has been running)
Write-Host "`n[5] Paper Trading Activity..." -ForegroundColor Yellow
$query4 = "SELECT COUNT(*) as total_paper_trades, COUNT(CASE WHEN status = 'OPENED' THEN 1 END) as open_positions, COUNT(CASE WHEN status = 'CLOSED' THEN 1 END) as closed_trades FROM trades WHERE mode = 'paper' AND created_at >= CURRENT_DATE;"

try {
    $result4 = docker exec -it tradepanel-db psql -U postgres -d trading_platform -c $query4 2>&1 | Select-String -Pattern "total_paper|open_positions|closed|[0-9]" -Context 0
    if ($result4) { Write-Host $result4 -ForegroundColor Gray } else { Write-Host "⚠ No paper trades yet (paper mode may just be starting)" -ForegroundColor Yellow }
} catch {
    Write-Host "✗ Error querying paper trades: $_" -ForegroundColor Red
}

Write-Host "`n[6] INTERPRETATION" -ForegroundColor Yellow
Write-Host "If Dashboard Shows 84 Total (vs 148): Likely filtered view or old data." -ForegroundColor Gray
Write-Host "If PASS count is 3 (vs 35): Dashboard is querying OLD data from earlier failed backtest. Clear old data." -ForegroundColor Gray
Write-Host "If Latest Backtest < 2026-05-05: May 5 backtest results weren't saved to database." -ForegroundColor Gray

Write-Host "`n[7] NEXT STEP" -ForegroundColor Yellow
Write-Host "If database shows OLD data from before May 5, run:" -ForegroundColor Cyan
Write-Host "docker exec tradepanel-db psql -U postgres -d trading_platform -c `"DELETE FROM backtest_runs WHERE created_at < '2026-05-05';`"" -ForegroundColor Cyan
