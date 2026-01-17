"""
Quantum-N3BULA API - A FastAPI-based microservice
"""

from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi import status as http_status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application metadata
APP_NAME = "Quantum-N3BULA API"
VERSION = "1.0.0"
DESCRIPTION = "A FastAPI-based microservice for quantum operations"

# In-memory log storage
log_storage: List[dict] = []
MAX_LOGS = 1000


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    add_log("INFO", f"{APP_NAME} v{VERSION} started successfully")
    logger.info(f"{APP_NAME} v{VERSION} is starting up...")
    yield
    # Shutdown
    add_log("INFO", f"{APP_NAME} is shutting down")
    logger.info(f"{APP_NAME} is shutting down...")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


class ExecuteRequest(BaseModel):
    """Request model for execute endpoint"""
    command: str = Field(..., description="Command to execute")
    parameters: Optional[dict] = Field(default={}, description="Command parameters")


class ExecuteResponse(BaseModel):
    """Response model for execute endpoint"""
    task_id: str
    status: str
    result: Optional[str] = None
    timestamp: str


class LogEntry(BaseModel):
    """Model for log entries"""
    timestamp: str
    level: str
    message: str
    endpoint: Optional[str] = None


def add_log(level: str, message: str, endpoint: Optional[str] = None):
    """Add a log entry to the in-memory storage"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        "endpoint": endpoint
    }
    log_storage.append(log_entry)
    
    # Keep only the last MAX_LOGS entries
    if len(log_storage) > MAX_LOGS:
        log_storage.pop(0)
    
    # Also log to the logger
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[{endpoint}] {message}" if endpoint else message)


@app.get("/ping", tags=["Health"])
async def ping():
    """
    Simple ping endpoint to check if the service is alive
    
    Returns:
        dict: A simple pong response
    """
    add_log("INFO", "Ping endpoint called", "/ping")
    return {"message": "pong", "timestamp": datetime.utcnow().isoformat()}


@app.get("/status", tags=["Health"])
async def status():
    """
    Get the current status of the service
    
    Returns:
        dict: Service status information including uptime, version, and health
    """
    add_log("INFO", "Status endpoint called", "/status")
    
    return {
        "service": APP_NAME,
        "version": VERSION,
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "total_logs": len(log_storage)
    }


@app.post("/execute", response_model=ExecuteResponse, tags=["Operations"])
async def execute(request: ExecuteRequest):
    """
    Execute a quantum operation command
    
    Args:
        request: ExecuteRequest containing command and parameters
    
    Returns:
        ExecuteResponse: Execution result with task ID and status
    
    Raises:
        HTTPException: If command execution fails
    """
    try:
        add_log("INFO", f"Execute endpoint called with command: {request.command}", "/execute")
        
        # Validate command
        if not request.command or not request.command.strip():
            add_log("ERROR", "Empty command provided", "/execute")
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Command cannot be empty"
            )
        
        # Generate task ID based on timestamp
        task_id = f"task_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        # Simulate command execution
        # In a real implementation, this would execute actual quantum operations
        result_message = f"Command '{request.command}' executed successfully with parameters: {request.parameters}"
        
        add_log("INFO", f"Task {task_id} completed successfully", "/execute")
        
        return ExecuteResponse(
            task_id=task_id,
            status="completed",
            result=result_message,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        add_log("ERROR", error_msg, "/execute")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )


@app.get("/logs", tags=["Monitoring"])
async def get_logs(
    limit: int = 100,
    level: Optional[str] = None,
    endpoint: Optional[str] = None
):
    """
    Retrieve application logs
    
    Args:
        limit: Maximum number of logs to return (default: 100, max: 1000)
        level: Filter logs by level (INFO, WARNING, ERROR)
        endpoint: Filter logs by endpoint
    
    Returns:
        dict: List of log entries and metadata
    """
    add_log("INFO", f"Logs endpoint called with limit={limit}, level={level}, endpoint={endpoint}", "/logs")
    
    # Validate limit
    if limit < 1:
        limit = 1
    if limit > MAX_LOGS:
        limit = MAX_LOGS
    
    # Filter logs
    filtered_logs = log_storage.copy()
    
    if level:
        level_upper = level.upper()
        filtered_logs = [log for log in filtered_logs if log["level"] == level_upper]
    
    if endpoint:
        filtered_logs = [log for log in filtered_logs if log.get("endpoint") == endpoint]
    
    # Get the most recent logs up to the limit
    recent_logs = filtered_logs[-limit:]
    
    return {
        "total_logs": len(log_storage),
        "filtered_logs": len(filtered_logs),
        "returned_logs": len(recent_logs),
        "logs": recent_logs
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions
    """
    error_msg = f"Unhandled exception: {str(exc)}"
    add_log("ERROR", error_msg)
    return JSONResponse(
        status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
