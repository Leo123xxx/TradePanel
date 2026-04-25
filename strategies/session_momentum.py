import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H1"]

class SessionMomentumStrategy(BaseStrategy):
    """
    Session-Based Momentum (London/NY Overlap).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "session_start_utc":  13.5, # 13:30 UTC
                "session_end_utc":    15.5, # 15:30 UTC
                "pre_session_bars":    8,
                "atr_period":         14,
                "tp_atr_mult":         2.0,
                "sl_atr_mult":         0.8,
                "min_adx_filter":     20,
                "vol_threshold_mult": 1.2,  # NEW: volume confirmation
                "fast_ema":           20,
                "slow_ema":           50,
                "use_partial_tp":      False,  # 2-hr window — momentum fades, skip partial
            }
        super().__init__(
            name="Session_Momentum",
            category="Session-Based / Momentum",
            params=params,
            regime=["TRENDING"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        London/NY overlap session breakout strategy.

        Logic:
          - Build a reference range from the N bars immediately BEFORE session open
          - During the session window, enter on a CONFIRMED BREAKOUT above/below that range
          - Only enter when EMA trend and ADX both agree

        v1 problem: entry fired when price was "near" the high (within 20 pips below it).
          This is the END of a move, not a breakout.  v2 fires when close EXCEEDS the
          pre-session range high/low — a true breakout entry.
        """
        df = data.copy()

        start          = self.params.get("session_start_utc",  13.5)
        end            = self.params.get("session_end_utc",     15.5)
        pre_bars       = self.params.get("pre_session_bars",     8)
        fast_ema_p     = self.params.get("fast_ema",            20)
        slow_ema_p     = self.params.get("slow_ema",            50)
        adx_min        = self.params.get("min_adx_filter",      20)
        vol_mult       = self.params.get("vol_threshold_mult",  1.2)

        # ── Indicators ────────────────────────────────────────────────────────
        df['ema_fast'] = ta.ema(df['close'], length=fast_ema_p)
        df['ema_slow'] = ta.ema(df['close'], length=slow_ema_p)
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # ── Volume confirmation ───────────────────────────────────────────────
        df['avg_vol'] = df['tick_volume'].rolling(window=20).mean().shift(1)
        df['vol_ok'] = df['tick_volume'] >= (df['avg_vol'] * vol_mult)

        # ── Daily/Previous Session Bias ───────────────────────────────────────
        # Use daily close-to-close return to determine bias
        # For intra-day H1 data, we can resample to D1 to get the daily direction
        daily_close = df['close'].resample('D').last().ffill()
        df['daily_direction'] = (daily_close - daily_close.shift(1)).reindex(df.index, method='ffill')
        df['bias_long'] = df['daily_direction'] > 0
        df['bias_short'] = df['daily_direction'] < 0

        # ── Pre-session range (N bars before session open) ────────────────────
        # shift(1) ensures we use the range that was established before the current bar
        df['pre_range_high'] = df['high'].rolling(window=pre_bars).max().shift(1)
        df['pre_range_low']  = df['low'].rolling(window=pre_bars).min().shift(1)

        # ── Session mask ──────────────────────────────────────────────────────
        # Use fractional hours since start/end can be 13.5
        df['hour_float'] = df.index.hour + df.index.minute / 60.0
        in_session = (df['hour_float'] >= start) & (df['hour_float'] < end)

        # ── Breakout signals ──────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            in_session &
            (df['close'] > df['pre_range_high']) &    # close BREAKS ABOVE pre-session high
            (df['adx'] >= adx_min) &
            (df['ema_fast'] > df['ema_slow']) &       # uptrend bias
            df['vol_ok'] &                            # volume confirmation
            df['bias_long']                           # daily trend bias
        )

        short_cond = (
            in_session &
            (df['close'] < df['pre_range_low']) &     # close BREAKS BELOW pre-session low
            (df['adx'] >= adx_min) &
            (df['ema_fast'] < df['ema_slow']) &       # downtrend bias
            df['vol_ok'] &                            # volume confirmation
            df['bias_short']                          # daily trend bias
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
