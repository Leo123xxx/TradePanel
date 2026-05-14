import os
import yaml
from pathlib import Path

def load_config(config_file="config.yaml"):
    """
    Load YAML configuration from the config/ directory.
    """
    root = Path(__file__).parent.parent.parent
    path = root / "config" / config_file
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
        
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_strategies():
    """
    Load strategies.yaml configuration.
    """
    return load_config("strategies.yaml")
