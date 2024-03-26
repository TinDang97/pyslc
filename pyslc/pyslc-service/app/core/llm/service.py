from typing import Protocol, TypeVar

from app.core.llm.base import LLMEngine
from app.core.types import UIDType

L = TypeVar("L", bound=LLMEngine)


class LLMService(Protocol[L]):
    def get_engine(self, engine_uid: UIDType) -> L:
        ...

    def add_engine(self, engine_uid: UIDType, engine: L):
        ...

    def delete_engine(self, engine_uid: UIDType):
        ...

    def init_engine(self, collection_uid: UIDType, docs):
        ...

    def refresh_engine(self, engine_uid: UIDType, docs):
        ...

    def __call__(self, engine_uid, collection_uid: UIDType, docs=None) -> L:
        ...
