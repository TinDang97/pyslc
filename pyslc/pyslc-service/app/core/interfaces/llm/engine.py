# Created by tindang at 28/3/24
from typing import Optional, Protocol

from app.core.types import ChatHistory


class LLMEngine(Protocol):
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

    def agent(self, chat_history: Optional[ChatHistory] = None):
        ...
