"""Service layer for system operations."""

import asyncio
import platform
import sys
import time
from datetime import datetime, timezone
from typing import Any

from app.logging_config import logger


# Track service start time for uptime calculation
_start_time = time.time()


async def get_system_status() -> dict:
    """Get current system health status."""
    uptime = time.time() - _start_time
    
    logger.info(
        "System status check performed",
        extra={"endpoint": "/status", "uptime_seconds": uptime}
    )
    
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }


async def execute_command(command: str, parameters: dict[str, Any] | None = None) -> dict:
    """
    Execute a simulated command.
    
    This is a simulation - in a real scenario, this would execute actual commands
    with proper security controls and sandboxing.
    """
    start_time = time.time()
    
    logger.info(
        f"Executing command: {command}",
        extra={"endpoint": "/execute", "command": command}
    )
    
    # Simulate command processing with async delay
    await asyncio.sleep(0.01)  # 10ms simulated processing
    
    # Simulated command handling
    result: Any
    status = "success"
    
    if command.lower() == "echo":
        result = parameters.get("message", "") if parameters else ""
    elif command.lower() == "time":
        result = datetime.now(timezone.utc).isoformat()
    elif command.lower() == "info":
        result = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "processor": platform.processor() or "unknown"
        }
    elif command.lower() == "calculate":
        # Simple calculation simulation using ast.literal_eval for safety
        if parameters and "expression" in parameters:
            try:
                import ast
                import operator
                
                # Only allow safe numeric operations
                expr = str(parameters["expression"])
                
                # Define allowed operators
                ops = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.USub: operator.neg,
                    ast.UAdd: operator.pos
                }
                
                def safe_eval(node):
                    """Safely evaluate a math expression AST node."""
                    if isinstance(node, ast.Constant):  # Numbers
                        if isinstance(node.value, (int, float)):
                            return node.value
                        raise ValueError("Only numeric constants allowed")
                    elif isinstance(node, ast.BinOp):  # Binary operations
                        left = safe_eval(node.left)
                        right = safe_eval(node.right)
                        op_type = type(node.op)
                        if op_type in ops:
                            return ops[op_type](left, right)
                        raise ValueError(f"Unsupported operator: {op_type}")
                    elif isinstance(node, ast.UnaryOp):  # Unary operations
                        operand = safe_eval(node.operand)
                        op_type = type(node.op)
                        if op_type in ops:
                            return ops[op_type](operand)
                        raise ValueError(f"Unsupported unary operator: {op_type}")
                    elif isinstance(node, ast.Expression):
                        return safe_eval(node.body)
                    else:
                        raise ValueError(f"Unsupported node type: {type(node)}")
                
                tree = ast.parse(expr, mode='eval')
                result = safe_eval(tree)
            except (SyntaxError, TypeError, ZeroDivisionError, ValueError) as e:
                result = f"Calculation error: {str(e)}"
                status = "error"
        else:
            result = "No expression provided"
            status = "error"
    else:
        result = f"Command '{command}' acknowledged"
    
    execution_time_ms = (time.time() - start_time) * 1000
    
    logger.info(
        f"Command execution completed: {command}",
        extra={
            "endpoint": "/execute",
            "command": command,
            "status": status,
            "duration_ms": round(execution_time_ms, 2)
        }
    )
    
    return {
        "command": command,
        "status": status,
        "result": result,
        "execution_time_ms": round(execution_time_ms, 2)
    }
