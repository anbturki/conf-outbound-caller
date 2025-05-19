import json

from livekit.agents import JobContext
from schemas.metadata import AssistantJobMetadata
from shared.logger import logger


def extract_job_metadata(ctx: JobContext) -> AssistantJobMetadata:
    try:
        logger.info(f"Job metadata - parsing: {ctx.job.metadata}")
        job_metadata = json.loads(ctx.job.metadata)
        logger.info(f"Job metadata - parsed: {job_metadata}")
        return AssistantJobMetadata(assistant_id=job_metadata.get("assistant_id"))
    except Exception as e:
        logger.error(f"Error extracting job metadata: {e}")
        raise e
