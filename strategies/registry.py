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
        import inspect
        import pkgutil
        
        # Determine the package name
        package_name = folder_path.replace("/", ".").replace("\\", ".")
        
        # Get the path to the strategies folder
        strategies_dir = os.path.join(os.getcwd(), folder_path)
        
        for _, module_name, is_pkg in pkgutil.iter_modules([strategies_dir]):
            if is_pkg or module_name == "__init__" or module_name == "base_strategy" or module_name == "registry":
                continue
                
            try:
                module = importlib.import_module(f"{package_name}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BaseStrategy) and obj is not BaseStrategy:
                        # Register using the filename as the key (standard practice in this repo)
                        self.register(module_name, obj)
            except Exception as e:
                print(f"Error loading strategy module {module_name}: {e}")

# Global instance
registry = StrategyRegistry()
registry.load_all_from_folder()
