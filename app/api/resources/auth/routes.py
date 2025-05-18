from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.utils.responses import (
    created_response,
    success_response,
)
from app.common.schemas.success_responses import GenericResponse, MessageResponse
from app.core.exceptions import ResourceExistsException

from .schemas import (
    EmailRequest,
    LoginResponse,
    RegisterRequest,
    VerifyEmailRequest,
)
from .service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    body: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
):
    # Create user
    if auth_service.is_user_exists(body.email):
        raise ResourceExistsException(
            resource_type="User",
            identifier="email",
            identifier_value=body.email,
        )
    auth_service.register_user(body, request)
    return created_response(
        message="User registered successfully, please verify your email",
    )


@router.post("/login", response_model=GenericResponse[LoginResponse])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return success_response(
        data=auth_service.authenticate(
            email=form_data.username,
            password=form_data.password,
        )
    )


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    body: VerifyEmailRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
):
    auth_service.verify_email(
        token=body.token,
        request=request,
    )
    return success_response(
        message="Email verified successfully",
    )


@router.post("/resend-email-verification", response_model=MessageResponse)
async def resend_email_verification(
    body: EmailRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
):
    auth_service.resend_email_verification(
        email=body.email,
        request=request,
    )

    return success_response(
        message="If you have not verified your email, you will receive a new verification email",
    )
