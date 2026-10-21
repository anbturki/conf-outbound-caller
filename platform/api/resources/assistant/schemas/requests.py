from typing import Optional

from core.base_models import CamelCaseModel


class CreateAssistantRequest(CamelCaseModel):
    name: str
    description: Optional[str] = None
    voice_id: Optional[str] = None
    first_message: Optional[str] = None
    prompt: Optional[str] = None


class UpdateAssistantSchema(CamelCaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    voice_id: Optional[str] = None
    first_message: Optional[str] = None
    prompt: Optional[str] = None


class AssistantDispatchRequest(CamelCaseModel):
    call_id: str
