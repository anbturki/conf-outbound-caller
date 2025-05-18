from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    last_login: datetime
    org_id: UUID
