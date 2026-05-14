import yaml
import os

# Paths
STRATEGIES_YAML = r"f:\REPOS\leo123xxx\TradePanel\config\strategies.yaml"
DOC_PATH = r"f:\REPOS\leo123xxx\TradePanel\docs\STRATEGY_MASTER_LIST.md"

def generate_doc():
    with open(STRATEGIES_YAML, 'r', encoding='utf-8') as f:
        strategies = yaml.safe_load(f)

    tier1 = []
    tier2 = []
    tier3 = []

    for key, val in strategies.items():
        if key == 'active': continue
        if not isinstance(val, dict): continue
        
        info = {
            'id': key,
            'name': val.get('name', key),
            'cat': val.get('category', 'N/A'),
            'pairs': ", ".join(val.get('pairs', [])[:5]) + ("..." if len(val.get('pairs', [])) > 5 else ""),
            'tfs': ", ".join(val.get('timeframes', [])[:4]),
            'tier': val.get('tier', 'TIER_3')
        }
        
        if info['tier'] == 'TIER_1': tier1.append(info)
        elif info['tier'] == 'TIER_2': tier2.append(info)
        else: tier3.append(info)

    md = f"""# 📈 TradePanel Strategy Master List
    
This document is automatically generated and synchronized with `strategies.yaml`.
Last Updated: 2026-05-10

---

## 🏆 TIER 1: High Conviction (Proven Edge)
Strategies with Win Rate >= 65% or exceptional Sharpe ratios. Fully enabled for production.

| Strategy | Category | Primary Pairs | Timeframes |
| :--- | :--- | :--- | :--- |
"""
    for s in sorted(tier1, key=lambda x: x['name']):
        md += f"| **{s['name']}** | {s['cat']} | {s['pairs']} | {s['tfs']} |\n"

    md += """
---

## 🛰️ TIER 2: Active Validation (Live Demo Testing)
Strategies undergoing final tweaks or scaling up from Tier 3.

| Strategy | Category | Primary Pairs | Timeframes |
| :--- | :--- | :--- | :--- |
"""
    for s in sorted(tier2, key=lambda x: x['name']):
        md += f"| **{s['name']}** | {s['cat']} | {s['pairs']} | {s['tfs']} |\n"

    md += """
---

## 🧪 TIER 3: Incubator (Experimental / Low Sample)
Strategies currently disabled or limited to backtesting due to insufficient data.

| Strategy | Category | Primary Pairs | Timeframes |
| :--- | :--- | :--- | :--- |
"""
    for s in sorted(tier3, key=lambda x: x['name']):
        md += f"| **{s['name']}** | {s['cat']} | {s['pairs']} | {s['tfs']} |\n"

    with open(DOC_PATH, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"Documentation generated at {DOC_PATH}")

if __name__ == "__main__":
    generate_doc()
