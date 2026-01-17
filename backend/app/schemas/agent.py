"""Agent schemas for API requests/responses."""

from datetime import datetime

from pydantic import BaseModel


class AgentCreate(BaseModel):
    """Schema for creating a new agent."""

    name: str
    description: str | None = None


class AgentResponse(BaseModel):
    """Schema for agent response."""

    id: int
    name: str
    description: str | None = None
    status: str
    is_active: bool
    last_heartbeat: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
