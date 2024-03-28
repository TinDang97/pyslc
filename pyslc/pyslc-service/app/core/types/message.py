# Created by tindang at 28/3/24
import enum
from typing import Optional

from pydantic import BaseModel


class MessageRole(str, enum.Enum):
    """
    Message roles class.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"
    CHATBOT = "chatbot"


class ChatMessage(BaseModel):
    """
    Chat message data class.
    """

    name: Optional[str] = None
    content: str
    role: MessageRole

    def __repr__(self):
        """str: Return the string representation of the class. limit to 10 characters."""
        content = self.content
        return f"<{self.__class__.__name__}({content=:_<10.7}, role={self.role})>"
