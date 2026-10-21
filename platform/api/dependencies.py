"""
Dependencies for the API
"""

from typing import Annotated

from api.resources.user.models.user import User
from common.schemas.dtos import CurrentUser
from core.database import get_db
from core.exceptions import AuthenticationException
from core.security.tokens import decode_access_token
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class PaginationParams:
    """
    Dependency for pagination parameters.
    """

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> CurrentUser:
    payload = decode_access_token(token)
    user = db.query(User).filter_by(id=payload.sub).first()

    if not user:
        raise AuthenticationException()

    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
        last_login=user.last_login,
        org_id=user.org_id,
    )
