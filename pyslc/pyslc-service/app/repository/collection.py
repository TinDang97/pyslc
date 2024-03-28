from __future__ import annotations

from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.types import UIDType
from app.model.collection import Collection
from app.model.knowledge import Knowledge
from app.repository.base import BaseRepository
from app.repository.util import map_dict_to_entity, paginate
from app.schema.query import ListResponse, QueryParams


class CollectionRepository(BaseRepository[Collection]):
    _entity = Collection

    def get_collections(self, query: QueryParams) -> ListResponse[Collection]:
        with self.session_factory() as session:
            smt = select(Collection).options(joinedload(Collection.knowledges))
            return paginate(smt, query, session)

    def get_collection_by_uid(self, uid: UIDType) -> Collection | None:
        return self.get(uid)

    def get_collection_by_uid_with_knowledges(self, uid: UIDType) -> Collection | None:
        with self.session_factory() as session:
            smt = (
                select(Collection)
                .options(
                    joinedload(
                        Collection.knowledges.and_(Knowledge.is_deleted.__eq__(False))
                    )
                )
                .filter(
                    Collection.uid == uid,
                    Collection.is_deleted.__eq__(False),
                )
            )
            collection = session.execute(smt).unique().scalar_one_or_none()
            return collection

    def create_collection(
        self, payload: Dict, created_by: str, knowledges: List[Dict] | None = None
    ) -> Collection:
        if knowledges:
            payload[Collection.knowledges.key] = [
                map_dict_to_entity(Knowledge, **knowledge, created_by=created_by)
                for knowledge in knowledges
            ]
        return self.create(payload=payload, created_by=created_by)

    def delete_collection(self, uid: UIDType, deleted_by: str):
        return self.delete(uid=uid, deleted_by=deleted_by)

    def update_collection(self, uid: UIDType, payload: Dict, updated_by: str):
        self.update(uid=uid, payload=payload, updated_by=updated_by)

    def get_collection_by_name(self, name: str) -> Collection | None:
        with self.session_factory() as session:
            smt = select(Collection).filter(
                Collection.name == name,
                Collection.is_deleted.__eq__(False),
            )
            collection = session.execute(smt).scalar_one_or_none()
            return collection
