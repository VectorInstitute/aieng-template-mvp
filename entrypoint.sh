#!/bin/sh
set -e

# Start the FastAPI/uvicorn server in the background on port 8000.
# nginx (below) proxies API requests to it once it is ready.
uv run uvicorn app.api:app --host 0.0.0.0 --port 8000 &

# Start nginx in the foreground on port 8080.
# nginx serves the UI immediately and proxies /health, /generate, etc. to uvicorn.
exec nginx -c /app/nginx.conf -g 'daemon off;'
