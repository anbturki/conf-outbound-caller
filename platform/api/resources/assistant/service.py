from typing import Annotated

from api.resources.call.models.call import Call
from api.resources.call.services.call import CallService, get_call_service
from core.base_models import BaseQueryParams
from core.base_service import BaseService
from core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from .models.assistant import Assistant
from .schemas.requests import UpdateAssistantSchema


class AssistantService(BaseService[Assistant, UpdateAssistantSchema, BaseQueryParams]):
    def __init__(self, db: Session, call_service: CallService):
        super().__init__(db, Assistant)
        self.call_service = call_service

    def save_call(self, call: Call):
        return self.call_service.save(call)

    def get_call_by_id(self, call_id: str, assistant_id: str) -> Call:
        return self.call_service.get_one_or_raise(call_id, assistant_id=assistant_id)


def get_assistant_service(
    db: Annotated[Session, Depends(get_db)],
    call_service: Annotated[CallService, Depends(get_call_service)],
) -> AssistantService:
    return AssistantService(db, call_service)
