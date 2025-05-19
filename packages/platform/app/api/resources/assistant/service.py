from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.resources.call.models.call import Call
from app.api.resources.call.services.call import CallService, get_call_service
from app.core.base_models import BaseQueryParams
from app.core.base_service import BaseService
from app.core.database import get_db

from .models.assistant import Assistant
from .schemas.requests import UpdateAssistantSchema


class AssistantService(BaseService[Assistant, UpdateAssistantSchema, BaseQueryParams]):
    def __init__(self, db: Session, call_service: CallService):
        super().__init__(db, Assistant)
        self.call_service = call_service

    def create_call(self, call: Call):
        return self.call_service.save(call)


def get_assistant_service(
    db: Annotated[Session, Depends(get_db)],
    call_service: Annotated[CallService, Depends(get_call_service)],
) -> AssistantService:
    return AssistantService(db, call_service)
