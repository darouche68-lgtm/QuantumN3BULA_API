# Quantum-N3BULA API

A production-ready FastAPI microservice for quantum operations simulation.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- **Health Endpoints**: `/ping` and `/status` for service health monitoring
- **Command Execution**: `/execute` endpoint for simulated command execution
- **Logging**: `/logs` endpoint for viewing application logs
- **Async Routes**: All endpoints are async for high performance
- **Structured Logging**: JSON-formatted logs with detailed metadata
- **Docker Support**: Multi-stage Dockerfile for production deployment
- **CI/CD**: GitHub Actions workflow for automated testing and Docker Hub deployment

## Project Structure

```
QuantumN3BULA_API/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── logging_config.py    # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic request/response models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py        # API route handlers
│   └── services/
│       ├── __init__.py
│       └── system_service.py # Business logic
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API endpoint tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API information |
| `/ping` | GET | Simple health check returning "pong" |
| `/status` | GET | Detailed system status and health info |
| `/execute` | POST | Execute a simulated command |
| `/logs` | GET | Retrieve application logs |
| `/logs` | DELETE | Clear all stored logs |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation (ReDoc) |

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/QuantumN3BULA_API.git
   cd QuantumN3BULA_API
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

### Using Docker

1. **Build the image**
   ```bash
   docker build -t quantum-n3bula-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 quantum-n3bula-api
   ```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `MAX_LOG_ENTRIES` | `1000` | Max log entries to store |

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

## CI/CD

The GitHub Actions workflow automatically:

1. Runs tests on every push and pull request
2. Builds Docker image on successful tests
3. Pushes to Docker Hub with appropriate tags

### Required Secrets

Set these secrets in your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

## API Examples

### Ping
```bash
curl http://localhost:8000/ping
```

### Status
```bash
curl http://localhost:8000/status
```

### Execute Command
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "echo", "parameters": {"message": "Hello, World!"}}'
```

### Get Logs
```bash
curl "http://localhost:8000/logs?limit=10&level=INFO"
```

## License

MIT License