from typing import List
from uuid import UUID

from pydantic import BaseModel


class _Base(BaseModel):
    content: str
    collection_id: UUID


class KnowledgeBasePayload(_Base):
    pass


class KnowledgeBaseCreatePayload(_Base):
    pass


class KnowledgeBaseResponse(_Base):
    id: UUID


class KnowledgeBaseListPayloadResponse(BaseModel):
    collection_id: UUID
    data: List[str]
    size: int


class KnowledgeBaseDeletePayload(BaseModel):
    id: str
