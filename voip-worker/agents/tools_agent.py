from livekit import api as lk_api
from livekit.agents import AgentSession, JobContext, RunContext
from livekit.agents.llm.tool_context import function_tool

from shared import logger


# want to indicate that class is only inherited, and job_context must be provided
class ToolsAgent:
    job_context: JobContext
    session: AgentSession

    @function_tool
    async def end_call(self, context: RunContext):
        """
        Use this tool to end the call when the conversation is over.
        """
        if not self.job_context:
            logger.error("No job context available")
            await self.session.say("I'm sorry, I can't end the call at this time.")
            return None, "Failed to end call: No job context available"

        room_name = self.job_context.room.name
        logger.info(f"Ending call by deleting room {room_name}")

        try:
            await context.session.generate_reply(
                instructions="Thank you for your time. I'll be ending this call now. Goodbye!"
            )
            await self.job_context.api.room.delete_room(
                lk_api.DeleteRoomRequest(room=room_name)
            )

            logger.info(f"Successfully deleted room {room_name}")
            return None, "Call ended successfully."

        except Exception as e:
            logger.error(f"Error ending call: {e}")
            return None, f"Failed to end call: {e}"
