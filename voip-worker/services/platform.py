import os
from dataclasses import dataclass

from dotenv import load_dotenv
from httpx import AsyncClient
from shared import logger

load_dotenv()


@dataclass
class Assistant:
    id: str
    name: str
    description: str
    voice_id: str
    first_message: str
    prompt: str


class PlatformService:
    def __init__(self):
        api_key = os.getenv("PLATFORM_API_KEY")
        url = os.getenv("PLATFORM_URL")
        logger.info(f"Platform URL: {url}")
        if not api_key or not url:
            raise ValueError("PLATFORM_API_KEY and PLATFORM_URL must be set")

        self.client = AsyncClient(
            base_url=url,
            headers={"X-API-Key": api_key},
        )

    async def get_assistants(self, assistant_id: str) -> Assistant:
        logger.info(f"Fetching assistant with id: {assistant_id}")
        response = await self.client.get(f"/workers/assistants/{assistant_id}")
        if response.status_code != 200:
            logger.error(f"Failed to get assistant: {response.json()}")
            raise Exception(f"Failed to get assistant: {response.json()}")
        dict_response = response.json().get("assistant")
        return Assistant(
            id=dict_response.get("id"),
            name=dict_response.get("name"),
            description=dict_response.get("description"),
            voice_id=dict_response.get("voice_id"),
            first_message=dict_response.get("first_message"),
            prompt=dict_response.get("prompt"),
        )


platform_service = PlatformService()
