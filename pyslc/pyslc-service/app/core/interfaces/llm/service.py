# Created by tindang at 28/3/24
from typing import Optional, Protocol, TypeVar

from app.core.interfaces.llm.engine import LLMEngine
from app.core.interfaces.llm.agent import Agent
from app.core.types import ChatMessages, UIDType, DocParam

L = TypeVar("L", bound=LLMEngine)
A = TypeVar("A", bound=Agent, covariant=True)


class LLMService(Protocol[L]):
    def get_engine(self, engine_uid: UIDType) -> L:
        ...

    def add_engine(self, engine_uid: UIDType, engine: L):
        ...

    def delete_engine(self, engine_uid: UIDType):
        ...

    def init_engine(self, collection_uid: UIDType, docs: DocParam):
        ...

    def refresh_engine(self, engine_uid: UIDType, docs: DocParam):
        ...

    def __call__(self, engine_uid, collection_uid: UIDType, docs=None) -> L:
        ...


class AgentService(Protocol[A]):
    def get_agent(self, session_id: UIDType) -> A | None:
        ...

    def add_agent(self, session_id: UIDType, chat_agent):
        ...

    def init_chat_agent(
        self,
        collection_uid: UIDType,
        docs: Optional[DocParam],
        chat_history: Optional[ChatMessages] = None,
    ) -> A:
        ...

    def __call__(
        self,
        session_id: UIDType,
        collection_uid: UIDType,
        docs: Optional[DocParam],
        chat_history: Optional[ChatMessages] = None,
    ) -> A:
        ...
