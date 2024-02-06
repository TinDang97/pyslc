from typing import TypeVar, Generic

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository class.
    """

    def __init__(self, session):
        """
        Constructor.

        :param session: SQLAlchemy session
        """
        self.session = session

    def get(self, id):
        """
        Get a single entity by its ID.

        :param id: entity ID
        :return: entity
        """
        return self.session.query(self.entity).get(id)

    def get_all(self):
        """
        Get all entities.

        :return: list of entities
        """
        return self.session.query(self.entity).all()

    def add(self, entity):
        """
        Add an entity.

        :param entity: entity
        """
        self.session.add(entity)

    def delete(self, entity):
        """
        Delete an entity.

        :param entity: entity
        """
        self.session.delete(entity)

    def commit(self):
        """
        Commit the current transaction.
        """
        self.session.commit()

    def rollback(self):
        """
        Rollback the current transaction.
        """
        self.session.rollback()
