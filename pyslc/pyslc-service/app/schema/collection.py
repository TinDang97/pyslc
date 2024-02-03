from pydantic import BaseModel


class CollectionBase(BaseModel):
    collection_name: str


class CollectionPayload(CollectionBase):
    knowledge_content: str
