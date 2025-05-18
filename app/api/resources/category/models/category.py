import enum

from sqlalchemy import (
    Column,
    Enum,
    String,
    UniqueConstraint,
)

from app.core.base_models import BaseDBModel


class CategoryResource(str, enum.Enum):
    DOCUMENT = "document"
    ASSISTANT = "assistant"


class Category(BaseDBModel):
    __tablename__ = "categories"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "org_id",
            "resource",
            name="uq_name_org_id_resource",
        ),
    )

    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    # Category can belong to a resource, for example, a persona, assistant, knowledge base, etc.
    resource = Column(
        Enum(CategoryResource),
        nullable=False,
    )
