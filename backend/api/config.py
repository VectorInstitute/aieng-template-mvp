"""Configuration settings for the FastAPI application."""

from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the API.

    This class uses Pydantic's BaseSettings to load configuration from environment
    variables. The class attributes will be populated from environment variables
    with the same name (case-insensitive).
    """

    # API settings
    backend_port: int = Field(default=8000, description="Port for the backend service")
    frontend_port: int = Field(
        default=3000, description="Port for the frontend service"
    )

    # Add your custom settings here
    # example_api_key: str = Field(
    #     default="", description="API key for Example service"
    # )

    model_config = SettingsConfigDict(
        env_file=".env.development", env_file_encoding="utf-8", case_sensitive=False
    )


def get_fastapi_settings() -> Dict[str, Any]:
    """Get FastAPI application settings.

    Returns
    -------
    Dict[str, Any]
        Dictionary with FastAPI settings.
    """
    return {
        "title": "MVP API",
        "description": "API for MVP application",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
