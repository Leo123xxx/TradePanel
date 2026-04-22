import yaml
import os
import sys

# Add project root to path
sys.path.insert(0, os.getcwd())
from scripts.run_backtest import STRATEGY_MAP

def find_missing():
    path = "config/strategies.yaml"
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    yaml_keys = set(data.keys())
    map_keys = set(STRATEGY_MAP.keys())
    
    missing_in_yaml = map_keys - yaml_keys
    extra_in_yaml = yaml_keys - map_keys
    
    print(f"Missing in YAML: {missing_in_yaml}")
    print(f"Extra in YAML (not in backtest map): {extra_in_yaml}")

if __name__ == "__main__":
    find_missing()
