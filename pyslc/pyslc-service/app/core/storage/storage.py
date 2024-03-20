from __future__ import annotations

from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")


class Storage(Generic[K, T]):
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

    def __call__(self, session_id: K) -> T | None:
        return self.get(session_id)
