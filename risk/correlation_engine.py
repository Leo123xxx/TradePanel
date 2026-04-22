import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.db_client import DBClient

class CorrelationEngine:
    def __init__(self, db: DBClient):
        self.db = db
        self.threshold = 0.8

    def get_strategy_correlations(self, active_strategies: list, window_bars=100):
        """
        Calculates the correlation matrix for a list of active strategies.
        Returns a list of high-correlation pairs (str1, str2, corr).
        """
        if not active_strategies or len(active_strategies) < 2:
            return []

        # 1. Fetch returns for each strategy's primary assets
        # For simplicity, we use the price returns of the first pair in the strategy config
        # as a proxy for the strategy's exposure.
        returns_data = {}
        
        for strat_name, strat_obj in active_strategies:
            # We need to find the pair this strategy trades
            # Since strategies move between pairs, we'll look at the price action 
            # of the pairs they are currently 'enabled' for.
            pair = strat_obj.pairs[0] if hasattr(strat_obj, 'pairs') and strat_obj.pairs else "XAUUSD"
            
            query = """
                SELECT timestamp, close FROM market_data 
                WHERE pair = %s AND timeframe = 'H1' 
                ORDER BY timestamp DESC LIMIT %s
            """
            rows = self.db.execute_query(query, (pair, window_bars))
            if not rows:
                continue
                
            df = pd.DataFrame(rows, columns=['timestamp', 'close'])
            df.set_index('timestamp', inplace=True)
            df['returns'] = df['close'].pct_change()
            returns_data[strat_name] = df['returns'].dropna()

        if len(returns_data) < 2:
            return []

        # 2. Align data and calculate correlation
        df_corr = pd.DataFrame(returns_data).corr()
        
        high_corr_pairs = []
        labels = df_corr.columns
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                corr_val = df_corr.iloc[i, j]
                if abs(corr_val) > self.threshold:
                    high_corr_pairs.append({
                        "strat_1": labels[i],
                        "strat_2": labels[j],
                        "correlation": round(corr_val, 3)
                    })
        
        return high_corr_pairs

    def check_signal_redundancy(self, new_strategy, new_pair, open_positions):
        """
        Checks if a new signal is redundant because of existing positions
        in highly correlated strategies.
        """
        if not open_positions:
            return False, 0.0

        # This is a simplified check for the 'WARNING' phase.
        # It checks if we have an open position in the same pair or a correlated pair.
        for pos in open_positions:
            # If same pair, it's already a cluster risk if different strategies
            if pos.symbol == new_pair:
                # We'll calculate correlation between self and the strategy of the open position
                # But for now, we'll just flag it if it's the same asset.
                return True, 1.0
            
            # TODO: Harder check using price correlation between new_pair and pos.symbol
            # For brevity in this phase, we focus on the asset clusters.
        
        return False, 0.0
