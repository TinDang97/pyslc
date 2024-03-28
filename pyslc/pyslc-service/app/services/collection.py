from __future__ import annotations


from app.repository.collection import CollectionRepository
from app.repository.knowledge import KnowledgeRepository
from app.schema.collection import (
    CollectionCreatePayload,
    CollectionListResponse,
    CollectionResponse,
    CollectionWithKnowledgeResponse,
    UpdateCollectionPayload,
)
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
)
from app.schema.query import QueryParams
from app.services.base import ServiceBase
from app.core.types import UIDType


class CollectionService(ServiceBase):
    def __init__(
        self,
        *,
        collection_repository: CollectionRepository,
        knowledge_repository: KnowledgeRepository,
    ):
        self.collection_repository = collection_repository
        self.knowledge_repository = knowledge_repository

    def list(self, query: QueryParams) -> CollectionListResponse:
        collections = self.collection_repository.get_collections(query)
        return CollectionListResponse.model_validate(collections, from_attributes=True)

    def create(
        self, payload: CollectionCreatePayload, created_by: str
    ) -> CollectionResponse:
        if self.collection_repository.get_collection_by_name(payload.name):
            raise ValueError("Collection already exists")

        collection = self.collection_repository.create_collection(
            payload=payload.model_dump(exclude={"knowledge_content"}),
            created_by=created_by,
        )
        if payload.knowledge_content:
            for content in payload.knowledge_content:
                self.knowledge_repository.create_knowledge(
                    KnowledgeBaseCreatePayload(
                        collection_uid=collection.uid,
                        content=content,
                    ).model_dump(),
                    created_by,
                )
        return CollectionResponse(
            uid=collection.uid,
            name=collection.name,
            description=collection.description,
        )

    def update(
        self, uid: UIDType, payload: UpdateCollectionPayload, updated_by: str
    ) -> CollectionResponse:
        collection = self.collection_repository.update_collection(
            uid, payload=payload.model_dump(), updated_by=updated_by
        )
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse(
            uid=collection.uid, name=collection.name, description=collection.description
        )

    def delete(self, uid: UIDType, deleted_by: str):
        if not self.collection_repository.get_collection_by_uid(uid):
            raise ValueError("Collection not found")

        return self.collection_repository.delete_collection(uid, deleted_by)

    def get(self, uid: UIDType) -> CollectionResponse:
        collection = self.collection_repository.get_collection_by_uid(uid)
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse.model_validate(collection, from_attributes=True)

    def find_by_name(self, name: str) -> CollectionResponse:
        collection = self.collection_repository.get_collection_by_name(name)
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse.model_validate(collection, from_attributes=True)

    def get_knowledge_by_collection_uid(
        self, collection_uid: str, query: QueryParams
    ) -> CollectionWithKnowledgeResponse:
        collection = self.collection_repository.get_collection_by_uid_with_knowledges(
            collection_uid
        )
        if not collection:
            raise ValueError("Collection not found")

        return CollectionWithKnowledgeResponse.model_validate(
            collection,
            from_attributes=True,
        )
