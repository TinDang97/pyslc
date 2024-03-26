from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.core.types import UIDType


class _Base(BaseModel):
    content: str


class KnowledgeBasePayload(_Base):
    uid: UIDType


class KnowledgeBaseCreatePayload(_Base):
    collection_uid: UIDType


class KnowledgeBaseResponse(_Base):
    collection_uid: UIDType
    content: str


class KnowledgeBaseListPayloadResponse(BaseModel):
    collection_uid: UIDType
    data: List[KnowledgeBaseResponse]
    size: int


class KnowledgeBaseUpdatePayload(BaseModel):
    content: str


class KnowledgeBaseDeletePayload(BaseModel):
    uid: str
