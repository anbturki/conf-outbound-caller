import json
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.resources.assistant.schemas.responses import (
    AssistantResponse,
    MinimalAssistantResponse,
)
from app.api.utils.responses import (
    created_response,
    paginated_response,
    success_response,
)
from app.clients.lkapi import create_explicit_dispatch
from app.common.schemas.dtos import CurrentUser
from app.common.schemas.success_responses import (
    GenericResponse,
    MessageResponse,
    PagedResponse,
)
from app.core.base_models import BaseQueryParams

from ...dependencies import get_current_user
from .models.assistant import Assistant
from .schemas.requests import CreateAssistantRequest, UpdateAssistantSchema
from .service import AssistantService, get_assistant_service

router = APIRouter(prefix="/assistants", tags=["assistants"])


@router.post(
    "/",
    response_model=GenericResponse[MinimalAssistantResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_assistant(
    body: CreateAssistantRequest,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = Assistant(
        name=body.name,
        description=body.description,
        voice_id=body.voice_id,
        first_message=body.first_message,
        prompt=body.prompt,
        org_id=current_user.org_id,
        user_id=current_user.id,
    )
    assistant_service.save(assistant)
    return created_response(
        message="Assistant created successfully",
        data=assistant,
        response_model=MinimalAssistantResponse,
    )


@router.get("/", response_model=PagedResponse[MinimalAssistantResponse])
async def list_assistants(
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    query_params: Annotated[BaseQueryParams, Depends()],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistants, total = assistant_service.paginate(
        query_params,
        base_filters={"org_id": current_user.org_id},
    )

    return paginated_response(
        items=assistants,
        total=total,
        page=query_params.page,
        limit=query_params.limit,
        response_model=MinimalAssistantResponse,
    )


@router.get("/{assistant_id}")
async def get_assistant(
    assistant_id: str,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = assistant_service.get_one_or_raise(
        assistant_id,
        current_user.org_id,
    )

    return success_response(data=assistant, response_model=AssistantResponse)


@router.put("/{assistant_id}", response_model=MessageResponse)
async def update_assistant(
    assistant_id: str,
    body: UpdateAssistantSchema,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant_service.get_one_or_raise(
        assistant_id,
        current_user.org_id,
    )

    assistant_service.update_by_id(assistant_id, body)
    return success_response(message="Assistant updated successfully")


@router.delete("/{assistant_id}", response_model=MessageResponse)
async def delete_assistant(
    assistant_id: str,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant_service.get_one_or_raise(
        assistant_id,
        current_user.org_id,
    )
    assistant_service.delete_by_id(assistant_id)
    return success_response(message="Assistant deleted successfully")


@router.post("/{assistant_id}/test")
async def test_assistant(
    assistant_id: str,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = assistant_service.get_one_or_raise(
        assistant_id,
        current_user.org_id,
    )

    await create_explicit_dispatch(
        agent_name="voip-worker-assistant",
        room=str(uuid.uuid4()),
        metadata=json.dumps({"assistant_id": str(assistant.id)}),
    )

    return success_response(message="Assistant testing started successfully")
