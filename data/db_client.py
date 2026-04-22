import os
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import pool
from dotenv import load_dotenv
from typing import List, Optional

class DBClient:
    """
    PostgreSQL client with proper connection lifecycle management.
    Every method opens a connection, executes, commits/rolls back, and closes.
    Uses a SimpleConnectionPool to avoid exhausting Postgres connection limits.
    """
    _pool: Optional[pool.SimpleConnectionPool] = None

    def __init__(self):
        load_dotenv()
        self.conn_params = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "trading_platform"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres")
        }
        if DBClient._pool is None:
            DBClient._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                **self.conn_params
            )

    def get_connection(self):
        """Gets a connection from the pool."""
        return DBClient._pool.getconn()

    def release_connection(self, conn):
        """Returns a connection to the pool."""
        DBClient._pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None):
        """
        Executes a query. Returns rows for SELECT, None for INSERT/UPDATE/DELETE.
        Always releases the connection back to the pool.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall() if cur.description else None
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.release_connection(conn)

    def insert_market_data(self, data: List[tuple]):
        """
        Bulk inserts OHLCV rows into market_data.
        Uses ON CONFLICT DO NOTHING so re-runs are safe.
        """
        query = """
            INSERT INTO market_data (pair, timeframe, timestamp, open, high, low, close, tick_volume, spread)
            VALUES %s
            ON CONFLICT (pair, timeframe, timestamp) DO NOTHING
        """
        self.execute_batch(query, data)

    def execute_batch(self, query: str, data: List[tuple]):
        """
        Executes a bulk batch query using execute_values.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                execute_values(cur, query, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.release_connection(conn)

if __name__ == "__main__":
    db = DBClient()
    res = db.execute_query("SELECT version();")
    print(f"PostgreSQL Version: {res[0][0]}")
