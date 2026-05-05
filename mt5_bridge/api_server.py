import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn
import MetaTrader5 as mt5
from pydantic import BaseModel
import pandas as pd
from mt5_bridge.connector import MT5Connector

connector = MT5Connector()

class OrderRequest(BaseModel):
    symbol: str
    order_type: int
    volume: float
    price: float = None
    sl: float = None
    tp: float = None
    magic: int = 123456
    comment: str = "MT5_Bridge"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not connector.connect():
        print("WARNING: MT5 Bridge failed to connect to MT5 terminal on startup.")
    yield
    # Shutdown
    connector.disconnect(shutdown=True)

app = FastAPI(title="MT5 Bridge API", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok", "mt5_connected": connector.connected}

@app.get("/account")
def get_account_info():
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    info = mt5.account_info()
    if info is None:
        raise HTTPException(status_code=500, detail="Failed to get account info")
    return info._asdict()

@app.get("/tick/{symbol}")
def get_tick(symbol: str):
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise HTTPException(status_code=404, detail="Tick not found")
    return tick._asdict()

@app.get("/rates/{symbol}/{tf}")
def get_rates(symbol: str, tf: str, n: int = 100):
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    tf_mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    
    if tf not in tf_mapping:
        raise HTTPException(status_code=400, detail="Invalid timeframe")
        
    rates = mt5.copy_rates_from_pos(symbol, tf_mapping[tf], 0, n)
    if rates is None:
        raise HTTPException(status_code=404, detail="Rates not found")
        
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df.to_dict(orient="records")

@app.post("/order")
def place_order(order: OrderRequest):
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
        
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.symbol,
        "volume": order.volume,
        "type": order.order_type,
        "magic": order.magic,
        "comment": order.comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    if order.price:
        request["price"] = order.price
    else:
        tick = mt5.symbol_info_tick(order.symbol)
        if order.order_type == mt5.ORDER_TYPE_BUY:
            request["price"] = tick.ask
        elif order.order_type == mt5.ORDER_TYPE_SELL:
            request["price"] = tick.bid
            
    if order.sl:
        request["sl"] = order.sl
    if order.tp:
        request["tp"] = order.tp
        
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise HTTPException(status_code=500, detail=f"Order failed: {result.retcode}")
        
    return result._asdict()

@app.get("/positions")
def get_positions(symbol: str = None):
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
        
    if symbol:
        positions = mt5.positions_get(symbol=symbol)
    else:
        positions = mt5.positions_get()
        
    if positions is None:
        return []
        
    return [pos._asdict() for pos in positions]

@app.get("/history/{ticket}")
def get_history(ticket: int):
    if not connector.connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
        
    deals = mt5.history_deals_get(ticket=ticket)
    if deals is None:
        return []
        
    return [deal._asdict() for deal in deals]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
