from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.schema.types import UIDType
from app.schema.query import ListResponse


class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None


class CollectionPayload(CollectionBase):
    uid: str
    knowledge_content: List[str]


class UpdateCollectionPayload(CollectionBase):
    knowledge_content: Optional[str] = None
    collection_name: Optional[str] = None


class CollectionResponse(CollectionBase):
    uid: UUID


class CollectionListResponse(ListResponse[CollectionResponse]):
    items: List[CollectionResponse]


class KnowledgeBaseResponse(BaseModel):
    uid: UIDType
    content: str


class CollectionWithKnowledgeResponse(CollectionBase):
    uid: UIDType
    knowledges: List[KnowledgeBaseResponse]


class CollectionCreatePayload(CollectionBase):
    knowledge_content: Optional[List[str]] = None


class CollectionCreateResponse(CollectionBase):
    uid: UIDType
    knowledge_content: List[KnowledgeBaseResponse]
