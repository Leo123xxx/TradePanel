import logging
import json
import sys
from datetime import datetime
from pathlib import Path

class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings for Loki ingestion.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "service": getattr(record, "service", "tradepanel"),
            "module": record.module,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if they exist
        if hasattr(record, "metrics"):
            log_record["metrics"] = record.metrics
            
        return json.dumps(log_record)

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    Setup a logger with dual handlers:
    1. Console (Human readable)
    2. JSON File (For Loki ingestion)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 2. JSON File Handler
    if log_file:
        log_path = Path("logs") / log_file
        log_path.parent.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        json_formatter = JsonFormatter(datefmt='%Y-%m-%dT%H:%M:%SZ')
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

    return logger

# Example usage:
# logger = setup_logger("backtest", "backtest.json.log")
# logger.info("Backtest started", extra={"metrics": {"pairs": 5}})
