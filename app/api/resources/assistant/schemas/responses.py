from datetime import datetime
from uuid import UUID

from app.core.base_models import CamelCaseModel


class MinimalAssistantResponse(CamelCaseModel):
    id: UUID
    name: str
    voice_id: str | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class AssistantResponse(MinimalAssistantResponse):
    voice_id: str | None = None
    first_message: str | None = None
    prompt: str | None = None
