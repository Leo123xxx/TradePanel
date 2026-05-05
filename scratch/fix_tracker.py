"""Repair truncated demotion_tracker.json"""
import json

path = "results/demotion_tracker.json"
with open(path, "r") as f:
    raw = f.read()

# Find the last complete entry (last '},' before the truncated key)
last_complete = raw.rfind('},')
if last_complete > 0:
    fixed = raw[:last_complete + 1] + '\n}'
    parsed = json.loads(fixed)
    print(f"Repaired JSON: {len(parsed)} entries, valid=True")
    with open(path, "w") as f:
        json.dump(parsed, f, indent=2)
    print("File saved successfully")
else:
    print("Could not find repair point")
