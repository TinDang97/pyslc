from logging import Logger
from typing import Callable, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model import Knowledge
from app.repository.util import paginate
from app.schema.query import QueryParams, ListResponse
from app.repository.base import BaseRepository
from app.core.types import UIDType


class KnowledgeRepository(BaseRepository[Knowledge]):
    def __init__(self, session_factory: Callable[[], Session], logger: Logger):
        super().__init__(Knowledge, session_factory, logger)

    def get_knowledges(self, query: QueryParams) -> ListResponse[Knowledge]:
        knowledge_parts = self.find_all(query)
        return knowledge_parts

    def get_knowledge_by_id(self, uid: UIDType) -> Knowledge | None:
        return self.get(uid)

    def create_knowledge(self, payload: Dict, created_by: str) -> Knowledge:
        return self.create(payload=payload, created_by=created_by)

    def delete_knowledge(self, uid: UIDType, deleted_by: str) -> None:
        self.delete(uid=uid, deleted_by=deleted_by)

    def get_knowledges_by_collection_uid(
        self, collection_uid: UIDType, query: QueryParams
    ) -> ListResponse[Knowledge]:
        with self.session_factory() as session:
            statement = select(Knowledge).filter(
                Knowledge.collection_uid == collection_uid,
                Knowledge.is_deleted.__eq__(False),
            )
            return paginate(statement, query, session)
