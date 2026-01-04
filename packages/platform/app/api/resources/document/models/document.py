from sqlalchemy import JSON, Column, ForeignKey, Integer, String

from app.common.aliases import PGUUID
from app.core.base_models import BaseDBModel


class Document(BaseDBModel):
    __tablename__ = "documents"

    name = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    file_ext = Column(String, nullable=True)
    category_id = Column(PGUUID, ForeignKey("categories.id"), nullable=True)

    file_metadata = Column(JSON, nullable=True)
