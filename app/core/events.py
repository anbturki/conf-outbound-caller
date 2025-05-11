"""
This module contains the events for the application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.config import environment_config
from app.core.database import Base, engine
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    This function is called when the application starts and shuts down.
    """
    # Startup
    setup_logging()
    logger.info(f"Starting Confera API - Environment: {environment_config.env}")

    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    engine.dispose()
    logger.info("Confera API shutdown complete")
