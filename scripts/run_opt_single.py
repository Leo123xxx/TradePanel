#!/usr/bin/env python3
"""Run optimizer for a single strategy and append result to a shared JSON file."""
import sys, json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.param_optimizer import load_all_strategies, GRIDS, grid_search

PASS_WR  = 60.0
OUT_FILE = PROJECT_ROOT / "results" / "daily_validation" / "opt_results.json"

def main():
    name = sys.argv[1]
    strats = load_all_strategies()

    if name not in strats:
        print(f"Unknown strategy: {name}"); return
    if name not in GRIDS:
        print(f"No grid for: {name}"); return

    cls, pair, tf = strats[name]
    print(f"  {name} | {pair} {tf} ...", end="", flush=True)

    best = grid_search(name, cls, pair, tf, GRIDS[name], quick=True, seeds=(42,))

    if best["metrics"] is None:
        result = {"status": "NO_TRADES", "params": best["params"], "metrics": None}
        print(" NO TRADES")
    else:
        m = best["metrics"]
        wr = m["win_rate"]
        status = "PASS" if wr >= PASS_WR else ("NEAR" if wr >= 50 else "FAIL")
        result = {"status": status, "params": best["params"], "metrics": m}
        print(f" [{status}] WR={wr:.1f}%  PF={m['profit_factor']:.2f}"
              f"  trades={m['trades']:.0f}  PnL=R{m['pnl_zar']:.0f}")
        print(f"  params: {best['params']}")

    # Load existing results and merge
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if OUT_FILE.exists():
        with open(OUT_FILE) as f:
            existing = json.load(f)
    existing[name] = result
    with open(OUT_FILE, "w") as f:
        json.dump(existing, f, indent=2, default=str)

if __name__ == "__main__":
    main()
