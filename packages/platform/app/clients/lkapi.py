from livekit.api import CreateAgentDispatchRequest, LiveKitAPI

# agent_name: str
# room: str
# metadata: str
from shared import logger

# print(f"there are {len(dispatches)} dispatches in {room_name}")


async def create_explicit_dispatch(agent_name: str, room: str, metadata: str):
    lk_api = LiveKitAPI()
    agent_dispatch_request = CreateAgentDispatchRequest(
        agent_name=agent_name,
        room=room,
        metadata=metadata,
    )
    logger.info(f"Creating explicit dispatch request: {agent_dispatch_request}")
    dispatch = await lk_api.agent_dispatch.create_dispatch(agent_dispatch_request)
    logger.info(f"Created explicit dispatch: {dispatch}")
    dispatches = await lk_api.agent_dispatch.list_dispatch(room_name=room)
    logger.info(f"There are {len(dispatches)} dispatches in {room}")
    await lk_api.aclose()
    return dispatch
