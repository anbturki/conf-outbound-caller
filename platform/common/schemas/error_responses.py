from enum import Enum
from typing import Any, Dict, Optional, Union

from core.base_models import CamelCaseModel
from pydantic import Field


class ErrorCode(str, Enum):
    """
    Error codes for the application
    """

    REQUIRED = "REQUIRED"
    INVALID_INPUT = "INVALID_INPUT"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_EXISTS = "RESOURCE_EXISTS"
    BAD_REQUEST = "BAD_REQUEST"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"


class ErrorDetail(CamelCaseModel):
    code: ErrorCode
    message: str


class ValidationErrorDetails(CamelCaseModel):
    """Model for validation error details container."""

    message: str = Field(
        description="The error message",
        examples=["The provided data didn't pass validation"],
    )

    details: ErrorDetail


class ErrorResponse(CamelCaseModel):
    """Standardized error response model."""

    success: bool = Field(
        default=False,
        description="Whether the operation was successful",
        examples=[False],
    )
    code: ErrorCode = Field(
        description="The error code",
        examples=[ErrorCode.INVALID_INPUT],
    )
    message: str = Field(
        description="The error message",
        examples=["Invalid input"],
    )
    statusCode: int
    error: Optional[Union[ValidationErrorDetails, Dict[str, Any]]] = None
