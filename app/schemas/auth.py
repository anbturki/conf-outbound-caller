from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.utils.validators import StrongPassword

######## Responses ########


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: str


class UserResponse(BaseModel):
    email: EmailStr
    name: str
    last_login: str


class LoginResponse(TokenResponse):
    user: UserResponse


######## Requests ########


class RegisterRequest(BaseModel):
    # should be true
    terms_accepted: bool
    name: str
    email: EmailStr
    password: StrongPassword

    @field_validator("terms_accepted")
    @classmethod
    def check_terms_accepted(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Terms must be accepted")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class VerifyEmailRequest(BaseModel):
    token: str


######## Models ########


class AuthenticatedUser(BaseModel):
    id: str
    email: EmailStr
    name: str
    last_login: str
    active_organization_id: str | None


class TokenPayload(BaseModel):
    sub: str
    exp: datetime


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    new_password_confirm: str


class EmailVerificationRequest(BaseModel):
    token: str
