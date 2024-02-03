from typing import List

from pydantic import BaseModel


class _Base(BaseModel):
    content: str
    collection_id: str


class KnowledgeBasePayload(_Base):
    pass


class KnowledgeBaseCreatePayload(_Base):
    pass


class KnowledgeBaseResponse(_Base):
    id: str


class KnowledgeBaseListPayloadResponse(BaseModel):
    collection_id: str
    data: List[str]
    size: int


class KnowledgeBaseDeletePayload(BaseModel):
    id: str
