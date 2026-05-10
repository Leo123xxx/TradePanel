import queue
import threading
import logging
from typing import Callable, Any, Dict, List

logger = logging.getLogger("EventBus")

class EventBus:
    """
    Task 3.3: In-Memory EventBus (Pub/Sub)
    Simple singleton to decouple modules. 
    Allows modules to subscribe to events like 'SIGNAL_FIRED' or 'HEALTH_ERROR'
    without direct dependency on the triggering module.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._subscribers: Dict[str, List[Callable]] = {}
                cls._instance._queue = queue.Queue()
                cls._instance._running = False
        return cls._instance

    def subscribe(self, event_type: str, callback: Callable):
        """Registers a callback for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}")

    def publish(self, event_type: str, data: Any = None):
        """Adds an event to the processing queue."""
        self._queue.put((event_type, data))
        if not self._running:
            self._start_processor()

    def _start_processor(self):
        """Starts the background thread that processes events."""
        self._running = True
        thread = threading.Thread(target=self._process_events, daemon=True, name="EventBusProcessor")
        thread.start()

    def _process_events(self):
        """Main loop that executes callbacks for events in the queue."""
        while True:
            try:
                event_type, data = self._queue.get()
                if event_type in self._subscribers:
                    for callback in self._subscribers[event_type]:
                        try:
                            callback(data)
                        except Exception as e:
                            logger.error(f"Error in EventBus callback for {event_type}: {e}")
                self._queue.task_done()
            except Exception as e:
                logger.error(f"EventBus processor error: {e}")

# Singleton instance
bus = EventBus()
