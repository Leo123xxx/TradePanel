import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class RVGICCIConfluence(BaseStrategy):
    """
    RVGI-CCI-SMA Confluence Breakout v2.

    v2 upgrades (2026-05-01) — targeting 70%+ WR:
    - EMA200 macro gate: only long above EMA200, only short below EMA200
    - RSI gate added: RSI > 55 for longs, RSI < 45 for shorts (momentum confirmation)
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rvgi_period":   14,
                "cci_period":    14,
                "sma_period":    20,
                "ema100_period": 100,
                "ema200_period": 200,   # NEW: macro trend gate
                "tp_atr_mult":    2.5,
                "sl_atr_mult":    0.8,
                "cci_buy_min":    0,
                "cci_sell_max":   0,
                "adx_min":       22,
                "rsi_period":    14,    # NEW: RSI momentum gate
                "rsi_long_min":  52,    # loosened 55→52
                "rsi_short_max": 48,    # loosened 45→48
                "atr_period":    14,
                "cooldown_bars": 8,    # loosened 15→8
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

        rvgi_p        = self.params['rvgi_period']
        cci_buy_min   = self.params.get("cci_buy_min",   0)
        cci_sell_max  = self.params.get("cci_sell_max",  0)
        ema100_p      = self.params.get("ema100_period", 100)
        ema200_p      = self.params.get("ema200_period", 200)
        adx_min       = self.params.get("adx_min",       22)
        rsi_p         = self.params.get("rsi_period",    14)
        rsi_long_min  = self.params.get("rsi_long_min",  55)
        rsi_short_max = self.params.get("rsi_short_max", 45)
        cooldown      = self.params.get("cooldown_bars", 15)

        # 1. RVGI
        num = (df['close'] - df['open']) + 2 * (df['close'].shift(1) - df['open'].shift(1)) + \
              2 * (df['close'].shift(2) - df['open'].shift(2)) + (df['close'].shift(3) - df['open'].shift(3))
        den = (df['high'] - df['low']) + 2 * (df['high'].shift(1) - df['low'].shift(1)) + \
              2 * (df['high'].shift(2) - df['low'].shift(2)) + (df['high'].shift(3) - df['low'].shift(3))

        df['rvgi_val'] = num.rolling(window=rvgi_p).sum() / den.rolling(window=rvgi_p).sum()
        df['rvgi_sig'] = (df['rvgi_val'] + 2 * df['rvgi_val'].shift(1) +
                          2 * df['rvgi_val'].shift(2) + df['rvgi_val'].shift(3)) / 6

        # 2. CCI
        tp = (df['high'] + df['low'] + df['close']) / 3
        sma_tp = tp.rolling(window=self.params['cci_period']).mean()
        mad_tp = tp.rolling(window=self.params['cci_period']).apply(lambda x: (x - x.mean()).abs().mean())
        df['cci'] = (tp - sma_tp) / (0.015 * mad_tp)

        # 3. EMA100 (short-term structure) + EMA200 (macro gate)
        df['ema100'] = ta.ema(df['close'], length=ema100_p)
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # 4. ADX gate
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]
        trend_ok  = df['adx'] >= adx_min

        # 5. RSI momentum gate
        df['rsi'] = ta.rsi(df['close'], length=rsi_p)
        rsi_ok_long  = df['rsi'] > rsi_long_min
        rsi_ok_short = df['rsi'] < rsi_short_max

        # 6. Signals
        df['signal'] = 0

        df.loc[
            (df['rvgi_val'] > df['rvgi_sig']) &
            (df['rvgi_val'].shift(1) <= df['rvgi_sig'].shift(1)) &
            (df['cci'] > cci_buy_min) &
            (df['close'] > df['ema100']) &
            macro_up & trend_ok & rsi_ok_long,
            'signal'
        ] = 1

        df.loc[
            (df['rvgi_val'] < df['rvgi_sig']) &
            (df['rvgi_val'].shift(1) >= df['rvgi_sig'].shift(1)) &
            (df['cci'] < cci_sell_max) &
            (df['close'] < df['ema100']) &
            macro_down & trend_ok & rsi_ok_short,
            'signal'
        ] = -1

        # Cooldown filter
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
