from livekit.agents import Agent, JobContext
from livekit.agents.llm import llm
from livekit.agents.llm.chat_context import NOT_GIVEN, NotGivenOr

from .tools_agent import ToolsAgent

things_to_avoid = """
### Things to avoid
- Don't mention the tools in your response, just use them.
- Don't use unpronounceable words.
"""


assistant_instructions = """
You are a helpful voice AI assistant.
"""

telephone_instructions = """
### Telephone instructions
- Be concise and to the point.
- Telephone calls are short, so don't be too verbose.
- Don't mention the tools in your response, just use them.
- Don't use unpronounceable words.
"""


def build_instructions() -> str:
    return f"{assistant_instructions}\n{things_to_avoid}\n{telephone_instructions}"


class MainAgent(Agent, ToolsAgent):
    def __init__(
        self,
        chat_ctx: NotGivenOr[llm.ChatContext | None] = NOT_GIVEN,
        job_ctx: JobContext | None = None,
    ) -> None:
        self.job_context = job_ctx
        super().__init__(
            chat_ctx=chat_ctx,
            instructions=build_instructions(),
        )
