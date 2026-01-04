from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.api.resources.auth.schemas.response import AuthUserResponse
from app.api.utils.responses import GenericResponse, success_response
from app.common.schemas.dtos import CurrentUser

router = APIRouter(prefix="/users")


@router.get("/me", response_model=GenericResponse[AuthUserResponse])
async def me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    return success_response(data=current_user)
