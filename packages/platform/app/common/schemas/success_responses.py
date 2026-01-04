"""
Schemas for responses
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import Field

from app.core.base_models import CamelCaseModel

T = TypeVar("T")


# Base generic response model
class GenericResponse(CamelCaseModel, Generic[T]):
    """Model for generic response."""

    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None


# Message-only response
class MessageResponse(CamelCaseModel):
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


class PaginationMeta(CamelCaseModel):
    """Model for pagination metadata."""

    limit: int
    total: int
    pages: int
    page: int


# Paginated response
class PagedResponse(CamelCaseModel, Generic[T]):
    """Model for paged response."""

    success: bool = True
    message: Optional[str] = None
    data: List[T]
    meta: PaginationMeta
