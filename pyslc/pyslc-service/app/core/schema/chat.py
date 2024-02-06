from typing import Optional, List

from pydantic import BaseModel, validator, Field
from uuid import uuid4


class Chat(BaseModel):
    session_id: Optional[str] = None


class CreateQueryRequestPayload(BaseModel):
    document: List[str]
    name: str = Field(default_factory=lambda: str(uuid4().hex))

    @validator("document", pre=True)  # noqa
    @classmethod
    def validate_message(cls, v: List[str]):
        doc = list(map(lambda x: x.strip()[:500], v))
        return doc


class ChatCreate(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
