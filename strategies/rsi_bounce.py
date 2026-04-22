import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class RSIBounceStrategy(BaseStrategy):
    """
    RSI Mean Reversion Strategy.
    Generates signals when RSI crosses back into the neutral zone from extremes.
    """
    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period": 14, 
                "oversold": 30, 
                "overbought": 70
            }
        super().__init__("RSI_Bounce", "Mean Reversion", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Buy (1): RSI was <= 30 and is now > 30 (Bounce out of oversold)
        Sell (-1): RSI was >= 70 and is now < 70 (Bounce out of overbought)
        """
        df = data.copy()
        
        rsi_period = self.params.get("rsi_period", 14)
        overbought = self.params.get("overbought", 70)
        oversold = self.params.get("oversold", 30)
        
        # Calculate RSI
        # Ensure we have at least rsi_period * 2 bars for stable RSI
        df['rsi'] = ta.rsi(df['close'], length=rsi_period)
        
        df['signal'] = 0
        
        # Determine signals
        # Buy: RSI crosses above oversold
        df.loc[(df['rsi'] > oversold) & (df['rsi'].shift(1) <= oversold), 'signal'] = 1
        
        # Sell: RSI crosses below overbought
        df.loc[(df['rsi'] < overbought) & (df['rsi'].shift(1) >= overbought), 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        rsi = self.params.get("rsi_period", 0)
        ob = self.params.get("overbought", 0)
        os = self.params.get("oversold", 0)
        
        if rsi <= 0: return False
        if os < 0 or os > 50: return False
        if ob < 50 or ob > 100: return False
        
        return True
