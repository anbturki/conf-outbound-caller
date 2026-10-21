from typing import Annotated, Any

from core.database import get_db
from fastapi import Depends
from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.orm import Session

from .models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_one(self, *criterion: ColumnExpressionArgument[bool]) -> User:
        return self.db.query(User).filter(*criterion).first()

    def get_one_by(self, **kwargs: Any) -> User:
        return self.db.query(User).filter_by(**kwargs).first()

    def save(self, user: User, commit: bool = True) -> User:
        self.db.add(user)
        if commit:
            self.db.commit()
            self.db.refresh(user)
        else:
            self.db.flush([user])
        return user


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(db)
