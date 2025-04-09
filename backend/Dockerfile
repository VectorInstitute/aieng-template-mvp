FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    groupadd -g 1000 appuser && \
    useradd -m -u 1000 -g appuser appuser && \
    chown -R appuser:appuser /app

COPY --chown=appuser:appuser . .

USER appuser

RUN pip install -e .

ARG BACKEND_PORT
ARG FRONTEND_PORT
ENV BACKEND_PORT=${BACKEND_PORT} \
    FRONTEND_PORT=${FRONTEND_PORT}

EXPOSE ${BACKEND_PORT}

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "${BACKEND_PORT}"]
