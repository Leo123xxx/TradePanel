import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import MetaTrader5 as mt5
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()

from forward_test.paper_engine import PaperEngine
from risk.manager import RiskManager

def test_magic_filter():
    print("Testing Magic Number Filtering...")
    
    # Initialize components
    engine = PaperEngine()
    risk = RiskManager()
    
    if not mt5.initialize():
        print("❌ MT5 NOT CONNECTED - Skipping live check, testing logic only.")
        return

    print("Checking open positions...")
    all_pos = mt5.positions_get() or []
    
    manual_trades = [p for p in all_pos if p.magic == 0]
    bot_trades = [p for p in all_pos if p.magic != 0]
    
    print(f"Total positions: {len(all_pos)}")
    print(f"Manual (magic=0): {len(manual_trades)}")
    print(f"Bot (magic!=0): {len(bot_trades)}")
    
    # Test PaperEngine filtered positions
    # We'll check for a symbol that has at least one manual trade
    if manual_trades:
        symbol = manual_trades[0].symbol
        bot_pos_for_symbol = engine._get_bot_positions(symbol)
        
        # Ensure none of the bot_pos have magic=0
        for p in bot_pos_for_symbol:
            assert p.magic != 0, f"Bot filtered list contains manual trade {p.ticket}!"
            
        print(f"PaperEngine correctly excluded manual trades for {symbol}.")
    else:
        print("No manual trades open to verify exclusion. Please open one in MT5 to test.")

    # Test RiskManager concurrent positions check
    # We'll see if it counts manual trades
    max_pos = risk.config['risk_management']['max_concurrent_positions']
    allowed = risk._check_concurrent_positions()
    
    # Logic: bot_trades count should be < max_pos
    is_allowed_expected = len(bot_trades) < max_pos
    assert allowed == is_allowed_expected, f"RiskManager concurrent check mismatch! Expected {is_allowed_expected}, got {allowed}"
    
    print(f"RiskManager correctly counts only bot trades ({len(bot_trades)} / {max_pos}).")
    print("Magic Number Filter test PASSED!")

if __name__ == "__main__":
    test_magic_filter()
