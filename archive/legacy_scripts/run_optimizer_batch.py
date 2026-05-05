#!/usr/bin/env python3
"""
run_optimizer_batch.py -- Runs param_optimizer in batches, saving results after each strategy.
Designed to survive 40-second sandbox limits by writing results incrementally.

Usage:
    python scripts/run_optimizer_batch.py --batch 0   # strategies 0-6
    python scripts/run_optimizer_batch.py --batch 1   # strategies 7-13
    python scripts/run_optimizer_batch.py --batch 2   # strategies 14-21
    python scripts/run_optimizer_batch.py --merge      # merge all batch outputs
"""

import sys, os, json, argparse, itertools
from pathlib import Path
from datetime import datetime

import numpy as np

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backtesting.engine import BacktestEngine
from scripts.param_optimizer import (
    make_ohlcv, run_backtest, load_all_strategies, GRIDS, grid_search
)

PASS_WR   = 60.0
OUT_DIR   = PROJECT_ROOT / "results" / "daily_validation"


def run_batch(batch_idx: int):
    """Run one batch of ~7 strategies and write results to a batch JSON file."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    strats = load_all_strategies()
    eligible = [(name, val) for name, val in strats.items() if name in GRIDS]
    BATCH_SIZE = 7
    start = batch_idx * BATCH_SIZE
    end   = min(start + BATCH_SIZE, len(eligible))
    batch = eligible[start:end]

    if not batch:
        print(f"Batch {batch_idx}: nothing to process (start={start} >= {len(eligible)})")
        return {}

    print(f"\n{'='*70}")
    print(f"  Batch {batch_idx}  |  Strategies {start+1}-{end} of {len(eligible)}")
    print(f"  mode=ULTRAQUICK  seeds=1  max_combos=20")
    print(f"{'='*70}\n")

    results = {}

    for name, (cls, pair, tf) in batch:
        print(f"  {name:<35} {pair} {tf} ...", end="", flush=True)

        # ultraquick: 1 seed, 20 combos, 400 bars
        best = grid_search(name, cls, pair, tf, GRIDS[name], quick=True, seeds=(42,))

        if best["metrics"] is None:
            print(" NO TRADES")
            results[name] = {"status": "NO_TRADES", "params": best["params"], "metrics": None}
            continue

        m   = best["metrics"]
        wr  = m["win_rate"]
        status = "PASS" if wr >= PASS_WR else ("NEAR" if wr >= 50 else "FAIL")
        tag = {"PASS": "[PASS]", "NEAR": "[NEAR]", "FAIL": "[FAIL]"}[status]
        print(f" {tag}  WR={wr:.1f}%  PF={m['profit_factor']:.2f}"
              f"  trades={m['trades']:.0f}  PnL=R{m['pnl_zar']:.0f}")
        print(f"       params: {best['params']}")

        results[name] = {"status": status, "params": best["params"], "metrics": m}

    # Save batch results
    out_path = OUT_DIR / f"opt_batch_{batch_idx}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Batch {batch_idx} saved: {out_path}")
    return results


def merge_batches():
    """Merge all batch JSON files into a single optimization_params file."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    merged = {}

    for i in range(10):
        p = OUT_DIR / f"opt_batch_{i}.json"
        if p.exists():
            with open(p) as f:
                merged.update(json.load(f))
            print(f"  Merged batch {i}: {p}")

    if not merged:
        print("No batch files found.")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = OUT_DIR / f"optimization_params_{ts}.json"
    with open(out, "w") as f:
        json.dump(merged, f, indent=2, default=str)

    passed = [n for n, r in merged.items() if r.get("status") == "PASS"]
    near   = [n for n, r in merged.items() if r.get("status") == "NEAR"]
    failed = [n for n, r in merged.items() if r.get("status") in ("FAIL", "NO_TRADES")]

    print(f"\n{'='*70}")
    print(f"  FINAL SUMMARY: {len(passed)} PASS | {len(near)} NEAR | {len(failed)} FAIL")
    print(f"{'='*70}")
    print(f"  Passed: {', '.join(passed)}")
    if near:   print(f"  Near:   {', '.join(near)}")
    if failed: print(f"  Failed: {', '.join(failed)}")
    print(f"\n  Full results: {out}")
    return merged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=-1)
    parser.add_argument("--merge", action="store_true")
    args = parser.parse_args()

    if args.merge:
        merge_batches()
    elif args.batch >= 0:
        run_batch(args.batch)
    else:
        print("Usage: --batch N  or  --merge")


if __name__ == "__main__":
    main()
