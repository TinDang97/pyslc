from typing import List

from pydantic import BaseModel, Field

from app.schema.types import UIDType
from app.schema.query import ListResponse


class ChatBase(BaseModel):
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")


class ChatCreatePayload(BaseModel):
    collection_uid: str = Field(..., title="Collection ID")
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")


class ChatCreateResponse(ChatBase):
    uid: UIDType = Field(..., title="Chat ID")
    collection_uid: UIDType = Field(..., title="Collection ID")
    created_by: str = Field(..., title="Created by")


class ChatPayload(ChatBase):
    pass


class ChatInfoResponsePayload(ChatBase):
    uid: UIDType = Field(..., title="Chat ID")


class ChatListResponsePayload(ListResponse[ChatInfoResponsePayload]):
    items: List[ChatInfoResponsePayload]
