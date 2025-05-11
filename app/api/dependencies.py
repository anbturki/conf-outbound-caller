"""
Dependencies for the API
"""

from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AuthenticationException
from app.core.security import decode_access_token, oauth2_scheme
from app.models.user import User
from app.schemas.auth import AuthenticatedUser


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
) -> AuthenticatedUser:
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.sub).first()
    if not user:
        raise AuthenticationException(message="User not found")
    return AuthenticatedUser(
        id=str(user.id),
        email=user.email,
        name=user.name,
        last_login=user.last_login.isoformat(),
        active_organization_id=user.active_organization_id,
    )
