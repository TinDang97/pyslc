from typing import TypeVar, Generic

from sqlalchemy import update
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository class.
    """

    def __init__(self, entity):
        """
        Constructor.

        :param session: SQLAlchemy session
        """
        self.entity = entity

    def get(self, session: Session, id):
        """
        Get a single entity by its ID.

        :param session:
        :type session:
        """
        return session.query(self.entity).get(id)

    def get_all(self, session: Session, limit: int = 10, offset: int = 0):
        """
        Get all entities.

        :return: list of entities
        """
        return session.query(self.entity).limit(limit).offset(offset).all()

    def create(self, session: Session, entity: T) -> T:
        """
        Create a new entity.

        :param session:
        :type session:
        :param entity: entity to create
        """
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def update(self, session: Session, entity: T):
        """
        Update an entity.

        :param session:
        :type session:
        :param entity: entity to update
        """
        session.commit()
        return entity

    def update_by_id(self, session: Session, id: str, entity: T) -> T:
        """
        Update an entity by its ID.

        :param session:
        :type session:
        :param id: entity ID
        :param entity: entity to update
        """
        if not isinstance(entity, self.entity.__class__):
            raise ValueError("Entity type does not match repository type")

        update_exec = update(entity).where(self.entity.id == id)
        session.execute(update_exec)
        return entity

    def delete(self, session: Session, id):
        """
        Delete an entity by its ID.

        :param session:
        :type session:
        :param id: entity ID
        """
        entity = session.query(self.entity).get(id)
        session.delete(entity)
        session.commit()
        return entity
