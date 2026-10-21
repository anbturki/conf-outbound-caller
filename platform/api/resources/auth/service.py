from datetime import datetime, timezone
from typing import Annotated

from api.resources.auth.schemas import (
    LoginResponse,
    RegisterRequest,
)
from api.resources.auth.schemas.response import AuthUserResponse
from api.resources.organization.models.organization import Organization
from api.resources.organization.models.user_organization import OrgRoles
from api.resources.organization.service import OrganizationService
from api.resources.user.models.user import User
from api.resources.user.service import UserService
from api.resources.verification import (
    VerificationService,
    VerificationType,
)
from core.config import jwt_config
from core.database import get_db
from core.exceptions import (
    AuthenticationException,
    BadRequestException,
)
from core.security import (
    hash_password,
    verify_password,
)
from core.security.tokens import create_access_token
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from utils.format import convert_to_timedelta

from shared import logger


class AuthService:
    def __init__(
        self,
        db: Session,
        user_service: UserService,
        organization_service: OrganizationService,
        verification_service: VerificationService,
    ):
        self.user_service = user_service
        self.organization_service = organization_service
        self.verification_service = verification_service
        self.db = db

    def is_user_exists(self, email: str) -> bool:
        return self.user_service.get_one_by(email=email) is not None

    def create_org(self, user: User):
        org = self.organization_service.save(
            Organization(
                name=f"{user.first_name}'s Organization",
                owner_id=user.id,
            ),
            commit=False,
        )
        user.org_id = org.id

        self.organization_service.add_member(
            org=org,
            user=user,
            role=OrgRoles.OWNER,
            commit=False,
        )

    def register_user(self, body: RegisterRequest, request: Request):
        first_name, last_name = self._split_name(body.name)
        user = User(
            email=body.email,
            first_name=first_name,
            last_name=last_name,
            terms_accepted=True,
            hashed_password=hash_password(body.password),
        )
        self.user_service.save(user, commit=False)
        self.create_org(user)
        self.db.commit()
        self.db.refresh(user)
        self.verification_service.create_for_email(
            user=user,
            request=request,
        )
        return user

    def validate_user_credentials_or_raise(self, email: str, password: str) -> User:
        user = self.user_service.get_one_by(email=email)
        invalid_credentials_exception = AuthenticationException(
            message="Email or password is incorrect"
        )
        if not user:
            raise invalid_credentials_exception
        if not user.is_email_verified:
            raise AuthenticationException(
                message="Email not verified, please verify your email"
            )
        if not verify_password(password, user.hashed_password):
            raise invalid_credentials_exception
        return user

    def login(self, user: User):
        expires_delta = convert_to_timedelta(jwt_config.access_expiration)
        access_token, expire = create_access_token(str(user.id), expires_delta)
        user.last_login = datetime.now(timezone.utc)
        self.user_service.save(user)
        return LoginResponse(
            access_token=access_token,
            expires_at=expire.isoformat(),
            token_type="Bearer",
            user=AuthUserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                last_login=user.last_login,
                org_id=str(user.org_id),
            ),
        )

    def authenticate(self, email: str, password: str) -> LoginResponse:
        user = self.validate_user_credentials_or_raise(email, password)
        return self.login(user)

    def verify_email(self, token: str, request: Request):
        token = self.verification_service.verify_for_email(
            token=token,
            request=request,
        )
        user = self.user_service.get_one_by(id=token.user_id)
        if not user:
            raise BadRequestException(message="Invalid verification token")
        user.is_email_verified = True
        self.user_service.save(user)
        return user

    def resend_email_verification(self, email: str, request: Request):
        user = self.user_service.get_one_by(email=email)
        if not user:
            logger.info(f"User {email} not found")
            return None
        if user.is_email_verified:
            logger.info(f"User {email} already verified")
            return None

        # Deactivate the existing token
        verification = self.verification_service.find_one_by(
            email=email,
            token_type=VerificationType.EMAIL,
        )

        if verification:
            logger.info(f"Deactivating verification for user {email}")
            self.verification_service.deactivate_for_email(verification)

        return self.verification_service.create_for_email(
            user=user,
            request=request,
        )

    def _split_name(self, name: str) -> tuple[str, str | None]:
        first_name = name.split(" ")[0]
        last_name = " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else None
        return first_name, last_name


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
) -> AuthService:
    return AuthService(
        db=db,
        user_service=UserService(db),
        organization_service=OrganizationService(db),
        verification_service=VerificationService(db),
    )
