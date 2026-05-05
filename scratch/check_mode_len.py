"""Check mode message length."""
import yaml
from pathlib import Path

strat_path = Path("config/strategies.yaml")
with open(strat_path) as f:
    strat_cfg = yaml.safe_load(f)

enabled = []
for s_name, s_def in strat_cfg.items():
    if not isinstance(s_def, dict) or not s_def.get("enabled", False):
        continue
    p_list = ", ".join(s_def.get("pairs", ["N/A"]))
    tf_list = ", ".join(s_def.get("timeframes", ["N/A"]))
    name = s_def.get("name", s_name)
    tier = s_def.get("tier", "")
    enabled.append(f"  • {name} [{tier}]\n    └ {p_list} ({tf_list})")

strat_list = "\n".join(enabled)
msg = f"🛠 Operating Mode: PAPER\n\n📋 Active Strategies:\n{strat_list}"
print(f"Enabled strategies: {len(enabled)}")
print(f"Message length: {len(msg)} chars")
print(f"Exceeds limit: {len(msg) > 4096}")
