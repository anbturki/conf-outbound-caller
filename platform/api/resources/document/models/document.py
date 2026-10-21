from typing import Optional
from uuid import UUID

from common.aliases import PGUUID
from core.base_models import BaseDBModel
from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Document(BaseDBModel):
    __tablename__ = "documents"

    name: Mapped[str] = mapped_column(String(), nullable=False)
    original_name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    file_type: Mapped[str] = mapped_column(String(), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer(), nullable=False)
    file_path: Mapped[str] = mapped_column(String(), nullable=False)
    file_ext: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    category_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID, ForeignKey("categories.id"), nullable=True
    )

    file_metadata: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
