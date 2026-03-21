"""Basic API tests — run with: uv run pytest."""

import os


# Must be set before importing app modules that read env vars at import time
os.environ.setdefault("VLLM_BASE_URL", "http://localhost:9999/v1")

from fastapi.testclient import TestClient  # noqa: E402

from app.api import MAX_INPUT_CHARS, app  # noqa: E402


def test_health_before_client_ready() -> None:
    """Health endpoint returns 'starting' when client is not initialised."""
    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert "status" in body


def test_generate_input_too_long() -> None:
    """Generate endpoint rejects prompts over MAX_INPUT_CHARS."""
    with TestClient(app, raise_server_exceptions=False) as client:
        oversized = "x" * (MAX_INPUT_CHARS + 1)
        resp = client.post("/generate", json={"prompt": oversized})
        assert resp.status_code == 422
