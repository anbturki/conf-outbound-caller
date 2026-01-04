from app.core.base_models import CamelCaseModel

from ..models.category import CategoryResource


class CategoryResponse(CamelCaseModel):
    id: str
    name: str
    description: str
    resource: CategoryResource
