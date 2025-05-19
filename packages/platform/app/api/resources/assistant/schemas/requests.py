from app.core.base_models import CamelCaseModel


class CreateAssistantRequest(CamelCaseModel):
    name: str
    description: str | None = None
    voice_id: str | None = None
    first_message: str | None = None
    prompt: str | None = None


class UpdateAssistantSchema(CamelCaseModel):
    name: str | None = None
    description: str | None = None
    voice_id: str | None = None
    first_message: str | None = None
    prompt: str | None = None
