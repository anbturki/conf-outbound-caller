from pydantic import EmailStr, field_validator

from app.core.base_models import CamelCaseModel
from app.utils.validators import StrongPassword


class RegisterRequest(CamelCaseModel):
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


class LoginRequest(CamelCaseModel):
    email: EmailStr
    password: str


class EmailRequest(CamelCaseModel):
    email: EmailStr


class VerifyEmailRequest(CamelCaseModel):
    # token cannot be empty
    token: str

    @field_validator("token")
    @classmethod
    def check_token(cls, value: str) -> str:
        if not value:
            raise ValueError("Token cannot be empty")
        return value


class EmailVerificationRequest(CamelCaseModel):
    token: str
