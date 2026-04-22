import yaml
import os

def update_strategies():
    path = "config/strategies.yaml"
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    # Define tiers based on docs
    t1 = [
        "ma_crossover", "rsi_bounce", "macd_trend", "gold_momentum_breakout", 
        "range_breakout", "bb_mean_reversion", "ema_ribbon_trend", 
        "stoch_divergence", "stat_arb_gold_silver"
    ]
    t2 = [
        "rsi_pullback", "session_momentum", "dual_ema_momentum", "hikkake_trap",
        "rvgi_cci_confluence", "vwap_momentum", "orb", "turtle_soup"
    ]
    t3 = [
        "crypto_rsi_extremes", "volatility_squeeze_breakout", "institutional_silver_bullet",
        "dual_ema_fractal", "rsi_2", "triple_macd_scalping", "naked_price_action"
    ]
    staging = ["ict_judas_swing"]
    disabled = ["cot_sentiment", "regime_aware", "news_breakout", "ml_classifier"]

    # Pair restrictions
    best_pairs = {
        "ma_crossover": ["EURUSD"],
        "rsi_bounce": ["EURUSD"],
        "macd_trend": ["EURUSD", "USDJPY"],
        "gold_momentum_breakout": ["XAUUSD", "GBPUSD"],
        "range_breakout": ["XAUUSD"],
        "bb_mean_reversion": ["XAUUSD"],
        "ema_ribbon_trend": ["BTCUSD"],
        "stoch_divergence": ["EURUSD"],
        "stat_arb_gold_silver": ["XAUUSD"],
        "rsi_pullback": ["XAUUSD"],
        "session_momentum": ["XAUUSD"],
        "dual_ema_momentum": ["XAUUSD"],
        "hikkake_trap": ["XAUUSD"],
        "rvgi_cci_confluence": ["EURUSD"],
        "vwap_momentum": ["GBPUSD"],
        "orb": ["XAGUSD"],
        "turtle_soup": ["EURUSD"],
        "crypto_rsi_extremes": ["USDJPY"],
        "volatility_squeeze_breakout": ["GBPUSD"],
        "institutional_silver_bullet": ["EURUSD"],
        "dual_ema_fractal": ["EURUSD"],
        "rsi_2": ["USDJPY"],
        "triple_macd_scalping": ["USDJPY"],
        "naked_price_action": ["USDJPY"],
        "ict_judas_swing": ["EURUSD"],
    }

    # Add missing strategies if they don't exist
    if "macd_trend" not in data:
        data["macd_trend"] = {
            "name": "MACD Trend",
            "category": "Trend Following",
            "status": "implemented",
            "parameters": {
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "adx_length": 14,
                "adx_threshold": 25
            }
        }
    if "gold_momentum_breakout" not in data:
        data["gold_momentum_breakout"] = {
            "name": "Gold Momentum Breakout",
            "category": "Breakout",
            "status": "implemented",
            "parameters": {
                "bb_length": 20, 
                "bb_std": 2.0, 
                "rsi_length": 14,
                "rsi_buy_min": 50,
                "rsi_sell_max": 50,
                "squeeze_threshold_pct": 0.05
            }
        }

    for strat_id, strat_data in data.items():
        if not isinstance(strat_data, dict):
            continue
        
        # Assign Tier
        if strat_id in t1:
            strat_data['tier'] = "TIER_1"
            strat_data['enabled'] = True
        elif strat_id in t2:
            strat_data['tier'] = "TIER_2"
            strat_data['enabled'] = True
        elif strat_id in t3:
            strat_data['tier'] = "TIER_3"
            strat_data['enabled'] = True
        elif strat_id in staging:
            strat_data['tier'] = "STAGING"
            strat_data['enabled'] = True
            strat_data['mode'] = "monitor_only"
        elif strat_id in disabled:
            strat_data['tier'] = "DISABLED"
            strat_data['enabled'] = False
        else:
            strat_data['enabled'] = False
            strat_data.setdefault('tier', 'DISABLED')

        # Update pairs and timeframes
        if strat_id in best_pairs:
            strat_data['pairs'] = best_pairs[strat_id]
        
        # Default timeframes if missing
        if 'timeframes' not in strat_data:
            strat_data['timeframes'] = ["H1"]

        # Ensure mode exists for non-staging
        if strat_id not in staging:
            strat_data['mode'] = "trade"

    # Save back
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False, indent=2)

    print("Successfully updated strategies.yaml")

if __name__ == "__main__":
    update_strategies()
