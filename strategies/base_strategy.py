from abc import ABC, abstractmethod
from typing import List
import pandas as pd

class BaseStrategy(ABC):
    """
    Abstract base class all strategies must inherit.
    Enforces a standard interface so any strategy can be plugged into
    the backtesting engine, paper trading engine, or live engine without modification.

    Required overrides: generate_signals(), validate_params()
    Optional overrides: get_parameters(), get_metadata()
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
        # Regime tags — must match keys from regime_detector output:
        # TRENDING | RANGING | HIGH_VOL | LOW_VOL | ANY
        self.regime = regime or ["ANY"]
        # Timeframes this strategy is designed to run on
        self.timeframes = timeframes or []
        # Pairs this strategy is approved to trade
        self.pairs = pairs or []
        self.confirm_tf = params.get("confirm_timeframe")
        self.use_regime_filter = params.get("use_regime_filter", False)

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Processes OHLCV data and returns a DataFrame with a 'signal' column.
        Signal values: 1 = Buy, -1 = Sell, 0 = Hold
        Only past data visible at each bar — no look-ahead.
        """
        pass

    def get_parameters(self) -> dict:
        """Returns the current parameter set (used by optimiser and logger)."""
        return self.params

    def get_metadata(self) -> dict:
        """
        Returns full strategy metadata.
        Used by: regime detector, paper engine, scheduler, Telegram /strategies command.
        """
        return {
            "name": self.name,
            "category": self.category,
            "params": self.params,
            "regime": self.regime,
            "timeframes": self.timeframes,
            "pairs": self.pairs,
            "confirm_tf": self.confirm_tf,
            "use_regime_filter": self.use_regime_filter
        }

    @abstractmethod
    def validate_params(self) -> bool:
        """Validates that parameters are within acceptable ranges before running."""
        pass
