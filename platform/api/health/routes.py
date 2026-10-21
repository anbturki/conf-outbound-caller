# Health check endpoint
from core.config import api_config
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "version": api_config.version,
        "environment": api_config.env,
        "debug": api_config.debug_enabled,
    }


@router.get("/", tags=["root"])
async def root():
    """
    Root endpoint for the API.
    """
    return {
        "name": api_config.name,
        "description": api_config.description,
        "version": api_config.version,
        "environment": api_config.env,
        "debug": api_config.debug_enabled,
    }
