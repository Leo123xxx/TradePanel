#!/usr/bin/env python3
"""
run_near_pass_suite.py
Master orchestrator for V3 near-pass candidate optimization.
"""

import sys, json, subprocess, argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

STRATEGIES_TO_RUN = [
    "hikkake_trap",
    "session_momentum",
    "range_breakout",
    "dual_ema_momentum",
    "rsi_pullback",
    "rsi_extremes_scalp",
    "ema_ribbon_trend",
]

PASS_THRESHOLDS = {
    "sharpe": 1.5,
    "win_rate": 65.0,
    "profit_factor": 1.0,
}

def run_optimization_batch(strategy_names: list, quick: bool = False, extended: bool = False) -> dict:
    """Run optimize_near_pass.py for all strategies."""
    cmd = [
        sys.executable, "-m",
        "scripts.backtest.optimization.optimize_near_pass",
        "--strategy",
    ] + strategy_names
    
    if quick: cmd.append("--quick")
    if extended: cmd.append("--extended")

    print(f"\n[*] Running Parallel Optimization: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    
    return {"status": "OK" if result.returncode == 0 else "ERROR"}

def aggregate_results() -> dict:
    opt_file = PROJECT_ROOT / "results" / "data" / "near_pass_optimization.json"
    if not opt_file.exists(): return {}
    with open(opt_file) as f:
        return json.load(f)

def generate_summary_report(results: dict) -> str:
    report = ["# Near-PASS Optimization Results (V3)"]
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("## Overview\n")
    report.append("| Strategy | Best Sharpe | Best WR% | Status |")
    report.append("|----------|-------------|---------|--------|")

    for strat_name, strat_data in results.items():
        if strat_data.get("status") != "OK": continue
        top_5 = strat_data.get("top_5", [])
        if not top_5: continue
        best = top_5[0]; m = best["metrics"]
        sharpe = m.get("sharpe", 0); wr = m.get("win_rate", 0)
        status = "PASS" if sharpe >= 1.5 and wr >= 65 else "WORKING"
        report.append(f"| {strat_name} | {sharpe:.2f} | {wr:.1f} | {status} |")

    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="V3 Near-Pass Suite")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--no-run", action="store_true")
    args = parser.parse_args()

    if not args.no_run:
        run_optimization_batch(STRATEGIES_TO_RUN, quick=args.quick, extended=args.extended)

    results = aggregate_results()
    report = generate_summary_report(results)
    
    report_file = PROJECT_ROOT / "results" / "reports" / "near_pass_report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w") as f:
        f.write(report)

    print(f"\n[OK] V3 Report saved to: {report_file}")

if __name__ == "__main__":
    main()
