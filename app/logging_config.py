"""Logging configuration for Quantum-N3BULA API."""

import logging
import sys
from datetime import datetime, timezone
from collections import deque
from typing import Deque

from pythonjsonlogger import jsonlogger

from app.config import settings


class LogEntry:
    """Represents a single log entry."""
    
    def __init__(self, level: str, message: str, timestamp: str, extra: dict | None = None):
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.extra = extra or {}
    
    def to_dict(self) -> dict:
        """Convert log entry to dictionary."""
        return {
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
            **self.extra
        }


class InMemoryLogHandler(logging.Handler):
    """Custom handler that stores log entries in memory."""
    
    def __init__(self, max_entries: int = 1000):
        super().__init__()
        self.log_entries: Deque[LogEntry] = deque(maxlen=max_entries)
    
    def emit(self, record: logging.LogRecord) -> None:
        """Store log record in memory."""
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        extra = {}
        
        # Capture extra fields from record
        for key in ['request_id', 'endpoint', 'command', 'duration_ms', 'status']:
            if hasattr(record, key):
                extra[key] = getattr(record, key)
        
        entry = LogEntry(
            level=record.levelname,
            message=record.getMessage(),
            timestamp=timestamp,
            extra=extra
        )
        self.log_entries.append(entry)
    
    def get_logs(self, limit: int | None = None, level: str | None = None) -> list[dict]:
        """Retrieve stored log entries."""
        entries = list(self.log_entries)
        
        if level:
            entries = [e for e in entries if e.level.upper() == level.upper()]
        
        if limit:
            entries = entries[-limit:]
        
        return [e.to_dict() for e in entries]
    
    def clear_logs(self) -> int:
        """Clear all stored logs. Returns count of cleared entries."""
        count = len(self.log_entries)
        self.log_entries.clear()
        return count


# Global in-memory log handler instance
log_handler = InMemoryLogHandler(max_entries=settings.max_log_entries)


def setup_logging() -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("quantum_n3bula")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    
    # Console handler with JSON format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)
    
    # In-memory handler for /logs endpoint
    log_handler.setFormatter(json_formatter)
    logger.addHandler(log_handler)
    
    return logger


# Initialize logger
logger = setup_logging()
