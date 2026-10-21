from livekit.agents import AgentSession
from livekit.agents.voice.events import AgentStateChangedEvent, UserStateChangedEvent
from livekit.rtc import ConnectionState, DisconnectReason, Room
from shared.logger import logger


def on_agent_state_change(event: AgentStateChangedEvent):
    logger.info(f"Agent state changed: {event}")


def on_user_state_change(event: UserStateChangedEvent):
    logger.info(f"User state changed: {event}")


async def listen_for_events(session: AgentSession):
    logger.info("Listening for session events")

    session.on("agent_state_changed", on_agent_state_change)
    session.on("user_state_changed", on_user_state_change)


# Room events
def on_connection_state_changed(connection_state: ConnectionState):
    logger.info(f"Room connection state changed: {connection_state}")


def on_room_disconnected(reason: DisconnectReason):
    logger.info(f"Room disconnected: {reason}")


async def listen_for_room_events(room: Room):
    logger.info(f"Listening for room events {room.name}")
    room.on("connection_state_changed", on_connection_state_changed)
    room.on("disconnected", on_room_disconnected)
