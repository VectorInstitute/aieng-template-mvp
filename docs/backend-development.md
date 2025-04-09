# Backend Development

This guide covers the key aspects of backend development using the FastAPI framework in this template.

## Environment Setup

### Setting Up with uv

We recommend using [uv](https://github.com/astral-sh/uv) for Python package management, which is faster than pip and provides better dependency resolution.

```bash
# Install uv if you don't have it
pip install uv

# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies including development packages
uv pip install -e ".[dev]"
```

### Running the Backend Server

```bash
# With the virtual environment activated
uvicorn api.main:app --reload
```

## Project Structure

The backend is organized as follows:

```
backend/
├── api/                  # FastAPI application
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── main.py           # Application entry point
│   └── routes.py         # API endpoints
├── services/             # Business logic
│   ├── __init__.py
│   └── example_service.py
├── tests/                # Test files
│   ├── __init__.py
│   └── test_example_service.py
├── pyproject.toml        # Project configuration
└── README.md
```

## API Endpoints

The template includes several example endpoints in `api/routes.py`:

- `GET /`: Root endpoint returning a welcome message
- `GET /healthcheck`: Health check endpoint
- `GET /api/example`: Simple example endpoint
- `GET /api/examples`: Returns a list of examples from the example service
- `GET /api/examples/{example_id}`: Returns a specific example by ID

## Adding New Endpoints

To add a new endpoint, follow these steps:

1. Create a new service in the `services` directory if needed
2. Add the endpoint to `api/routes.py`
3. Update API documentation as needed

Example:

```python
@router.get("/api/new-endpoint")
async def new_endpoint() -> Dict[str, str]:
    """New endpoint description.

    Returns
    -------
    Dict[str, str]
        Response data.
    """
    return {"message": "This is a new endpoint"}
```

## Services

The services directory contains the business logic of your application. The template includes an example service (`example_service.py`) that demonstrates a simple data service.

### Adding a New Service

Create a new file in the `services` directory:

```python
"""New service module."""

class NewService:
    """New service class."""

    def __init__(self) -> None:
        """Initialize the new service."""
        pass

    def some_method(self) -> str:
        """Do something.

        Returns
        -------
        str
            Result of the operation.
        """
        return "Result"
```

## Testing

The template uses pytest for testing. Tests are located in the `tests` directory.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=api --cov=services
```

### Writing Tests

Here's an example of a test for a new service:

```python
"""Tests for new service."""

from services.new_service import NewService

class TestNewService:
    """Tests for NewService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = NewService()

    def test_some_method(self) -> None:
        """Test some_method."""
        result = self.service.some_method()
        assert result == "Result"
```

## Code Quality

The template includes configuration for several code quality tools:

- **Ruff**: For linting and formatting
- **MyPy**: For type checking
- **Pytest**: For testing

### Running Linting

```bash
# Run ruff for linting
ruff check .

# Run mypy for type checking
mypy .
```

## API Documentation

FastAPI automatically generates interactive API documentation. When the server is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
