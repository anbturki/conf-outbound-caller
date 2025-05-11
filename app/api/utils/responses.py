"""
Utils for responses
"""

from typing import Any, Dict, List, Optional, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, create_model

from app.schemas.responses import GenericResponse, MessageResponse

T = TypeVar("T")


# Function to create response models dynamically
def create_response_model(name: str, model_type: Any) -> type:
    """
    Create a response model for a specific data type.

    Args:
        name: Name for the response model
        model_type: Type for the data field

    Returns:
        Pydantic model class
    """
    return create_model(
        f"{name}Response",
        success=(bool, True),
        message=(Optional[str], None),
        data=(Optional[model_type], None),
        __base__=BaseModel,
    )


# Helper to generate list response models
def create_list_response_model(name: str, item_type: Any) -> type:
    """
    Create a response model for a list of items.

    Args:
        name: Name for the response model
        item_type: Type for the list items

    Returns:
        Pydantic model class
    """
    return create_model(
        f"{name}ListResponse",
        success=(bool, True),
        message=(Optional[str], None),
        data=(List[item_type], []),
        __base__=BaseModel,
    )


def success_response(
    data: Optional[Any] = None,
    message: str = "Operation successful",
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    """Create a standardized success response."""
    response = GenericResponse(
        success=True,
        message=message,
        data=data,
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True),
    )


def created_response(
    data: Optional[Any] = None,
    message: str = "Operation successful",
    status_code: int = status.HTTP_201_CREATED,
) -> JSONResponse:
    """Create a standardized created response."""
    response = GenericResponse(
        success=True,
        message=message,
        data=data,
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True),
    )


def message_response(
    message: str, status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a message-only response.

    Args:
        message: Response message
        status_code: HTTP status code

    Returns:
        JSONResponse with standardized format
    """
    response = MessageResponse(success=True, message=message)
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True),
    )


def paginated_response(
    items: List[T],
    total: int,
    page: int,
    page_size: int,
    message: str = "Items retrieved successfully",
) -> Dict[str, Any]:
    """
    Create a paginated response.

    Args:
        items: List of items
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        message: Success message

    Returns:
        Dictionary with paginated response format
    """
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0

    response = GenericResponse(
        success=True,
        message=message,
        data=items,
        meta={"total": total, "page": page, "page_size": page_size, "pages": pages},
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True),
    )
