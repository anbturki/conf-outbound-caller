from typing import Annotated

from app.core.base_service import BaseService
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.call import Call


class CallService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Call)


def get_call_service(db: Annotated[Session, Depends(get_db)]) -> CallService:
    return CallService(db)
