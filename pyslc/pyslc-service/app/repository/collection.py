from typing import List

from sqlalchemy.orm import joinedload

from app.model.collection import Collection
from app.repository.base import BaseRepository
from app.repository.util import map_dict_to_entity


class CollectionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Collection)

    def get_collections(
        self, session, limit: int = 10, offset: int = 0
    ) -> List[Collection]:
        collection = (
            session.query(Collection)
            .options(joinedload(Collection.knowledge))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return collection

    def get_collection_by_id(self, session, id: str) -> Collection:
        collection = (
            session.query(Collection)
            .options(joinedload(Collection.knowledge))
            .filter(Collection.id == id)
            .first()
        )
        return collection

    def create_collection(self, session, **payload) -> Collection:
        return self.create(session=session, **payload)

    def delete_collection(self, session, id: str):
        return self.delete(session=session, id=id)

    def update_collection(self, session, id: str, **payload) -> Collection:
        collection = map_dict_to_entity(**payload)
        return self.update_by_id(session=session, id=id, entity=collection)

    def get_collection_by_name(self, session, name: str) -> Collection:
        return session.query(Collection).filter(Collection.name == name).first()
