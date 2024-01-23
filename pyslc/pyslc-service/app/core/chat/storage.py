from __future__ import annotations

from collections import defaultdict
from typing import Dict, TypeVar, Generic

T = TypeVar("T")


class ChatStorage(Generic[T]):
    def __init__(self):
        self._storage: Dict[str, T] = defaultdict()

    def get(self, session_id: str) -> T | None:
        return self._storage.get(session_id)

    def add(self, session_id: str, instance: T) -> None:
        self._storage[session_id] = instance

    def clear(self, session_id: str) -> None:
        self._storage.pop(session_id)
