"""
Schemas for responses
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field

from app.core.exceptions import ErrorCode

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Model for individual field error details."""

    code: str
    message: str


class ValidationErrorDetails(BaseModel):
    """Model for validation error details container."""

    message: str = Field(
        description="The error message",
        examples=["The provided data didn't pass validation"],
    )

    details: ErrorDetail = Field(
        description="The error details",
        examples=[
            {
                "email": ErrorDetail(code="Required", message="This field is required"),
                "password": ErrorDetail(
                    code="Required", message="This field is required"
                ),
            }
        ],
    )


class ErrorResponse(BaseModel):
    """Standardized error response model."""

    success: bool = Field(
        default=False,
        description="Whether the operation was successful",
        examples=[False],
    )
    code: str = Field(
        type=ErrorCode,
        description="The error code",
        examples=["invalid_request"],
    )
    message: str = Field(
        description="The error message",
        examples=["Invalid request"],
    )
    statusCode: int
    error: Optional[Union[ValidationErrorDetails, Dict[str, Any]]] = None


# Base generic response model
class GenericResponse(BaseModel, Generic[T]):
    """Model for generic response."""

    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None


# Message-only response
class MessageResponse(BaseModel):
    """Model for message-only response."""

    success: bool = Field(
        default=True,
        description="Whether the operation was successful",
        examples=[True],
    )
    message: str = Field(
        description="A message describing the operation",
        examples=["Operation successful"],
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional data associated with the operation",
        examples=[{"key": "value"}],
    )


class PaginationMeta(BaseModel):
    """Model for pagination metadata."""

    total: int
    page: int
    page_size: int
    pages: int


# Paginated response
class PagedResponse(BaseModel, Generic[T]):
    """Model for paged response."""

    success: bool = True
    message: Optional[str] = None
    data: List[T]
    meta: PaginationMeta
