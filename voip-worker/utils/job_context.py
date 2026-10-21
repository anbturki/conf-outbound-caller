from livekit.agents import JobContext

from shared.definitions import AssistantDispatchMetadata
from shared.logger import logger
from shared.utils import json_loads


def extract_job_metadata(ctx: JobContext) -> AssistantDispatchMetadata | None:
    logger.info(f"Extracting job metadata: {ctx.job.metadata}")
    try:
        if not ctx.job.metadata:
            return None
        return json_loads(ctx.job.metadata, cls=AssistantDispatchMetadata)
    except Exception as e:
        logger.error(f"Error extracting job metadata: {e}")
        return None
