import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime, timedelta
import MetaTrader5 as mt5

# Import classes to test
from forward_test.paper_engine import PaperEngine
from mt5_bridge.order_manager import OrderManager
from forward_test.signal_checker import SignalChecker
from mt5_bridge.connector import MT5Connector

@pytest.fixture
def mock_mt5():
    with patch('mt5_bridge.order_manager.mt5') as mocked:
        yield mocked

@pytest.fixture
def engine():
    # Mock dependencies of PaperEngine to avoid DB/MT5 connections during init
    with patch('forward_test.paper_engine.MT5Connector'), \
         patch('forward_test.paper_engine.OrderManager'), \
         patch('forward_test.paper_engine.RiskManager'), \
         patch('forward_test.paper_engine.SignalChecker'), \
         patch('forward_test.paper_engine.DBClient'), \
         patch('forward_test.paper_engine.TelegramBot'), \
         patch('forward_test.paper_engine.CommandRouter'):
        return PaperEngine()

# ════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: SIGNAL DEDUPLICATION
# ════════════════════════════════════════════════════════════════════════════

def test_signal_dedup_logic(engine):
    """Test that duplicate signals are correctly identified and blocked."""
    strat = "range_breakout"
    symbol = "XAUUSD"
    tf = mt5.TIMEFRAME_H4
    direction = 1
    signal_time = datetime(2026, 4, 20, 12, 0)
    
    key = engine._create_signal_key(strat, symbol, tf, direction)
    
    # 1. Initially, not a duplicate
    assert engine._check_signal_duplicate(key, signal_time) is False
    
    # 2. Track it
    engine._track_processed_signal(key, signal_time)
    
    # 3. Now it should be a duplicate
    assert engine._check_signal_duplicate(key, signal_time) is True
    
    # 4. Different direction should NOT be a duplicate
    other_key = engine._create_signal_key(strat, symbol, tf, -1)
    assert engine._check_signal_duplicate(other_key, signal_time) is False

def test_dedup_cache_cleanup(engine):
    """Test that expired entries are removed from the cache."""
    key = ("strat", "sym", 0, 1)
    old_time = datetime.now() - timedelta(minutes=10)
    
    engine.attempted_signals[key] = old_time
    assert len(engine.attempted_signals) == 1
    
    engine._clean_dedup_cache()
    assert len(engine.attempted_signals) == 0

# ════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: ORDER VALIDATION
# ════════════════════════════════════════════════════════════════════════════

def test_validation_insufficient_equity(mock_mt5):
    """Check #5: Equity threshold ($1000 minimum)."""
    # Initialize with mock config or values
    with patch('builtins.open', MagicMock()):
        with patch('yaml.safe_load', return_value={
            'risk_management': {'min_equity_threshold': 1000},
            'pairs': {}
        }):
            om = OrderManager()
            
            # Mock account info with low equity
            mock_mt5.account_info.return_value = MagicMock(equity=500, balance=500, margin=0, margin_free=500)
            mock_mt5.symbol_info.return_value = MagicMock(visible=True, volume_min=0.01, volume_max=100.0)
            
            # Mock trading hours to pass
            with patch.object(om, '_is_trading_hours', return_value=True):
                valid, msg = om._validate_order("EURUSD", 0.1)
                assert valid is False
                assert "Account equity below minimum" in msg

def test_validation_insufficient_margin(mock_mt5):
    """Check #6: Margin check (free margin >= required * 1.5)."""
    with patch('builtins.open', MagicMock()):
        with patch('yaml.safe_load', return_value={
            'risk_management': {'min_equity_threshold': 100},
            'pairs': {}
        }):
            om = OrderManager()
            om.margin_safety_buffer = 1.5
            
            # Mock account info: $500 free margin
            mock_mt5.account_info.return_value = MagicMock(equity=2000, balance=2000, margin=0, margin_free=500)
            mock_mt5.symbol_info.return_value = MagicMock(
                visible=True, volume_min=0.01, volume_max=100.0, 
                margin_initial=0, trade_contract_size=100000
            ) 
            mock_mt5.symbol_info_tick.return_value = MagicMock(ask=1.1000)
            
            # Required margin for 1 lot EURUSD at 1.1000 using 2% default = $2200.
            # Buffer 1.5x = $3300.
            # Free margin $500 is NOT enough.
            
            with patch.object(om, '_is_trading_hours', return_value=True):
                valid, msg = om._validate_order("EURUSD", 1.0)
                assert valid is False
                assert "Insufficient margin" in msg

# ════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: DATA FRESHNESS
# ════════════════════════════════════════════════════════════════════════════

def test_stale_data_detection():
    """Test that data older than 24 hours is blocked."""
    checker = SignalChecker()
    checker.max_data_age_hours = 24
    
    # Create synthetic data with old timestamp
    old_time = datetime.now() - timedelta(hours=25)
    df = pd.DataFrame({'close': [1.0, 1.1]}, index=[old_time - timedelta(hours=1), old_time])
    
    is_fresh, msg = checker._is_data_stale("EURUSD", mt5.TIMEFRAME_H1, df)
    assert is_fresh is False
    assert "Data is 25" in msg or "Data is 24" in msg

def test_gap_detection():
    """Test that gaps > 1 hour are blocked."""
    checker = SignalChecker()
    checker.gap_threshold_minutes = 60
    
    # Create data with a 2-hour gap
    t1 = datetime.now() - timedelta(hours=3)
    t2 = t1 + timedelta(hours=2) # 2 hour gap
    df = pd.DataFrame({'close': [1.0, 1.1]}, index=[t1, t2])
    
    # H1 timeframe: expected internal 60 min. Actual 120 min.
    is_fresh, msg = checker._is_data_stale("EURUSD", mt5.TIMEFRAME_H1, df)
    assert is_fresh is False
    assert "Data gap detected" in msg

# ════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: MT5 CONNECTOR (LIVE TERMINAL)
# ════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not mt5.initialize(), reason="MT5 terminal not available")
def test_live_connector_verification():
    """Verify live connectivity and symbol setup."""
    connector = MT5Connector()
    connected = connector.connect()
    assert connected is True
    
    # Verify at least one core symbol is OK
    results = connector.validate_data_streams()
    assert "XAUUSD" in results
    # We don't assert all True as markets might be closed, 
    # but the connector should return a status for each.
    
    connector.disconnect()
