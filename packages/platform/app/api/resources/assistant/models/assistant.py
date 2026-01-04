from sqlalchemy import Column, String

from app.core.base_models import BaseDBModel


class Assistant(BaseDBModel):
    __tablename__ = "assistants"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    voice_id = Column(String, nullable=True)
    first_message = Column(String, nullable=True)
    prompt = Column(String, nullable=True)
