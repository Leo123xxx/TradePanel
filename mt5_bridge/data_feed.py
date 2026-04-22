import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from data.db_client import DBClient
from typing import Optional

# Timeframe integer → string mapping (MT5 constants → DB labels)
TF_MAP = {
    mt5.TIMEFRAME_M1:   'M1',
    mt5.TIMEFRAME_M5:   'M5',
    mt5.TIMEFRAME_M15:  'M15',
    mt5.TIMEFRAME_H1:   'H1',
    mt5.TIMEFRAME_H2:   'H2',
    mt5.TIMEFRAME_H4:   'H4',
    mt5.TIMEFRAME_H6:   'H6',
    mt5.TIMEFRAME_H12:  'H12',
    mt5.TIMEFRAME_D1:   'D1',
}

# Default historical start date for all pairs.
# Change this to pull more/less history.
DEFAULT_START_DATE = datetime(2020, 1, 1)


class MT5DataFeed:
    """
    Pulls OHLCV data from the connected MT5 terminal and stores it
    in the market_data PostgreSQL table.

    Two modes:
      pull_historical_data()  — date-range pull (for initial ingest / backfill)
      pull_latest_bars()      — last N bars (for live updates / incremental sync)
    """

    def __init__(self):
        self.db = DBClient()

    # ------------------------------------------------------------------
    # PRIMARY METHOD: Date-range historical pull
    # Use this for initial ingest. Pulls all bars between start and end.
    # ------------------------------------------------------------------
    def pull_historical_data(
        self,
        symbol: str,
        timeframe: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """
        Pulls OHLCV bars between start_date and end_date from MT5
        and stores them in the market_data table. 
        Uses a robust chunked approach to avoid Terminal: 'Invalid params' errors.
        """
        if start_date is None:
            start_date = DEFAULT_START_DATE
        if end_date is None:
            end_date = datetime.now()

        tf_str = TF_MAP.get(timeframe, str(timeframe))
        print(f"Pulling {symbol} {tf_str} history towards {start_date.date()}...")

        total_inserted = 0
        current_end = end_date
        chunk_size = 99999 # Safe large chunk

        while current_end > start_date:
            rates = mt5.copy_rates_from(symbol, timeframe, current_end, chunk_size)
            
            if rates is None or len(rates) == 0:
                # If chunk fails, maybe we reached the end of history
                break
                
            # Filter rates that are before our target start_date
            valid_rates = [r for r in rates if datetime.fromtimestamp(r['time']) >= start_date and datetime.fromtimestamp(r['time']) < current_end]
            
            if not valid_rates:
                break
                
            data_to_insert = [
                (
                    symbol,
                    tf_str,
                    datetime.fromtimestamp(rate['time']),
                    float(rate['open']),
                    float(rate['high']),
                    float(rate['low']),
                    float(rate['close']),
                    int(rate['tick_volume']),
                    int(rate['spread'])
                )
                for rate in valid_rates
            ]

            self.db.insert_market_data(data_to_insert)
            total_inserted += len(data_to_insert)
            
            # Move our end marker to the earliest bar we just got
            new_end = datetime.fromtimestamp(rates[0]['time'])
            if new_end >= current_end: # Prevent infinite loop
                break
            current_end = new_end
            
            if len(rates) < chunk_size: # We got everything available from the broker
                break

        print(f"  OK: {total_inserted:,} total bars stored for {symbol} {tf_str}.")
        return total_inserted

    # ------------------------------------------------------------------
    # INCREMENTAL METHOD: Last N bars (live sync / scheduler top-up)
    # ------------------------------------------------------------------
    def pull_latest_bars(self, symbol: str, timeframe: int, count: int = 500) -> int:
        """
        Pulls the most recent `count` bars. Used by the daily data ingest
        scheduler job to top up the DB without a full re-pull.

        Args:
            symbol:    e.g. "EURUSD"
            timeframe: MT5 constant
            count:     Number of recent bars to pull

        Returns:
            Number of rows inserted (duplicates silently skipped by DB).
        """
        tf_str = TF_MAP.get(timeframe, str(timeframe))
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

        if rates is None or len(rates) == 0:
            print(f"  WARNING: No data for {symbol} {tf_str}. Error: {mt5.last_error()}")
            return 0

        data_to_insert = [
            (
                symbol,
                tf_str,
                datetime.fromtimestamp(rate['time']),
                float(rate['open']),
                float(rate['high']),
                float(rate['low']),
                float(rate['close']),
                int(rate['tick_volume']),
                int(rate['spread'])
            )
            for rate in rates
        ]

        self.db.insert_market_data(data_to_insert)
        return len(data_to_insert)

    # ------------------------------------------------------------------
    # CONVENIENCE: Check how much data exists in DB for a pair/timeframe
    # ------------------------------------------------------------------
    def get_data_range(self, symbol: str, timeframe_str: str) -> dict:
        """
        Returns the earliest and latest timestamp stored in the DB
        for a given pair and timeframe string (e.g. 'M1').
        """
        query = """
            SELECT MIN(timestamp), MAX(timestamp), COUNT(*)
            FROM market_data
            WHERE pair = %s AND timeframe = %s
        """
        result = self.db.execute_query(query, (symbol, timeframe_str))
        if result and result[0][0]:
            return {
                "pair": symbol,
                "timeframe": timeframe_str,
                "earliest": result[0][0],
                "latest": result[0][1],
                "total_bars": result[0][2]
            }
        return {"pair": symbol, "timeframe": timeframe_str, "total_bars": 0}


# ------------------------------------------------------------------
# Run directly to perform a quick data check or manual backfill
# ------------------------------------------------------------------
if __name__ == "__main__":
    from mt5_bridge.connector import MT5Connector

    conn = MT5Connector()
    if conn.connect():
        feed = MT5DataFeed()

        # Check existing data
        for pair in ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]:
            info = feed.get_data_range(pair, "M1")
            bars = info.get("total_bars", 0)
            if bars > 0:
                print(f"{pair} M1: {bars:,} bars  ({info['earliest'].date()} → {info['latest'].date()})")
            else:
                print(f"{pair} M1: No data in DB yet — run ingestion.py to backfill.")

        conn.disconnect()
