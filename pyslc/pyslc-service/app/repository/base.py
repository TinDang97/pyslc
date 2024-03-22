from __future__ import annotations

from logging import Logger
from typing import (
    Callable,
    Dict,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    MutableMapping,
)

from sqlalchemy import literal, update, select
from sqlalchemy.orm import Session

from app.core.types import UIDType
from app.databases.database import Base

R = TypeVar("R", bound=Base, covariant=True)
T = TypeVar("T", bound=Base)


class ReadBaseRepository(Protocol[R]):
    def get(self, uid: UIDType, **filter_criteria) -> R | None:
        ...

    def find_all(
        self, limit: int = 10, offset: int = 0, **filter_criteria
    ) -> Sequence[R]:
        ...

    def find(self, **filter_criteria) -> R | None:
        ...

    def is_exists(self, uid: UIDType, **filter_criteria) -> bool:
        ...


class WriteBaseRepository(Protocol):
    def create(self, payload: Dict, created_by: str):
        ...

    def update(
        self,
        uid: UIDType,
        payload: MutableMapping,
        updated_by: str,
        **filter_criteria,
    ):
        ...

    def delete(self, uid: UIDType, deleted_by: str, **filter_criteria):
        ...

    def delete_all(self, deleted_by: str, **filter_criteria):
        ...


class BaseRepository(ReadBaseRepository[T], WriteBaseRepository):
    """
    Base repository class.
    """

    def __init__(
        self, entity: Type[T], session_factory: Callable[[], Session], logger: Logger
    ):
        self.entity = entity
        self.session_factory = session_factory
        self.logger = logger

    def is_exists(self, uid: UIDType, **filter_criteria) -> bool:
        with self.session_factory() as session:
            q = session.query(self.entity).filter_by(id=uid, **filter_criteria).exists()
            return session.query(literal(True)).filter(q).scalar()

    def get(self, uid: UIDType, **filter_criteria) -> T | None:
        """
        Get a single entity by its ID.

        Parameters:
        - uid: The ID of the entity to retrieve.

        Returns:
        - The entity with the specified ID, if found. Otherwise, returns None.
        """
        with self.session_factory() as session:
            smt = select(self.entity).filter_by(id=uid, **filter_criteria)
            return session.execute(smt).scalar_one_or_none()

    def find_all(
        self,
        limit: int = 10,
        offset: int = 0,
        order_by: str = "id",
        desc: bool = False,
        **filter_criteria,
    ) -> Sequence[T]:
        """
        Get all entities.

        :return: list of entities
        """
        with self.session_factory() as session:
            smt = (
                select(self.entity)
                .filter_by(**filter_criteria)
                .limit(limit)
                .offset(offset)
            )
            return session.execute(smt).scalars().all()

    def create(self, payload: Dict, created_by: str):
        """
        Create a new entity.
        """
        entity = self.entity(
            **payload,
            created_by=created_by,
        )
        with self.session_factory() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update(
        self,
        uid: UIDType,
        payload: MutableMapping,
        updated_by: str,
        **filter_criteria,
    ):
        """
        Update an entity.
        """
        with self.session_factory() as session:
            update_exec = (
                update(self.entity)
                .filter_by(uid=uid, **filter_criteria)
                .values(**payload, updated_by=updated_by)
            )
            session.execute(update_exec)
            session.commit()

    def delete(self, uid: UIDType, deleted_by: str, **filter_criteria):
        """
        Delete an entity by update is_deleted to True.
        """
        with self.session_factory() as session:
            delete_exec = (
                update(self.entity)
                .filter_by(id=uid, **filter_criteria)
                .values(deleted_by=deleted_by, is_deleted=True)
            )
            session.execute(delete_exec)
            session.commit()

    def delete_all(self, deleted_by: str, **filter_criteria):
        """
        Delete all entities by update `is_deleted` to True
        """
        with self.session_factory() as session:
            delete_exec = (
                update(self.entity)
                .filter_by(**filter_criteria)
                .values(deleted_by=deleted_by, is_deleted=True)
            )
            session.execute(delete_exec)
            session.commit()
