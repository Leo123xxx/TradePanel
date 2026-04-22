import pandas as pd
from data.db_client import DBClient
from datetime import datetime

class DataResampler:
    def __init__(self, db: DBClient):
        self.db = db

    def resample_m1_to_higher(self, symbol: str, target_tfs=['H1', 'H4', 'D1'], lookback_days=7):
        """
        Fetches M1 data for a symbol and resamples it into target timeframes.
        Upserts the results into market_data_resampled.
        """
        print(f"Resampling {symbol} from M1 into {target_tfs}...")
        
        # 1. Fetch M1 data
        query = """
            SELECT timestamp, open, high, low, close, tick_volume 
            FROM market_data 
            WHERE pair = %s AND timeframe = 'M1' 
            AND timestamp > %s
            ORDER BY timestamp
        """
        start_date = datetime.now() - pd.Timedelta(days=lookback_days)
        rows = self.db.execute_query(query, (symbol, start_date))
        
        if not rows:
            print(f"  No M1 data found for {symbol} in the last {lookback_days} days.")
            return

        df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume'])
        df.set_index('timestamp', inplace=True)
        
        # 2. Resample for each target timeframe
        for tf in target_tfs:
            resample_rule = self._get_resample_rule(tf)
            if not resample_rule:
                continue
                
            resampled = df.resample(resample_rule).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'tick_volume': 'sum'
            }).dropna()
            
            # 3. Upsert into DB
            self._upsert_resampled_data(symbol, tf, resampled)

    def _get_resample_rule(self, tf: str):
        mapping = {
            'M5': '5min',
            'M15': '15min',
            'M30': '30min',
            'H1': 'h',
            'H4': '4h',
            'D1': 'D'
        }
        return mapping.get(tf)

    def _upsert_resampled_data(self, symbol, timeframe, df):
        insert_query = """
            INSERT INTO market_data_resampled (pair, timeframe, timestamp, open, high, low, close, tick_volume)
            VALUES %s
            ON CONFLICT (pair, timeframe, timestamp) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                tick_volume = EXCLUDED.tick_volume
        """
        data_to_insert = []
        for ts, row in df.iterrows():
            data_to_insert.append((
                symbol, timeframe, ts, 
                float(row['open']), float(row['high']), 
                float(row['low']), float(row['close']), 
                int(row['tick_volume'])
            ))
            
        self.db.execute_batch(insert_query, data_to_insert)
        print(f"  OK: Upserted {len(data_to_insert)} bars for {timeframe}.")

if __name__ == "__main__":
    db = DBClient()
    resampler = DataResampler(db)
    # Test for XAUUSD
    resampler.resample_m1_to_higher("XAUUSD")
