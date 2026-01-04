from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # Use Pydantic's built-in to_camel
        populate_by_name=True,  # Allow population by field name or alias
        from_attributes=True,  # Enable mapping from SQLAlchemy objects
        arbitrary_types_allowed=True,  # Allow arbitrary types like SQLAlchemy UUID
    )


class BaseQueryParams(CamelCaseModel):
    page: int = 1
    limit: int = 10
    search: str | None = None
    sort: str | None = None
    order: str | None = None
