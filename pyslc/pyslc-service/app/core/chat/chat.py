from __future__ import annotations

from contextlib import contextmanager
from typing import TypeVar, Generic
from uuid import UUID

from llama_index.agent.runner.base import BaseAgentRunner
from llama_index.chat_engine.types import StreamingAgentChatResponse

from app.core.llm.storage import ChatStorage

T = TypeVar("T", bound=BaseAgentRunner)


class ChatAgent(Generic[T]):
    def __init__(self, engine: T):
        self.engine = engine

    def chat(self, message: str, chat_history=None):
        return self.engine.chat(message, chat_history)

    def stream(self, message: str, chat_history=None):
        stream_msg: StreamingAgentChatResponse = self.engine.stream_chat(
            message, chat_history
        )
        for msg, _, _ in stream_msg.response_gen:
            yield msg


chat_storage = ChatStorage[UUID, ChatAgent]()


@contextmanager
def get_chat_storage(engine_id: UUID):
    yield chat_storage.get(engine_id)


@contextmanager
def add_chat_storage(*, engine_id: UUID, engine: T):
    chat_storage.add(engine_id, ChatAgent(engine))
    yield chat_storage.get(engine_id)
