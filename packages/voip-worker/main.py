from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import JobContext
from services.platform import Assistant, platform_service
from shared.logger import logger, setup_logging
from utils.agent_session import create_session
from utils.job_context import extract_job_metadata
from utils.session_events import listen_for_events

load_dotenv()
setup_logging()


async def connect_to_room(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect()

    @ctx.room.on("connection_state_changed")
    def on_connection_state_changed(event: rtc.ConnectionState):
        logger.info(f"Connection state changed: {event}")

    logger.info(f"Connected to room {ctx.room.name}")


async def get_assistant_config(assistant_id: str) -> Assistant:
    assistant = await platform_service.get_assistants(assistant_id)
    return assistant


async def entrypoint(ctx: JobContext):
    job_metadata = extract_job_metadata(ctx)
    assistant = await get_assistant_config(job_metadata.assistant_id)
    session = await create_session(assistant.voice_id)
    await listen_for_events(session)
    await connect_to_room(ctx)


if __name__ == "__main__":
    logger.info("Starting voip worker agent")
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint, agent_name="voip-worker-assistant"
        )
    )
