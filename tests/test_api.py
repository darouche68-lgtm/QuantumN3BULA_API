"""Tests for Quantum-N3BULA API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client fixture."""
    return TestClient(app)


class TestPingEndpoint:
    """Tests for /ping endpoint."""
    
    def test_ping_returns_pong(self, client):
        """Test that ping endpoint returns pong message."""
        response = client.get("/ping")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "pong"
        assert "timestamp" in data
    
    def test_ping_timestamp_format(self, client):
        """Test that ping timestamp is ISO format."""
        response = client.get("/ping")
        data = response.json()
        
        # Should be valid ISO format
        assert "T" in data["timestamp"]


class TestStatusEndpoint:
    """Tests for /status endpoint."""
    
    def test_status_returns_healthy(self, client):
        """Test that status endpoint returns healthy status."""
        response = client.get("/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "Quantum-N3BULA API"
        assert data["system"]["status"] == "healthy"
    
    def test_status_includes_uptime(self, client):
        """Test that status includes uptime information."""
        response = client.get("/status")
        data = response.json()
        
        assert "uptime_seconds" in data["system"]
        assert data["system"]["uptime_seconds"] >= 0
    
    def test_status_includes_version(self, client):
        """Test that status includes version information."""
        response = client.get("/status")
        data = response.json()
        
        assert "version" in data["system"]
        assert "python_version" in data["system"]


class TestExecuteEndpoint:
    """Tests for /execute endpoint."""
    
    def test_execute_echo_command(self, client):
        """Test execute endpoint with echo command."""
        response = client.post(
            "/execute",
            json={"command": "echo", "parameters": {"message": "Hello, World!"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["command"] == "echo"
        assert data["status"] == "success"
        assert data["result"] == "Hello, World!"
    
    def test_execute_time_command(self, client):
        """Test execute endpoint with time command."""
        response = client.post("/execute", json={"command": "time"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["command"] == "time"
        assert data["status"] == "success"
        assert "T" in data["result"]  # ISO timestamp
    
    def test_execute_info_command(self, client):
        """Test execute endpoint with info command."""
        response = client.post("/execute", json={"command": "info"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "platform" in data["result"]
    
    def test_execute_calculate_command(self, client):
        """Test execute endpoint with calculate command."""
        response = client.post(
            "/execute",
            json={"command": "calculate", "parameters": {"expression": "2 + 2"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["result"] == 4
    
    def test_execute_unknown_command(self, client):
        """Test execute endpoint with unknown command."""
        response = client.post("/execute", json={"command": "unknown_cmd"})
        
        assert response.status_code == 200
        data = response.json()
        assert "acknowledged" in data["result"]
    
    def test_execute_includes_timing(self, client):
        """Test that execute includes execution time."""
        response = client.post("/execute", json={"command": "echo"})
        data = response.json()
        
        assert "execution_time_ms" in data
        assert data["execution_time_ms"] >= 0


class TestLogsEndpoint:
    """Tests for /logs endpoint."""
    
    def test_logs_returns_entries(self, client):
        """Test that logs endpoint returns log entries."""
        # Make some requests to generate logs
        client.get("/ping")
        client.get("/status")
        
        response = client.get("/logs")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_entries" in data
        assert "entries" in data
        assert isinstance(data["entries"], list)
    
    def test_logs_with_limit(self, client):
        """Test logs endpoint with limit parameter."""
        response = client.get("/logs?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) <= 5
    
    def test_logs_with_level_filter(self, client):
        """Test logs endpoint with level filter."""
        response = client.get("/logs?level=INFO")
        
        assert response.status_code == 200
        data = response.json()
        for entry in data["entries"]:
            assert entry["level"] == "INFO"
    
    def test_clear_logs(self, client):
        """Test clearing logs."""
        response = client.delete("/logs")
        
        assert response.status_code == 200
        data = response.json()
        assert "Cleared" in data["message"]


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_returns_api_info(self, client):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Quantum-N3BULA API"
        assert "version" in data
        assert data["docs"] == "/docs"
