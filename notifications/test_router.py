import asyncio
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from notifications.router import CommandRouter

async def test_all_commands():
    router = CommandRouter()
    
    # Mapping of "command" to actual method in router
    commands = {
        "/help": router.get_help,
        "/status": router.get_status,
        "/health": router.get_health,
        "/balance": router.get_balance,
        "/active": router.get_active,
        "/risk": router.get_risk,
        "/signals": router.get_signals,
        "/analysis": router.get_analysis,
        "/mode": router.get_mode,
        "/wfo": router.get_wfo_summary,
        "/backtest_report": router.get_backtest_report,
        "/best_pairs": router.get_best_pairs,
        "/top_strategies": router.get_top_strategies,
        "/backtest_status": router.get_backtest_status,
        "/params": router.get_strategy_params,
        "/backups": router.get_backups,
        "/data": router.get_data_coverage,
        "/demotion": router.get_demotion,
        "/morning_brief": router.get_morning_brief,
    }
    
    print(f"Testing {len(commands)} router methods...")
    
    for cmd, func in commands.items():
        try:
            print(f"Testing {cmd}...", end=" ")
            # Check if it's a coroutine or regular function
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
            
            if result:
                # print("✅ PASS")
                # Sample the result for the report
                sample = str(result)[:100].replace('\n', ' ')
                print(f"✅ PASS | Sample: {sample}...")
            else:
                print("⚠️ EMPTY RESPONSE")
        except Exception as e:
            print(f"❌ FAIL: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_commands())
