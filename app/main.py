"""
Main module for the application
"""

from time import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import api_config, cors_config
from app.core.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.events import lifespan
from app.core.exceptions import AppException

app = FastAPI(title="Confera Platform API", version="1.0.0", lifespan=lifespan)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, http_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add request ID middleware
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    """
    Middleware to add request ID to the request.
    """
    request_id = request.headers.get("X-Request-ID", f"req-{time()}")
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add process time header to the response.
    """
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=api_config.prefix)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "version": api_config.version,
        "environment": api_config.environment,
    }


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint for the API.
    """
    return {
        "name": api_config.name,
        "description": api_config.description,
        "version": api_config.version,
        "environment": api_config.environment,
    }
