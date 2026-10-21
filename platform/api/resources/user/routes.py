from typing import Annotated

from api.dependencies import get_current_user
from api.resources.auth.schemas.response import AuthUserResponse
from api.utils.responses import GenericResponse, success_response
from common.schemas.dtos import CurrentUser
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users")


@router.get("/me", response_model=GenericResponse[AuthUserResponse])
async def me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    return success_response(data=current_user)
