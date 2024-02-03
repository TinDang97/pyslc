from typing import List

from app.repository.base import BaseRepository
from app.model.knowledge import Knowledge
from app.repository.util import map_dict_to_entity


class KnowledgeRepository(BaseRepository[Knowledge]):
    def __init__(self):
        super().__init__(Knowledge)

    def get_knowledge(self, session) -> List[Knowledge]:
        return self.get_all(session)

    def get_knowledge_by_id(self, session, id: str) -> Knowledge:
        return self.get(session, id)

    def create_knowledge(self, session, **payload) -> Knowledge:
        knowledge = map_dict_to_entity(Knowledge, **payload)
        return self.create(session, knowledge)

    def delete_knowledge(self, session, id: str):
        return self.delete(session, id)

    def get_knowledge_by_collection(
        self, session, collection_id: str
    ) -> List[Knowledge]:
        return (
            session.query(self.entity)
            .filter(Knowledge.collection_id == collection_id)
            .all()
        )
