import sys
import os

# Add project root to sys.path
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import MetaTrader5 as mt5
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()

from forward_test.paper_engine import PaperEngine

def test_reconciliation():
    print("Testing Position Reconciliation...")
    
    # 1. Verify mapping
    engine = PaperEngine()
    print(f"Magic Mapping size: {len(engine.magic_to_strategy)}")
    assert len(engine.magic_to_strategy) > 0, "Magic mapping should not be empty"
    
    # Check if a known strategy is in the mapping
    # Assuming 'macd_trend' exists in STRATEGY_REGISTRY
    import zlib
    from forward_test.paper_engine import STRATEGY_REGISTRY
    
    for name in STRATEGY_REGISTRY:
        magic = zlib.adler32(name.encode()) % 1000000
        assert engine.magic_to_strategy[magic] == name
        print(f"Verified mapping: {magic} -> {name}")
        break # Just check one
        
    # 2. Test reconciliation logic
    if not mt5.initialize():
        print("MT5 NOT CONNECTED - Skipping live check.")
        return

    # Check if any bot positions exist
    positions = mt5.positions_get() or []
    bot_positions = [p for p in positions if p.magic != 0]
    
    if bot_positions:
        print(f"Found {len(bot_positions)} bot positions to reconcile.")
        # Trigger reconciliation
        engine._reconcile_open_positions()
        
        # Verify attempted_signals is populated
        print(f"Processed signals after recon: {len(engine.attempted_signals)}")
        assert len(engine.attempted_signals) > 0, "attempted_signals should be populated after reconciliation"
        
        # Check one ticket
        p = bot_positions[0]
        strat_name = engine.magic_to_strategy.get(p.magic)
        if strat_name:
            print(f"Position ticket={p.ticket} (strat={strat_name}) should be tracked.")
    else:
        print("No bot positions open to verify reconciliation. Open a bot trade to test.")

    print("Position Reconciliation test PASSED!")

if __name__ == "__main__":
    test_reconciliation()
