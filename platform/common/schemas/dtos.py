from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: UUID
    email: str
    name: str
    last_login: datetime
    org_id: UUID
