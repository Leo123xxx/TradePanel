import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class GoldMomentumBreakoutStrategy(BaseStrategy):
    """
    Gold Momentum Breakout Strategy.
    Identifies a sustained squeeze (consolidation) in Bollinger Bands, and a breakout
    confirmed by RSI showing momentum in the breakout direction.
    squeeze_threshold_pct tightened to 0.03 (was 0.05) and must persist for 3 bars
    to reduce overtrading (was generating 2400+ trades).
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "bb_length": 20,
                "bb_std": 2.0,
                "rsi_length": 14,
                "rsi_buy_min": 55,              # tighter: was 50
                "rsi_sell_max": 45,             # tighter: was 50
                "squeeze_threshold_pct": 0.03,  # tighter squeeze: was 0.05
                "squeeze_lookback": 3,          # squeeze must persist N bars
                "tp_atr_mult": 3.0,             # RR 3:1
                "sl_atr_mult": 1.0,
                "atr_period": 14,
                "cooldown_bars": 12   # was generating 1693+ trades — throttle
            }
        super().__init__("Gold_Momentum_Breakout", "Breakout", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        bb_length = self.params.get("bb_length", 20)
        bb_std = self.params.get("bb_std", 2.0)
        rsi_length = self.params.get("rsi_length", 14)
        rsi_buy_min = self.params.get("rsi_buy_min", 55)
        rsi_sell_max = self.params.get("rsi_sell_max", 45)
        squeeze_threshold_pct = self.params.get("squeeze_threshold_pct", 0.03)
        squeeze_lookback = self.params.get("squeeze_lookback", 3)

        # Bollinger Bands
        bb = ta.bbands(df['close'], length=bb_length, std=bb_std)
        if bb is None or bb.empty:
            df['signal'] = 0
            return df

        bb_lower_col = bb.columns[0]  # L
        bb_mid_col = bb.columns[1]    # M
        bb_upper_col = bb.columns[2]  # U

        df = pd.concat([df, bb], axis=1)

        # Bollinger Band Width as % of middle band
        df['bb_width_pct'] = (df[bb_upper_col] - df[bb_lower_col]) / df[bb_mid_col]

        # RSI
        df['rsi'] = ta.rsi(df['close'], length=rsi_length)

        df['signal'] = 0

        # Sustained squeeze: bb_width must be < threshold for N consecutive bars
        in_squeeze = df['bb_width_pct'] < squeeze_threshold_pct
        sustained_squeeze = in_squeeze.rolling(window=squeeze_lookback).min().shift(1).fillna(0).astype(bool)

        # Buy: Close > upper band AND sustained squeeze AND RSI > min threshold
        buy_cond = (df['close'] > df[bb_upper_col]) & sustained_squeeze & (df['rsi'] > rsi_buy_min)

        # Sell: Close < lower band AND sustained squeeze AND RSI < max threshold
        sell_cond = (df['close'] < df[bb_lower_col]) & sustained_squeeze & (df['rsi'] < rsi_sell_max)

        df.loc[buy_cond, 'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        # Cooldown filter — suppress signals within N bars of last signal
        cooldown = self.params.get("cooldown_bars", 12)
        signal_arr = df['signal'].values.copy()
        last_signal_bar = -cooldown - 1
        for i in range(len(signal_arr)):
            if signal_arr[i] != 0:
                if i - last_signal_bar <= cooldown:
                    signal_arr[i] = 0
                else:
                    last_signal_bar = i
        df['signal'] = signal_arr

        return df

    def validate_params(self) -> bool:
        return self.params.get("bb_length", 0) > 0 and self.params.get("rsi_length", 0) > 0
