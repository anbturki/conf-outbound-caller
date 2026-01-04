from app.core.database import Base
from app.core.sqlalchemy_mixins import IDMixin, OrgIdMixin, TimestampMixin, UserIdMixin


class MinimalBaseModel(Base, TimestampMixin, IDMixin):
    __abstract__ = True  # Extendable only


class BaseDBModel(
    MinimalBaseModel,
    UserIdMixin,
    OrgIdMixin,
):
    __abstract__ = True  # Extendable only
