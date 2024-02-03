from __future__ import annotations

from contextlib import contextmanager
from typing import TypeVar, Generic, List

from app.core.llm.zep import ZepEngine

T = TypeVar("T")


class ChatStorage(Generic[T]):
    def __init__(self):
        self._storage = dict[str, T]()

    def __contains__(self, item):
        return item in self._storage

    def get(self, session_id: str) -> T | None:
        return self._storage.get(session_id, None)

    def add(self, session_id: str, instance: T) -> None:
        self._storage[session_id] = instance

    def clear(self, session_id: str) -> None:
        self._storage.pop(session_id)


chat_storage = ChatStorage[ZepEngine]()


@contextmanager
def get_chat_storage(collection_name: str):
    yield chat_storage.get(collection_name)


@contextmanager
def add_chat_storage(collection_name: str, data: List[str]):
    chat_storage.add(collection_name, ZepEngine(collection_name, data))
    yield chat_storage.get(collection_name)
