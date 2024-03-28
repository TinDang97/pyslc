from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.schema.types import UIDType
from app.schema.query import ListResponse


class KnownledgeBase(BaseModel):
    content: str


class KnowledgeBasePayload(KnownledgeBase):
    uid: UIDType


class KnowledgeBaseCreatePayload(KnownledgeBase):
    collection_uid: UIDType


class KnowledgeBaseResponse(KnownledgeBase):
    collection_uid: UIDType
    uid: UIDType


class CollectionKnowledgesResponse(ListResponse[KnowledgeBasePayload]):
    items: List[KnowledgeBasePayload]


class KnowledgeBaseUpdatePayload(BaseModel):
    content: str


class KnowledgeBaseListResponse(ListResponse[KnowledgeBaseResponse]):
    items: List[KnowledgeBaseResponse]


class KnowledgeBaseDeletePayload(BaseModel):
    uid: str
