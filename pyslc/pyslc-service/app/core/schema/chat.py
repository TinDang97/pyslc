from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class Chat(BaseModel):
    session_id: Optional[int] = Field(...)


class ChatRequest(Chat):
    message: str = Field(...)


class ChatCreate(BaseModel):
    message: str = Field(...)


class ChatResponse(Chat):
    response: List[Dict[str, str]] = Field(...)
