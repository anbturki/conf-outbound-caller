import enum
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from common.aliases import PGUUID
from core.base_models import MinimalBaseModel
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column


class VerificationStatus(str, enum.Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    VERIFIED = "verified"
    EXPIRED = "expired"


class VerificationType(str, enum.Enum):
    EMAIL = "email"
    PHONE = "phone"


class Verification(MinimalBaseModel):
    __tablename__ = "verifications"

    __table_args__ = (
        # Create unique constraints based on token_type
        UniqueConstraint("token_type", "email", "token", name="uq_email_token"),
        UniqueConstraint("token_type", "phone_number", "token", name="uq_phone_token"),
        # Add indexes for better query performance
        Index("idx_token_status", "token", "status"),
        Index("idx_user_tokens", "user_id", "token_type", "status"),
        Index("idx_expires_at", "expires_at"),
    )

    token: Mapped[str] = mapped_column(String(128), nullable=False)
    token_type: Mapped[VerificationType] = mapped_column(
        Enum(VerificationType), nullable=False
    )

    # Store identifier based on token type
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Set reasonable default expiration (e.g., 24 hours)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: func.now() + func.interval("24 hours"),
    )

    # Set max attempts to prevent brute force
    attempts: Mapped[int] = mapped_column(Integer(), default=0)

    status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus),
        default=VerificationStatus.ACTIVE,
        nullable=False,
    )

    # No need for separate enum since status covers the same information
    deactivation_reason: Mapped[Optional[str]] = mapped_column(String(), nullable=True)

    is_verified: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Security tracking
    created_from_ip: Mapped[Optional[str]] = mapped_column(
        String(45), nullable=True
    )  # IPv6 support
    created_from_user_agent: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    verified_from_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    verified_from_user_agent: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("users.id"), nullable=False
    )

    @property
    def is_valid(self):
        return (
            self.status == VerificationStatus.ACTIVE
            and not self.is_expired
            and not self.is_verified
            and self.attempts < self.max_attempts
        )

    @property
    def is_expired(self):
        return self.expires_at < datetime.now(timezone.utc)

    @property
    def is_deactivated(self):
        return self.status == VerificationStatus.DEACTIVATED

    def increment_attempts(self) -> None:
        """Increment attempt counter and update status if max reached"""
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.status = VerificationStatus.DEACTIVATED
            self.deactivation_reason = "Maximum attempts exceeded"

    def mark_as_verified(
        self, ip: Optional[str] = None, user_agent: Optional[str] = None
    ) -> None:
        """Mark the token as verified with tracking information"""
        self.is_verified = True
        self.status = VerificationStatus.VERIFIED
        self.verified_at = func.now()
        self.verified_from_ip = ip
        self.verified_from_user_agent = user_agent

    def mark_as_expired(self) -> None:
        """Mark the token as expired"""
        self.status = VerificationStatus.EXPIRED
        self.deactivation_reason = "Token expired"

    def create_email_verification_token(
        self,
        email: str,
        user_id: UUID,
        ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        self.created_from_ip = ip
        self.created_from_user_agent = user_agent
        self.token_type = VerificationType.EMAIL
        self.email = email
        self.user_id = user_id
        self.token = str(uuid.uuid4())
        self.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        self.status = VerificationStatus.ACTIVE
        self.is_verified = False
        self.verified_at = None

    def __repr__(self):
        return f"<VerificationToken(id={self.id}, type={self.token_type.value}, status={self.status.value})>"
