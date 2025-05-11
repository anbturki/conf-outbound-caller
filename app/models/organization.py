import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String

from app.core.database import Base


class Organization(Base):
    """Organization model."""

    __tablename__ = "organizations"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Owner reference
    owner_id = Column(UUID, ForeignKey("users.id"))

    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name})>"
