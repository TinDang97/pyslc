from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.core.types import UIDType


class _Base(BaseModel):
    content: str
    collection_uid: UIDType


class KnowledgeBasePayload(_Base):
    pass


class KnowledgeBaseCreatePayload(_Base):
    pass


class KnowledgeBaseResponse(_Base):
    uid: UIDType
    content: str


class KnowledgeBaseListPayloadResponse(BaseModel):
    collection_uid: UIDType
    data: List[KnowledgeBaseResponse]
    size: int


class KnowledgeBaseUpdatePayload(BaseModel):
    content: str


class KnowledgeBaseDeletePayload(BaseModel):
    id: str
