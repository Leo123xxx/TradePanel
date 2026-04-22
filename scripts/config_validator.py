#!/usr/bin/env python3
import yaml
import sys
from pathlib import Path

def validate_config(config_path):
    print(f"Validating {config_path}...")
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML: {e}")
        return False

    required_fields = ['name', 'category', 'status', 'tier', 'enabled', 'pairs', 'timeframes']
    valid_tiers = ['TIER_1', 'TIER_2', 'TIER_3', 'STAGING', 'DISABLED']
    
    errors = []
    tier_counts = {}

    for strat_id, strat_data in data.items():
        if not isinstance(strat_data, dict):
            continue
            
        # Check required fields
        for field in required_fields:
            if field not in strat_data:
                errors.append(f"Strategy '{strat_id}' is missing required field: {field}")
        
        # Check tier validity
        tier = strat_data.get('tier')
        if tier and tier not in valid_tiers:
            errors.append(f"Strategy '{strat_id}' has invalid tier: {tier}")
        
        # Count tiers for summary
        if tier:
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
        # Check mode for STAGING
        if tier == 'STAGING' and strat_data.get('mode') != 'monitor_only':
            errors.append(f"Strategy '{strat_id}' is STAGING but mode is not 'monitor_only'")

    if errors:
        print("\nValidation Errors:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("\nValidation Successful!")
    print(f"Tier Distribution: {tier_counts}")
    return True

if __name__ == "__main__":
    config_file = Path("config/strategies.yaml")
    if not validate_config(config_file):
        sys.exit(1)
