import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

# Pairs and timeframes this strategy is approved to trade.
# Tune fast/slow periods per pair in strategies.yaml — defaults here are fallbacks.
APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H1", "H4", "D1"]

class MACrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover — Trend Following.

    Signal logic:
      Buy  (1):  Fast EMA crosses ABOVE Slow EMA
      Sell (-1): Fast EMA crosses BELOW Slow EMA
      Hold (0):  No crossover on this bar

    Regime: TRENDING preferred (ADX > 25). Avoid RANGING markets.
    Works on all 5 approved pairs; parameter defaults tuned for H1 timeframe.
    Per-pair parameter overrides loaded from strategies.yaml at runtime.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_period": 10,       # Widened from 9 — more separation = fewer whipsaws
                "slow_period": 50,       # Widened from 21 — clear trend filter
                "ma_type": "EMA",
                "atr_period": 14,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.0,
                "adx_filter": 25         # Raised from 20 — only enter in confirmed trends
            }
        super().__init__(
            name="MA_Crossover",
            category="Trend Following",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Returns the input DataFrame with a 'signal' column (1 / -1 / 0).

        Entry logic:
          - Fast EMA crosses above Slow EMA → BUY, if ADX filter passes
          - Fast EMA crosses below Slow EMA → SELL, if ADX filter passes
          - ADX filter: skip signal if ADX < adx_filter (choppy market guard)
        """
        df = data.copy()

        fast_period = self.params.get("fast_period", 10)
        slow_period = self.params.get("slow_period", 50)
        ma_type     = self.params.get("ma_type", "EMA").upper()
        adx_min     = self.params.get("adx_filter", 25)

        # ── Moving averages ──────────────────────────────────────────────────
        if ma_type == "EMA":
            df['fast_ma'] = ta.ema(df['close'], length=fast_period)
            df['slow_ma'] = ta.ema(df['close'], length=slow_period)
        else:
            df['fast_ma'] = ta.sma(df['close'], length=fast_period)
            df['slow_ma'] = ta.sma(df['close'], length=slow_period)

        # ── ADX trend-strength filter ────────────────────────────────────────
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df[f"ADX_14"]
        adx_ok = (adx_min == 0) | (df['adx'] >= adx_min)

        # ── Crossover signal (fires only on the bar the bias changes) ────────
        df['signal_val'] = 0
        df.loc[df['fast_ma'] > df['slow_ma'], 'signal_val'] = 1
        df.loc[df['fast_ma'] < df['slow_ma'], 'signal_val'] = -1

        df['signal'] = 0
        df.loc[
            (df['signal_val'] == 1) & (df['signal_val'].shift(1) == -1) & adx_ok,
            'signal'
        ] = 1
        df.loc[
            (df['signal_val'] == -1) & (df['signal_val'].shift(1) == 1) & adx_ok,
            'signal'
        ] = -1

        return df

    def validate_params(self) -> bool:
        fast = self.params.get("fast_period", 0)
        slow = self.params.get("slow_period", 0)
        tp = self.params.get("tp_atr_mult", 0)
        sl = self.params.get("sl_atr_mult", 0)
        return (
            fast > 0
            and slow > fast
            and tp > sl > 0
        )
