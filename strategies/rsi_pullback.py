import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]

class RSIPullbackStrategy(BaseStrategy):
    """
    RSI Pullback in Trend Strategy v2.
    EMA200 macro gate + ADX range gate (20-45) + MACD histogram turn + tighter RSI zones.
    Enters on RSI pullback within an established EMA trend.
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period": 14,
                "rsi_pullback_lower": 38,   # tightened from 30 - higher quality longs
                "rsi_pullback_upper": 47,   # tightened from 50
                "rsi_short_lower": 53,      # shorts: RSI must be 53-65
                "rsi_short_upper": 65,
                "fast_ema": 20,
                "slow_ema": 50,
                "ema200_period": 200,
                "adx_min": 20,              # trend must be established
                "adx_max": 45,              # avoid extended/exhausted trends
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "atr_period": 14,
                "tp_atr_mult": 3.0,
                "sl_atr_mult": 1.0,
                "sl_bars_lookback": 5
            }
        super().__init__(
            name="RSI_Pullback",
            category="Trend + Reversion Hybrid",
            params=params,
            regime=["TRENDING"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        rsi_period    = self.params.get("rsi_period", 14)
        fast_ema      = self.params.get("fast_ema", 20)
        slow_ema      = self.params.get("slow_ema", 50)
        ema200_period = self.params.get("ema200_period", 200)
        p_lower       = self.params.get("rsi_pullback_lower", 38)
        p_upper       = self.params.get("rsi_pullback_upper", 47)
        s_lower       = self.params.get("rsi_short_lower", 53)
        s_upper       = self.params.get("rsi_short_upper", 65)
        adx_min       = self.params.get("adx_min", 20)
        adx_max       = self.params.get("adx_max", 45)
        macd_fast     = self.params.get("macd_fast", 12)
        macd_slow     = self.params.get("macd_slow", 26)
        macd_signal   = self.params.get("macd_signal", 9)

        # --- Indicators ---
        df['rsi']      = ta.rsi(df['close'], length=rsi_period)
        df['ema_fast'] = ta.ema(df['close'], length=fast_ema)
        df['ema_slow'] = ta.ema(df['close'], length=slow_ema)
        df['ema200']   = ta.ema(df['close'], length=ema200_period)

        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        macd_df = ta.macd(df['close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
        hist_col = f"MACDh_{macd_fast}_{macd_slow}_{macd_signal}"
        df['macd_hist'] = macd_df[hist_col] if hist_col in macd_df.columns else 0.0

        # --- Gates ---
        # Macro direction: price must be above/below EMA200
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # Trend structure: both EMAs aligned AND price above/below fast EMA (AND, not OR)
        trend_up   = (df['ema_fast'] > df['ema_slow']) & (df['close'] > df['ema_fast'])
        trend_down = (df['ema_fast'] < df['ema_slow']) & (df['close'] < df['ema_fast'])

        # ADX in trending-but-not-exhausted zone
        adx_ok = df['adx'].between(adx_min, adx_max)

        # MACD histogram turning toward entry direction
        hist_turning_up   = df['macd_hist'] > df['macd_hist'].shift(1)
        hist_turning_down = df['macd_hist'] < df['macd_hist'].shift(1)

        # --- Signals ---
        df['signal'] = 0

        long_cond = (
            macro_up
            & trend_up
            & adx_ok
            & df['rsi'].between(p_lower, p_upper)
            & hist_turning_up
        )

        short_cond = (
            macro_down
            & trend_down
            & adx_ok
            & df['rsi'].between(s_lower, s_upper)
            & hist_turning_down
        )

        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive identical signals (entry only, not continuation)
        df.loc[(df['signal'] == 1)  & (df['signal'].shift(1) == 1),  'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
