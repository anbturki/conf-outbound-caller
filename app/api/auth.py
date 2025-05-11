from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user
from app.api.utils.responses import (
    created_response,
    success_response,
)
from app.schemas.auth import (
    AuthenticatedUser,
    LoginResponse,
    RegisterRequest,
    VerifyEmailRequest,
)
from app.schemas.custom import AuthenticatedUserResponse
from app.schemas.responses import GenericResponse, MessageResponse
from app.services.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
    summary="Register a new user",
    response_description="User registered successfully",
)
async def register(
    body: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
):
    # Create user
    auth_service.throw_if_user_exists(body.email)
    user = auth_service.register_user(body)
    auth_service.create_verification_token(
        user=user,
        ip=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )
    return created_response(
        message="User registered successfully",
    )


@router.post("/login", response_model=GenericResponse[LoginResponse])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    user = auth_service.validate_user_credentials(
        form_data.username, form_data.password
    )
    return success_response(data=auth_service.authenticate(user))


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    body: VerifyEmailRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
):
    auth_service.verify_email(
        token=body.token,
        ip=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )
    return success_response(
        message="Email verified successfully",
    )


@router.get("/me", response_model=AuthenticatedUserResponse)
async def me(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    """
    Get the current user
    """
    return success_response(data=current_user)
