import enum

from app.common.aliases import PGUUID
from app.core.base_models import MinimalBaseModel
from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB


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

    assistant_id = Column(PGUUID, ForeignKey("assistants.id"), nullable=False)

    platform = Column(Enum(CallPlatform), nullable=False)
    status = Column(Enum(CallStatus), nullable=False, default=CallStatus.QUEUED)

    ended_reason = Column(Enum(EndedReason), nullable=True)

    is_testing = Column(Boolean, nullable=False, default=False)
    testing_user_id = Column(PGUUID, ForeignKey("users.id"), nullable=True)

    contact_sid = Column(String, nullable=True)

    call_sid = Column(String, nullable=True)

    call_metadata = Column(JSONB, nullable=True)
