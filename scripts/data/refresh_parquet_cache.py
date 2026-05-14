import os
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Setup root path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lib.db_client import DatabaseClient
from scripts.lib.logger import setup_logger

def refresh_cache():
    logger = setup_logger("cache_refresher", "cache_refresher.json.log")
    db = DatabaseClient("cache_refresher")
    
    cache_dir = PROJECT_ROOT / "results" / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting Parquet cache refresh...")
    
    # Get list of pairs and timeframes in DB
    try:
        combinations = db.execute_query("SELECT DISTINCT pair, timeframe FROM market_data")
        if not combinations:
            logger.warning("No market data found in DB.")
            return

        for pair, timeframe in combinations:
            logger.info(f"Caching {pair} {timeframe}...")
            
            # Fetch data
            query = """
                SELECT timestamp, open, high, low, close, tick_volume, spread 
                FROM market_data 
                WHERE pair = %s AND timeframe = %s
                ORDER BY timestamp ASC
            """
            data = db.execute_query(query, (pair, timeframe))
            
            if not data:
                continue
                
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume', 'spread'])
            
            # Save to Parquet
            file_name = f"{pair}_{timeframe}.parquet"
            file_path = cache_dir / file_name
            df.to_parquet(file_path, engine='pyarrow', index=False)
            
            logger.info(f"Saved {len(df)} bars to {file_name}")

        logger.info("Parquet cache refresh complete.")
        
    except Exception as e:
        logger.error(f"Cache refresh failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    refresh_cache()
