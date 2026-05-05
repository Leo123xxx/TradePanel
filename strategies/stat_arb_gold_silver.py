import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy
from data.db_client import DBClient

class StatArbGoldSilver(BaseStrategy):
    """
    Statistical Arbitrage (XAUUSD vs XAGUSD) v3.

    Logic:
    1. Ratio: Calculate XAUUSD/XAGUSD ratio.
    2. Z-Score: Distance from window-period mean in standard deviations.
    3. Signal:
       - Z-Score > z_entry (default 2.0): Gold expensive -> Sell Gold
       - Z-Score < -z_entry (default 2.0): Gold cheap -> Buy Gold

    v3 changes (2026-05-01):
    - D1 disabled: D1 WR=38.5%, MaxDD=106.4% — unacceptable. The daily TF
      has too few signals to provide statistical validity and the extreme drawdown
      suggests the mean-reversion window is too short for daily bars.
    - Added H1, M30, M15 support: tighter timeframes provide more signals and
      allow the z-score window to remain statistically meaningful (200 bars = ~8 days
      on H1 vs 200 trading days on D1).
    - Timeframe auto-detection retained from v1.

    Implementation: strategy processes XAUUSD; fetches XAGUSD at the same TF from DB.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "window":           200,
                "z_entry":           2.0,
                "z_exit":            0.0,
                "secondary_symbol": "XAGUSD"
            }
        super().__init__(
            name="Stat_Arb_Gold_Silver",
            category="Advanced",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["H4", "H1", "M30", "M15"],   # D1 disabled (MaxDD=106%)
            pairs=["XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        db = DBClient()

        secondary = self.params.get("secondary_symbol", "XAGUSD")
        start = df.index.min()
        end   = df.index.max()

        # Detect timeframe from bar spacing
        diff = df.index[1] - df.index[0]
        if diff.days > 0:
            tf = "D1"
        elif diff.seconds >= 14400:
            tf = "H4"
        elif diff.seconds >= 3600:
            tf = "H1"
        elif diff.seconds >= 1800:
            tf = "M30"
        else:
            tf = "M15"

        rows = db.execute_query(
            "SELECT timestamp, close FROM market_data WHERE pair = %s AND timeframe = %s "
            "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
            (secondary, tf, start, end)
        )

        if not rows:
            # Fallback: try H4
            print("[StatArb] WARNING: No data for {} on {}. Trying H4 fallback...".format(secondary, tf))
            rows = db.execute_query(
                "SELECT timestamp, close FROM market_data WHERE pair = %s AND timeframe = %s "
                "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
                (secondary, "H4", start, end)
            )

        if not rows:
            print("[StatArb] ERROR: No data for {}".format(secondary))
            df['signal'] = 0
            return df

        df_sec = pd.DataFrame(rows, columns=['timestamp', 'close_sec'])
        df_sec['timestamp'] = pd.to_datetime(df_sec['timestamp'])
        df_sec.set_index('timestamp', inplace=True)
        df_sec['close_sec'] = df_sec['close_sec'].astype(float)

        df.index = pd.to_datetime(df.index)
        df = df.join(df_sec, how='left')
        df['close_sec'] = df['close_sec'].ffill().bfill()

        # Z-Score on ratio
        df['ratio']      = df['close'] / df['close_sec']
        df['mean_ratio'] = df['ratio'].rolling(window=self.params['window']).mean()
        df['std_ratio']  = df['ratio'].rolling(window=self.params['window']).std()
        df['zscore']     = (df['ratio'] - df['mean_ratio']) / df['std_ratio']

        df['signal'] = 0
        df.loc[df['zscore'] >  self.params['z_entry'], 'signal'] = -1   # Gold expensive
        df.loc[df['zscore'] < -self.params['z_entry'], 'signal'] =  1   # Gold cheap

        return df

    def validate_params(self) -> bool:
        return True
