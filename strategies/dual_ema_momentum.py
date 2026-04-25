import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class DualEMAMomentum(BaseStrategy):
    """
    Dual EMA Momentum Continuity

    Logic:
    1. Trend: Fast EMA > Slow EMA (Bullish) or Fast EMA < Slow EMA (Bearish).
    2. Momentum: ADX > adx_min.
    3. Signal: Price makes an engulfing candle in the direction of the trend.
    RR = 3.5:1 (tp_atr_mult=3.5, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_ema": 20,
                "slow_ema": 50,
                "adx_min": 25,
                "atr_period": 14,
                "tp_atr_mult": 3.5,   # RR 3.5:1 (was 1.67:1)
                "sl_atr_mult": 1.0    # tighter SL
            }
        super().__init__(
            name="Dual_EMA_Momentum",
            category="Trend Following",
            params=params,
            regime=["TRENDING"],
            timeframes=["H1", "H4"],
            pairs=["BTCUSD", "ETHUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # 1. EMA Ribbons
        df['fast_ema'] = ta.ema(df['close'], length=self.params['fast_ema'])
        df['slow_ema'] = ta.ema(df['close'], length=self.params['slow_ema'])

        # 2. ADX Filter
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # 3. Engulfing Candle detection
        df['is_bull_engulfing'] = (
            (df['close'] > df['open']) &
            (df['open'] < df['close'].shift(1)) &
            (df['close'] > df['open'].shift(1)) &
            (df['open'].shift(1) > df['close'].shift(1))   # prev was bearish
        )
        df['is_bear_engulfing'] = (
            (df['close'] < df['open']) &
            (df['open'] > df['close'].shift(1)) &
            (df['close'] < df['open'].shift(1)) &
            (df['open'].shift(1) < df['close'].shift(1))   # prev was bullish
        )

        # 4. Signal Generation
        df['signal'] = 0

        # Bullish: Trend Up + ADX Strong + Bull Engulfing
        df.loc[
            (df['fast_ema'] > df['slow_ema']) &
            (df['adx'] > self.params['adx_min']) &
            df['is_bull_engulfing'],
            'signal'
        ] = 1

        # Bearish: Trend Down + ADX Strong + Bear Engulfing
        df.loc[
            (df['fast_ema'] < df['slow_ema']) &
            (df['adx'] > self.params['adx_min']) &
            df['is_bear_engulfing'],
            'signal'
        ] = -1

        return df

    def validate_params(self) -> bool:
        return self.params['fast_ema'] < self.params['slow_ema']
