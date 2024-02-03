from typing import List

from pydantic import BaseModel


class _Base(BaseModel):
    data: List[str]
    collection_name: str


class KnowledgeBasePayload(_Base):
    pass


class KnowledgeBaseResponse(_Base):
    response: List[str]
    collection_name: str


class KnowledgeBaseDeletePayload(BaseModel):
    id: str
