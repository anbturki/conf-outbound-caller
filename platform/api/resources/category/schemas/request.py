from pydantic import BaseModel

from ..models.category import CategoryResource


class CreateCategoryRequest(BaseModel):
    name: str
    description: str
    resource: CategoryResource
