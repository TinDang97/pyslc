from typing import List

from app.model.collection import Collection
from app.repository.base import BaseRepository
from app.repository.util import map_dict_to_entity


class CollectionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Collection)

    def get_collection(
        self, session, limit: int = 10, offset: int = 0
    ) -> List[Collection]:
        return self.get_all(session, limit, offset)

    def get_collection_by_id(self, session, id: str) -> Collection:
        return self.get(session, id)

    def create_collection(self, session, **payload) -> Collection:
        collection = map_dict_to_entity(**payload)
        return self.create(session, collection)

    def delete_collection(self, session, id: str):
        return self.delete(session, id)

    def update_collection(self, session, id: str, **payload) -> Collection:
        collection = map_dict_to_entity(**payload)
        return self.update_by_id(session, id, collection)

    def get_collection_by_name(self, session, name: str) -> Collection:
        return session.query(Collection).filter(Collection.name == name).first()
