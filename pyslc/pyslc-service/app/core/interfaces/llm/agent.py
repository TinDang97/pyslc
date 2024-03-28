# Created by tindang at 28/3/24
from typing import Optional, Protocol, Generator, Sequence

from app.core.types import ChatHistory
from app.core.types.message import ChatMessage


class Agent(Protocol):
    def chat(
        self, message: str, chat_history: Optional[ChatHistory] = None
    ) -> Sequence[ChatMessage]:
        ...

    def stream(
        self, message: str, chat_history: Optional[ChatHistory] = None
    ) -> Generator[ChatMessage, None, None]:
        ...
