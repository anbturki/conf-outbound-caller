import enum
from typing import Optional
from uuid import UUID

from common.aliases import PGUUID
from core.base_models import MinimalBaseModel
from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class CallPlatform(str, enum.Enum):
    WEB = "web"
    MOBILE = "mobile"


class CallStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    QUEUED = "queued"
    RINGING = "ringing"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    ENDED = "ended"


class EndedReason(str, enum.Enum):
    USER_HANGUP = "user_hangup"
    SYSTEM_HANGUP = "system_hangup"


class Call(MinimalBaseModel):
    __tablename__ = "calls"

    assistant_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("assistants.id"), nullable=False
    )

    platform: Mapped[CallPlatform] = mapped_column(Enum(CallPlatform), nullable=False)
    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus), nullable=False, default=CallStatus.QUEUED
    )

    ended_reason: Mapped[Optional[EndedReason]] = mapped_column(
        Enum(EndedReason), nullable=True
    )

    is_testing: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    testing_user_id: Mapped[UUID] = mapped_column(
        PGUUID, ForeignKey("users.id"), nullable=True
    )

    contact_sid: Mapped[Optional[str]] = mapped_column(String(), nullable=True)

    call_sid: Mapped[Optional[str]] = mapped_column(String(), nullable=True)

    call_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
