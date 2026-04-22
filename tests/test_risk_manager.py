import pytest
import MetaTrader5 as mt5
from risk.manager import RiskManager
from mt5_bridge.connector import MT5Connector
import os

@pytest.fixture(scope="module")
def mt5_conn():
    connector = MT5Connector()
    if not connector.connect():
        pytest.skip("MT5 Terminal not running or login failed.")
    yield connector
    connector.disconnect()

def test_risk_checks_general(mt5_conn):
    rm = RiskManager()
    
    # Basic check for a valid pair
    passed, reason = rm.check_all("range_breakout", "XAUUSD", 0.1, "BUY")
    print(f"\nAudit: {reason}")
    assert isinstance(passed, bool)

def test_lot_size_violation(mt5_conn):
    rm = RiskManager()
    # 10.0 lots should exceed default max of 1.0 in config.yaml
    passed, reason = rm.check_all("range_breakout", "XAUUSD", 10.0, "BUY")
    assert passed is False
    assert "exceeds max limit" in reason

def test_strategy_disabled(mt5_conn):
    rm = RiskManager()
    # rsi_bounce is disabled by default in config.yaml template
    passed, reason = rm.check_all("rsi_bounce", "XAUUSD", 0.1, "BUY")
    assert passed is False
    assert "disabled/paused" in reason

def test_trading_hours_logic():
    # This might fail if run on a weekend, which is correct
    rm = RiskManager()
    passed = rm._check_trading_hours("XAUUSD")
    from datetime import datetime
    day = datetime.now().weekday()
    if day > 4: # Sat/Sun
        assert passed is False
    else:
        assert passed is True # Assuming current time is within 00:00 - 23:59

from unittest.mock import patch, MagicMock

def test_max_concurrent_positions(mt5_conn):
    rm = RiskManager()
    with patch("MetaTrader5.positions_total", return_value=10): # 10 exceeds the max config of 5
        passed, reason = rm.check_all("range_breakout", "XAUUSD", 0.1, "BUY")
        assert passed is False
        assert "Max concurrent" in reason

def test_max_spread_pips(mt5_conn):
    rm = RiskManager()
    mock_info = MagicMock()
    mock_info.spread = 1000 # 1000 points * 0.01 / 0.01 = 1000 pips
    mock_info.point = 0.01
    mock_info.digits = 2
    with patch("MetaTrader5.symbol_info", return_value=mock_info):
        passed, reason = rm.check_all("range_breakout", "XAUUSD", 0.1, "BUY")
        assert passed is False
        assert "spread exceeds max allowed" in reason

def test_margin_insufficient(mt5_conn):
    rm = RiskManager()
    mock_info = MagicMock()
    mock_info.spread = 10
    mock_info.point = 0.01
    mock_info.digits = 2
    mock_info.ask = 2000.0
    mock_info.bid = 2000.0
    
    with patch("MetaTrader5.symbol_info", return_value=mock_info), \
         patch("MetaTrader5.order_calc_margin", return_value=5000.0), \
         patch.object(rm.account, "get_margin_free", return_value=100.0): # not enough margin
         
        passed, reason = rm.check_all("range_breakout", "XAUUSD", 0.1, "BUY")
        assert passed is False
        assert "Insufficient free margin" in reason
