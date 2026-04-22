import asyncio
import json
import psycopg2
import select
from typing import List, Callable, Awaitable
from data.db_client import DBClient

class EventBus:
    """
    Listens to Postgres NOTIFY events on 'bot_events' channel and 
    distributes them to connected WebSocket clients.
    """
    def __init__(self):
        self.subscribers: List[Callable[[dict], Awaitable[None]]] = []
        self.db = DBClient()
        self._running = False

    def subscribe(self, callback: Callable[[dict], Awaitable[None]]):
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[dict], Awaitable[None]]):
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def _notify_subscribers(self, payload: dict):
        tasks = [callback(payload) for callback in self.subscribers]
        if tasks:
            await asyncio.gather(*tasks)

    async def start_listening(self):
        """Main loop that listens for NOTIFY events."""
        self._running = True
        conn = self.db.get_connection()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        try:
            with conn.cursor() as cur:
                cur.execute("LISTEN bot_events;")
            
            while self._running:
                if select.select([conn], [], [], 1.0) == ([], [], []):
                    # Timeout, check if still running
                    await asyncio.sleep(0.1)
                else:
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        try:
                            payload = json.loads(notify.payload)
                            await self._notify_subscribers(payload)
                        except Exception as e:
                            print(f"Error processing NOTIFY payload: {e}")
        except Exception as e:
            print(f"EventBus listening error: {e}")
        finally:
            self.db.release_connection(conn)

    def stop(self):
        self._running = False

# Global bus instance
bus = EventBus()
