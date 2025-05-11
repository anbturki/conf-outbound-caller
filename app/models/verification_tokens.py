import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)

from app.core.database import Base


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    __table_args__ = (
        # Create unique constraints based on token_type
        UniqueConstraint("token_type", "email", "token", name="uq_email_token"),
        UniqueConstraint("token_type", "phone_number", "token", name="uq_phone_token"),
        # Add indexes for better query performance
        Index("idx_token_status", "token", "status"),
        Index("idx_user_tokens", "user_id", "token_type", "status"),
        Index("idx_expires_at", "expires_at"),
    )

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    token = Column(String(128), nullable=False)
    token_type = Column(String, nullable=False)

    # Store identifier based on token type
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)

    # Set reasonable default expiration (e.g., 24 hours)
    expires_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=24),
    )

    # Set max attempts to prevent brute force
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=5)

    status = Column(
        String,
        default="active",
        nullable=False,
    )

    # No need for separate enum since status covers the same information
    deactivation_reason = Column(String, nullable=True)

    is_verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime, nullable=True)

    # Security tracking
    created_from_ip = Column(String(45), nullable=True)  # IPv6 support
    created_from_user_agent = Column(String(255), nullable=True)
    verified_from_ip = Column(String(45), nullable=True)
    verified_from_user_agent = Column(String(255), nullable=True)

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    @property
    def is_valid(self) -> bool:
        return (
            self.status == "active"
            and not self.is_expired
            and not self.is_verified
            and self.attempts < self.max_attempts
        )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(timezone.utc)

    @property
    def is_deactivated(self) -> bool:
        return self.status == "deactivated"

    def increment_attempts(self) -> None:
        """Increment attempt counter and update status if max reached"""
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.status = "deactivated"
            self.deactivation_reason = "Maximum attempts exceeded"

    def mark_as_verified(
        self, ip: Optional[str] = None, user_agent: Optional[str] = None
    ) -> None:
        """Mark the token as verified with tracking information"""
        self.is_verified = True
        self.status = "verified"
        self.verified_at = datetime.now(timezone.utc)
        self.verified_from_ip = ip
        self.verified_from_user_agent = user_agent

    def mark_as_expired(self) -> None:
        """Mark the token as expired"""
        self.status = "expired"
        self.deactivation_reason = "Token expired"

    def create_email_verification_token(
        self,
        email: str,
        user_id: str,
        ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        print(email, user_id, ip, user_agent)
        self.created_from_ip = ip
        self.created_from_user_agent = user_agent
        self.token_type = "email"
        self.email = email
        self.user_id = user_id
        self.token = uuid.uuid4()
        self.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        self.status = "active"
        self.is_verified = False
        self.verified_at = None

    def __repr__(self):
        return f"<VerificationToken(id={self.id}, type={self.token_type.value}, status={self.status.value})>"
