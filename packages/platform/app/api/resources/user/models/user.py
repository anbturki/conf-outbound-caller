from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
)

from app.common.aliases import PGUUID
from app.core.base_models import MinimalBaseModel


class User(MinimalBaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_email_verified = Column(Boolean, default=False)

    org_id = Column(PGUUID, nullable=True)

    terms_accepted = Column(Boolean, default=False)

    last_login = Column(DateTime, nullable=True)

    @property
    def name(self):
        return (
            self.first_name + " " + self.last_name
            if self.last_name is not None
            else self.first_name
        )
