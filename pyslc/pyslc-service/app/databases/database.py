from contextlib import contextmanager
from logging import Logger
from typing import Any, Generator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker

from app.core.util import json_serializer, json_deserializer
from app.settings import settings
from sqlalchemy.orm import DeclarativeBase

__all__ = ["Database", "Base"]


constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"schema": settings.db.schema_} if settings.db.schema_ else None
    metadata = MetaData(
        schema=settings.db.schema_, naming_convention=constraint_naming_conventions
    )


class Database:
    def __init__(self, db_url: str, *, schema: str = "public", logger: Logger):
        self._engine = create_engine(
            db_url, json_serializer=json_serializer, json_deserializer=json_deserializer
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )
        self.schema = schema
        self.logger = logger

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, Any, None]:
        session = self._session_factory()
        try:
            yield session
        except Exception as e:
            self.logger.error(f"Error occurred: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
