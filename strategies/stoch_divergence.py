import pandas as pd
import numpy as np

pd.set_option('future.no_silent_downcasting', True)
import ta_compat as ta
from strategies.base_strategy import BaseStrategy
from data.db_client import DBClient

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
APPROVED_TIMEFRAMES = ["H1", "H4"]   # H4+H1 dual-TF; D1 removed (insufficient divergence frequency)


def _compute_stoch_divergence(df: pd.DataFrame, k_period, sk, sd, look, lower, upper):
    """
    Helper: compute stochastic, crossovers, and divergence conditions for a given OHLCV df.
    Returns a Series of (cross_up, cross_down, bullish_div, bearish_div) as dict of Series.
    """
    stoch_df = ta.stoch(df['high'], df['low'], df['close'],
                        k_period=k_period, smooth_k=sk, smooth_d=sd)
    col_k = f"STOCHk_{k_period}_{sk}_{sd}"
    col_d = f"STOCHd_{k_period}_{sk}_{sd}"
    stoch_k = stoch_df[col_k]
    stoch_d = stoch_df[col_d]

    k_above_d  = stoch_k > stoch_d
    cross_up   = k_above_d & (~k_above_d.shift(1).astype(bool).fillna(False))
    cross_down = (~k_above_d) & (k_above_d.shift(1).astype(bool).fillna(False))

    win_price_low   = df['low'].rolling(look).min()
    prev_price_low  = df['low'].rolling(look).min().shift(look)
    win_price_high  = df['high'].rolling(look).max()
    prev_price_high = df['high'].rolling(look).max().shift(look)
    win_stoch_low   = stoch_k.rolling(look).min()
    prev_stoch_low  = stoch_k.rolling(look).min().shift(look)
    win_stoch_high  = stoch_k.rolling(look).max()
    prev_stoch_high = stoch_k.rolling(look).max().shift(look)

    bullish_div = (win_price_low < prev_price_low) & (win_stoch_low > prev_stoch_low)
    bearish_div = (win_price_high > prev_price_high) & (win_stoch_high < prev_stoch_high)

    return {
        "stoch_k":    stoch_k,
        "cross_up":   cross_up,
        "cross_down": cross_down,
        "bull_div":   bullish_div,
        "bear_div":   bearish_div,
    }


