#!/usr/bin/env python3
"""
optimize_near_pass.py

Focused parameter optimization for 8 Near-PASS candidate strategies.
Each candidate is one metric away from PASS status.

Near-PASS candidates (priority order):
  1. hikkake_trap | GBPUSD | H4 — needs +2pp win rate
  2. session_momentum | XAUUSD | H1 — needs +24.4pp win rate
  3. session_momentum | GBPJPY | H1 — needs +22.9pp win rate
  4. range_breakout | US500 | H4 — needs +0.32 Sharpe + 6.1pp WR
  5. dual_ema_momentum | XAUUSD | H1 — needs +0.34 Sharpe + 8.1pp WR
  6. rsi_pullback | GBPJPY | H4 — extending data (currently 80% WR)
  7. rsi_extremes_scalp | USOIL | M15 — extending data (currently 75% WR)
  8. ema_ribbon_trend | NVDA | H4 — needs more trades

Usage:
  python scripts/optimize_near_pass.py                    # all candidates
  python scripts/optimize_near_pass.py --strategy hikkake_trap session_momentum
  python scripts/optimize_near_pass.py --strategy session_momentum --pair XAUUSD
  python scripts/optimize_near_pass.py --quick            # fewer grid points
  python scripts/optimize_near_pass.py --extended         # more aggressive search
"""

import sys, json, argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.param_optimizer import (
    load_all_strategies, run_backtest, GRIDS, make_ohlcv,
    TF_BARS, SCALPER_MIN_TF_MINS
)

# ── Focused parameter grids for near-pass candidates ────────────────────────────
NEAR_PASS_GRIDS = {
    # PRIORITY 1: Only needs +2pp WR to pass (68 → 70)
    "hikkake_trap": {
        "pair": "GBPUSD",
        "timeframe": "H4",
        "focus": "win_rate",
        "params": {
            "cooldown_bars": [2, 3, 4, 5, 6, 8, 10, 12],  # Wider search
            "tp_atr_mult":   [1.5, 1.8, 2.0, 2.2],        # Test TP variations
            "sl_atr_mult":   [0.6, 0.8, 1.0, 1.2],        # Test SL variations
            "atr_period":    [10, 12, 14, 16],
        },
        "n_bars": 1200,  # Increase to get enough trades for H4
    },

    # PRIORITY 2-3: Session momentum needs entry filter tightening (+24pp WR)
    "session_momentum": {
        "pairs": ["XAUUSD", "GBPJPY"],  # Test both together
        "timeframe": "H1",
        "focus": "win_rate",
        "params": {
            "fast_ema":           [8, 10, 12, 15, 20],     # Tighter fast EMA
            "slow_ema":           [20, 34, 50, 75],        # Higher slow EMA
            "min_adx_filter":     [25, 28, 30, 32],        # Increase ADX min (key fix)
            "vol_threshold_mult": [1.0, 1.2, 1.5],        # Volume filter
            "tp_atr_mult":        [1.8, 2.0, 2.2],
            "sl_atr_mult":        [0.8, 1.0],
            "atr_period":         [14],
        }
    },

    # PRIORITY 4: Range breakout needs Sharpe + WR boost
    "range_breakout": {
        "pair": "US500",
        "timeframe": "H4",
        "focus": "sharpe_and_wr",
        "params": {
            "consolidation_bars":  [8, 10, 15, 20, 25],    # Wider consolidation detection
            "vol_threshold_mult":  [1.0, 1.2, 1.5, 1.8],   # Volume filter tuning
            "adx_min_filter":      [15, 18, 20, 25, 28],   # Trend confirmation
            "tp_atr_mult":         [1.8, 2.0, 2.2],
            "sl_atr_mult":         [0.6, 0.8, 1.0],
            "atr_period":          [12, 14, 16],
        }
    },

    # PRIORITY 5: Dual EMA momentum needs improvements on both metrics
    "dual_ema_momentum": {
        "pair": "XAUUSD",
        "timeframe": "H1",
        "focus": "sharpe_and_wr",
        "params": {
            "fast_ema":      [8, 10, 15, 20, 30],          # Wider fast range
            "slow_ema":      [50, 75, 100, 150],           # Higher slow EMA
            "adx_min":       [20, 25, 28, 30],             # ADX filter (key)
            "tp_atr_mult":   [1.8, 2.0, 2.2, 2.5],
            "sl_atr_mult":   [0.6, 0.8, 1.0, 1.2],
            "atr_period":    [10, 12, 14, 16],
        }
    },

    # PRIORITY 6: RSI pullback (already 80% WR) — validate on more data
    "rsi_pullback": {
        "pair": "GBPJPY",
        "timeframe": "H4",
        "focus": "validation",
        "params": {
            "rsi_period":         [14],
            "fast_ema":           [20, 50],
            "slow_ema":           [100, 200],
            "rsi_pullback_lower": [30, 35],
            "rsi_pullback_upper": [50, 55, 60],
            "tp_atr_mult":        [2.0],
            "sl_atr_mult":        [0.8, 1.0],
            "atr_period":         [14],
        }
    },

    # PRIORITY 7: RSI extremes scalp (already 75% WR) — validate on more data
    # NOTE: This is a scalper, must ensure it runs on M15+ (not M1)
    "rsi_extremes_scalp": {
        "pair": "USOIL",
        "timeframe": "M15",
        "focus": "validation",
        "params": {
            "rsi_period":    [7, 14],
            "oversold":      [20, 25, 30],
            "overbought":    [70, 75, 80],
            "tp_atr_mult":   [2.0],
            "sl_atr_mult":   [0.8, 1.0],
            "atr_period":    [14],
        }
    },

    # PRIORITY 8: EMA ribbon trend on NVDA — extend data to get 20+ trades
    "ema_ribbon_trend": {
        "pair": "NVDA",
        "timeframe": "H4",
        "focus": "data_extension",
        "params": {
            "fast_ema":    [5, 8, 10, 13],
            "mid_ema":     [21, 34, 50],
            "slow_ema":    [55, 89, 144],
            "adx_min":     [18, 20, 25],
            "tp_atr_mult": [2.0],
            "sl_atr_mult": [0.8, 1.0],
            "atr_period":  [14],
        }
    },
}

