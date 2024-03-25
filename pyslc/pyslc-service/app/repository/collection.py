from __future__ import annotations

from logging import Logger
from typing import Callable, Dict, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, Session

from app.model.collection import Collection
from app.model.knowledge import Knowledge
from app.repository.base import BaseRepository
from app.repository.util import map_dict_to_entity


class CollectionRepository(BaseRepository[Collection]):
    def __init__(self, session_factory: Callable[[], Session], logger: Logger):
        super().__init__(Collection, session_factory, logger)

    def get_collections(self, limit: int = 10, offset: int = 0) -> List[Collection]:
        with self.session_factory() as session:
            smt = (
                select(Collection)
                .options(joinedload(Collection.knowledge_parts))
                .limit(limit)
                .offset(offset)
            )
            collections = session.execute(smt).scalars().all()
            return list(collections)

    def get_collection_by_id(self, uid: str | UUID) -> Collection | None:
        return self.get(uid)

    def create_collection(
        self, payload: Dict, created_by: str, knowledges: List[Dict] | None = None
    ) -> Collection:
        if knowledges:
            payload[Collection.knowledge_parts.key] = [
                map_dict_to_entity(Knowledge, **knowledge, created_by=created_by)
                for knowledge in knowledges
            ]
        return self.create(payload=payload, created_by=created_by)

    def delete_collection(self, uid: str | UUID, deleted_by: str):
        return self.delete(uid=uid, deleted_by=deleted_by)

    def update_collection(self, uid: str | UUID, payload: Dict, updated_by: str):
        self.update(uid=uid, payload=payload, updated_by=updated_by)

    def get_collection_by_name(self, name: str) -> Collection | None:
        with self.session_factory() as session:
            smt = select(Collection).filter(
                Collection.name == name,
                Collection.is_deleted.__eq__(False),
            )
            collection = session.execute(smt).scalar_one_or_none()
            return collection
