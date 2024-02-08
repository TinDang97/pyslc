from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.services.base import ServiceBase
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
    KnowledgeBaseResponse,
    KnowledgeBaseListPayloadResponse,
)
from app.repository.knowledge import KnowledgeRepository
from app.repository.collection import CollectionRepository

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.chat import ChatService


class KnowledgeService(ServiceBase):
    def __init__(
        self,
        *,
        knowledge_repository: KnowledgeRepository | None = None,
        collection_repository: CollectionRepository | None = None,
        chat_service: Optional["ChatService"] | None = None,
        session: Session,
    ):
        from app.services.chat import ChatService
        from app.services.collection import CollectionService

        self.knowledge_repository = knowledge_repository or KnowledgeRepository()
        self.collection_repository = collection_repository or CollectionRepository()
        self.chat_service = chat_service or ChatService(
            collection_service=CollectionService(
                collection_repository=self.collection_repository,
                knowledge_service=self,
                session=session,
            ),
            session=session,
        )
        self.session = session

    def create_knowledge_base(
        self, payload: KnowledgeBaseCreatePayload
    ) -> KnowledgeBaseResponse:
        if not self.collection_repository.get(
            session=self.session, id=payload.collection_id
        ):
            raise ValueError("Collection does not exist")

        return self.knowledge_repository.create_knowledge(
            session=self.session, **payload.model_dump()
        )

    def get_knowledge_base(self, id: str) -> KnowledgeBaseResponse:
        return self.knowledge_repository.get_knowledge_by_id(
            session=self.session, id=id
        )

    def get_knowledge_bases(
        self, limit: int = 10, offset: int = 0
    ) -> List[KnowledgeBaseResponse]:
        knowledge_parts = self.knowledge_repository.get_knowledge(
            session=self.session, limit=limit, offset=offset
        )
        return [
            KnowledgeBaseResponse(
                collection_id=knowledge_part.collection_id,
                content=knowledge_part.content,
                id=knowledge_part.id,
            )
            for knowledge_part in knowledge_parts
        ]

    def get_knowledge_bases_by_collection(
        self, collection_id: str, limit: int = 10, offset: int = 0
    ) -> KnowledgeBaseListPayloadResponse:
        knowledge_parts = self.knowledge_repository.get_knowledge_by_collection(
            session=self.session,
            collection_id=collection_id,
            limit=limit,
            offset=offset,
        )

        # parse the knowledge parts to get the collection name and the data
        data = [knowledge_part.content for knowledge_part in knowledge_parts]
        return KnowledgeBaseListPayloadResponse(
            collection_id=knowledge_parts[0].collection_id, data=data, size=len(data)
        )

    def get(self, id):
        return self.knowledge_repository.get(session=self.session, id=id)

    def list(self, limit: int = 10, offset: int = 0):
        return self.knowledge_repository.get_all(
            session=self.session, limit=limit, offset=offset
        )

    def create(self, data):
        return self.knowledge_repository.create(session=self.session, **data)

    def update(self, id, data):
        return self.knowledge_repository.update(session=self.session, id=id, **data)

    def delete(self, id):
        return self.knowledge_repository.delete(session=self.session, id=id)
