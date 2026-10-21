from uuid import UUID

from common.aliases import PGUUID
from core.base_models import MinimalBaseModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column


class User(MinimalBaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean(), default=False)

    org_id: Mapped[UUID] = mapped_column(PGUUID, nullable=True)

    terms_accepted: Mapped[bool] = mapped_column(Boolean(), default=False)

    last_login = Column(DateTime(), nullable=True)

    @property
    def name(self):
        return (
            self.first_name + " " + self.last_name
            if self.last_name is not None
            else self.first_name
        )
