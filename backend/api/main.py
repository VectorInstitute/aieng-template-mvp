"""Main module for the FastAPI application."""

import logging
from typing import Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.config import Settings
from api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Create the FastAPI app
app = FastAPI(
    title="MVP API",
    description="API for MVP application",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint of the API.

    Returns
    -------
    Dict[str, str]
        A welcome message for the API.
    """
    return {"message": "Welcome to the MVP API"}


@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Health check endpoint.

    This endpoint can be used to verify that the API is running and responsive.

    Returns
    -------
    Dict[str, str]
        A dictionary indicating the health status of the API.
    """
    return {"status": "healthy"}
