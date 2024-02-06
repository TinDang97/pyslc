from uuid import UUID

from pydantic import BaseModel, field_validator, Field

from app.core.util import split_string


class ChatBase(BaseModel):
    message: str = Field(..., title="Message")
    collection_id: UUID = Field(..., title="Collection ID")

    @field_validator("message")  # noqa
    @classmethod
    def message_must_not_be_empty(cls, v: str):
        if not v:
            raise ValueError("Message cannot be empty")

        if len(split_string(v)) > 1000:
            raise ValueError("Message cannot be longer than 1000 tokens")

        return v


class ChatCreatePayload(ChatBase):
    pass


class ChatResponsePayload(BaseModel):
    message: str
    collection_id: UUID
