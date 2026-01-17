"""API routes for health and system endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.config import settings
from app.logging_config import logger, log_handler
from app.models.schemas import (
    PingResponse,
    StatusResponse,
    SystemStatus,
    ExecuteRequest,
    ExecuteResponse,
    LogsResponse,
)
from app.services.system_service import get_system_status, execute_command


router = APIRouter()


@router.get("/ping", response_model=PingResponse, tags=["Health"])
async def ping() -> PingResponse:
    """
    Simple health check endpoint.
    
    Returns a pong response to verify the service is running.
    """
    logger.debug("Ping endpoint called", extra={"endpoint": "/ping"})
    
    return PingResponse(
        message="pong",
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get("/status", response_model=StatusResponse, tags=["Health"])
async def status() -> StatusResponse:
    """
    Detailed system status endpoint.
    
    Returns comprehensive information about the system health,
    including uptime, version, and Python runtime details.
    """
    system_status = await get_system_status()
    
    return StatusResponse(
        app_name=settings.app_name,
        system=SystemStatus(**system_status),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.post("/execute", response_model=ExecuteResponse, tags=["Commands"])
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """
    Execute a command (simulated).
    
    Accepts a command with optional parameters and returns the execution result.
    This is a simulated execution for demonstration purposes.
    
    Supported commands:
    - echo: Returns the message parameter
    - time: Returns current UTC time
    - info: Returns system information
    - calculate: Performs basic math on the expression parameter
    """
    result = await execute_command(request.command, request.parameters)
    
    return ExecuteResponse(
        command=result["command"],
        status=result["status"],
        result=result["result"],
        execution_time_ms=result["execution_time_ms"],
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get("/logs", response_model=LogsResponse, tags=["Monitoring"])
async def get_logs(
    limit: int | None = Query(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of log entries to return"
    ),
    level: str | None = Query(
        default=None,
        description="Filter logs by level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
) -> LogsResponse:
    """
    Retrieve application logs.
    
    Returns recent log entries from the in-memory log store.
    Supports filtering by log level and limiting the number of entries.
    """
    logger.info(
        "Logs endpoint accessed",
        extra={"endpoint": "/logs", "limit": limit, "level": level}
    )
    
    entries = log_handler.get_logs(limit=limit, level=level)
    
    return LogsResponse(
        total_entries=len(entries),
        entries=entries,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.delete("/logs", tags=["Monitoring"])
async def clear_logs() -> dict:
    """
    Clear all stored logs.
    
    Returns the count of cleared log entries.
    """
    count = log_handler.clear_logs()
    
    logger.info(f"Cleared {count} log entries", extra={"endpoint": "/logs"})
    
    return {
        "message": f"Cleared {count} log entries",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
