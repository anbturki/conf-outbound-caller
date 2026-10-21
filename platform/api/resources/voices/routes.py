from clients.elevenlabs import get_voices
from common.schemas.success_responses import GenericResponse
from fastapi import APIRouter

router = APIRouter(prefix="/voices", tags=["voices"])


@router.get("/")
async def list_voices():
    voices = get_voices()
    return GenericResponse(
        data=voices,
        message="Voices fetched successfully",
    )
