from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import (
    AuthenticationException,
    BadRequestException,
    ValidationException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.associations import UserOrganization
from app.models.organization import Organization
from app.models.user import User
from app.models.verification_tokens import (
    VerificationToken,
)
from app.schemas.auth import LoginResponse, RegisterRequest, TokenResponse, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def throw_if_user_exists(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            raise ValidationException(
                message="User with this email already exists˝",
                field_errors={
                    "email": {
                        "code": "USER_ALREADY_EXISTS",
                        "message": "User with this email already exists",
                    }
                },
            )

    def commit(self):
        self.db.commit()

    def create_user(self, body: RegisterRequest):
        first_name, last_name = self._split_name(body.name)
        user = User(
            email=body.email,
            first_name=first_name,
            last_name=last_name,
            terms_accepted=True,
            hashed_password=hash_password(body.password),
        )
        self.db.add(user)
        self.db.flush()
        return user

    def create_organization(self, user: User):
        organization = Organization(
            name=f"{user.first_name}'s Organization",
            owner_id=user.id,
        )
        self.db.add(organization)
        self.db.flush()
        return organization

    def register_user(self, body: RegisterRequest) -> User:
        user = self.create_user(body)
        organization = self.create_organization(user)

        # Add user to organization
        user_organization = UserOrganization(
            user_id=user.id,
            organization_id=organization.id,
            role="owner",
        )
        user.active_organization_id = organization.id
        self.db.add(user_organization)
        self.commit()
        self.db.refresh(user)
        return user

    def validate_user_credentials(self, email: str, password: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise AuthenticationException(message="Email or password is incorrect")
        if not user.is_email_verified:
            raise AuthenticationException(message="Email not verified")
        if not verify_password(password, user.hashed_password):
            raise AuthenticationException(message="Email or password is incorrect")
        return user

    def create_verification_token(
        self, user: User, ip: str, user_agent: str
    ) -> VerificationToken:
        token = VerificationToken()
        token.create_email_verification_token(
            email=user.email, user_id=user.id, ip=ip, user_agent=user_agent
        )

        self.db.add(token)
        self.commit()
        self.db.refresh(token)
        return token

    def verify_verification_token(
        self, token: str, ip: str, user_agent: str, token_type: str
    ) -> VerificationToken:
        token = (
            self.db.query(VerificationToken)
            .filter(
                VerificationToken.token == token,
                VerificationToken.status != "verified",
                VerificationToken.token_type == token_type,
            )
            .first()
        )

        if not token:
            raise BadRequestException(message="Invalid verification token")

        if token.status == "active" and not token.is_expired:
            token.mark_as_verified(ip=ip, user_agent=user_agent)
            self.commit()
            self.db.refresh(token)
            return token

        if token.status == "active" and token.is_expired:
            token.mark_as_expired()
            self.commit()
            self.db.refresh(token)
            raise ValidationException(message="Verification token expired")

        raise BadRequestException(message="Invalid verification token")

    def authenticate(self, user: User) -> LoginResponse:
        token = self.create_access_token(user.id)
        user.last_login = datetime.now(timezone.utc)
        self.commit()
        self.db.refresh(user)
        return LoginResponse(
            access_token=token.access_token,
            expires_at=token.expires_at,
            token_type=token.token_type,
            user=UserResponse(
                email=user.email,
                name=user.name,
                last_login=user.last_login.isoformat(),
            ),
        )

    def find_user_by_id(self, user_id: str) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_access_token(self, user_id: str) -> TokenResponse:
        """Create access token"""
        access_token, expire = create_access_token(str(user_id))
        return TokenResponse(
            access_token=access_token,
            expires_at=expire.isoformat(),
        )

    def create_refresh_token(self, user_id: str) -> str:
        """Create refresh token"""
        return create_refresh_token(str(user_id))

    def verify_email(self, token: str, ip: str, user_agent: str):
        token = self.verify_verification_token(
            token, ip=ip, user_agent=user_agent, token_type="email"
        )
        user = self.db.query(User).filter(User.id == token.user_id).first()
        if not user:
            raise BadRequestException(message="Invalid verification token")
        user.is_email_verified = True
        self.commit()
        self.db.refresh(user)
        return user

    def _split_name(self, name: str) -> tuple[str, str | None]:
        first_name = name.split(" ")[0]
        last_name = " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else None
        return first_name, last_name


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(db)
