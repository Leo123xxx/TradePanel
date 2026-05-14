import yaml
import os

# Paths
STRATEGIES_YAML = r"f:\REPOS\leo123xxx\TradePanel\config\strategies.yaml"

def cleanup_strategies():
    with open(STRATEGIES_YAML, 'r', encoding='utf-8') as f:
        strategies = yaml.safe_load(f)

    active_list = []
    tier_1_list = []
    tier_2_list = []
    tier_3_list = []

    for key, value in strategies.items():
        if key == 'active': continue
        if not isinstance(value, dict): continue

        tier = value.get('tier', 'TIER_3')
        
        if tier == 'TIER_1':
            tier_1_list.append(key)
            value['enabled'] = True
            active_list.append(key)
        elif tier == 'TIER_2':
            tier_2_list.append(key)
            value['enabled'] = True
            active_list.append(key)
        else:
            tier_3_list.append(key)
            value['enabled'] = False

    # Update active list
    strategies['active'] = active_list

    # Save
    with open(STRATEGIES_YAML, 'w', encoding='utf-8') as f:
        yaml.dump(strategies, f, sort_keys=False, default_flow_style=False)

    print(f"Cleanup Complete:")
    print(f"- Active (T1/T2): {len(active_list)}")
    print(f"- Disabled (T3): {len(tier_3_list)}")
    print(f"- Tier 1: {len(tier_1_list)}")
    print(f"- Tier 2: {len(tier_2_list)}")

if __name__ == "__main__":
    cleanup_strategies()
