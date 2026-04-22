from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from data.db_client import DBClient
from webapp.bus import bus

router = APIRouter()
db = DBClient()

@router.get("/logs")
async def get_recent_logs(limit: int = 100):
    """Fetch recent logs from the bot_health table."""
    query = """
        SELECT timestamp, event_type, status, message, meta_data 
        FROM bot_health 
        ORDER BY timestamp DESC 
        LIMIT %s
    """
    rows = db.execute_query(query, (limit,))
    logs = []
    if rows:
        for row in rows:
            logs.append({
                "timestamp": row[0].isoformat(),
                "event_type": row[1],
                "status": row[2],
                "message": row[3],
                "meta_data": row[4]
            })
    return logs

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """Stream real-time logs via WebSocket."""
    await websocket.accept()
    
    async def send_log(payload: dict):
        try:
            await websocket.send_json(payload)
        except Exception:
            # Socket likely closed, will be handled by disconnect
            pass

    bus.subscribe(send_log)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        bus.unsubscribe(send_log)
    except Exception as e:
        print(f"WebSocket error: {e}")
        bus.unsubscribe(send_log)
