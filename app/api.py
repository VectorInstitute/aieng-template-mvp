"""Demo app — FastAPI proxy to vLLM inference server.

Replace the /generate endpoint logic with your own use case.
The UI in app/demo/ calls this API.
"""

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Generator

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel


# ── Configuration (set via Cloud Run environment variables) ─────────────────
VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL")  # e.g. https://…/v1
VLLM_MODEL_NAME = os.environ.get("VLLM_MODEL_NAME", "my-model")
MAX_INPUT_CHARS = int(os.environ.get("MAX_INPUT_CHARS", "2000"))

DEMO_DIR = Path(__file__).parent / "demo"


# ── Lifespan — connect to vLLM on startup ───────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialise the vLLM client on startup."""
    if not VLLM_BASE_URL:
        raise RuntimeError("VLLM_BASE_URL is not set. Set it to the /v1 URL of your vLLM Cloud Run service.")
    app.state.client = OpenAI(base_url=VLLM_BASE_URL, api_key="EMPTY")
    print(f"Connected to vLLM at {VLLM_BASE_URL} (model: {VLLM_MODEL_NAME})")
    yield
    app.state.client = None


# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="vLLM Demo App",
    description="Proxy demo for a vLLM-backed Cloud Run GPU service.",
    version="0.1.0",
    lifespan=lifespan,
)

if (DEMO_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=DEMO_DIR / "static"), name="static")


# ── Request / response models ────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    """Request body for the /generate endpoint."""

    prompt: str


class HealthResponse(BaseModel):
    """Response body for /health."""

    status: str
    model: str


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the demo UI."""
    html_file = DEMO_DIR / "templates" / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=404, detail="Demo UI not found.")
    return html_file.read_text()


@app.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    """Check if the server and vLLM client are ready."""
    client = getattr(request.app.state, "client", None)
    if client is not None:
        return HealthResponse(status="ok", model=f"{VLLM_MODEL_NAME} @ {VLLM_BASE_URL}")
    return HealthResponse(status="starting", model="not connected")


@app.post("/generate")
def generate(request: Request, body: GenerateRequest) -> dict:
    """Send a prompt to vLLM and return the completion.

    Replace this with your own endpoint logic — parse the response,
    apply post-processing, etc.
    """
    client = getattr(request.app.state, "client", None)
    if client is None:
        raise HTTPException(status_code=500, detail="vLLM client not ready.")
    if len(body.prompt) > MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=422,
            detail=f"Prompt too long: {len(body.prompt)} chars (max {MAX_INPUT_CHARS}).",
        )
    try:
        completion = client.chat.completions.create(
            model=VLLM_MODEL_NAME,
            messages=[{"role": "user", "content": body.prompt}],
            max_tokens=1024,
            temperature=0.7,
        )
        return {"text": completion.choices[0].message.content or ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/generate/stream")
def generate_stream(request: Request, body: GenerateRequest) -> StreamingResponse:
    """Stream tokens from vLLM via Server-Sent Events.

    Each SSE event is one of:
      data: {"t": "<token>"}          — token during generation
      data: {"done": true}            — generation complete
      data: {"error": "<message>"}    — error during generation
    """
    client = getattr(request.app.state, "client", None)
    if client is None:
        raise HTTPException(status_code=500, detail="vLLM client not ready.")
    if len(body.prompt) > MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=422,
            detail=f"Prompt too long: {len(body.prompt)} chars (max {MAX_INPUT_CHARS}).",
        )

    prompt = body.prompt

    def event_stream() -> Generator[str, None, None]:
        try:
            stream = client.chat.completions.create(
                model=VLLM_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.7,
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    yield "data: " + json.dumps({"t": token}) + "\n\n"
            yield "data: " + json.dumps({"done": True}) + "\n\n"
        except Exception as e:
            yield "data: " + json.dumps({"error": str(e)}) + "\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
