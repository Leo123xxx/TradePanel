import os
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

# Setup root path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.db_client import DBClient
from scripts.lib.logger import setup_logger

def _refresh_single_pair(pair, timeframe):
    """Worker function for parallel refresh."""
    db = DBClient()
    logger = setup_logger(f"cache_{pair}_{timeframe}", f"cache_{pair}_{timeframe}.json.log")
    
    cache_dir = PROJECT_ROOT / "results" / "data" / "cache"
    file_name = f"{pair}_{timeframe}.parquet"
    file_path = cache_dir / file_name
    
    try:
        last_timestamp = None
        if file_path.exists():
            # Incremental check: get last timestamp from existing parquet
            existing_df = pd.read_parquet(file_path, columns=['timestamp'])
            if not existing_df.empty:
                last_timestamp = existing_df['timestamp'].max()
        
        if last_timestamp:
            logger.info(f"Incremental refresh for {pair} {timeframe} since {last_timestamp}")
            query = """
                SELECT timestamp, open, high, low, close, tick_volume, spread 
                FROM market_data 
                WHERE pair = %s AND timeframe = %s AND timestamp > %s
                ORDER BY timestamp ASC
            """
            new_data = db.execute_query(query, (pair, timeframe, last_timestamp))
            
            if new_data:
                new_df = pd.DataFrame(new_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume', 'spread'])
                full_df = pd.concat([pd.read_parquet(file_path), new_df]).drop_duplicates(subset=['timestamp'])
                full_df.to_parquet(file_path, engine='pyarrow', index=False)
                logger.info(f"Appended {len(new_df)} new bars to {file_name}")
            else:
                logger.info(f"No new data for {pair} {timeframe}")
        else:
            logger.info(f"Full refresh for {pair} {timeframe}")
            query = """
                SELECT timestamp, open, high, low, close, tick_volume, spread 
                FROM market_data 
                WHERE pair = %s AND timeframe = %s
                ORDER BY timestamp ASC
            """
            data = db.execute_query(query, (pair, timeframe))
            if data:
                df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume', 'spread'])
                df.to_parquet(file_path, engine='pyarrow', index=False)
                logger.info(f"Saved {len(df)} bars to {file_name}")

    except Exception as e:
        logger.error(f"Failed to refresh {pair} {timeframe}: {e}")
    finally:
        # DBClient singleton handles pool, but we should be clean
        pass

def refresh_cache():
    logger = setup_logger("cache_refresher", "cache_refresher.json.log")
    db = DBClient()
    
    cache_dir = PROJECT_ROOT / "results" / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting Parallel Parquet cache refresh...")
    
    try:
        combinations = db.execute_query("SELECT DISTINCT pair, timeframe FROM market_data")
        if not combinations:
            logger.warning("No market data found in DB.")
            return

        # Balanced parallel processing: use half of available cores, max 4
        num_workers = min(max(1, os.cpu_count() // 2), 4)
        logger.info(f"Using {num_workers} workers for parallel refresh.")
        
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            executor.map(lambda p: _refresh_single_pair(*p), combinations)

        logger.info("Parquet cache refresh complete.")
        
    except Exception as e:
        logger.error(f"Cache refresh failed: {e}")
    finally:
        db.close_all()

if __name__ == "__main__":
    refresh_cache()
