import sys
import os
from unittest.mock import MagicMock, patch
import MetaTrader5 as mt5

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forward_test.paper_engine import PaperEngine

def test_breakeven_logic():
    print("\n--- Testing Breakeven Management ---")
    
    # Mock PaperEngine dependencies
    with patch('forward_test.paper_engine.MT5Connector'), \
         patch('forward_test.paper_engine.OrderManager') as mock_order_mgr_class, \
         patch('forward_test.paper_engine.RiskManager'), \
         patch('forward_test.paper_engine.SignalChecker'), \
         patch('forward_test.paper_engine.DBClient'), \
         patch('forward_test.paper_engine.TelegramBot'), \
         patch('forward_test.paper_engine.CommandRouter'), \
         patch('MetaTrader5.symbol_info') as mock_symbol_info:

        mock_order_mgr = mock_order_mgr_class.return_value
        mock_order_mgr.modify_position.return_value = (MagicMock(retcode=mt5.TRADE_RETCODE_DONE), "SUCCESS")

        engine = PaperEngine()
        
        # Setup strategy with breakeven enabled
        mock_strategy = MagicMock()
        mock_strategy.params = {
            'use_breakeven': True,
            'breakeven_trigger_mult': 1.5
        }
        
        # Setup symbol info (XAUUSD)
        symbol = "XAUUSD"
        mock_symbol_info.return_value = MagicMock(
            point=0.01,
            digits=2,
            bid=2050.00,  # Current Price
            ask=2050.05,
            trade_tick_value=1.66,
            trade_tick_size=0.01
        )
        
        # Setup a profitable position
        mock_pos = MagicMock(
            ticket=12345,
            symbol=symbol,
            type=mt5.POSITION_TYPE_BUY,
            price_open=2000.00,
            sl=1950.00,
            tp=2100.00
        )
        
        latest_atr = 10.00
        print(f"Testing BUY position: Entry={mock_pos.price_open}, Current={mock_symbol_info.return_value.bid}, ATR={latest_atr}")
        
        engine._manage_breakeven(symbol, mock_strategy, [mock_pos], latest_atr)
        
        if mock_order_mgr.modify_position.called:
            args, kwargs = mock_order_mgr.modify_position.call_args
            new_sl = kwargs.get('sl') if kwargs.get('sl') else args[1]
            print(f"SUCCESS: modify_position called with new_sl={new_sl}")
        else:
            print("FAILED: modify_position was not called")

        # Test Case 2: SELL position
        mock_order_mgr.modify_position.reset_mock()
        mock_pos_sell = MagicMock(
            ticket=54321,
            symbol=symbol,
            type=mt5.POSITION_TYPE_SELL,
            price_open=2000.00,
            sl=2050.00,
            tp=1900.00
        )
        mock_symbol_info.return_value.ask = 1950.00 # Current Price
        
        print(f"Testing SELL position: Entry={mock_pos_sell.price_open}, Current={mock_symbol_info.return_value.ask}, ATR={latest_atr}")
        engine._manage_breakeven(symbol, mock_strategy, [mock_pos_sell], latest_atr)
        
        if mock_order_mgr.modify_position.called:
            args, kwargs = mock_order_mgr.modify_position.call_args
            new_sl = kwargs.get('sl') if kwargs.get('sl') else args[1]
            print(f"SUCCESS: modify_position called with new_sl={new_sl}")
        else:
            print("FAILED: modify_position was not called")

if __name__ == "__main__":
    test_breakeven_logic()
