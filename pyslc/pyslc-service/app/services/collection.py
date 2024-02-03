from typing import List

from sqlalchemy.orm import Session

from app.model.collection import Collection
from app.model.knowledge import Knowledge
from app.services.base import ServiceBase
from app.repository.collection import CollectionRepository
from app.repository.knowledge import KnowledgeRepository
from app.core.chat.storage import get_chat_storage, add_chat_storage
from app.schema.collection import CollectionPayload


class CollectionService(ServiceBase):
    def __init__(
        self,
        collection_repository: CollectionRepository,
        knowledge_repository: KnowledgeRepository,
        session: Session,
    ):
        self.collection_repository: CollectionRepository = collection_repository
        self.knowledge_repository = knowledge_repository
        self.session: Session = session

    def list(self, limit: int = 10, offset: int = 0):
        return self.collection_repository.get_collection(self.session, limit, offset)

    def create(self, payload: CollectionPayload):
        return self.collection_repository.create_collection(
            self.session, **payload.model_dump()
        )

    def update(self, id, payload: CollectionPayload):
        return self.collection_repository.update_collection(
            self.session, id, **payload.model_dump()
        )

    def delete(self, id: str):
        return self.collection_repository.delete_collection(self.session, id)

    def get(self, id: str):
        return self.collection_repository.get_collection_by_id(self.session, id)

    def query(self, collection: str, query: str):
        with get_chat_storage(collection) as zep_engine:
            return zep_engine.query(query)

    def create_engine(self, collection_name: str):
        collection: Collection = self.collection_repository.get_collection_by_name(
            self.session, collection_name
        )
        knowledge_parts: List[
            Knowledge
        ] = self.knowledge_repository.get_knowledge_by_collection(
            self.session, collection.id
        )
        data = [knowledge_part.content for knowledge_part in knowledge_parts]
        with add_chat_storage(collection.id, data) as zep_engine:
            return zep_engine
