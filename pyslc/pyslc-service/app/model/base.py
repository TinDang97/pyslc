__all__ = ["ModelBase", "ModelMixin", "TimestampMixin", "UserMixin"]
__author__ = "Tin Dang"
__description__ = "Base model for all models"

from datetime import datetime

from sqlalchemy import DateTime, Integer, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.databases.database import Base
from app.settings import settings
from uuid import uuid4, UUID as UUIDType


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class UserMixin:
    created_by: Mapped[datetime] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[datetime] = mapped_column(Integer, nullable=True)
    deleted_by: Mapped[datetime] = mapped_column(Integer, nullable=True)


class ModelMixin(TimestampMixin, UserMixin):
    id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)


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
