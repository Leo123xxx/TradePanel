import pytest
import pandas as pd
from strategies.base_strategy import BaseStrategy

# Mock strategy for testing
class MockStrategy(BaseStrategy):
    def __init__(self, params):
        super().__init__("MockStrategy", "Trend Following", params)

    def generate_signals(self, data):
        data['signal'] = 0
        return data

    def validate_params(self):
        return True

def test_strategy_interface():
    params = {"fast_ma": 10, "slow_ma": 20}
    strategy = MockStrategy(params)
    
    # Test metadata
    meta = strategy.get_metadata()
    assert meta["name"] == "MockStrategy"
    assert meta["params"]["fast_ma"] == 10
    
    # Test signal generation stub
    df = pd.DataFrame({'close': [1, 2, 3]})
    df_with_signals = strategy.generate_signals(df)
    assert 'signal' in df_with_signals.columns

if __name__ == "__main__":
    pytest.main([__file__])
