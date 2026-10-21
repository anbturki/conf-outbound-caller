from typing import Annotated

from api.dependencies import get_current_user
from api.resources.assistant import AssistantService, get_assistant_service
from common.schemas.dtos import CurrentUser
from fastapi import APIRouter, Depends
from livekit.api import ListRoomsRequest, LiveKitAPI

from .schemas.request import CallCreate

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post("/")
async def create_call(
    call_create: CallCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    # Check assistant
    # Check phone number if provided
    # Create Call record
    # Dispatch job to voip worker
    return call_create


@router.post("/web")
async def create_call_from_web(
    call_create: CallCreate,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = assistant_service.get_one_or_raise(
        call_create.assistant_id, org_id=current_user.org_id
    )

    return assistant
    # Check assistant
    # Create Call record
    # Create User Token
    # Dispatch Agent
    # Return User Token


@router.get("/{call_id}")
async def get_call(call_id: str):
    return {"message": "Hello, World!"}


@router.get("/")
async def list_calls():
    lkapi = LiveKitAPI()
    rooms = await lkapi.room.list_rooms(ListRoomsRequest())
    await lkapi.aclose()
    return rooms.rooms