PASS_THRESHOLDS = {
    "sharpe": 1.5,
    "win_rate": 65.0,
    "trades": 10,
}

def grid_search_focused(strategy_name: str, cls, cfg: dict,
                       pairs_tfs: list, quick: bool = False) -> list:
    """
    Run focused grid search on given strategy/pair/TF combinations.
    Returns sorted list of (params, metrics) tuples.
    """
    from itertools import product
    
    results = []
    params_grid = cfg["params"]
    params_list = list(product(*params_grid.values()))
    
    if quick:
        # Sample every 2nd combo for quick runs
        params_list = params_list[::2] if len(params_list) > 10 else params_list
    
    for i, param_values in enumerate(params_list):
        params_dict = dict(zip(params_grid.keys(), param_values))
        
        for pair, tf in pairs_tfs:
            try:
                n_bars = cfg.get("n_bars", TF_BARS.get(tf, 500))
                metrics = run_backtest(cls, params_dict, pair, tf,
                                      n_bars=n_bars, seed=42)
                
                if metrics is None or metrics["trades"] < PASS_THRESHOLDS["trades"]:
                    continue
                
                score = (metrics.get("sharpe", 0) * 0.4 +
                        (metrics.get("win_rate", 0) / 100.0) * 0.6)
                results.append({
                    "params": params_dict,
                    "metrics": metrics,
                    "pair": pair,
                    "tf": tf,
                    "score": score,
                })
            except Exception as e:
                print(f"  ERROR [{strategy_name} {pair} {tf}]: {e}")
                continue
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Optimize Near-PASS candidate strategies")
    parser.add_argument("--strategy", nargs="+", help="Strategy names to optimize")
    parser.add_argument("--pair", help="Override pair for single strategy")
    parser.add_argument("--quick", action="store_true", help="Quick run (fewer grid points)")
    parser.add_argument("--extended", action="store_true", help="Extended search (more grid points)")
    args = parser.parse_args()

    strats = load_all_strategies()
    output_file = PROJECT_ROOT / "results" / "optimization" / "near_pass_optimization.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results_all = {}

    # Determine which strategies to optimize
    if args.strategy:
        strategies_to_run = [s for s in args.strategy if s in NEAR_PASS_GRIDS]
    else:
        strategies_to_run = list(NEAR_PASS_GRIDS.keys())

    for strategy_name in strategies_to_run:
        if strategy_name not in strats:
            print(f"  [WARN] Strategy not found: {strategy_name}")
            continue

        if strategy_name not in NEAR_PASS_GRIDS:
            print(f"  [WARN] No near-pass grid for: {strategy_name}")
            continue

        cfg = NEAR_PASS_GRIDS[strategy_name]
        cls, default_pair, default_tf = strats[strategy_name]

        # Determine pair/TF combinations
        if "pair" in cfg:
            pairs_tfs = [(cfg["pair"], cfg["timeframe"])]
        elif "pairs" in cfg:
            pairs_tfs = [(p, cfg["timeframe"]) for p in cfg["pairs"]]
        else:
            pairs_tfs = [(default_pair, default_tf)]

        # Override pair if specified
        if args.pair:
            pairs_tfs = [(args.pair, pairs_tfs[0][1])]

        print(f"\n[*] {strategy_name.upper()}")
        print(f"   Pairs: {pairs_tfs}")
        print(f"   Focus: {cfg.get('focus', 'general')}")
        print(f"   Running grid search...", end="", flush=True)

        best_results = grid_search_focused(
            strategy_name, cls, cfg, pairs_tfs, quick=args.quick
        )

        if not best_results:
            print(" NO RESULTS")
            results_all[strategy_name] = {"status": "NO_RESULTS", "results": []}
            continue

        top_5 = best_results[:5]
        results_all[strategy_name] = {
            "status": "OK",
            "total_combos": len(best_results),
            "top_5": [
                {
                    "params": r["params"],
                    "metrics": r["metrics"],
                    "pair": r["pair"],
                    "tf": r["tf"],
                    "score": r["score"],
                }
                for r in top_5
            ]
        }

        # Print summary
        best = top_5[0]
        m = best["metrics"]
        print(f" [OK]")
        print(f"   Best result for {best['pair']} {best['tf']}:")
        print(f"     Sharpe: {m['sharpe']:.3f} | WR: {m['win_rate']:.1f}% | " +
              f"PF: {m['profit_factor']:.2f} | Trades: {m['trades']:.0f}")
        print(f"     Params: {best['params']}")

    # Save results
    with open(output_file, "w") as f:
        json.dump(results_all, f, indent=2, default=str)

    print(f"\n[OK] Results saved to: {output_file}")
    print(f"\n[INFO] Summary:")
    print(f"   Strategies run: {len([s for s in results_all if results_all[s]['status'] == 'OK'])}")
    print(f"   Total combos tested: {sum([results_all[s].get('total_combos', 0) for s in results_all])}")


if __name__ == "__main__":
    main()
