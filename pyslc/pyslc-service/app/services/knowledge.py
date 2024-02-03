from typing import List

from sqlalchemy.orm import Session

from app.services.base import ServiceBase
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
    KnowledgeBaseResponse,
    KnowledgeBaseListPayloadResponse,
)
from app.repository.knowledge import KnowledgeRepository


class KnowledgeService(ServiceBase):
    def __init__(self, repository: KnowledgeRepository, session: Session):
        self.repository = repository
        self.session = session

    def create_knowledge_base(
        self, payload: KnowledgeBaseCreatePayload
    ) -> KnowledgeBaseResponse:
        return self.repository.create_knowledge(
            session=self.session, **payload.model_dump()
        )

    def get_knowledge_base(self, id: str) -> KnowledgeBaseResponse:
        return self.repository.get_knowledge_by_id(session=self.session, id=id)

    def get_knowledge_bases(
        self, limit: int = 10, offset: int = 0
    ) -> List[KnowledgeBaseResponse]:
        knowledge_parts = self.repository.get_knowledge(
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
        knowledge_parts = self.repository.get_knowledge_by_collection(
            session=self.session,
            collection_id=collection_id,
            limit=limit,
            offset=offset,
        )

        # parse the knowledge parts to get the collection name and the data
        collection_id = knowledge_parts[0].collection_id
        data = [knowledge_part.content for knowledge_part in knowledge_parts]
        return KnowledgeBaseListPayloadResponse(
            collection_id=collection_id, data=data, size=len(data)
        )

    def get(self, id):
        return self.repository.get(session=self.session, id=id)

    def list(self, limit: int = 10, offset: int = 0):
        return self.repository.get_all(session=self.session, limit=limit, offset=offset)

    def create(self, data):
        return self.repository.create(session=self.session, **data)

    def update(self, id, data):
        return self.repository.update(session=self.session, id=id, **data)

    def delete(self, id):
        return self.repository.delete(session=self.session, id=id)
