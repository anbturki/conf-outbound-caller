from typing import Optional

from core.base_models import BaseDBModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Assistant(BaseDBModel):
    __tablename__ = "assistants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    voice_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_message: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    prompt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
