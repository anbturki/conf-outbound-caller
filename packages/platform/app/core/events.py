"""
This module contains the events for the application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from shared import logger, setup_logging

from app.core.config import api_config, log_config
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    This function is called when the application starts and shuts down.
    """
    # Startup
    setup_logging(
        log_level=log_config.level,
        log_format=log_config.format,
        log_path=log_config.path,
    )
    logger.info(f"Starting Confera API - Environment: {api_config.env}")

    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    engine.dispose()
    logger.info("Confera API shutdown complete")
