import enum
from datetime import datetime, timezone

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey

from app.core.database import Base


class OrgRoles(enum.Enum):
    OWNER = "owner"
    MEMBER = "member"


class UserOrganization(Base):
    __tablename__ = "user_organization"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"), primary_key=True)
    role = Column(Enum(OrgRoles), default=OrgRoles.MEMBER)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
