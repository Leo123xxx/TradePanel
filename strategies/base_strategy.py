from abc import ABC, abstractmethod
from typing import List
import pandas as pd

# Session hours (UTC) for peak liquidity per pair.
# Signals generated OUTSIDE these windows are suppressed on intraday bars.
SESSION_WINDOWS = {
    "EURUSD": [(7, 17)],
    "GBPUSD": [(7, 17)],
    "USDJPY": [(0, 3), (12, 17)],
    "XAUUSD": [(7, 20)],
    "XAGUSD": [(7, 20)],
    "BTCUSD": [(0, 24)],
    "ETHUSD": [(0, 24)],
}
DEFAULT_SESSION = [(0, 24)]


class BaseStrategy(ABC):
    """
    Abstract base class all strategies must inherit.

    Session filter (filter_by_session):
      Called by the engine after generate_signals(). Zeroes out signals fired
      outside peak liquidity hours for intraday bars.
      Daily+ data (median bar gap ≥ 20 h) is always passed through unfiltered —
      this handles brokers that store D1 bars at 21:00 or 22:00 UTC rather than midnight.
    """

    def __init__(
        self,
        name: str,
        category: str,
        params: dict,
        regime: List[str] = None,
        timeframes: List[str] = None,
        pairs: List[str] = None
    ):
        self.name = name
        self.category = category
        self.params = params
        self.regime = regime or ["ANY"]
        self.timeframes = timeframes or []
        self.pairs = pairs or []
        self.confirm_tf = params.get("confirm_timeframe")
        self.use_regime_filter = params.get("use_regime_filter", False)
        self.use_session_filter = params.get("use_session_filter", True)

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def filter_by_session(self, df: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Zeroes out signals outside peak liquidity hours for intraday data.
        Daily+ timeframes (median bar gap ≥ 20 h) are always passed through
        regardless of the bar's clock time — this is robust to brokers that
        anchor D1 bars at 21:00/22:00 UTC instead of midnight.
        """
        if not self.use_session_filter:
            return df
        if not hasattr(df.index, 'hour'):
            return df

        # Detect daily+ data by median bar spacing — broker-agnostic
        if len(df) > 1:
            try:
                median_gap_hours = (
                    df.index.to_series().diff().median().total_seconds() / 3600
                )
                if median_gap_hours >= 20:
                    return df  # D1 / W1 / MN — skip session filter
            except Exception:
                pass

        windows = SESSION_WINDOWS.get(pair, DEFAULT_SESSION)
        if windows == [(0, 24)]:
            return df

        hour = df.index.hour
        in_session = pd.Series(False, index=df.index)
        for start_h, end_h in windows:
            if start_h < end_h:
                in_session |= (hour >= start_h) & (hour < end_h)
            else:
                in_session |= (hour >= start_h) | (hour < end_h)

        df = df.copy()
        df.loc[~in_session, 'signal'] = 0
        return df

    def get_parameters(self) -> dict:
        return self.params

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "params": self.params,
            "regime": self.regime,
            "timeframes": self.timeframes,
            "pairs": self.pairs,
            "confirm_tf": self.confirm_tf,
            "use_regime_filter": self.use_regime_filter,
            "use_session_filter": self.use_session_filter,
        }

    @abstractmethod
    def validate_params(self) -> bool:
        pass
