from sqlalchemy import Boolean, Column, ForeignKey, String

from app.common.aliases import PGUUID
from app.core.base_models import MinimalBaseModel


class Organization(MinimalBaseModel):
    """Organization model."""

    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Owner reference
    owner_id = Column(PGUUID, ForeignKey("users.id"))
