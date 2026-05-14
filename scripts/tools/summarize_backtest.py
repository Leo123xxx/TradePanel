
import json
from pathlib import Path

def summarize_backtest():
    report_path = Path("results/overnight/20260510_backtest_report_final.json")
    if not report_path.exists():
        print("Report not found")
        return
    
    with open(report_path, "r") as f:
        data = json.load(f)
    
    results = data.get("results", [])
    passed = [r for r in results if r.get("status") == "PASS" or (r.get("sharpe_ratio", 0) >= 2.0 and r.get("win_rate", 0) >= 60.0)]
    
    print(f"Total backtest runs: {len(results)}")
    print(f"Passed/Winning combos: {len(passed)}")
    for p in passed:
        print(f"Strategy: {p['strategy']}, Pair: {p['pair']}, TF: {p['timeframe']}, Sharpe: {p.get('sharpe_ratio')}, WR: {p.get('win_rate')}%")

if __name__ == "__main__":
    summarize_backtest()
