import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class StochDivergenceStrategy(BaseStrategy):
    """
    Stochastic Divergence Mean Reversion — v2.

    Entry logic (bullish):
      - Stochastic K crosses ABOVE D (momentum turn)
      - Crossover occurs while K is still near oversold zone (<= oversold + 10)
      - Rolling window divergence: price made a lower low BUT stoch made a higher low
        (classic bullish divergence — momentum leading price)

    Entry logic (bearish):
      - Stochastic K crosses BELOW D
      - Crossover while K is still near overbought zone (>= overbought - 10)
      - Price made a higher high BUT stoch made a lower high (bearish divergence)

    v1 problem: fixed-lookback comparison was not real divergence; IS Sharpe was
    already negative across all walk-forward windows.  v2 uses K/D crossover as
    the precise trigger and a rolling window to verify the divergence condition.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "stoch_period":          14,
                "stoch_smooth_k":         3,
                "stoch_smooth_d":         3,
                "divergence_lookback":   10,   # bars to measure divergence window
                "stoch_oversold":        25,   # raised from 20 — catches more signals
                "stoch_overbought":      75,   # lowered from 80
                "atr_period":            14,
                "tp_atr_mult":            2.0,
                "sl_atr_mult":            1.0,
                "use_partial_tp":          False,  # divergence = mean reversion, no partial
            }
        super().__init__(
            name="Stoch_Divergence",
            category="Divergence / Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        k_period  = self.params.get("stoch_period",       14)
        sk        = self.params.get("stoch_smooth_k",      3)
        sd        = self.params.get("stoch_smooth_d",      3)
        look      = self.params.get("divergence_lookback", 10)
        lower     = self.params.get("stoch_oversold",      25)
        upper     = self.params.get("stoch_overbought",    75)

        # ── Stochastic ────────────────────────────────────────────────────────
        stoch_df = ta.stoch(df['high'], df['low'], df['close'],
                            k_period=k_period, smooth_k=sk, smooth_d=sd)
        df['stoch_k'] = stoch_df[f"STOCHk_{k_period}_{sk}_{sd}"]
        df['stoch_d'] = stoch_df[f"STOCHd_{k_period}_{sk}_{sd}"]

        # ── K / D crossover ───────────────────────────────────────────────────
        k_above_d       = df['stoch_k'] > df['stoch_d']
        df['cross_up']  = k_above_d & (~k_above_d.shift(1).fillna(False))
        df['cross_down']= (~k_above_d) & (k_above_d.shift(1).fillna(False))

        # ── Rolling window extremes (no look-ahead) ───────────────────────────
        # Price: lowest low and highest high in last `look` bars
        df['win_price_low']   = df['low'].rolling(look).min()
        df['prev_price_low']  = df['low'].rolling(look).min().shift(look)
        df['win_price_high']  = df['high'].rolling(look).max()
        df['prev_price_high'] = df['high'].rolling(look).max().shift(look)

        # Stoch: lowest and highest K in last `look` bars
        df['win_stoch_low']   = df['stoch_k'].rolling(look).min()
        df['prev_stoch_low']  = df['stoch_k'].rolling(look).min().shift(look)
        df['win_stoch_high']  = df['stoch_k'].rolling(look).max()
        df['prev_stoch_high'] = df['stoch_k'].rolling(look).max().shift(look)

        # ── Divergence conditions ─────────────────────────────────────────────
        # Bullish: price lower low  +  stoch higher low  (momentum leading price up)
        bullish_div = (
            (df['win_price_low']  < df['prev_price_low'])  &   # price: LL
            (df['win_stoch_low']  > df['prev_stoch_low'])       # stoch: HL
        )

        # Bearish: price higher high  +  stoch lower high  (momentum leading price down)
        bearish_div = (
            (df['win_price_high'] > df['prev_price_high']) &   # price: HH
            (df['win_stoch_high'] < df['prev_stoch_high'])      # stoch: LH
        )

        # ── Final signals ─────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            df['cross_up'] &
            (df['stoch_k'] <= lower + 10) &   # crossover near oversold zone
            bullish_div
        )
        short_cond = (
            df['cross_down'] &
            (df['stoch_k'] >= upper - 10) &   # crossover near overbought zone
            bearish_div
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
