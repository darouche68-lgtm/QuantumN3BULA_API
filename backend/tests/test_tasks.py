"""Tests for task endpoints."""


def test_list_tasks(client):
    """Test listing tasks."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_task_requires_auth(client):
    """Test creating task requires authentication."""
    response = client.post(
        "/api/tasks",
        json={
            "name": "test-task",
            "command": "echo hello",
        },
    )
    assert response.status_code == 401


def test_create_task(authenticated_client):
    """Test creating a task."""
    response = authenticated_client.post(
        "/api/tasks",
        json={
            "name": "test-task",
            "command": "echo hello",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-task"
    assert data["command"] == "echo hello"
    assert data["status"] == "pending"


def test_get_task(authenticated_client):
    """Test getting a specific task."""
    # Create task
    create_response = authenticated_client.post(
        "/api/tasks",
        json={
            "name": "get-task",
            "command": "ls -la",
        },
    )
    task_id = create_response.json()["id"]

    # Get task
    response = authenticated_client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["name"] == "get-task"


def test_get_nonexistent_task(client):
    """Test getting a nonexistent task returns 404."""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_execute_task(authenticated_client):
    """Test executing a command."""
    response = authenticated_client.post(
        "/api/tasks/execute",
        json={"command": "echo test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["command"] == "echo test"
    assert data["status"] == "running"
