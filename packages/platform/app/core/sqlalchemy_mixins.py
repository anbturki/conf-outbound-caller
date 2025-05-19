import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, func

from app.common.aliases import PGUUID


class TimestampMixin:
    """Mixin for timestamp columns."""

    __abstract__ = True  # Extendable only

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class UserIdMixin:
    """Mixin for user_id column."""

    __abstract__ = True  # Extendable only

    user_id = Column(PGUUID, ForeignKey("users.id"), nullable=False)


class IDMixin:
    """Mixin for id column."""

    __abstract__ = True  # Extendable only

    id = Column(
        PGUUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )


class OrgIdMixin:
    """Mixin for org_id column."""

    __abstract__ = True  # Extendable only

    org_id = Column(PGUUID, ForeignKey("organizations.id"), nullable=False)
