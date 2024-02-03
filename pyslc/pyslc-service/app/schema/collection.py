from typing import Optional, List

from pydantic import BaseModel


class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None


class CollectionPayload(CollectionBase):
    id: str
    knowledge_content: List[str]


class UpdateCollectionPayload(CollectionBase):
    knowledge_content: Optional[str] = None
    collection_name: Optional[str] = None


class CollectionResponse(CollectionBase):
    id: str


class CollectionWithKnowledgeResponse(CollectionBase):
    id: str
    knowledge_content: List[str]


class CollectionCreatePayload(CollectionBase):
    knowledge_content: Optional[List[str]] = None
