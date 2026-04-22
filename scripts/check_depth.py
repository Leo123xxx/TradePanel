import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

def check_m1_data_depth(symbol="XAUUSD"):
    if not mt5.initialize():
        print(f"MT5 initialize failed, error code: {mt5.last_error()}")
        return

    print(f"--- M1 Data Depth Check for {symbol} ---")
    
    # Check current time
    now = datetime.now()
    
    # Request historical data for 10 years
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, now, 5256000) # ~10 years in minutes
    
    if rates is None or len(rates) == 0:
        print(f"ERROR: Could not retrieve M1 data for {symbol}")
    else:
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        start_date = df['time'].min()
        end_date = df['time'].max()
        count = len(df)
        
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Total M1 Bars retrieved: {count}")
        
        years = (end_date - start_date).days / 365.25
        print(f"Available Depth: {years:.2f} years")
        
        if years >= 5:
            print("SUCCESS: Data depth is >= 5 years.")
        else:
            print(f"WARNING: Data depth is only {years:.2f} years. Recommended is 5+.")

    mt5.shutdown()

if __name__ == "__main__":
    check_m1_data_depth("XAUUSD")
