import sys
import os
import types
import requests
import pandas as pd

class MT5MockModule(types.ModuleType):
    POSITION_TYPE_BUY = 0
    POSITION_TYPE_SELL = 1
    TRADE_RETCODE_DONE = 10009
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    ORDER_TIME_GTC = 0
    ORDER_FILLING_IOC = 1
    TRADE_ACTION_DEAL = 1
    
    TIMEFRAME_M1  = 1
    TIMEFRAME_M5  = 5
    TIMEFRAME_M15 = 15
    TIMEFRAME_M30 = 30
    TIMEFRAME_H1  = 16385
    TIMEFRAME_H2  = 16386
    TIMEFRAME_H4  = 16388
    TIMEFRAME_H6  = 16390
    TIMEFRAME_H8  = 16392
    TIMEFRAME_H12 = 16396
    TIMEFRAME_D1  = 16408
    TIMEFRAME_W1  = 32769
    TIMEFRAME_MN1 = 49153

    def __init__(self, name):
        super().__init__(name)
        self.base_url = os.getenv("MT5_BRIDGE_URL", "http://host.docker.internal:8001")

    def initialize(self, *args, **kwargs):
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            return r.status_code == 200
        except:
            return False

    def login(self, *args, **kwargs):
        return True

    def terminal_info(self):
        class Info:
            connected = True
        return Info()

    def account_info(self):
        try:
            r = requests.get(f"{self.base_url}/account", timeout=5)
            if r.status_code == 200:
                class Info:
                    def __init__(self, d):
                        self._data = d
                        for k, v in d.items():
                            setattr(self, k, v)
                    def _asdict(self):
                        return self._data
                return Info(r.json())
        except:
            pass
        return None

    def symbol_select(self, symbol, enable=True):
        return True

    def symbol_info(self, symbol):
        try:
            r = requests.get(f"{self.base_url}/tick/{symbol}", timeout=5)
            if r.status_code == 200:
                d = r.json()
                class Info:
                    def __init__(self, d):
                        self._data = d
                        self.ask = d.get("ask", 0)
                        self.bid = d.get("bid", 0)
                        self.digits = 5 if "JPY" not in symbol else 3
                        self.point = 0.00001 if "JPY" not in symbol else 0.001
                        self.trade_mode = 4  # mt5.SYMBOL_TRADE_MODE_FULL
                        self.trade_calc_mode = 0  # forex
                        self.spread = d.get("spread", 10)
                        self.trade_tick_value = d.get("trade_tick_value", 1.0)
                        self.trade_tick_size = d.get("trade_tick_size", self.point)
                        self.trade_contract_size = d.get("trade_contract_size", 100000)
                        self.margin_initial = d.get("margin_initial", 0.0)
                        self.visible = True
                        self.volume_min = 0.01
                        self.volume_max = 100.0
                        self.volume_step = 0.01
                    def _asdict(self):
                        return self._data
                return Info(d)
        except:
            pass
        return None

    def symbol_info_tick(self, symbol):
        return self.symbol_info(symbol)

    def positions_get(self, symbol=None):
        try:
            url = f"{self.base_url}/positions"
            if symbol:
                url += f"?symbol={symbol}"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                class Pos:
                    def __init__(self, d):
                        self._data = d
                        for k, v in d.items():
                            setattr(self, k, v)
                    def _asdict(self):
                        return self._data
                return [Pos(d) for d in r.json()]
        except:
            pass
        return None

    def history_deals_get(self, ticket=None, **kwargs):
        try:
            url = f"{self.base_url}/history/{ticket}"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                class Deal:
                    def __init__(self, d):
                        self._data = d
                        for k, v in d.items():
                            setattr(self, k, v)
                    def _asdict(self):
                        return self._data
                return [Deal(d) for d in r.json()]
        except:
            pass
        return None

    def copy_rates_from_pos(self, symbol, tf, start, count):
        tf_map = {1: "M1", 5: "M5", 15: "M15", 30: "M30", 16385: "H1",
                  16386: "H2", 16388: "H4", 16390: "H6", 16392: "H8", 16396: "H12", 16408: "D1", 32769: "W1", 49153: "MN1"}
        tf_str = tf_map.get(tf, "H1")
        try:
            r = requests.get(f"{self.base_url}/rates/{symbol}/{tf_str}?n={count}", timeout=10)
            if r.status_code == 200:
                return r.json()
        except:
            pass
        return None

    def copy_rates_from(self, symbol, tf, date_from, count):
        """Date-from variant — fetches latest bars from bridge and filters by date."""
        import sys as _sys
        # The bridge only supports 'last N bars'. Fetch a large window and filter.
        data = self.copy_rates_from_pos(symbol, tf, 0, min(count, 5000))
        if data is None:
            return None
        if date_from is None:
            return data
        # Filter to bars on-or-after date_from
        from datetime import datetime as _dt
        filtered = []
        for row in data:
            t = row.get("time")
            if t is None:
                continue
            try:
                bar_dt = _dt.fromisoformat(str(t)) if isinstance(t, str) else _dt.fromtimestamp(t)
                if bar_dt >= date_from:
                    filtered.append(row)
            except Exception:
                filtered.append(row)
        return filtered if filtered else data  # Fall back to unfiltered if nothing matches

    def order_calc_margin(self, action, symbol, volume, price):
        # Dummy calculation
        return volume * 1000

    def order_send(self, request):
        try:
            payload = {
                "symbol": request.get("symbol"),
                "order_type": request.get("type"),
                "volume": request.get("volume"),
                "price": request.get("price"),
                "sl": request.get("sl"),
                "tp": request.get("tp"),
                "magic": request.get("magic", 123456),
                "comment": request.get("comment", "Docker")
            }
            r = requests.post(f"{self.base_url}/order", json=payload, timeout=10)
            if r.status_code == 200:
                d = r.json()
                class OrderResult:
                    def __init__(self, d, req_price):
                        self._data = d
                        self.retcode = d.get("retcode", 10009)
                        self.price = d.get("price", req_price)
                        self.order = d.get("order", 0)
                    def _asdict(self):
                        return self._data
                return OrderResult(d, request.get("price"))
            else:
                class OrderResultFail:
                    def __init__(self, retcode):
                        self.retcode = retcode
                        self.price = 0
                        self.order = 0
                    def _asdict(self):
                        return {"retcode": self.retcode, "price": 0, "order": 0}
                return OrderResultFail(10013) # Invalid request
        except:
            class OrderResultFail:
                def __init__(self, retcode):
                    self.retcode = retcode
                    self.price = 0
                    self.order = 0
                def _asdict(self):
                    return {"retcode": self.retcode, "price": 0, "order": 0}
            return OrderResultFail(10027) # Timeout

    def shutdown(self):
        """No-op: bridge stays alive on the Windows host."""
        return True

    def last_error(self):
        return (0, "No error (Docker mock)")

    def copy_rates_range(self, symbol, tf, date_from, date_to):
        return self.copy_rates_from_pos(symbol, tf, 0, 500)

    def history_orders_get(self, **kwargs):
        return []

    def orders_get(self, **kwargs):
        return []

def setup_mock():
    try:
        import MetaTrader5
    except ImportError:
        mock = MT5MockModule("MetaTrader5")
        sys.modules["MetaTrader5"] = mock
