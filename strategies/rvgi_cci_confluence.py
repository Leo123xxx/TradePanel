import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class RVGICCIConfluence(BaseStrategy):
    """
    RVGI-CCI-SMA Confluence Breakout

    Logic:
    1. RVGI (Relative Vigor Index): Fast cross Slow (Bullish/Bearish).
    2. CCI: Must be in bullish zone (>cci_buy_min) for Buy, bearish zone (<cci_sell_max) for Sell.
    3. SMA: Price must be in trend alignment (Close > SMA for Buy).
    RR = 3.1:1 (tp_atr_mult=2.5, sl_atr_mult=0.8). CCI thresholds tightened to -50/+50.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rvgi_period": 10,
                "cci_period": 20,
                "sma_period": 30,
                "tp_atr_mult": 2.5,   # RR 3.1:1 (was 1.5:1)
                "sl_atr_mult": 0.8,   # tighter SL improves RR
                "cci_buy_min": -50,   # tighter: was -100
                "cci_sell_max": 50,   # tighter: was +100
                "atr_period": 14,
                "cooldown_bars": 15   # was generating 1279+ trades — throttle
            }
        super().__init__(
            name="RVGI_CCI_Confluence",
            category="Breakout",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["H1"],
            pairs=["GBPUSD", "USDJPY"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # 1. RVGI Calculation (Simplified)
        num = (df['close'] - df['open']) + 2 * (df['close'].shift(1) - df['open'].shift(1)) + \
              2 * (df['close'].shift(2) - df['open'].shift(2)) + (df['close'].shift(3) - df['open'].shift(3))
        den = (df['high'] - df['low']) + 2 * (df['high'].shift(1) - df['low'].shift(1)) + \
              2 * (df['high'].shift(2) - df['low'].shift(2)) + (df['high'].shift(3) - df['low'].shift(3))

        df['rvgi_val'] = num.rolling(window=self.params['rvgi_period']).sum() / \
                         den.rolling(window=self.params['rvgi_period']).sum()
        df['rvgi_sig'] = (df['rvgi_val'] + 2 * df['rvgi_val'].shift(1) +
                          2 * df['rvgi_val'].shift(2) + df['rvgi_val'].shift(3)) / 6

        # 2. CCI
        tp = (df['high'] + df['low'] + df['close']) / 3
        sma_tp = tp.rolling(window=self.params['cci_period']).mean()
        mad_tp = tp.rolling(window=self.params['cci_period']).apply(lambda x: (x - x.mean()).abs().mean())
        df['cci'] = (tp - sma_tp) / (0.015 * mad_tp)

        # 3. SMA
        df['sma'] = ta.sma(df['close'], length=self.params['sma_period'])

        # 4. Signals
        df['signal'] = 0
        cci_buy_min = self.params.get("cci_buy_min", -50)
        cci_sell_max = self.params.get("cci_sell_max", 50)

        # Buy: RVGI Cross Up + CCI in bullish zone + Price > SMA
        df.loc[
            (df['rvgi_val'] > df['rvgi_sig']) &
            (df['rvgi_val'].shift(1) <= df['rvgi_sig'].shift(1)) &
            (df['cci'] > cci_buy_min) &
            (df['close'] > df['sma']),
            'signal'
        ] = 1

        # Sell: RVGI Cross Down + CCI in bearish zone + Price < SMA
        df.loc[
            (df['rvgi_val'] < df['rvgi_sig']) &
            (df['rvgi_val'].shift(1) >= df['rvgi_sig'].shift(1)) &
            (df['cci'] < cci_sell_max) &
            (df['close'] < df['sma']),
            'signal'
        ] = -1

        # Cooldown filter — suppress signals within N bars of last signal
        cooldown = self.params.get("cooldown_bars", 15)
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
        return True
