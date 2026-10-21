"""
Error handlers for the application
"""

import traceback

from common.schemas.error_responses import ErrorResponse
from core.exceptions import AppException, ValidationException
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from shared import logger


async def app_exception_handler(_: Request, exc: AppException):
    """
    Handler for custom AppException.
    """
    logger.error(
        f"AppException: {exc.detail}, Code: {exc.error_code}, Status: {exc.status_code}"
    )

    # Create standardized error response
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            code=exc.error_code,
            message=exc.detail,
            statusCode=exc.status_code,
            error=exc.error_details,
        ).model_dump(),
    )


async def http_exception_handler(_: Request, exc: Exception):
    """
    General exception handler for all unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())

    # Create standardized error response for server errors
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            code="SERVER_ERROR",
            message="An unexpected error occurred",
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).model_dump(),
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """
    Handler for FastAPI's RequestValidationError.
    """
    error_details = {}
    logger.error(f"Validation error: {exc.errors()}")

    for error in exc.errors():
        # Get the field name from the error location
        logger.error(f"Error: {error}")
        field_path = error.get("loc", [])
        if not field_path:
            continue

        # Skip 'body' and get the actual field name
        if field_path[0] == "body":
            field_name = ".".join(str(loc) for loc in field_path[1:])
        else:
            field_name = ".".join(str(loc) for loc in field_path)

        # Get error type and message
        error_type = error.get("type", "unknown")
        error_msg = error.get("msg", "Unknown validation error")

        # Map error types to more user-friendly codes
        error_code_map = {
            "missing": "Required",
            "type_error": "InvalidType",
            "value_error": "InvalidValue",
            "value_error.missing": "Required",
            "value_error.email": "InvalidEmail",
            "value_error.url": "InvalidURL",
            "value_error.number.not_gt": "TooSmall",
            "value_error.number.not_lt": "TooLarge",
            "value_error.number.not_ge": "TooSmall",
            "value_error.number.not_le": "TooLarge",
            "value_error.any_str.max_length": "TooLong",
            "value_error.any_str.min_length": "TooShort",
            "value_error.regex": "InvalidFormat",
        }

        error_code = error_code_map.get(
            error_type, error_type.split(".")[-1].capitalize()
        )

        # Format the error detail
        error_details[field_name or "body"] = {"code": error_code, "message": error_msg}

    # Create standardized error response
    raise ValidationException(field_errors=error_details)
