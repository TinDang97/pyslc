__all__ = ["ModelBase", "ModelMixin", "TimestampMixin", "UserMixin"]
__author__ = "Tin Dang"
__description__ = "Base model for all models"

from datetime import datetime
from uuid import UUID as UUIDType, uuid4

from sqlalchemy import Boolean, DateTime, func, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


class UserMixin:
    created_by: Mapped[str] = mapped_column(String, nullable=True)
    updated_by: Mapped[str] = mapped_column(String, nullable=True)
    deleted_by: Mapped[str] = mapped_column(String, nullable=True)


class ModelMixin:
    uid: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.uuid_generate_v4(),
        nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)


class ModelBase(Base, ModelMixin):
    __abstract__ = True

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.uid}, is_deleted={self.is_deleted})>"

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.uid}, is_deleted={self.is_deleted})>"
