from pydantic import BaseModel, field_validator, Field

from app.core.util import split_string


class ChatBase(BaseModel):
    message: str = Field(..., title="Message")
    collection_id: str = Field(..., title="Collection ID")

    @field_validator("message")
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
    collection_id: str
    collection_name: str
