from datetime import datetime

from core.base_models import CamelCaseModel
from pydantic import EmailStr


class TokenResponse(CamelCaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: str


class AuthUserResponse(CamelCaseModel):
    id: str
    org_id: str
    email: EmailStr
    name: str
    last_login: datetime


class LoginResponse(TokenResponse):
    user: AuthUserResponse
