import json
import os

def extract_summary():
    json_path = "results/daily_validation/dashboard_20260421_230853.json"
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    perf = data.get('charts', {}).get('performance_matrix', [])
    
    strategies = {}
    for entry in perf:
        name = entry['strategy']
        if name not in strategies:
            strategies[name] = []
        strategies[name].append(entry)

    print("| Strategy | Best Pair | Best Tier | All Pairs (Tiers) |")
    print("|---|---|---|---|")
    
    for name, entries in strategies.items():
        # Sort by Tier (T1 > T2 > T3) then by Sharpe
        tier_map = {"TIER_1": 1, "TIER_2": 2, "TIER_3": 3, "STAGING": 4}
        entries.sort(key=lambda x: (tier_map.get(x['tier'], 5), -x['sharpe_ratio']))
        
        best = entries[0]
        all_pairs = ", ".join([f"{e['pair']} ({e['tier']})" for e in entries])
        print(f"| {name} | {best['pair']} | {best['tier']} | {all_pairs} |")

if __name__ == "__main__":
    extract_summary()
