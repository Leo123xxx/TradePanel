import json
import yaml
import os
import shutil

# Paths
REPORT_PATH = r"F:\REPOS\leo123xxx\TradePanel\results\overnight\20260510_backtest_report_final.json"
STRATEGIES_YAML = r"f:\REPOS\leo123xxx\TradePanel\config\strategies.yaml"

def process_reviews():
    if not os.path.exists(REPORT_PATH):
        return

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(STRATEGIES_YAML, 'r', encoding='utf-8') as f:
        strategies = yaml.safe_load(f)

    results = data.get("results", [])
    
    strat_decisions = {} 

    for res in results:
        strat_id = res['strategy']
        status = res['status']
        wr = res.get('win_rate', 0)
        sharpe = res.get('sharpe_ratio', 0)
        trades = res.get('total_trades', 0)
        pf = res.get('profit_factor', 0)
        pair = res['pair']

        if strat_id not in strategies: continue

        # NEW REQUIREMENTS: 
        # 1. Promote if Win Rate >= 65% AND Sample Size >= 10
        # 2. Promote if Sharpe >= 3.5 AND Sample Size >= 20 (even if WR is < 65%)
        # 3. Promote if PF >= 2.5 AND Sample Size >= 15
        
        is_high_quality = (
            (wr >= 65 and trades >= 10) or 
            (sharpe >= 3.5 and trades >= 20) or
            (pf >= 2.5 and trades >= 15)
        )

        if is_high_quality:
            strat_decisions[strat_id] = 'TIER_1'
        
        elif status == "REVIEW" and trades < 5 and strat_decisions.get(strat_id) != 'TIER_1':
            strat_decisions[strat_id] = 'TIER_3'

        # Apply tweaks for the "Close" candidates
        if status == "REVIEW" and 55 <= wr < 65:
            if 'pair_overrides' not in strategies[strat_id]:
                strategies[strat_id]['pair_overrides'] = {}
            if pair not in strategies[strat_id]['pair_overrides']:
                strategies[strat_id]['pair_overrides'][pair] = {}
            
            strategies[strat_id]['pair_overrides'][pair]['adx_min'] = 30 # Tighten
            current_tp = strategies[strat_id]['parameters'].get('tp_atr_mult', 2.0)
            strategies[strat_id]['pair_overrides'][pair]['tp_atr_mult'] = round(current_tp + 0.3, 1)

    # Apply decisions
    for s_id, tier in strat_decisions.items():
        strategies[s_id]['tier'] = tier

    # Save
    shutil.copy(STRATEGIES_YAML, STRATEGIES_YAML + ".bak_latest")
    with open(STRATEGIES_YAML, 'w', encoding='utf-8') as f:
        yaml.dump(strategies, f, sort_keys=False, default_flow_style=False)

    print(f"Update complete. Applied TIER_1 to {list(strat_decisions.values()).count('TIER_1')} strategies.")

if __name__ == "__main__":
    process_reviews()
