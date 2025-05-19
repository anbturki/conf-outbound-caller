from livekit.agents import AgentSession
from livekit.agents.voice.events import AgentStateChangedEvent, UserStateChangedEvent
from shared.logger import logger


def on_agent_state_change(event: AgentStateChangedEvent):
    logger.info(f"Agent state changed: {event}")


def on_user_state_change(event: UserStateChangedEvent):
    logger.info(f"User state changed: {event}")


async def listen_for_events(session: AgentSession):
    logger.info("Listening for session events")

    session.on("agent_state_change", on_agent_state_change)
    session.on("user_state_change", on_user_state_change)
