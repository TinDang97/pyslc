from __future__ import annotations

from contextlib import contextmanager
from typing import TypeVar, Generic, List
from uuid import UUID

from app.core.llm.zep import ZepEngine

T = TypeVar("T")
K = TypeVar("K")


class ChatStorage(Generic[K, T]):
    def __init__(self):
        self._storage = dict[K, T]()

    def __contains__(self, item):
        return item in self._storage

    def get(self, session_id: K) -> T | None:
        return self._storage.get(session_id, None)

    def add(self, session_id: K, instance: T) -> None:
        self._storage[session_id] = instance

    def clear(self, session_id: K) -> None:
        self._storage.pop(session_id)


chat_storage = ChatStorage[UUID, ZepEngine]()


@contextmanager
def get_chat_storage(engine_id: UUID):
    yield chat_storage.get(engine_id)


@contextmanager
def add_chat_storage(
    *, engine_id: UUID, collection_name: str, data: List[str] | None = None, **kwargs
):
    chat_storage.add(engine_id, ZepEngine(collection_name, data))
    yield chat_storage.get(engine_id)
