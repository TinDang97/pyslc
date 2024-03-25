from __future__ import annotations

from logging import Logger
from typing import Callable, Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repository.base import BaseRepository
from app.model.knowledge import Knowledge
from app.core.types import UIDType


class Knowledges(List[Knowledge]):
    def raw(self) -> List[str]:
        return [knowledge.content for knowledge in self]


class KnowledgeRepository(BaseRepository[Knowledge]):
    def __init__(self, session_factory: Callable[[], Session], logger: Logger):
        super().__init__(Knowledge, session_factory, logger)

    def get_knowledges(self, *, limit: int = 10, offset: int = 0) -> Knowledges:
        return Knowledges(self.find_all(limit=limit, offset=offset))

    def get_knowledge_by_id(self, uid: UIDType) -> Knowledge | None:
        return self.get(uid)

    def create_knowledge(self, payload: Dict, created_by: str) -> Knowledge:
        return self.create(payload=payload, created_by=created_by)

    def delete_knowledge(self, uid: UIDType, deleted_by: str) -> None:
        self.delete(uid=uid, deleted_by=deleted_by)

    def get_knowledge_by_collection(
        self, collection_id: UIDType, limit: int = 10, offset: int = 0
    ) -> Knowledges:
        with self.session_factory() as session:
            statement = (
                select(Knowledge)
                .filter(Knowledge.collection_uid == collection_id)
                .limit(limit)
                .offset(offset)
            )
            knowledges = session.execute(statement).scalars().all()
            return Knowledges(knowledges)
