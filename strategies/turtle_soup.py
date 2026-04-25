import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class TurtleSoup(BaseStrategy):
    """
    Turtle Soup Strategy (SMC / Liquidity Sweep)

    Logic:
    1. Identify a 20-bar High or Low level.
    2. Price must penetrate the level (liquidity sweep).
    3. Reversal: Price must reverse and close back within the 20-bar level.
    4. Cooldown: No new signal for N bars after a signal fires (prevents 3000+ trade overtrading).
    RR = 2.5:1 (tp_atr_mult=2.5, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback": 20,
                "min_penetration_pips": 5,
                "max_penetration_pips": 30,
                "atr_period": 14,
                "tp_atr_mult": 2.5,    # RR 2.5:1
                "sl_atr_mult": 1.0,    # ATR-based SL
                "sl_buffer_pips": 5,   # kept for reference only
                "cooldown_bars": 15    # suppress new signal within 15 bars of last (was 6 — still 1143 trades)
            }
        super().__init__(
            name="Turtle_Soup",
            category="SMC",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["H1", "H4"],
            pairs=["XAUUSD", "BTCUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        lookback = self.params.get("lookback", 20)

        # 1. Previous N-bar High and Low
        df['h20'] = df['high'].rolling(window=lookback).max().shift(1)
        df['l20'] = df['low'].rolling(window=lookback).min().shift(1)

        # 2. Sweep Detection
        # Low swept: current low < l20, but current close > l20 (reversal back inside)
        df['sweep_low'] = (df['low'] < df['l20']) & (df['close'] > df['l20'])
        # High swept: current high > h20, but current close < h20 (reversal back inside)
        df['sweep_high'] = (df['high'] > df['h20']) & (df['close'] < df['h20'])

        # 3. Raw signals
        df['signal'] = 0
        df.loc[df['sweep_low'], 'signal'] = 1
        df.loc[df['sweep_high'], 'signal'] = -1

        # 4. Cooldown filter — suppress repeated signals within N bars
        cooldown = self.params.get("cooldown_bars", 6)
        signal_arr = df['signal'].values.copy()
        last_signal_bar = -cooldown - 1
        for i in range(len(signal_arr)):
            if signal_arr[i] != 0:
                if i - last_signal_bar <= cooldown:
                    signal_arr[i] = 0  # suppress — too soon after last signal
                else:
                    last_signal_bar = i
        df['signal'] = signal_arr

        return df

    def validate_params(self) -> bool:
        return self.params.get("lookback", 0) > 0
