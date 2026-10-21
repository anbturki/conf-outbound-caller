from agents.main_agent import MainAgent
from livekit.agents import AgentSession, AutoSubscribe, ChatContext, JobContext
from livekit.plugins import cartesia, deepgram, openai, silero
from utils.background_audio import play_background_audio
from utils.job_context import extract_job_metadata

from shared import logger


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Connected to room {ctx.room.name}")
    metadata = extract_job_metadata(ctx)
    if metadata:
        logger.info(f"Job metadata: {metadata}")
    else:
        logger.warning("No job metadata found")

    session = AgentSession(
        stt=deepgram.STT(language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
    )
    initial_ctx = ChatContext()

    await session.start(
        room=ctx.room,
        agent=MainAgent(chat_ctx=initial_ctx, job_ctx=ctx),
    )
    await play_background_audio(session, ctx)

    session.say("Hello, how are you?")
