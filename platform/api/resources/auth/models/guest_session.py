from datetime import datetime
from enum import Enum

from common.aliases import PGUUID
from core.database import Base
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class GuestSessionStatus(Enum):
    LINKED = "linked"
    UNLINKED = "unlinked"


class GuestSession(Base):
    __tablename__ = "guest_sessions"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    ip_address = mapped_column(String(), nullable=False)
    user_agent = mapped_column(String(), nullable=False)

    linked_user_id = mapped_column(PGUUID, nullable=True)

    # if logged in, deprecated this guest session and link it with a user
    session_status: Mapped[GuestSessionStatus] = mapped_column(
        nullable=False, default=GuestSessionStatus.UNLINKED
    )

    # if not logged in, delete this guest session after 1 hour of inactivity

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    last_active_at = mapped_column(DateTime(timezone=True), default=datetime.now)
