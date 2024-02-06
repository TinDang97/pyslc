from typing import List

from app.repository.base import BaseRepository
from app.model.knowledge import Knowledge


class KnowledgeRepository(BaseRepository[Knowledge]):
    def __init__(self):
        super().__init__(Knowledge)

    def get_knowledge(
        self, *, session, limit: int = 10, offset: int = 0
    ) -> List[Knowledge]:
        return self.get_all(session=session, limit=limit, offset=offset)

    def get_knowledge_by_id(self, *, session, id: str) -> Knowledge:
        return self.get(session=session, id=id)

    def create_knowledge(self, *, session, **payload) -> Knowledge:
        return self.create(session=session, **payload)

    def delete_knowledge(self, *, session, id: str):
        return self.delete(session=session, id=id)

    def get_knowledge_by_collection(
        self, *, session, collection_id: str, limit: int = 10, offset: int = 0
    ) -> List[Knowledge]:
        return (
            session.query(self.entity)
            .filter(Knowledge.collection_id == collection_id)
            .limit(limit)
            .offset(offset)
            .all()
        )
