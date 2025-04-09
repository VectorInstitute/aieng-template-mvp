# MVP Backend

This is the backend for the AI Engineering MVP Template built with FastAPI.

## Development

### Local Development

```bash
# Install in development mode
pip install -e .

# Run the development server
uvicorn api.main:app --reload
```

### With Docker

```bash
# From the root directory
docker compose --env-file .env.development -f docker-compose.dev.yml up backend-dev
```

## Project Structure

- **api**: Contains the FastAPI application
  - **main.py**: Main application entry point
  - **config.py**: Configuration management
  - **routes.py**: API endpoints
- **services**: Business logic and services

## API Documentation

When running the server, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
