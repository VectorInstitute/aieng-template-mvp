# ============================================================
# Demo App — Cloud Run CPU Service
# Serves the UI and proxies /analyze requests to the vLLM GPU service.
#
# nginx starts instantly on port 8080 (serves UI from filesystem),
# uvicorn loads in the background (~20-30s) and handles API calls.
# ============================================================
FROM python:3.12-slim

LABEL maintainer="Vector Institute AI Engineering"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy and install Python dependencies first (layer cache)
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

# Copy application code
COPY app/ app/
COPY nginx.conf entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

ENV TOKENIZERS_PARALLELISM=false
ENV PORT=8080
EXPOSE 8080

# Run as non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# nginx serves the UI immediately; uvicorn loads in the background.
CMD ["/app/entrypoint.sh"]
