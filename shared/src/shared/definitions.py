from typing import Union

from pydantic import BaseModel


class AssistantDispatchMetadata(BaseModel):
    """
    Metadata for the assistant dispatch.
    if from_number and to_number are not provided, it means the assistant is being test through the web, otherwise, it's a phone call trigger
    """

    from_number: Union[str, None] = None
    to_number: Union[str, None] = None
    assistant_id: str
    sid: str
    participant_id: str
