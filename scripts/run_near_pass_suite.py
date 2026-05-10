#!/usr/bin/env python3
"""
run_near_pass_suite.py

Master orchestrator for near-pass candidate optimization.
Runs the full suite of focused optimizations, aggregates results,
and generates recommendations.

Usage:
  python scripts/run_near_pass_suite.py                    # Full suite
  python scripts/run_near_pass_suite.py --quick             # Quick validation
  python scripts/run_near_pass_suite.py --extended          # Aggressive search
"""

import sys, json, subprocess, argparse
from pathlib import Path
from datetime import datetime
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
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


def run_optimization_batch(strategy_names: list, quick: bool = False) -> dict:
    """Run optimize_near_pass.py for all strategies in one go."""
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "optimize_near_pass.py"),
        "--strategy",
    ] + strategy_names
    
    if quick:
        cmd.append("--quick")

    print(f"\n[*] Running: {' '.join(cmd)}")
    # We use capture_output=False here so that optimize_near_pass.py's live output 
    # (which we already fixed for Unicode) prints directly to the terminal.
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode != 0:
        print(f"  [WARN] Non-zero exit code: {result.returncode}")
        return {"status": "ERROR"}

    return {"status": "OK"}


def aggregate_results() -> dict:
    """Load and aggregate results from optimization runs."""
    opt_file = PROJECT_ROOT / "results" / "optimization" / "near_pass_optimization.json"
    
    if not opt_file.exists():
        print(f"  [WARN] No results file found: {opt_file}")
        return {}

    with open(opt_file) as f:
        data = json.load(f)

    return data


def generate_summary_report(results: dict) -> str:
    """Generate markdown summary of optimization results."""
    report = []
    report.append("# Near-PASS Optimization Results")
    report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

    # Overview table
    report.append("## Overview\n")
    report.append("| Strategy | Pairs Tested | Best Sharpe | Best WR% | Status |")
    report.append("|----------|--------------|-------------|---------|--------|")

    promotions = []  # Strategies that passed thresholds
    improvements = []  # Strategies that improved but not yet pass
    
    for strat_name, strat_data in results.items():
        if strat_data.get("status") != "OK":
            report.append(f"| {strat_name} | - | - | - | [ERR] |")
            continue

        top_5 = strat_data.get("top_5", [])
        if not top_5:
            report.append(f"| {strat_name} | - | - | - | [EMPTY] |")
            continue

        best = top_5[0]
        m = best["metrics"]
        sharpe = m.get("sharpe", 0)
        wr = m.get("win_rate", 0)
        pairs = len(set(r["pair"] for r in top_5))

        # Determine status
        if sharpe >= PASS_THRESHOLDS["sharpe"] and wr >= PASS_THRESHOLDS["win_rate"]:
            status = "PASS"
            promotions.append(strat_name)
        elif sharpe >= PASS_THRESHOLDS["sharpe"] or wr >= PASS_THRESHOLDS["win_rate"]:
            status = "PARTIAL"
            improvements.append(strat_name)
        else:
            status = "WORKING"
            improvements.append(strat_name)

        report.append(f"| {strat_name} | {pairs} | {sharpe:.2f} | {wr:.1f} | {status} |")

    # Detail sections
    report.append("\n\n## Detailed Results\n")

    for strat_name, strat_data in results.items():
        if strat_data.get("status") != "OK":
            continue

        top_5 = strat_data.get("top_5", [])
        if not top_5:
            continue

        report.append(f"### {strat_name.upper()}\n")
        report.append(f"**Total combos tested:** {strat_data.get('total_combos', 0)}\n")

        for i, result in enumerate(top_5, 1):
            m = result["metrics"]
            p = result["params"]
            
            report.append(f"#### #{i} — {result['pair']} {result['tf']}\n")
            report.append(f"- **Score:** {result['score']:.3f}")
            report.append(f"- **Sharpe:** {m['sharpe']:.3f}")
            report.append(f"- **Win Rate:** {m['win_rate']:.1f}%")
            report.append(f"- **Profit Factor:** {m['profit_factor']:.2f}")
            report.append(f"- **Max Drawdown:** {m['max_dd']:.1f}%")
            report.append(f"- **Trades:** {m['trades']:.0f}")
            report.append(f"- **PnL (ZAR):** R{m['pnl_zar']:.2f}")
            report.append("\n**Parameters:**\n```\n")
            
            for param_name, param_value in p.items():
                report.append(f"  {param_name}: {param_value}\n")
            
            report.append("```\n")

    # Recommendations
    report.append("\n## Recommendations\n")
    
    if promotions:
        report.append(f"### [PASS] Promoted to PASS Status\n")
        report.append(f"The following {len(promotions)} strateg(y/ies) now meet PASS criteria:\n\n")
        for strat in promotions:
            report.append(f"- **{strat}** — Update parameters in `config/strategies.yaml`\n")
    
    if improvements:
        report.append(f"### [NEAR] Near-PASS (Close to Promotion)\n")
        report.append(f"The following {len(improvements)} strateg(y/ies) show improvement but need tuning:\n\n")
        for strat in improvements:
            report.append(f"- **{strat}** — Review top parameter sets above\n")

    report.append("\n## Next Steps\n")
    report.append("1. Review promoted strategies' parameters in detail\n")
    report.append("2. Validate promising parameters with extended backtest window\n")
    report.append("3. Update `config/strategies.yaml` with new parameters for promoted strategies\n")
    report.append("4. Re-run overnight backtest to confirm improvements\n")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Run full near-pass optimization suite")
    parser.add_argument("--quick", action="store_true", help="Quick validation run")
    parser.add_argument("--extended", action="store_true", help="Extended search")
    parser.add_argument("--no-run", action="store_true", help="Only aggregate existing results")
    args = parser.parse_args()

    print("=" * 70)
    print("NEAR-PASS STRATEGY OPTIMIZATION SUITE")
    print("=" * 70)

    if not args.no_run:
        print(f"\n[*] Starting focused optimization suite for {len(STRATEGIES_TO_RUN)} strategies...")
        status = run_optimization_batch(STRATEGIES_TO_RUN, quick=args.quick)
        if status["status"] != "OK":
            print(f"  [FAIL] Optimization suite exited with errors.")

    print("\n\n[INFO] Aggregating results...")
    results = aggregate_results()

    print(f"   Found results for {len(results)} strategies")

    # Generate report
    report = generate_summary_report(results)
    
    # Save report
    report_file = PROJECT_ROOT / "results" / "optimization" / "near_pass_report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w") as f:
        f.write(report)

    print(f"\n[OK] Report saved to: {report_file}")
    
    # Print summary to console
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(report)


if __name__ == "__main__":
    main()
