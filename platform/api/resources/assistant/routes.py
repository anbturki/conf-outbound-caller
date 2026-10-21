from typing import Annotated
from uuid import UUID

from api.resources.assistant.schemas.responses import (
    AssistantResponse,
    AssistantTestingResponse,
    MinimalAssistantResponse,
)
from api.resources.call.models.call import Call, CallPlatform
from api.utils.responses import (
    created_response,
    paginated_response,
    success_response,
)
from clients.lkapi import create_access_token, create_explicit_dispatch
from common.schemas.dtos import CurrentUser
from common.schemas.success_responses import (
    GenericResponse,
    MessageResponse,
    PagedResponse,
)
from core.base_models import BaseQueryParams
from fastapi import APIRouter, Depends, status

from shared.definitions import AssistantDispatchMetadata
from shared.utils import json_dumps

from ...dependencies import get_current_user
from .models.assistant import Assistant
from .schemas.requests import (
    AssistantDispatchRequest,
    CreateAssistantRequest,
    UpdateAssistantSchema,
)
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
    assistant = Assistant()
    assistant.name = body.name
    assistant.description = body.description
    assistant.voice_id = body.voice_id
    assistant.first_message = body.first_message
    assistant.prompt = body.prompt
    assistant.org_id = current_user.org_id
    assistant.user_id = current_user.id
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
        search_fields=["name", "description", "prompt"],
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
    assistant_id: UUID,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = assistant_service.get_one_or_raise(
        assistant_id,
        org_id=current_user.org_id,
    )

    return success_response(data=assistant, response_model=AssistantResponse)


@router.put("/{assistant_id}", response_model=MessageResponse)
async def update_assistant(
    assistant_id: UUID,
    body: UpdateAssistantSchema,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant_service.get_one_or_raise(
        assistant_id,
        org_id=current_user.org_id,
    )

    assistant_service.update_by_id(assistant_id, body)
    return success_response(message="Assistant updated successfully")


@router.delete("/{assistant_id}", response_model=MessageResponse)
async def delete_assistant(
    assistant_id: UUID,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant_service.get_one_or_raise(
        assistant_id,
        org_id=current_user.org_id,
    )
    assistant_service.delete_by_id(assistant_id)
    return success_response(message="Assistant deleted successfully")


@router.post(
    "/{assistant_id}/test", response_model=GenericResponse[AssistantTestingResponse]
)
async def test_assistant(
    assistant_id: UUID,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    assistant = assistant_service.get_one_or_raise(
        assistant_id,
        org_id=current_user.org_id,
    )

    call = Call()
    call.assistant_id = assistant.id
    call.is_testing = True
    call.testing_user_id = current_user.id
    call.platform = CallPlatform.WEB

    assistant_service.save_call(call)

    dispatch_metadata = AssistantDispatchMetadata(
        assistant_id=str(assistant.id),
        sid=str(call.id),
        participant_id=str(current_user.id),
    )

    await create_explicit_dispatch(
        agent_name="voip-worker",
        room=str(call.id),
        metadata=json_dumps(dispatch_metadata),
    )

    token = create_access_token(
        room=str(call.id),
        user_id=str(current_user.id),
        user_name=current_user.name,
    )

    return success_response(
        message="Session initiated successfully",
        data=AssistantTestingResponse(
            access_token=token,
            sid=str(call.id),
        ),
    )


@router.post("/{assistant_id}/dispatch")
async def request_assistant_dispatch(
    assistant_id: UUID,
    body: AssistantDispatchRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
):
    assistant = assistant_service.get_one_or_raise(
        assistant_id,
        org_id=current_user.org_id,
    )
    call = assistant_service.get_call_by_id(body.call_id, str(assistant.id))

    dispatch_metadata = AssistantDispatchMetadata(
        assistant_id=str(assistant.id),
        sid=str(call.id),
        participant_id=str(current_user.id),
    )

    await create_explicit_dispatch(
        agent_name="voip-worker",
        room=str(call.id),
        metadata=json_dumps(dispatch_metadata),
    )

    return call
