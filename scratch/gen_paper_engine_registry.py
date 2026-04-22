import os
import re

def generate_registry():
    strat_dir = "strategies"
    files = [f for f in os.listdir(strat_dir) if f.endswith('.py') and f != '__init__.py' and f != 'base_strategy.py' and f != 'registry.py']
    
    imports = []
    registry_entries = []
    
    for f in sorted(files):
        module_name = f[:-3]
        class_name = "".join([word.capitalize() for word in module_name.split('_')])
        
        # Exceptions for manual mapping
        mapping = {
            "institutional_silver_bullet": "InstitutionalSilverBullet",
            "ict_judas_swing": "ICTJudasSwing",
            "turtle_soup": "TurtleSoup",
            "dual_ema_momentum": "DualEMAMomentum",
            "triple_macd_scalping": "TripleMACDScalping",
            "dual_ema_fractal": "DualEMAFractal",
            "vwap_momentum": "VWAPMomentum",
            "hikkake_trap": "HikkakeTrap",
            "rvgi_cci_confluence": "RVGICCIConfluence",
            "volatility_contraction": "VolatilityContraction",
            "stat_arb_gold_silver": "StatArbGoldSilver",
            "naked_price_action": "NakedPriceAction",
            "rsi_2": "RSITwoStrategy",
            "orb": "ORBStrategy",
            "ensemble": "EnsembleStrategy"
        }
        
        real_class_name = mapping.get(module_name, class_name)
        # Handle cases where I don't know the exact class name
        # I'll check the file content for the class definition
        with open(os.path.join(strat_dir, f), 'r') as file:
            content = file.read()
            match = re.search(r'class\s+(\w+)\(BaseStrategy\)', content)
            if match:
                real_class_name = match.group(1)
            else:
                match = re.search(r'class\s+(\w+)\(', content)
                if match:
                    real_class_name = match.group(1)

        imports.append(f"from strategies.{module_name} import {real_class_name}")
        registry_entries.append(f"    \"{module_name}\": {real_class_name},")

    print("\n".join(imports))
    print("\nSTRATEGY_REGISTRY = {")
    print("\n".join(registry_entries))
    print("}")

if __name__ == "__main__":
    generate_registry()
