# Created by tindang at 26/3/24
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.core.util import split_string
from app.schema.query import ListResponse
from app.schema.types import UIDType


class MessageBase(BaseModel):
    content: str = Field(..., title="Content")
    chat_uid: UIDType = Field(..., title="Chat ID")

    @field_validator("content")  # noqa
    @classmethod
    def message_must_not_be_empty(cls, v: str):
        if not v:
            raise ValueError("Message cannot be empty")

        if len(split_string(v)) > 1024:
            raise ValueError("Message cannot be longer than 1024 tokens")

        return v


class MessageSendPayload(MessageBase):
    pass


class MessageResponsePayload(MessageBase):
    reply_content: str


class MessageListResponsePayload(ListResponse[MessageResponsePayload]):
    items: List[MessageResponsePayload]
