import asyncio

from livekit import rtc
from livekit.agents import Agent, AgentSession, RoomInputOptions, metrics
from livekit.plugins import openai
from shared.logger import logger
from utils.session_events import listen_for_events


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


async def prepare_session(session: AgentSession):
    usage_collector = metrics.UsageCollector()

    # Log metrics and collect usage data
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        logger.info(f"Metrics collected: {agent_metrics}")
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)

    session.on("metrics_collected", on_metrics_collected)
    await listen_for_events(session)

    return session


async def start_session(room: rtc.Room, session: AgentSession):
    logger.info("Starting session")
    return asyncio.create_task(
        session.start(
            agent=OutboundCallerAgent(),
            room=room,
            room_input_options=RoomInputOptions(),
        )
    )
