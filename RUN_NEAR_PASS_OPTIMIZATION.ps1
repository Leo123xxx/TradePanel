# RUN_NEAR_PASS_OPTIMIZATION.ps1
# V3 Modular PowerShell runner for near-pass candidate optimization suite.

param(
    [switch]$Quick,
    [switch]$Extended,
    [string]$Strategy
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 70
Write-Host "NEAR-PASS STRATEGY OPTIMIZATION SUITE (V3 Modular)" -ForegroundColor Cyan
Write-Host "=" * 70

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
} elseif (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & .\.venv\Scripts\Activate.ps1
}

# Determine mode
$mode = "normal"
if ($Quick) { $mode = "quick" }
elseif ($Extended) { $mode = "extended" }

Write-Host "[*] Mode: $mode" -ForegroundColor Yellow

# Build command
$cmd = "python scripts\backtest\run_near_pass_suite.py"

if ($Quick) { $cmd += " --quick" }
elseif ($Extended) { $cmd += " --extended" }

if ($Strategy) { $cmd += " --strategy $Strategy" }

# Run optimization
Invoke-Expression $cmd
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "ERROR: Optimization failed with exit code $exitCode" -ForegroundColor Red
    exit $exitCode
}

Write-Host ""
Write-Host "=" * 70
Write-Host "OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "=" * 70
Write-Host "Results available in:" -ForegroundColor Cyan
Write-Host "  - results\data\near_pass_optimization.json"
Write-Host "  - results\reports\near_pass_report.md"
