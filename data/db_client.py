import os
import sys
import time
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import pool
from dotenv import load_dotenv
from typing import List, Optional

class DBClient:
    """
    PostgreSQL client with proper connection lifecycle management.
    Every method opens a connection, executes, commits/rolls back, and closes.
    Uses a ThreadedConnectionPool to handle concurrent threads safely.
    get_connection() retries with exponential backoff on pool exhaustion.
    """
    _pool: Optional[pool.ThreadedConnectionPool] = None
    _instance: Optional['DBClient'] = None

    def __new__(cls):
        """Implement singleton pattern to ensure one pool per process."""
        if cls._instance is None:
            cls._instance = super(DBClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        load_dotenv()
        self.conn_params = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "trading_platform"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres"),
            "connect_timeout": 5
        }
        self._initialized = True
        # Pool is created lazily on first use — do NOT connect here.

    def _ensure_pool(self):
        """Create the connection pool on first use (lazy init)."""
        if DBClient._pool is None:
            mode = os.getenv("RUNNING_MODE", "DEFAULT")
            if mode == "LIVE":
                maxconn = 50
                minconn = 5
            elif mode == "BACKTEST":
                maxconn = 10
                minconn = 2
            else:
                maxconn = 20
                minconn = 5

            try:
                dsn = (
                    f"host={self.conn_params['host']} "
                    f"port={self.conn_params['port']} "
                    f"dbname={self.conn_params['database']} "
                    f"user={self.conn_params['user']} "
                    f"password={self.conn_params['password']} "
                    f"options='-c client_min_messages=error'"
                )
                DBClient._pool = pool.ThreadedConnectionPool(
                    minconn=minconn,
                    maxconn=maxconn,
                    dsn=dsn
                )
            except Exception as e:
                print(f"[DBClient] CRITICAL: Failed to create connection pool: {e}")
                raise

    def get_connection(self, retries: int = 3, base_delay: float = 2.0):
        """
        Gets a connection from the pool with exponential backoff retry.
        """
        self._ensure_pool()
        last_exc = None
        for attempt in range(retries):
            try:
                return DBClient._pool.getconn()
            except pool.PoolError as e:
                last_exc = e
                if attempt < retries - 1:
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        raise pool.PoolError(
            f"DB pool exhausted after {retries} attempts: {last_exc}"
        )

    def release_connection(self, conn):
        """Returns a connection to the pool."""
        if DBClient._pool is not None and conn is not None:
            DBClient._pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None):
        """
        Executes a query. Returns rows for SELECT, None for INSERT/UPDATE/DELETE.
        """
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall() if cur.description else None
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.release_connection(conn)

    def insert_market_data(self, data: List[tuple]):
        """Bulk inserts OHLCV rows into market_data."""
        q = (
            "INSERT INTO market_data "
            "(pair, timeframe, timestamp, open, high, low, close, tick_volume, spread) "
            "VALUES %s "
            "ON CONFLICT (pair, timeframe, timestamp) DO NOTHING"
        )
        self.execute_batch(q, data)

    def execute_batch(self, query: str, data: List[tuple], page_size: int = 1000):
        """Executes a bulk batch query using execute_values."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                execute_values(cur, query, data, page_size=page_size)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.release_connection(conn)

    def close_all(self):
        """Closes all connections in the pool."""
        if DBClient._pool is not None:
            DBClient._pool.closeall()
            DBClient._pool = None

    def refresh_materialized_view(self, view_name: str = "mv_daily_metrics"):
        """Refreshes a materialized view concurrently."""
        try:
            self.execute_query(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view_name}")
        except Exception:
            self.execute_query(f"REFRESH MATERIALIZED VIEW {view_name}")

if __name__ == "__main__":
    db = DBClient()
    res = db.execute_query("SELECT version();")
    print(f"PostgreSQL Version: {res[0][0]}")
