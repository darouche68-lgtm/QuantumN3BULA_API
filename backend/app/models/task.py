"""Task model for execution tracking."""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Task status enum."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(Base):
    """Task model for execution tracking."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    command = Column(Text, nullable=False)
    status = Column(String(20), default=TaskStatus.PENDING.value)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    agent_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
