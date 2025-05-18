import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey

from app.common.aliases import PGUUID
from app.core.database import Base


class OrgRoles(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"


class UserOrganization(Base):
    __tablename__ = "user_organization"

    user_id = Column(PGUUID, ForeignKey("users.id"), primary_key=True)
    org_id = Column(PGUUID, ForeignKey("organizations.id"), primary_key=True)
    role = Column(Enum(OrgRoles), default=OrgRoles.MEMBER)
    joined_at = Column(DateTime, default=datetime.now(timezone.utc))
