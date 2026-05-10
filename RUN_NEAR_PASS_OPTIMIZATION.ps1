# RUN_NEAR_PASS_OPTIMIZATION.ps1
#
# PowerShell runner for near-pass candidate optimization suite.
# For Windows users who prefer PowerShell over batch files.
#
# Usage:
#   .\RUN_NEAR_PASS_OPTIMIZATION.ps1
#   .\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Quick
#   .\RUN_NEAR_PASS_OPTIMIZATION.ps1 -Extended
#

param(
    [switch]$Quick,
    [switch]$Extended,
    [string]$Strategy
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 70
Write-Host "NEAR-PASS STRATEGY OPTIMIZATION SUITE" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "[*] Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Determine mode
$mode = "normal"
if ($Quick) {
    $mode = "quick"
    Write-Host "[*] Running in QUICK mode (fewer grid points)" -ForegroundColor Yellow
} elseif ($Extended) {
    $mode = "extended"
    Write-Host "[*] Running in EXTENDED mode (comprehensive search)" -ForegroundColor Yellow
} else {
    Write-Host "[*] Running in NORMAL mode" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70
Write-Host "OPTIMIZATION STARTING" -ForegroundColor Green
Write-Host "=" * 70
Write-Host ""

# Build command
$cmd = "python scripts\run_near_pass_suite.py"

if ($Quick) {
    $cmd += " --quick"
} elseif ($Extended) {
    $cmd += " --extended"
}

if ($Strategy) {
    $cmd += " --strategy $Strategy"
}

# Run optimization
Invoke-Expression $cmd
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Optimization failed with exit code $exitCode" -ForegroundColor Red
    exit $exitCode
}

Write-Host ""
Write-Host "=" * 70
Write-Host "OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "=" * 70
Write-Host ""
Write-Host "Results available in:" -ForegroundColor Cyan
Write-Host "  - results\optimization\near_pass_optimization.json (raw data)"
Write-Host "  - results\optimization\near_pass_report.md (summary report)"
Write-Host ""
