from __future__ import annotations

from uuid import UUID


from ..model.knowledge import Knowledge
from app.repository.collection import CollectionRepository
from app.repository.knowledge import KnowledgeRepository
from app.schema.collection import (
    CollectionCreatePayload,
    CollectionWithKnowledgeResponse,
    KnowledgeBaseResponse,
    UpdateCollectionPayload,
    CollectionResponse,
)
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
)
from app.schema.query import ListResponse, QueryParams
from app.services.base import ServiceBase


class CollectionService(ServiceBase):
    def __init__(
        self,
        *,
        collection_repository: CollectionRepository,
        knowledge_repository: KnowledgeRepository,
    ):
        self.collection_repository = collection_repository
        self.knowledge_repository = knowledge_repository

    def list(self, query: QueryParams) -> ListResponse[CollectionResponse]:
        collections = self.collection_repository.get_collections(query)
        return collections.map_model(CollectionResponse)

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
        self, uid: str | UUID, payload: UpdateCollectionPayload, updated_by: str
    ) -> CollectionResponse:
        collection = self.collection_repository.update_collection(
            uid, payload=payload.model_dump(), updated_by=updated_by
        )
        if not collection:
            raise ValueError("Collection not found")

        return CollectionResponse(
            uid=collection.uid, name=collection.name, description=collection.description
        )

    def delete(self, uid: str | UUID, deleted_by: str):
        if not self.collection_repository.get_collection_by_uid(uid):
            raise ValueError("Collection not found")

        return self.collection_repository.delete_collection(uid, deleted_by)

    def get(self, uid: str | UUID) -> CollectionResponse:
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
        collection = self.collection_repository.get_collection_by_uid(collection_uid)
        if not collection:
            raise ValueError("Collection not found")

        knowledge_parts: ListResponse[
            Knowledge
        ] = self.knowledge_repository.get_knowledges_by_collection_uid(
            collection_uid=collection.uid,
            query=query,
        )

        return CollectionWithKnowledgeResponse(
            uid=collection.uid,
            name=collection.name,
            description=collection.description,
            knowledges=knowledge_parts.map_model(KnowledgeBaseResponse),
        )
