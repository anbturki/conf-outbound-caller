from livekit import rtc
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import openai
from shared.logger import logger


class OutboundCallerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful voice AI assistant. You are able to answer questions and help with tasks."
        )


async def create_session(voice: str = "coral"):
    logger.info(f"Creating session with voice: {voice}")
    session = AgentSession(llm=openai.realtime.RealtimeModel(voice=voice))
    logger.info("Session created")
    return session


async def start_session(room: rtc.Room, session: AgentSession):
    await session.start(
        agent=OutboundCallerAgent(),
        room=room,
        room_input_options=RoomInputOptions(),
    )

    return session
