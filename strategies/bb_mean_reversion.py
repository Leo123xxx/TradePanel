import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H1", "H4"]

class BBMeanReversionStrategy(BaseStrategy):
    """
    Moving Average + Bollinger Bands Mean Reversion.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "sma_period":        20,
                "bb_period":         20,
                "bb_deviation":       2.0,
                "atr_period":        14,
                "rsi_period":        14,
                "rsi_os_low":        25,   # Tightened: 25 instead of 20
                "rsi_os_high":       35,   # tightened from 40 → higher WR bar for long entry
                "rsi_ob_low":        65,   # tightened from 60 → higher WR bar for short entry
                "rsi_ob_high":       75,   # Tightened: 75 instead of 80
                "vol_threshold_mult": 1.1,
                "vol_spike_mult":    1.3,   # NEW: volume spike confirmation
                "adx_max":           20,   # Tightened: 20 instead of 22
                "tp_atr_mult": 2.0,        # mean reversion TP 2:1
                "sl_atr_mult": 1.0,
                "atr_period": 14,
                "use_partial_tp": False,   # run straight to TP — no BE move
                "support_lookback":  50,   # NEW: bars to look back for support
                "support_buffer_pips": 10, # NEW: pips from support
            }
        super().__init__(
            name="BB_Mean_Reversion",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "CHOPPY", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Entry only when:
          - Price touches/crosses Bollinger Band extremes
          - Volatility is elevated (ATR above average OR BB width above median)
          - RSI confirms oversold (20-40 for longs) or overbought (60-80 for shorts)
          - ADX < adx_max (only in ranging/choppy markets — avoids trending XAUUSD)

        v1 problems fixed:
          - RSI long window was 20-30 (10 pts wide → almost never fired correctly)
          - No ADX guard → strategy traded into strong trends and lost
        """
        df = data.copy()

        sma_period   = self.params.get("sma_period",        20)
        bb_period    = self.params.get("bb_period",          20)
        bb_deviation = self.params.get("bb_deviation",       2.0)
        atr_period   = self.params.get("atr_period",         14)
        rsi_period   = self.params.get("rsi_period",         14)
        rsi_os_low   = self.params.get("rsi_os_low",         20)
        rsi_os_high  = self.params.get("rsi_os_high",        40)
        rsi_ob_low   = self.params.get("rsi_ob_low",         60)
        rsi_ob_high  = self.params.get("rsi_ob_high",        75)
        vol_mult     = self.params.get("vol_threshold_mult", 1.1)
        vol_spike_m  = self.params.get("vol_spike_mult",     1.3)
        adx_max      = self.params.get("adx_max",            20)
        sup_lb       = self.params.get("support_lookback",   50)
        sup_buff     = self.params.get("support_buffer_pips", 10)

        # ── Bollinger Bands ───────────────────────────────────────────────────
        bb_df = ta.bbands(df['close'], length=bb_period, std=bb_deviation)
        df['bb_lower'] = bb_df[f"BBL_{bb_period}_{bb_deviation}"]
        df['bb_mid']   = bb_df[f"BBM_{bb_period}_{bb_deviation}"]
        df['bb_upper'] = bb_df[f"BBU_{bb_period}_{bb_deviation}"]
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_width_median'] = df['bb_width'].rolling(window=100).median()

        # ── Supporting indicators ─────────────────────────────────────────────
        df['sma']     = ta.sma(df['close'], length=sma_period)
        df['atr']     = ta.atr(df['high'], df['low'], df['close'], length=atr_period)
        df['atr_sma'] = ta.sma(df['atr'], length=20)
        df['rsi']     = ta.rsi(df['close'], length=rsi_period)

        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # ── Support/Resistance Detection ──────────────────────────────────────
        pip = 0.1 if "XAU" in self.params.get('pair', 'XAUUSD') else 0.0001
        df['rolling_min'] = df['low'].rolling(window=sup_lb).min().shift(1)
        df['rolling_max'] = df['high'].rolling(window=sup_lb).max().shift(1)
        
        near_support = (df['bb_lower'] <= (df['rolling_min'] + sup_buff * pip))
        near_resistance = (df['bb_upper'] >= (df['rolling_max'] - sup_buff * pip))

        # ── Filters ───────────────────────────────────────────────────────────
        vol_elevated = (df['atr'] > df['atr_sma'] * vol_mult) | (df['bb_width'] > df['bb_width_median'])
        vol_spike    = df['tick_volume'] > (df['tick_volume'].rolling(window=20).mean().shift(1) * vol_spike_m)
        ranging      = df['adx'] < adx_max       # guard: no trades in strong trends

        # ── Signals ───────────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            (df['low'] <= df['bb_lower']) &
            vol_elevated &
            vol_spike &
            ranging &
            near_support &
            df['rsi'].between(rsi_os_low, rsi_os_high)
        )

        short_cond = (
            (df['high'] >= df['bb_upper']) &
            vol_elevated &
            vol_spike &
            ranging &
            near_resistance &
            df['rsi'].between(rsi_ob_low, rsi_ob_high)
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
