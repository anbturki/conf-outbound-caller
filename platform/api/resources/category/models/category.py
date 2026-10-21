import enum

from core.base_models import BaseDBModel
from sqlalchemy import (
    Enum,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column


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

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    # Category can belong to a resource, for example, a persona, assistant, knowledge base, etc.
    resource: Mapped[CategoryResource] = mapped_column(
        Enum(CategoryResource),
        nullable=False,
    )
