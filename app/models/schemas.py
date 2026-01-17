"""Pydantic models for Quantum-N3BULA API requests and responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    """Response model for the /ping endpoint."""
    
    message: str = "pong"
    timestamp: str


class SystemStatus(BaseModel):
    """System status information."""
    
    status: str = Field(description="Current system status (healthy, degraded, unhealthy)")
    uptime_seconds: float = Field(description="Time since service started in seconds")
    version: str = Field(description="API version")
    python_version: str = Field(description="Python runtime version")


class StatusResponse(BaseModel):
    """Response model for the /status endpoint."""
    
    app_name: str
    system: SystemStatus
    timestamp: str


class ExecuteRequest(BaseModel):
    """Request model for command execution."""
    
    command: str = Field(
        min_length=1,
        max_length=1000,
        description="Command to execute (simulated)"
    )
    parameters: dict[str, Any] | None = Field(
        default=None,
        description="Optional parameters for the command"
    )


class ExecuteResponse(BaseModel):
    """Response model for command execution."""
    
    command: str
    status: str = Field(description="Execution status (success, error)")
    result: Any = Field(description="Command execution result")
    execution_time_ms: float = Field(description="Execution time in milliseconds")
    timestamp: str


class LogEntry(BaseModel):
    """Model for a single log entry."""
    
    level: str
    message: str
    timestamp: str


class LogsResponse(BaseModel):
    """Response model for the /logs endpoint."""
    
    total_entries: int
    entries: list[dict]
    timestamp: str


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str
    detail: str | None = None
    timestamp: str
