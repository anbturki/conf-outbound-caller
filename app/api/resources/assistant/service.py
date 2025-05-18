from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_models import BaseQueryParams
from app.core.base_service import BaseService
from app.core.database import get_db

from .models.assistant import Assistant
from .schemas.requests import UpdateAssistantSchema


class AssistantService(BaseService[Assistant, UpdateAssistantSchema, BaseQueryParams]):
    def __init__(self, db: Session):
        super().__init__(db, Assistant)


def get_assistant_service(db: Annotated[Session, Depends(get_db)]) -> AssistantService:
    return AssistantService(db)
