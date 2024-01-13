__all__ = ["ModelBase", "ModelMixin", "TimestampMixin", "UserMixin"]
__author__ = "Tin Dang"
__description__ = "Base model for all models"


from sqlalchemy import Column, DateTime, Integer, Uuid
from app.databases.database import Base
from app.settings import settings


class TimestampMixin:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=True)


class UserMixin:
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
    deleted_by = Column(Integer, nullable=True)


class ModelMixin(TimestampMixin, UserMixin):
    id = Column(Uuid, primary_key=True, server_default="uuid_generate_v4()")
    is_deleted = Column(Integer, nullable=False, default=0)


class ModelBase(Base, ModelMixin):
    __abstract__ = True
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, is_deleted={self.is_deleted})>"
        )

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, is_deleted={self.is_deleted})>"
        )
