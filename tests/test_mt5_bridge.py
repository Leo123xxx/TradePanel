import pytest
import os
from mt5_bridge.connector import MT5Connector

def test_mt5_connection():
    connector = MT5Connector()
    # This test requires MT5 terminal to be running and credentials to be in .env
    assert connector.connect() is True
    connector.disconnect()
    assert connector.connected is False

if __name__ == "__main__":
    pytest.main([__file__])
