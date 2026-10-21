from uuid import UUID

from common.aliases import PGUUID
from core.base_models import MinimalBaseModel
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Organization(MinimalBaseModel):
    """Organization model."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Owner reference
    owner_id: Mapped[UUID] = mapped_column(PGUUID, ForeignKey("users.id"))
