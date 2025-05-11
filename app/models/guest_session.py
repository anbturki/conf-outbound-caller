from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, String

from app.core.database import Base


class GuestSessionStatus(Enum):
    LINKED = "linked"
    UNLINKED = "unlinked"


class GuestSession(Base):
    __tablename__ = "guest_sessions"

    id = Column(String, primary_key=True)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)

    linked_user_id = Column(String, nullable=True)

    # if logged in, deprected this guest session and link it with a user
    session_status = Column(
        Enum(GuestSessionStatus), nullable=False, default=GuestSessionStatus.UNLINKED
    )

    # if not logged in, delete this guest session after 1 hour of inactivity

    created_at = Column(DateTime, default=datetime.now)
    last_active_at = Column(DateTime, default=datetime.now)
