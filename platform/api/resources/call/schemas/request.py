from uuid import UUID

from core.base_models import CamelCaseModel


class CallCreate(CamelCaseModel):
    assistant_id: UUID
    phone_number_id: str


class CallCreateFromWeb(CamelCaseModel):
    assistant_id: UUID
