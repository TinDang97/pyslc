from typing import List

from sqlalchemy.orm import Session

from app.core.chat.storage import get_chat_storage, add_chat_storage
from app.model.collection import Collection
from app.repository.collection import CollectionRepository
from app.schema.collection import (
    CollectionCreatePayload,
    UpdateCollectionPayload,
    CollectionResponse,
)
from app.schema.knowledge import (
    KnowledgeBaseListPayloadResponse,
    KnowledgeBaseCreatePayload,
)
from app.services.base import ServiceBase
from app.services.knowledge import KnowledgeService


class CollectionService(ServiceBase):
    def __init__(
        self,
        collection_repository: CollectionRepository,
        knowledge_service: KnowledgeService,
        session: Session,
    ):
        self.collection_repository: CollectionRepository = collection_repository
        self.knowledge_service = knowledge_service
        self.session: Session = session

    def list(self, limit: int = 10, offset: int = 0) -> List[CollectionResponse]:
        collections = self.collection_repository.get_collections(
            self.session, limit, offset
        )
        return [
            CollectionResponse(
                id=collection.id,
                name=collection.name,
                description=collection.description,
            )
            for collection in collections
        ]

    def create(self, payload: CollectionCreatePayload):
        if self.collection_repository.get_collection_by_name(
            self.session, payload.name
        ):
            raise ValueError("Collection already exists")

        collection = self.collection_repository.create_collection(
            self.session, **payload.model_dump(exclude={"knowledge_content"})
        )
        if payload.knowledge_content:
            for content in payload.knowledge_content:
                self.knowledge_service.create_knowledge_base(
                    KnowledgeBaseCreatePayload(
                        collection_id=collection.id,
                        content=content,
                    )
                )

    def update(self, id, payload: UpdateCollectionPayload) -> CollectionResponse:
        collection = self.collection_repository.update_collection(
            self.session, id, **payload.model_dump()
        )
        return CollectionResponse(
            id=collection.id, name=collection.name, description=collection.description
        )

    def delete(self, id: str):
        return self.collection_repository.delete_collection(self.session, id)

    def get(self, id: str) -> CollectionResponse:
        collection = self.collection_repository.get_collection_by_id(self.session, id)
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse(
            id=collection.id, name=collection.name, description=collection.description
        )

    def get_by_name(self, name: str) -> CollectionResponse:
        collection = self.collection_repository.get_collection_by_name(
            self.session, name
        )
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse(
            id=collection.id, name=collection.name, description=collection.description
        )

    def query(self, collection_id: str, query: str):
        collection = self.collection_repository.get_collection_by_name(
            self.session, collection_id
        )
        if not collection:
            raise ValueError("Collection not found")

        with get_chat_storage(collection.id) as zep_engine:
            return zep_engine.query(query)

    def chat(self, collection_id, message: str):
        collection = self.collection_repository.get_collection_by_id(
            self.session, collection_id
        )
        if not collection:
            raise ValueError("Collection not found")

        with get_chat_storage(collection.id) as zep_engine:
            if zep_engine is None:
                raise ValueError("Engine not found")

            return zep_engine.chat(message)

    def create_engine(self, collection_id: str):
        collection: Collection = self.collection_repository.get_collection_by_id(
            self.session, collection_id
        )

        if not collection:
            raise ValueError("Collection not found")

        with get_chat_storage(collection.id) as zep_engine:
            if zep_engine is not None:
                return zep_engine

        knowledge_parts: KnowledgeBaseListPayloadResponse = (
            self.knowledge_service.get_knowledge_bases_by_collection(collection_id)
        )
        if not knowledge_parts.data:
            raise ValueError("No knowledge base found for this collection")

        with add_chat_storage(
            engine_id=collection.id,
            collection_name=collection.name,
            data=knowledge_parts.data,
        ) as zep_engine:
            return zep_engine
