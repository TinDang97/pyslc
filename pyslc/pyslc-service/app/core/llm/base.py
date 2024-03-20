# Created by tindang at 17/03/2024
from logging import Logger
from typing import Protocol, TypeVar

from app.core.types import UIDType


class LLMEngineInterface(Protocol):
    def load_storage(self, storage):
        ...

    def load_index(self, index_id):
        ...

    def refresh_index(self, docs):
        ...

    def add_document(self, doc):
        ...

    def query_engine(self):
        ...

    def retriever(self):
        ...

    def agent(self, chat_history=None):
        ...


class LLMEngine(LLMEngineInterface):
    def __init__(self, docs, openai_api_key, logger: Logger):
        self.docs = docs
        self.openai_api_key = openai_api_key
        self.logger = logger

    def load_storage(self, storage):
        ...

    def load_index(self, index_id):
        ...

    def add_document(self, doc):
        ...

    def query_engine(self):
        ...

    def retriever(self):
        ...

    def agent(self, chat_history=None):
        ...

    def refresh_index(self, docs):
        ...


L = TypeVar("L", bound=LLMEngine)


class LLMService(Protocol[L]):
    def get_engine(self, engine_uid: UIDType) -> L:
        ...

    def add_engine(self, engine_uid: UIDType, engine: L):
        ...

    def init_llm_engine(self, collection_uid: UIDType, docs):
        ...

    def __call__(self, engine_uid, collection_uid: UIDType, docs):
        ...
