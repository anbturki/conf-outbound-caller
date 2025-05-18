from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, RoomInputOptions
from livekit.plugins import openai

load_dotenv()


class OutboundCallerAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful voice AI assistant. You are able to answer questions and help with tasks."
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(llm=openai.realtime.RealtimeModel(voice="coral"))

    await session.start(
        agent=OutboundCallerAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(),
    )

    await session.generate_reply(user_input="Greet and ask how can you help them")


print("__name__", __name__)

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
