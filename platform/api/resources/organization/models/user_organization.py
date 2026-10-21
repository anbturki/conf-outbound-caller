import enum
from datetime import datetime, timezone
from uuid import UUID

from common.aliases import PGUUID
from core.database import Base
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class OrgRoles(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"


class UserOrganization(Base):
    __tablename__ = "user_organization"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("users.id"), primary_key=True
    )
    org_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("organizations.id"), primary_key=True
    )
    role: Mapped[OrgRoles] = mapped_column(Enum(OrgRoles), default=OrgRoles.MEMBER)
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
