from __future__ import annotations


from pydantic import BaseModel

from app.core.types import UIDType
from app.schema.query import ListResponse


class KnownledgeBase(BaseModel):
    content: str


class KnowledgeBasePayload(KnownledgeBase):
    uid: UIDType


class KnowledgeBaseCreatePayload(KnownledgeBase):
    collection_uid: UIDType


class KnowledgeBaseResponse(KnownledgeBase):
    collection_uid: UIDType


class CollectionKnowledgesResponse(ListResponse[KnownledgeBase]):
    collection_uid: UIDType


class KnowledgeBaseUpdatePayload(BaseModel):
    content: str


class KnowledgeBaseDeletePayload(BaseModel):
    uid: str
