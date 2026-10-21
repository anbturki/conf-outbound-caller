import json
import time
from typing import Annotated

from api.resources.assistant.schemas.responses import (
    AssistantResponse,
)
from api.resources.assistant.service import AssistantService, get_assistant_service
from clients import redis_client
from core.config import workers_config
from core.exceptions import AuthenticationException, ResourceNotFoundException
from fastapi import APIRouter, Depends
from fastapi.params import Security
from fastapi.security import APIKeyHeader

from shared import logger

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key is None or api_key != workers_config.voip_api_key:
        raise AuthenticationException(message="Invalid API key")
    return api_key


router = APIRouter(
    prefix="/workers", tags=["Workers Supplier"], dependencies=[Depends(verify_api_key)]
)


@router.get("/assistants/{assistant_id}")
async def get_assistant(
    assistant_id: str,
    assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
):
    start_time = time.time()
    assistant = redis_client.get(f"assistants:{assistant_id}")
    if assistant is None:
        logger.info(f"Assistant {assistant_id} not found in Redis, fetching from DB")
        assistant = assistant_service.get_by_id(assistant_id)
        if assistant is None:
            raise ResourceNotFoundException(
                resource_type="assistant", resource_id=assistant_id
            )
        logger.info(f"Assistant {assistant_id} found in DB, caching in Redis")
        redis_client.set(
            f"assistants:{assistant_id}",
            AssistantResponse.model_validate(assistant).model_dump_json(),
        )
    else:
        logger.info(f"Assistant {assistant_id} found in Redis")
        assistant = json.loads(assistant)
    end_time = time.time()

    # convert to seconds
    time_taken = (end_time - start_time) * 1000

    logger.info(f"Time taken to fetch assistant {assistant_id}: {time_taken} ms")
    return {
        "assistant": assistant,
        "time_taken": time_taken,
    }
