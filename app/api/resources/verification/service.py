from fastapi import Request
from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.orm import Session

from app.api.resources.user.models.user import User
from app.api.resources.verification import (
    Verification,
    VerificationStatus,
)
from app.core.exceptions import BadRequestException


class VerificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_for_email(
        self,
        user: User,
        request: Request,
    ) -> Verification:
        token = Verification()
        token.create_email_verification_token(
            email=user.email,
            user_id=user.id,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
        )
        return self.save(token)

    def save(self, token: Verification) -> Verification:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def verify_for_email(self, token: str, request: Request) -> Verification:
        return self.verify(
            token=token,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
            token_type="email",
        )

    def find_one(self, *criterion: ColumnExpressionArgument[bool]) -> Verification:
        return self.db.query(Verification).filter(*criterion).first()

    def find_one_by(self, **kwargs) -> Verification:
        return self.db.query(Verification).filter_by(**kwargs).first()

    def deactivate_for_email(self, verification: Verification) -> None:
        verification.status = VerificationStatus.DEACTIVATED
        verification.deactivation_reason = "User requested to resend email verification"
        self.db.commit()
        self.db.refresh(verification)

    def verify(
        self, token: str, ip: str, user_agent: str, token_type: str
    ) -> Verification:
        invalid_token_exception = BadRequestException(
            message="Invalid verification token or expired"
        )

        token = (
            self.db.query(Verification)
            .filter(
                Verification.token == token,
                Verification.status != VerificationStatus.VERIFIED,
                Verification.token_type == token_type,
            )
            .first()
        )

        if not token:
            raise invalid_token_exception

        if token.status == VerificationStatus.ACTIVE and not token.is_expired:
            token.mark_as_verified(ip=ip, user_agent=user_agent)
            self.db.commit()
            self.db.refresh(token)
            return token

        if token.status == VerificationStatus.ACTIVE and token.is_expired:
            token.mark_as_expired()
            self.db.commit()
            self.db.refresh(token)
            raise invalid_token_exception

        raise invalid_token_exception
