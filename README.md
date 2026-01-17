# Quantum-N3BULA API

A FastAPI-based microservice for quantum operations with modular architecture, comprehensive error handling, and CI/CD integration.

## Features

- **RESTful API** with FastAPI
- **Health Monitoring** endpoints (`/ping`, `/status`)
- **Operation Execution** endpoint (`/execute`) with validation and error handling
- **Logging System** with in-memory storage (`/logs`)
- **Docker Support** with multi-stage builds and health checks
- **CI/CD Pipeline** with GitHub Actions
- **Auto-generated API Documentation** (Swagger UI and ReDoc)

## API Endpoints

### Health Endpoints

#### `GET /ping`
Simple ping endpoint to check if the service is alive.

**Response:**
```json
{
  "message": "pong",
  "timestamp": "2024-01-17T19:00:00.000000"
}
```

#### `GET /status`
Get the current status of the service.

**Response:**
```json
{
  "service": "Quantum-N3BULA API",
  "version": "1.0.0",
  "status": "healthy",
  "timestamp": "2024-01-17T19:00:00.000000",
  "total_logs": 42
}
```

### Operations Endpoints

#### `POST /execute`
Execute a quantum operation command.

**Request Body:**
```json
{
  "command": "quantum_transform",
  "parameters": {
    "mode": "superposition",
    "qubits": 8
  }
}
```

**Response:**
```json
{
  "task_id": "task_20240117190000000000",
  "status": "completed",
  "result": "Command 'quantum_transform' executed successfully with parameters: {'mode': 'superposition', 'qubits': 8}",
  "timestamp": "2024-01-17T19:00:00.000000"
}
```

### Monitoring Endpoints

#### `GET /logs`
Retrieve application logs with optional filtering.

**Query Parameters:**
- `limit` (optional): Maximum number of logs to return (default: 100, max: 1000)
- `level` (optional): Filter by log level (INFO, WARNING, ERROR)
- `endpoint` (optional): Filter by endpoint (e.g., /ping, /execute)

**Response:**
```json
{
  "total_logs": 150,
  "filtered_logs": 100,
  "returned_logs": 100,
  "logs": [
    {
      "timestamp": "2024-01-17T19:00:00.000000",
      "level": "INFO",
      "message": "Execute endpoint called with command: quantum_transform",
      "endpoint": "/execute"
    }
  ]
}
```

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/darouche68-lgtm/QuantumN3BULA_API.git
   cd QuantumN3BULA_API
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker

1. **Build the Docker image:**
   ```bash
   docker build -t quantumn3bula-api:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 quantumn3bula-api:latest
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/ping

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. **Tests** the application on every push and pull request
2. **Builds** the Docker image
3. **Tests** the Docker container
4. **Pushes** to Docker Hub (on main/master branch only)

### Required Secrets

Configure these secrets in your GitHub repository:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token

## Architecture

### Modular Design
- **Pydantic Models**: Request/response validation
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Logging**: Structured logging with in-memory storage and filtering
- **Health Checks**: Built-in Docker health checks

### Best Practices
- Non-root user in Docker container
- Environment variables for configuration
- Multi-stage Docker builds (optimized)
- Security scanning ready
- Proper .dockerignore and .gitignore

## Technology Stack

- **Python**: 3.11
- **Framework**: FastAPI 0.109.0
- **ASGI Server**: Uvicorn 0.27.0
- **Validation**: Pydantic 2.5.3
- **Container**: Docker
- **CI/CD**: GitHub Actions

## Development

### Project Structure
```
QuantumN3BULA_API/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### Testing

Run basic import test:
```bash
python -c "from main import app; print('Application imports successfully')"
```

Test endpoints with curl:
```bash
# Ping
curl http://localhost:8000/ping

# Status
curl http://localhost:8000/status

# Execute
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "test_command", "parameters": {"key": "value"}}'

# Logs
curl http://localhost:8000/logs?limit=10&level=INFO
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.