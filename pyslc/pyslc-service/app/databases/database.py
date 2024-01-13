__all__ = ["database_client", "Base"]


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base(metadata=MetaData(schema=settings.POSTGRES_SCHEMA))


class Database:
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    def get_session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DatabaseContainer:
    instance = None

    @classmethod
    def init(cls):
        cls.instance = Database(settings.db.db_url)

    @classmethod
    def get_session(cls):
        if cls.instance is None:
            cls.init()
        return cls.instance.get_session()


database_client = DatabaseContainer
