from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.utils.responses import created_response
from app.common.schemas.success_responses import GenericResponse

from .models.category import Category
from .schemas.request import CreateCategoryRequest
from .schemas.response import CategoryResponse
from .service import CategoryService, get_category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", status_code=201, response_model=GenericResponse[CategoryResponse])
def create_category(
    body: CreateCategoryRequest,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    category = Category(
        name=body.name,
        description=body.description,
        resource=body.resource,
    )
    category_service.save(category)
    return created_response(
        CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            resource=category.resource,
        )
    )


@router.get("/")
def get_categories():
    return {
        "categories": [
            {
                "id": "1",
                "name": "Category 1",
            }
        ]
    }
