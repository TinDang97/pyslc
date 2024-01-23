from typing import Optional, List, Dict

from pydantic import BaseModel, validator


class Chat(BaseModel):
    session_id: Optional[str] = None


class ChatRequest(Chat):
    message: str

    @validator("message")  # noqa
    @classmethod
    def validate_message(cls, v):
        if len(v) >= 8192:
            raise ValueError("message must be less than 1000 characters")
        return v.encode().decode("utf-8")


class ChatCreate(BaseModel):
    message: str


class ChatResponse(Chat):
    response: List[Dict[str, str]]
