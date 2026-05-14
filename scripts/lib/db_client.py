import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from .logger import setup_logger

load_dotenv()

class DatabaseClient:
    def __init__(self, service_name="db_client"):
        self.logger = setup_logger(service_name, f"{service_name}.json.log")
        self.conn_params = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "trading_platform"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres")
        }
        self.conn = None

    def connect(self):
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
                self.conn.autocommit = False # Manual commit for batching
                self.logger.info("Database connected")
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            raise

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
                return cur.fetchall() if cur.description else None
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Query failed: {query}. Error: {e}")
            raise

    def batch_insert(self, query, data_list, page_size=1000):
        """
        Efficiently insert multiple rows using execute_values.
        """
        self.connect()
        try:
            with self.conn.cursor() as cur:
                execute_values(cur, query, data_list, page_size=page_size)
                self.conn.commit()
                self.logger.info(f"Batch insert successful: {len(data_list)} rows")
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Batch insert failed. Error: {e}")
            raise

    def upsert_market_data(self, data_list):
        """
        Specific helper for market_data upserts.
        """
        query = """
            INSERT INTO market_data (pair, timeframe, timestamp, open, high, low, close, tick_volume, spread)
            VALUES %s
            ON CONFLICT (pair, timeframe, timestamp) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                tick_volume = EXCLUDED.tick_volume,
                spread = EXCLUDED.spread
        """
        self.batch_insert(query, data_list)

# Example usage:
# db = DatabaseClient("backtest")
# db.batch_insert("INSERT INTO trades (trade_id, pair, ...) VALUES %s", trades_data)
