import sys
import os
from datetime import datetime, date

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient
from scheduler.docker_jobs import TradingScheduler
from risk.manager import RiskManager

def test_circuit_breaker():
    print("Testing Hard Drawdown Circuit Breaker...")
    db = DBClient()
    risk = RiskManager()
    
    # 1. Clean up old test data
    db.execute_query("DELETE FROM bot_health WHERE event_type = 'CIRCUIT_BREAKER'")
    db.execute_query("DELETE FROM daily_summary WHERE date = %s", (date.today(),))
    
    # 2. Verify bot is NOT paused initially
    is_paused, msg = risk._is_bot_paused()
    print(f"Initial state: Paused={is_paused}, Msg='{msg}'")
    assert not is_paused, "Bot should not be paused initially"
    
    # 3. Mock a huge loss in trades table
    import uuid
    db.execute_query(
        "INSERT INTO trades (trade_id, strategy_id, account_id, mode, pair, direction, lot_size, entry_price, exit_price, net_pnl, status, close_time) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (str(uuid.uuid4()), 1, 1, 'PAPER', 'XAUUSD', 'BUY', 1.0, 2000, 1850, -15000, 'CLOSED', datetime.now())
    )
    
    # 4. Run the scheduler rollup to trigger breaker
    # We need a mock scheduler or just call the method
    # For testing, we'll manually trigger the breaker logic
    scheduler = TradingScheduler()
    
    print("Running PnL roll-up check...")
    import MetaTrader5 as mt5
    if mt5.initialize():
        info = mt5.account_info()
        print(f"MT5 Account Balance: {info.balance}")
        print(f"Mocked Daily P&L: -15000")
        loss_pct = abs(-15000) / info.balance * 100
        print(f"Calculated Loss %: {loss_pct:.2f}%")
        
    # This should trigger _trigger_circuit_breaker internally
    scheduler._rollup_pnl()
    
    # 5. Verify bot_health entry
    rows = db.execute_query(
        "SELECT status, message FROM bot_health WHERE event_type = 'CIRCUIT_BREAKER' AND timestamp >= CURRENT_DATE"
    )
    print(f"Bot Health Rows: {rows}")
    assert len(rows) > 0, "Circuit breaker should have logged to bot_health"
    assert rows[0][0] == 'PAUSED', "Status should be PAUSED"
    
    # 6. Verify RiskManager now blocks trades
    is_paused, msg = risk._is_bot_paused()
    print(f"Final state: Paused={is_paused}, Msg='{msg}'")
    assert is_paused, "RiskManager should now report bot is paused"
    
    # 7. Resume bot
    from notifications.router import CommandRouter
    router = CommandRouter()
    print("Resuming bot...")
    router.resume_bot()
    
    is_paused, msg = risk._is_bot_paused()
    print(f"After resume: Paused={is_paused}")
    assert not is_paused, "Bot should be active after resume"
    
    print("Circuit Breaker test PASSED!")

if __name__ == "__main__":
    test_circuit_breaker()
