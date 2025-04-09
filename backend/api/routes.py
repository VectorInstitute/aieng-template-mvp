"""API routes for the application."""

import logging
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Path

from services.example_service import ExampleService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["api"])

# Initialize services
example_service = ExampleService()


@router.get("/example")
async def example_endpoint() -> Dict[str, str]:
    """Example endpoint.

    Returns
    -------
    Dict[str, str]
        Example response.
    """
    try:
        return {"message": "This is an example endpoint"}
    except Exception as e:
        logger.error(f"Error in example endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/examples", response_model=List[Dict[str, str]])
async def get_all_examples() -> List[Dict[str, str]]:
    """Get all examples.

    Returns
    -------
    List[Dict[str, str]]
        List of all examples.
    """
    try:
        return example_service.get_all_examples()
    except Exception as e:
        logger.error(f"Error getting all examples: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/examples/{example_id}", response_model=Dict[str, str])
async def get_example_by_id(
    example_id: str = Path(..., description="ID of the example"),
) -> Dict[str, str]:
    """Get an example by ID.

    Parameters
    ----------
    example_id : str
        ID of the example to retrieve.

    Returns
    -------
    Dict[str, str]
        Example data.
    """
    try:
        return example_service.get_example_by_id(example_id)
    except ValueError as e:
        logger.error(f"Example not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error getting example by ID: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
