import uuid
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from common.aliases import PGUUID
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin for timestamp columns."""

    __abstract__ = True  # Extendable only

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class UserIdMixin:
    """Mixin for user_id column."""

    __abstract__ = True  # Extendable only

    user_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("users.id"), nullable=False
    )


class IDMixin:
    """Mixin for id column."""

    __abstract__ = True  # Extendable only

    id: Mapped[UUID] = mapped_column(
        PGUUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )


class OrgIdMixin:
    """Mixin for org_id column."""

    __abstract__ = True  # Extendable only

    org_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("organizations.id"), nullable=False
    )
