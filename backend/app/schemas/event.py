"""Event schemas for API requests/responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Schema for creating a new event."""

    event_type: str
    payload: dict[str, Any] | None = None
    source: str | None = None
    task_id: int | None = None
    agent_id: int | None = None


class EventResponse(BaseModel):
    """Schema for event response."""

    id: int
    event_type: str
    payload: dict[str, Any] | None = None
    source: str | None = None
    task_id: int | None = None
    agent_id: int | None = None
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
