from datetime import datetime

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
