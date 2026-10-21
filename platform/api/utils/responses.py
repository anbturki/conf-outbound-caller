"""
Utils for responses
"""

from math import ceil
from typing import Any, List, Optional, Type, TypeVar

from common.schemas.success_responses import (
    GenericResponse,
    MessageResponse,
    PagedResponse,
    PaginationMeta,
)
from core.database import Base
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, create_model

T = TypeVar("T")
ModelType = TypeVar("ModelType", bound=BaseModel)


def serialize_model(data: Any) -> dict:
    """Serialize a Pydantic model to a dictionary."""
    return data.model_dump(mode="json", by_alias=True)


def is_pydantic_model(data: Any) -> bool:
    """Check if the data is a Pydantic model."""
    return isinstance(data, BaseModel)


def is_sqlalchemy_model(data: Any) -> bool:
    """Check if the data is a SQLAlchemy model."""
    return isinstance(data, Base)


def create_response(
    data: Optional[Any] = None,
    status_code: int = status.HTTP_200_OK,
    message: str = "Operation successful",
    response_model: Type[ModelType] = None,
) -> JSONResponse:
    """Create a response from a model."""

    if response_model:
        data = response_model.model_validate(data)

    response = GenericResponse(
        success=True,
        message=message,
        data=data,
    )

    return JSONResponse(
        status_code=status_code,
        content=serialize_model(response),
    )


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
    response_model: Type[ModelType] = None,
) -> JSONResponse:
    """Create a standardized success response."""
    return create_response(data, status.HTTP_200_OK, message, response_model)


def created_response(
    data: Optional[Any] = None,
    message: str = "Operation successful",
    response_model: Type[ModelType] = None,
) -> JSONResponse:
    """Create a standardized created response."""
    return create_response(
        data, status.HTTP_201_CREATED, message, response_model=response_model
    )


def message_response(
    message: str,
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    response = MessageResponse(success=True, message=message)
    return JSONResponse(
        status_code=status_code,
        content=serialize_model(response),
    )


def paginated_response(
    items: List[T],
    total: int,
    page: int,
    limit: int,
    message: str = "Items retrieved successfully",
    response_model: Type[ModelType] = None,
) -> JSONResponse:
    total_pages = ceil(total / limit)

    # if it is pydantic or sqlalchemy model, convert to dict
    if items and is_sqlalchemy_model(items[0]) and response_model:
        items = [response_model.model_validate(item) for item in items]

    response = PagedResponse(
        message=message,
        data=items,
        meta=PaginationMeta(
            total=total,
            page=page,
            limit=limit,
            pages=total_pages,
        ),
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=serialize_model(response),
    )
