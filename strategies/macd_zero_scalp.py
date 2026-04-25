"""
MACD Zero-Line Scalp - 1m/5m scalping
Enters on MACD zero-line crosses for trend reversals.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class MACDZeroScalp(BaseStrategy):
    """Scalps MACD zero-line crossovers on lower timeframes."""
    
    def __init__(self, params=None):
        params = params or {
            "macd_fast": 8,          # Shorter for faster signals
            "macd_slow": 17,
            "macd_signal": 9,
            "atr_period": 14,
            "tp_atr_mult": 0.8,
            "sl_atr_mult": 0.35,
            "volume_filter": 0.8,    # 80% of avg volume
        }
        super().__init__(
            name="macd_zero_scalp",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )
    
    def generate_signals(self, data):
        """Generate signals on MACD zero-line crossover."""
        df = data.copy()
        
        # MACD
        macd_result = ta.macd(df['close'], 
                              fast=self.params["macd_fast"],
                              slow=self.params["macd_slow"],
                              signal=self.params["macd_signal"])
        df['macd'] = macd_result['macd']
        df['macd_signal'] = macd_result['signal']
        df['macd_hist'] = macd_result['histogram']
        
        # ATR for stops/targets
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], 
                           self.params["atr_period"])
        
        # Volume filter
        df['volume_avg'] = df['volume'].rolling(10).mean()
        
        # Signal generation
        df['signal'] = 0
        
        # BUY: MACD crosses above zero line (bullish)
        buy_signal = (
            (df['macd'] > 0) & 
            (df['macd'].shift(1) <= 0) &
            (df['volume'] > (df['volume_avg'] * self.params["volume_filter"]))
        )
        df.loc[buy_signal, 'signal'] = 1
        
        # SELL: MACD crosses below zero line (bearish)
        sell_signal = (
            (df['macd'] < 0) & 
            (df['macd'].shift(1) >= 0) &
            (df['volume'] > (df['volume_avg'] * self.params["volume_filter"]))
        )
        df.loc[sell_signal, 'signal'] = -1
        
        return df[['signal']]

