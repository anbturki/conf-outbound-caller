import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    String,
)

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_email_verified = Column(Boolean, default=False)

    active_organization_id = Column(UUID, nullable=True)

    terms_accepted = Column(Boolean, default=False)

    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    @property
    def name(self):
        return (
            self.first_name + " " + self.last_name
            if self.last_name is not None
            else self.first_name
        )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"
