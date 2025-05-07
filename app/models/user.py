from datetime import datetime
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.base import Base


user_organization = Table(
    "user_organization",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("organization_id", UUID, ForeignKey("organizations.id"), primary_key=True),
    Column("role", String(50), default="member"),  # Role in the organization
    Column("created_at", DateTime, default=datetime.now(datetime.UTC)),
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_email_verified = Column(Boolean, default=False)

    password_reset_token = Column(String, nullable=True)
    password_reset_token_expires_at = Column(DateTime, nullable=True)

    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.now(datetime.UTC))

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"
