__all__ = ["ModelBase", "ModelMixin", "TimestampMixin", "UserMixin"]
__author__ = "Tin Dang"
__description__ = "Base model for all models"

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, UUID
from app.databases.database import Base
from app.settings import settings
from uuid import uuid4


class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)


class UserMixin:
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    deleted_by = Column(Integer, nullable=True)


class ModelMixin(TimestampMixin, UserMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    is_deleted = Column(Integer, nullable=False, default=0)


class ModelBase(Base, ModelMixin):
    __abstract__ = True
    __table_args__ = {"schema": settings.db.schema}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, is_deleted={self.is_deleted})>"
        )

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, is_deleted={self.is_deleted})>"
        )
