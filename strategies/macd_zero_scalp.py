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
            "macd_fast":    8,
            "macd_slow":    17,
            "macd_signal":  9,
            "atr_period":   14,
            "tp_atr_mult":  2.0,
            "sl_atr_mult":  1.0,
            "volume_filter": 1.0,
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

        # ta_compat.macd returns DataFrame with cols MACD_f_s_sig, MACDh_..., MACDs_...
        macd_result = ta.macd(df['close'],
                              fast=self.params["macd_fast"],
                              slow=self.params["macd_slow"],
                              signal=self.params["macd_signal"])
        # Extract by position -- col 0 = MACD line, col 1 = histogram, col 2 = signal
        df['macd']       = macd_result.iloc[:, 0]
        df['macd_hist']  = macd_result.iloc[:, 1]
        df['macd_signal'] = macd_result.iloc[:, 2]

        df['atr'] = ta.atr(df['high'], df['low'], df['close'], self.params["atr_period"])

        # Use tick_volume if 'volume' column not present
        vol_col = 'volume' if 'volume' in df.columns else 'tick_volume'
        df['volume_avg'] = df[vol_col].rolling(10).mean()

        df['signal'] = 0

        buy_signal = (
            (df['macd'] > 0) &
            (df['macd'].shift(1) <= 0) &
            (df[vol_col] > (df['volume_avg'] * self.params["volume_filter"]))
        )
        df.loc[buy_signal, 'signal'] = 1

        sell_signal = (
            (df['macd'] < 0) &
            (df['macd'].shift(1) >= 0) &
            (df[vol_col] > (df['volume_avg'] * self.params["volume_filter"]))
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("macd_fast", 0) > 0 and
                self.params.get("macd_slow", 0) > self.params.get("macd_fast", 0) and
                self.params.get("tp_atr_mult", 0) > 0 and
                self.params.get("sl_atr_mult", 0) > 0)
