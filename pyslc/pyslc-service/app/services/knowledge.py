from __future__ import annotations

from typing import List, TYPE_CHECKING

from app.core.types import UIDType
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
    KnowledgeBaseListPayloadResponse,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdatePayload,
)
from app.services.base import ServiceBase

if TYPE_CHECKING:
    from app.repository.knowledge import KnowledgeRepository
    from app.repository.collection import CollectionRepository


class KnowledgeService(ServiceBase):
    def __init__(
        self,
        *,
        knowledge_repository: "KnowledgeRepository",
        collection_repository: "CollectionRepository",
    ):
        self.knowledge_repository = knowledge_repository
        self.collection_repository = collection_repository

    def create_knowledge_base(
        self, payload: KnowledgeBaseCreatePayload, created_by: str
    ) -> KnowledgeBaseResponse:
        if not self.collection_repository.is_exists(uid=payload.collection_uid):
            raise ValueError("Collection does not exist")
        knowledge = self.knowledge_repository.create_knowledge(
            payload=payload.model_dump(), created_by=created_by
        )
        return KnowledgeBaseResponse.model_validate(knowledge, from_attributes=True)

    def get_knowledge(self, uid: UIDType) -> KnowledgeBaseResponse:
        knowledge = self.knowledge_repository.get(uid)
        return KnowledgeBaseResponse.model_validate(knowledge, from_attributes=True)

    def get_knowledges(
        self, limit: int = 10, offset: int = 0
    ) -> List[KnowledgeBaseResponse]:
        knowledge_parts = self.knowledge_repository.get_knowledges(
            limit=limit, offset=offset
        )
        return list(
            map(
                lambda x: KnowledgeBaseResponse.model_validate(x, from_attributes=True),
                knowledge_parts,
            )
        )

    def get_knowledge_bases_by_collection(
        self, collection_id: UIDType, limit: int = 10, offset: int = 0
    ) -> KnowledgeBaseListPayloadResponse:
        knowledges = self.knowledge_repository.get_knowledge_by_collection(
            collection_id=collection_id,
            limit=limit,
            offset=offset,
        )

        # parse the knowledge parts to get the collection name and the data
        return KnowledgeBaseListPayloadResponse.model_validate(
            dict(collection_uid=collection_id, data=knowledges, size=len(knowledges)),
            from_attributes=True,
        )

    def update_knowledge_base(
        self, uid: UIDType, payload: KnowledgeBaseUpdatePayload, updated_by: str
    ):
        self.knowledge_repository.update(
            payload=payload.model_dump(), updated_by=updated_by, uid=uid
        )

    def delete_knowledge_base(self, uid: UIDType, deleted_by: str) -> None:
        self.knowledge_repository.delete(uid=uid, deleted_by=deleted_by)

    def get(self, uid: UIDType):
        return self.get_knowledge(uid)

    def list(self, limit: int = 10, offset: int = 0):
        return self.get_knowledges(limit, offset)

    def create(self, payload: KnowledgeBaseCreatePayload, created_by: str):
        return self.create_knowledge_base(payload, created_by)

    def update(
        self, uid: UIDType, payload: KnowledgeBaseUpdatePayload, updated_by: str
    ):
        return self.update_knowledge_base(uid, payload, updated_by)

    def delete(self, uid: UIDType, deleted_by: str):
        return self.delete_knowledge_base(uid, deleted_by)
