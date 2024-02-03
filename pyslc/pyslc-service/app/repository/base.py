from typing import TypeVar, Generic, Type

from sqlalchemy import update
from sqlalchemy.orm import Session
from app.model.base import ModelBase


T = TypeVar("T", bound=Type[ModelBase])


class BaseRepository(Generic[T]):
    """
    Base repository class.
    """

    def __init__(self, entity: T):
        """
        Constructor.

        :param session: SQLAlchemy session
        """
        self.entity = entity

    def get(self, *, session: Session, id):
        """
        Get a single entity by its ID.

        :param session:
        :type session:
        """
        return session.query(self.entity).get(id)

    def get_all(self, *, session: Session, limit: int = 10, offset: int = 0):
        """
        Get all entities.

        :return: list of entities
        """
        return session.query(self.entity).limit(limit).offset(offset).all()

    def create(self, *, session: Session, **payload) -> T:
        """
        Create a new entity.

        :param session:
        :type session:
        :param entity: entity to create
        """
        entity = self.entity(**payload)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def update(self, *, session: Session, **payload) -> T:
        """
        Update an entity.

        :param session:
        :type session:
        :param entity: entity to update
        """
        entity = self.entity(**payload)
        session.commit()
        return entity

    def update_by_id(self, *, session: Session, id: str, **payload) -> T:
        """
        Update an entity by its ID.

        :param session:
        :type session:
        :param id: entity ID
        :param payload: update payload
        """
        update_exec = update(self.entity).where(self.entity.id == id).values(**payload)
        session.execute(update_exec)
        return self.get(session=session, id=id)

    def delete(self, *, session: Session, id: str):
        """
        Delete an entity by its ID.

        :param session:
        :type session:
        :param id: entity ID
        """
        update(self.entity).where(self.entity.id == id).values(deleted_at=True)
        session.commit()