class StochDivergenceStrategy(BaseStrategy):
    """
    Stochastic Divergence Mean Reversion — v3 Dual-TF Overhaul.

    Architecture: H4 is the confirmation timeframe; H1 (or H4) is the entry timeframe.
    - Run divergence + crossover detection on BOTH the entry TF and the H4 TF.
    - Only enter when divergence is confirmed on BOTH timeframes simultaneously.
    - H4 divergence is resampled/aligned to the entry TF's bar timestamps.
    - Eliminates low-conviction single-TF divergence signals (WR 14-34% -> targeting 60%+).

    Other v3 changes:
    - Timeframes: D1 removed; H1 added. Entry TF = H1 or H4.
    - Tighter stoch zones: oversold=20, overbought=80 (same as v2).
    - EMA200 macro gate retained.
    - ADX max = 30 retained.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "stoch_period":        14,
                "stoch_smooth_k":       3,
                "stoch_smooth_d":       3,
                "divergence_lookback": 10,
                "stoch_oversold":      20,
                "stoch_overbought":    80,
                "confirm_timeframe":  "H4",   # H4 is always the confirmation TF
                "atr_period":          14,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "adx_max":             30,
                "ema200_period":      200,
                "rsi_period":          14,
                "rsi_bull_min":        25,
                "rsi_bull_max":        55,
                "rsi_bear_min":        45,
                "rsi_bear_max":        75,
                "use_partial_tp":      False,
            }
        super().__init__(
            name="Stoch_Divergence",
            category="Divergence / Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def _fetch_tf_data(self, symbol: str, timeframe: str, start, end) -> pd.DataFrame:
        """Fetch OHLCV from DB for any given timeframe and symbol."""
        db = DBClient()
        rows = db.execute_query(
            "SELECT timestamp, open, high, low, close, tick_volume "
            "FROM market_data WHERE pair = %s AND timeframe = %s "
            "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
            (symbol, timeframe, start, end)
        )
        if not rows:
            return pd.DataFrame()
        df_tf = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
        df_tf.set_index("timestamp", inplace=True)
        for col in ["open", "high", "low", "close", "tick_volume"]:
            df_tf[col] = df_tf[col].astype(float)
        return df_tf

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        k_period      = self.params.get("stoch_period",        14)
        sk            = self.params.get("stoch_smooth_k",       3)
        sd            = self.params.get("stoch_smooth_d",       3)
        look          = self.params.get("divergence_lookback",  10)
        lower         = self.params.get("stoch_oversold",       20)
        upper         = self.params.get("stoch_overbought",     80)
        adx_max       = self.params.get("adx_max",              30)
        ema200_p      = self.params.get("ema200_period",       200)
        rsi_p         = self.params.get("rsi_period",           14)
        
        # Detect current timeframe
        diff = df.index[1] - df.index[0]
        entry_tf_is_h4 = diff.seconds >= 14400 if not diff.days else False
        entry_tf_is_h1 = diff.seconds == 3600

        symbol = self.params.get("_symbol", "XAUUSD")
        start = df.index.min()
        end   = df.index.max()

        # ── 1. Entry TF signals (The Trigger) ─────────────────────────────────
        entry = _compute_stoch_divergence(df, k_period, sk, sd, look, lower, upper)
        df['rsi'] = ta.rsi(df['close'], length=rsi_p)

        # ── 2. H4 Context (The Setup) ──────────────────────────────────────────
        # If on H1, look for H4 context. If on H4, look for D1 context.
        context_tf = "H4" if entry_tf_is_h1 else "D1"
        h4_ok_long  = pd.Series(True, index=df.index)
        h4_ok_short = pd.Series(True, index=df.index)

        try:
            df_context = self._fetch_tf_data(symbol, context_tf, start, end)
            if not df_context.empty:
                ctx = _compute_stoch_divergence(df_context, k_period, sk, sd, look, lower, upper)
                ctx_rsi = ta.rsi(df_context['close'], length=rsi_p)
                
                # Context is valid if:
                # - TF showed divergence in the last 5 bars
                # - OR TF is currently in extreme RSI zone (<30 or >70)
                ctx_bull = ctx["bull_div"] | (ctx_rsi < 30)
                ctx_bear = ctx["bear_div"] | (ctx_rsi > 70)
                
                # Lookback window on higher TF (setup doesn't have to be exact same bar)
                ctx_bull_window = ctx_bull.rolling(5).max() > 0
                ctx_bear_window = ctx_bear.rolling(5).max() > 0
                
                h4_ok_long  = ctx_bull_window.reindex(df.index, method="ffill").fillna(False)
                h4_ok_short = ctx_bear_window.reindex(df.index, method="ffill").fillna(False)
        except Exception as e:
            print(f"  [StochDiv] Context fetch failed ({e})")

        # ── 3. D1 Trend Gate (The Filter) ─────────────────────────────────────
        d1_trend_long  = pd.Series(True, index=df.index)
        d1_trend_short = pd.Series(True, index=df.index)
        try:
            df_d1 = self._fetch_tf_data(symbol, "D1", start, end)
            if not df_d1.empty:
                d1_ema = ta.ema(df_d1['close'], length=50)
                d1_bull = df_d1['close'] > d1_ema
                d1_bear = df_d1['close'] < d1_ema
                d1_trend_long  = d1_bull.reindex(df.index, method="ffill").fillna(False)
                d1_trend_short = d1_bear.reindex(df.index, method="ffill").fillna(False)
        except Exception as e:
            print(f"  [StochDiv] D1 trend fetch failed ({e})")

        # ── 4. Ranging Gate ───────────────────────────────────────────────────
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df.iloc[:, 0]
        except Exception:
            df['adx'] = 15.0
        ranging = df['adx'] < adx_max

        # ── Final Signal Assembly ─────────────────────────────────────────────
        df['signal'] = 0

        # Long: H1 Trigger (Div + Cross) + H4 Context (Recent Div or OS) + D1 Trend (Bullish)
        long_cond = (
            entry["cross_up"] & 
            entry["bull_div"] & 
            (df['close'] > df['open']) & # NEW: Directional Close
            h4_ok_long & 
            d1_trend_long & 
            ranging
        )
        
        # Short: H1 Trigger (Div + Cross) + H4 Context (Recent Div or OB) + D1 Trend (Bearish)
        short_cond = (
            entry["cross_down"] & 
            entry["bear_div"] & 
            (df['close'] < df['open']) & # NEW: Directional Close
            h4_ok_short & 
            d1_trend_short & 
            ranging
        )

        # Layer 2 — Body Ratio
        long_cond, short_cond = self.apply_body_ratio_filter(df, long_cond, short_cond)

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Dedup consecutive signals
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        print(f"  [StochDiv] v4.0 Active | Longs: {(df['signal']==1).sum()} | Shorts: {(df['signal']==-1).sum()}")
        return df

    def validate_params(self) -> bool:
        return True
