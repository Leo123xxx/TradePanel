import importlib
import os
from typing import Dict, Type
from strategies.base_strategy import BaseStrategy

class StrategyRegistry:
    def __init__(self):
        self.strategies: Dict[str, Type[BaseStrategy]] = {}

    def register(self, name: str, strategy_class: Type[BaseStrategy]):
        self.strategies[name] = strategy_class
        print(f"Registered strategy: {name}")

    def get_strategy(self, name: str, params: dict) -> BaseStrategy:
        strategy_class = self.strategies.get(name)
        if not strategy_class:
            raise ValueError(f"Strategy {name} not found in registry.")
        return strategy_class(params)

    def load_all_from_folder(self, folder_path: str = "strategies"):
        """Dynamically loads all strategy classes in the specified folder."""
        # Implementation for dynamic loading can be added here
        pass

# Global instance
registry = StrategyRegistry()
