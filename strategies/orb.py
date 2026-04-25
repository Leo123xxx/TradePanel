import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy


class ORBStrategy(BaseStrategy):
    """
    Opening Range Breakout (ORB)

    Logic:
    1. Define Opening Range (first 60 mins of the NY session window).
    2. Entry: Buy on first close above range high, Sell on first close below range low.
    3. Volume filter: hourly-normalised so NY-afternoon bars are not unfairly
       compared against London-open spikes (which caused 0 signals on EURUSD M15).
    """

    def __init__(self, params=None):
        if params is None:
            params = {
                'ny_offset_hours':     7,
                'range_start_ny':      9.5,
                'range_duration_mins': 60,
                'vol_filter':          1.2,
                'tp_atr_mult':         2.0,
                'sl_atr_mult':         1.0,
                # ORB manages its own session windows via is_range / is_post_range.
                # The generic BASE session filter (EURUSD: UTC 7-17) zeros out
                # every post-range signal because they start at SAST 17:30 = hour>=17.
                'use_session_filter':  False,
            }
        super().__init__(
            name='Opening_Range_Breakout',
            category='Breakout',
            params=params,
            regime=['TRENDING', 'ANY'],
            timeframes=['M15', 'H1'],
            pairs=['GBPUSD', 'EURUSD', 'XAUUSD'],
        )

    def generate_signals(self, data):
        df = data.copy()
        offset = self.params.get('ny_offset_hours', 7)

        # 1. Map each bar to its NY-equivalent hour
        df['hour_ny'] = (df.index.hour - offset) + (df.index.minute / 60.0)
        df['date'] = df.index.date

        # 2. Identify Opening Range bars
        start = self.params['range_start_ny']
        end   = start + (self.params['range_duration_mins'] / 60.0)
        df['is_range'] = (df['hour_ny'] >= start) & (df['hour_ny'] < end)

        range_high = df[df['is_range']].groupby('date')['high'].max()
        range_low  = df[df['is_range']].groupby('date')['low'].min()
        df['rh'] = df['date'].map(range_high)
        df['rl'] = df['date'].map(range_low)

        # 3. Post-range window: 4 hours after range closes
        df['is_post_range'] = (df['hour_ny'] >= end) & (df['hour_ny'] < (end + 4))

        # 4. Volume filter
        # Root cause of EURUSD 0-signal bug: a 20-bar rolling average at SAST 17:30
        # is dominated by the London/NY overlap bars immediately before it.
        # Post-range NY-afternoon bars (~200-400 ticks) almost never clear 1.2x of
        # that inflated average (~800-1200 ticks), so vol_ok was permanently False.
        #
        # Fix: normalise by hourly mean. Each bar competes only against bars from
        # the same clock-hour across the full dataset, eliminating session bias.
        #
        # If fewer than 50% of bars have non-zero tick_volume, bypass entirely.
        tv = df['tick_volume']
        nonzero_pct = (tv > 0).mean()
        volume_data_usable = nonzero_pct >= 0.5

        if volume_data_usable:
            # Volume filter applied to the RANGE bars, not the post-range breakout.
            # Rationale: a high-volume opening range signals genuine participation
            # and makes subsequent breakouts more reliable. Post-range NY-afternoon
            # bars are structurally quieter (London has closed), so applying vol_filter
            # to them anti-correlates with breakout timing and kills all signals.
            #
            # For each day: compute mean tick_volume of range bars vs hourly baseline.
            # Mark the day as vol_ok if range bars were above-average for their hours.
            df['_hr'] = df.index.hour
            hmean = df.groupby('_hr')['tick_volume'].transform('mean')
            df['_vol_rel'] = tv / hmean.clip(lower=1)  # relative volume vs hourly avg
            # Average relative volume for range bars on each day
            range_rel_vol = (
                df[df['is_range']]
                .groupby('date')['_vol_rel']
                .mean()
            )
            df['_day_range_vol_ok'] = df['date'].map(
                range_rel_vol >= self.params['vol_filter']
            )
            df['vol_ok'] = df['_day_range_vol_ok'].fillna(False)
            df.drop(columns=['_hr', '_vol_rel', '_day_range_vol_ok'], inplace=True)
        else:
            df['vol_ok'] = True

        # Diagnostic - surface timing/volume issues at a glance
        n_range       = int(df['is_range'].sum())
        n_post        = int(df['is_post_range'].sum())
        n_rh_valid    = int(df['rh'].notna().sum())
        n_vol_days    = int(df[df['is_range']]['vol_ok'].sum())
        n_close_above = int(
            (df['is_post_range'] & df['rh'].notna() & (df['close'] > df['rh'])).sum()
        )
        vol_tag = 'range-vol-filter' if volume_data_usable else 'bypassed'
        n_vol_ok_post  = int((df['is_post_range'] & df['vol_ok']).sum())
        n_crossover    = int((df['is_post_range'] & df['rh'].notna() & (df['close'] > df['rh']) & (df['close'].shift(1) <= df['rh'])).sum())
        n_all_three    = int((df['is_post_range'] & df['rh'].notna() & (df['close'] > df['rh']) & (df['close'].shift(1) <= df['rh']) & df['vol_ok']).sum())
        print(
            '[ORB] range_bars={}  post={}  vol_ok_days={}  vol_ok_post={}  close_above_rh={}  crossover={}  signals={} vol={}'.format(
                n_range, n_post, n_vol_days, n_vol_ok_post, n_close_above, n_crossover, n_all_three, vol_tag
            )
        )

        # 5. Signals
        df['signal'] = 0
        buy_cond = (
            df['is_post_range']
            & (df['close'] > df['rh'])
            & (df['close'].shift(1) <= df['rh'])
            & df['vol_ok']
        )
        sell_cond = (
            df['is_post_range']
            & (df['close'] < df['rl'])
            & (df['close'].shift(1) >= df['rl'])
            & df['vol_ok']
        )
        df.loc[buy_cond,  'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        return df

    def validate_params(self):
        return True
