"""Check if demotion message exceeds Telegram's 4096 char limit."""
import json

with open("results/demotion_tracker.json") as f:
    tracker = json.load(f)

print(f"Entries: {len(tracker)}")

# Simulate the message
msg = "⚠️ Demotion Tracker\n━━━━━━━━━━━━━━━\n"
for strat, info in sorted(tracker.items(), key=lambda x: -x[1].get("consecutive_fails", 0)):
    consec = info.get("consecutive_fails", 0)
    last_wr = info.get("last_wr")
    wr_str = f"{last_wr:.1f}%" if isinstance(last_wr, (int, float)) else "N/A"
    icon = "🔴" if consec >= 5 else ("🟡" if consec >= 3 else "🟢")
    msg += f"{icon} {strat}: {consec} consecutive fails | last WR {wr_str}\n"
msg += "\nAuto-demotion triggers at 5 consecutive fails."

print(f"Message length: {len(msg)} chars")
print(f"Telegram limit: 4096 chars")
print(f"Exceeds limit: {len(msg) > 4096}")
