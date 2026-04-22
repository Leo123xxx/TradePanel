import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

class MacroDataFeed:
    """
    Fetches macro indicators (DXY, VIX, 10Y Yields) to determine market regime.
    Uses Alpha Vantage for DXY, yfinance for VIX, and FRED for 10Y yields.
    """
    
    CACHE_FILE = "data/macro_cache.json"
    
    def __init__(self):
        load_dotenv()
        self.av_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.fred_key = os.getenv("FRED_API_KEY")
        
    def get_latest_data(self):
        """Returns the latest macro data, using cache if available and fresh (24h)."""
        cache = self._load_cache()
        if cache and self._is_fresh(cache['timestamp']):
            return cache['data']
            
        data = self._fetch_all()
        self._save_cache(data)
        return data
        
    def _fetch_all(self):
        """Fetches all metrics from APIs."""
        print("[MACRO] Fetching fresh macro data...")
        
        # 1. VIX (Yahoo Finance)
        vix = 0
        try:
            # ^VIX is the ticker
            vix_data = yf.download('^VIX', period='5d', progress=False)
            if not vix_data.empty:
                # Use .iloc[-1] and flatten if it's a multi-index
                close_col = vix_data['Close']
                if isinstance(close_col, pd.DataFrame):
                    # Multi-index or multi-symbol case
                    vix = float(close_col.iloc[-1, 0])
                else:
                    vix = float(close_col.iloc[-1])
        except Exception as e:
            print(f"[MACRO] VIX fetch error: {e}")
            
        # 2. DXY (Dollar Index - using yfinance instead of Alpha Vantage)
        dxy = 0
        dxy_50ma = 0
        try:
            # DX-Y.NYB is the ticker on Yahoo Finance
            dxy_data = yf.download('DX-Y.NYB', period='100d', progress=False)
            if not dxy_data.empty:
                close_col = dxy_data['Close']
                if isinstance(close_col, pd.DataFrame):
                    dxy = float(close_col.iloc[-1, 0])
                    dxy_50ma = float(close_col.iloc[-50:, 0].mean())
                else:
                    dxy = float(close_col.iloc[-1])
                    dxy_50ma = float(close_col.iloc[-50:].mean())
        except Exception as e:
            print(f"[MACRO] DXY fetch error: {e}")
            
        # 3. 10Y Real Yields (FRED)
        yields = 0
        yields_prev = 0
        try:
            # DFII10 is 10-Year Real Treasury Rate
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DFII10&api_key={self.fred_key}&file_type=json&sort_order=desc&limit=2"
            res = requests.get(url).json()
            if "observations" in res:
                # Observations might be '.' for non-trading days
                obs = [o for o in res["observations"] if o["value"] != "."]
                if len(obs) >= 2:
                    yields = float(obs[0]["value"])
                    yields_prev = float(obs[1]["value"])
                elif len(obs) == 1:
                    yields = float(obs[0]["value"])
        except Exception as e:
            print(f"[MACRO] Yields fetch error: {e}")
            
        return {
            'vix': vix,
            'dxy': dxy,
            'dxy_50ma': dxy_50ma,
            'yields': yields,
            'yields_prev': yields_prev,
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def _load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
        
    def _save_cache(self, data):
        cache = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(self.CACHE_FILE, 'w') as f:
            json.dump(cache, f)
            
    def _is_fresh(self, timestamp_iso):
        ts = datetime.fromisoformat(timestamp_iso)
        return datetime.now() - ts < timedelta(hours=24)

if __name__ == "__main__":
    feed = MacroDataFeed()
    print(feed.get_latest_data())
