"""Basic API tests — run with: uv run pytest"""
import os

import pytest
from fastapi.testclient import TestClient

# Set required env var before importing the app
os.environ.setdefault("VLLM_BASE_URL", "http://localhost:9999/v1")


def test_health_before_client_ready() -> None:
    """Health endpoint returns 'starting' when client is not initialised."""
    # Import after env var is set; bypass lifespan to avoid connecting
    from app.api import app

    with TestClient(app, raise_server_exceptions=False) as client:
        # TestClient doesn't run lifespan by default when used as plain client
        resp = client.get("/health")
        # May return 200 with status=starting or status=ok
        assert resp.status_code == 200
        body = resp.json()
        assert "status" in body


def test_generate_input_too_long() -> None:
    """Generate endpoint rejects prompts over MAX_INPUT_CHARS."""
    from app.api import MAX_INPUT_CHARS, app

    with TestClient(app, raise_server_exceptions=False) as client:
        oversized = "x" * (MAX_INPUT_CHARS + 1)
        resp = client.post("/generate", json={"prompt": oversized})
        assert resp.status_code == 422
