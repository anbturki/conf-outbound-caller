from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.guest_session import GuestSession

router = APIRouter(prefix="/guests", tags=["guest"])


@router.post("/")
async def create_guest_session(
    request: Request, db: Annotated[Session, Depends(get_db)]
):
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    guest_session = GuestSession(ip_address=ip_address, user_agent=user_agent)
    db.add(guest_session)
    db.commit()
    db.refresh(guest_session)
    return guest_session
