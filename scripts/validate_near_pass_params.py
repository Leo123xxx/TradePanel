#!/usr/bin/env python3
"""
validate_near_pass_params.py

Quick validation script for near-pass optimization results.
Compares new parameters against existing baseline, showing improvements.

Usage:
  python scripts/validate_near_pass_params.py hikkake_trap GBPUSD H4 \
    --new-params '{"cooldown_bars": 4, "tp_atr_mult": 2.0}'

  python scripts/validate_near_pass_params.py session_momentum XAUUSD H1 \
    --new-params '{"min_adx_filter": 28, "fast_ema": 12}'
"""

import sys, json, argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.param_optimizer import (
    load_all_strategies, run_backtest, TF_BARS
)


def get_current_params(strategy_name: str) -> dict:
    """Load current parameters from config/strategies.yaml."""
    import yaml
    
    config_file = PROJECT_ROOT / "config" / "strategies.yaml"
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Find the strategy in config
    for strat_name, strat_cfg in config.items():
        if strat_name.lower() == strategy_name.lower():
            return strat_cfg.get("params", {})
    
    return {}


def compare_results(baseline: dict, optimized: dict) -> dict:
    """Compare two metric sets and calculate improvements."""
    if not baseline or not optimized:
        return None
    
    return {
        "sharpe_delta": optimized.get("sharpe", 0) - baseline.get("sharpe", 0),
        "wr_delta": optimized.get("win_rate", 0) - baseline.get("win_rate", 0),
        "pf_delta": optimized.get("profit_factor", 0) - baseline.get("profit_factor", 0),
        "dd_delta": baseline.get("max_dd", 0) - optimized.get("max_dd", 0),  # Lower is better
        "trades_delta": optimized.get("trades", 0) - baseline.get("trades", 0),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate near-pass optimization results")
    parser.add_argument("strategy", help="Strategy name")
    parser.add_argument("pair", help="Pair (e.g., GBPUSD, XAUUSD)")
    parser.add_argument("timeframe", help="Timeframe (e.g., H4, H1, M15)")
    parser.add_argument("--new-params", help="New parameters as JSON string")
    parser.add_argument("--output", help="Save comparison to file")
    args = parser.parse_args()

    strats = load_all_strategies()
    
    if args.strategy not in strats:
        print(f" [ERR] Strategy not found: {args.strategy}")
        return 1

    cls, _, _ = strats[args.strategy]

    # Get current parameters
    current_params = get_current_params(args.strategy)
    print(f"📊 Validation: {args.strategy} | {args.pair} | {args.timeframe}")
    print()

    # Test with current params
    print("[*] Testing CURRENT parameters...")
    baseline = run_backtest(cls, current_params, args.pair, args.timeframe,
                           n_bars=TF_BARS.get(args.timeframe, 500), seed=42)

    if not baseline:
        print(" [ERR] Baseline test failed (no trades)")
        return 1

    print(f" [OK] Baseline results:")
    print(f"   Sharpe: {baseline['sharpe']:.3f}")
    print(f"   WR: {baseline['win_rate']:.1f}%")
    print(f"   PF: {baseline['profit_factor']:.2f}")
    print(f"   Trades: {baseline['trades']:.0f}")
    print()

    # Test with new params
    if not args.new_params:
        print(" [ERR] No new parameters provided (use --new-params)")
        return 1

    try:
        new_params = json.loads(args.new_params)
    except json.JSONDecodeError:
        print(f" [ERR] Invalid JSON for --new-params")
        return 1

    print("[*] Testing NEW parameters...")
    optimized = run_backtest(cls, new_params, args.pair, args.timeframe,
                            n_bars=TF_BARS.get(args.timeframe, 500), seed=42)

    if not optimized:
        print(" [ERR] Optimized test failed (no trades)")
        return 1

    print(f" [OK] Optimized results:")
    print(f"   Sharpe: {optimized['sharpe']:.3f}")
    print(f"   WR: {optimized['win_rate']:.1f}%")
    print(f"   PF: {optimized['profit_factor']:.2f}")
    print(f"   Trades: {optimized['trades']:.0f}")
    print()

    # Compare
    comparison = compare_results(baseline, optimized)
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print()

    # Sharpe improvement
    sharpe_delta = comparison["sharpe_delta"]
    sharpe_status = "[OK]" if sharpe_delta >= 0 else "[FAIL]"
    print(f"{sharpe_status} Sharpe:  {baseline['sharpe']:.3f} → {optimized['sharpe']:.3f} " +
          f"({sharpe_delta:+.3f})")

    # Win rate improvement
    wr_delta = comparison["wr_delta"]
    wr_status = "[OK]" if wr_delta >= 0 else "[FAIL]"
    print(f"{wr_status} Win Rate: {baseline['win_rate']:.1f}% → {optimized['win_rate']:.1f}% " +
          f"({wr_delta:+.1f}pp)")

    # Profit factor improvement
    pf_delta = comparison["pf_delta"]
    pf_status = "[OK]" if pf_delta >= 0 else "[FAIL]"
    print(f"{pf_status} PF:       {baseline['profit_factor']:.2f} → {optimized['profit_factor']:.2f} " +
          f"({pf_delta:+.2f})")

    # Max drawdown improvement (lower is better)
    dd_delta = comparison["dd_delta"]
    dd_status = "[OK]" if dd_delta >= 0 else "[FAIL]"
    print(f"{dd_status} Max DD:   {baseline['max_dd']:.1f}% → {optimized['max_dd']:.1f}% " +
          f"({dd_delta:+.1f}pp)")

    # Trade count
    trades_delta = comparison["trades_delta"]
    print(f"📈 Trades:  {baseline['trades']:.0f} → {optimized['trades']:.0f} " +
          f"({trades_delta:+.0f})")

    print()

    # PASS status check
    SHARPE_THRESHOLD = 1.5
    WR_THRESHOLD = 65.0

    if optimized['sharpe'] >= SHARPE_THRESHOLD and optimized['win_rate'] >= WR_THRESHOLD:
        print("🎉 STATUS: [PASS] CRITERIA MET!")
    elif optimized['sharpe'] >= SHARPE_THRESHOLD or optimized['win_rate'] >= WR_THRESHOLD:
        print(" [NEAR] Status: Partial PASS (one metric missing)")
    else:
        print(" [FAIL] Status: Not yet PASS (needs more tuning)")

    print()

    # Save comparison
    if args.output:
        output = {
            "strategy": args.strategy,
            "pair": args.pair,
            "timeframe": args.timeframe,
            "baseline": baseline,
            "optimized": optimized,
            "comparison": comparison,
            "pass_status": (
                "PASS" if (optimized['sharpe'] >= SHARPE_THRESHOLD and
                          optimized['win_rate'] >= WR_THRESHOLD)
                else "PARTIAL" if (optimized['sharpe'] >= SHARPE_THRESHOLD or
                                  optimized['win_rate'] >= WR_THRESHOLD)
                else "WORKING"
            )
        }
        
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2, default=str)
        
        print(f" [OK] Comparison saved to: {args.output}")

    print()
    print("RECOMMENDATION:")
    if comparison["sharpe_delta"] > 0.1 and comparison["wr_delta"] > 1:
        print(" [OK] These parameters show strong improvement. Update strategies.yaml and test live.")
    elif comparison["sharpe_delta"] > 0 or comparison["wr_delta"] > 0:
        print(" [WARN] Mixed results. Review specific improvements and test on extended data.")
    else:
        print(" [ERR] No improvement detected. Try different parameter ranges or diagnose signal logic.")


if __name__ == "__main__":
    sys.exit(main())
