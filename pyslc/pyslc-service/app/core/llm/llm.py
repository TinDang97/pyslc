from __future__ import annotations

import logging
import sys
from contextlib import contextmanager
from typing import List
from uuid import UUID

import openai
from llama_index.chat_engine.context import BaseChatEngine
from llama_index import VectorStoreIndex, StorageContext, ServiceContext, Document
from llama_index.embeddings import OpenAIEmbedding
from llama_index.vector_stores.zep import ZepVectorStore
from llama_index import load_index_from_storage

from app.core.llm.storage import ChatStorage
from app.settings import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

openai.api_key = settings.openai_api_key


class LlmEngine:
    def __init__(
        self,
        collection_name: str,
    ):
        self.vector_store = ZepVectorStore(
            api_url=settings.zep_url,
            collection_name=collection_name,
            embedding_dimensions=1536,
        )

        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store,
        )
        self.embed_model = OpenAIEmbedding(
            api_key=settings.openai_api_key,
            embed_batch_size=16,
        )
        self.service_context = ServiceContext.from_defaults(
            embed_model=self.embed_model
        )

        self.index: VectorStoreIndex = VectorStoreIndex(
            storage_context=self.storage_context,
            show_progress=True,
            service_context=self.service_context,
        )

    def load_storage(self, path: str):
        load_index_from_storage(self.storage_context, path)

    def load_index(self, index_id: str):
        return load_index_from_storage(self.storage_context, index_id)

    def add_documents(self, doc: str | Document):
        doc = Document(text=doc)
        self.index.insert(doc)

    def query_engine(self):
        return self.index.as_query_engine()

    def retriever(self):
        return self.index.as_retriever()

    def chat_agent(self, chat_history=None) -> BaseChatEngine:
        agent = self.index.as_chat_engine(chat_history=chat_history)
        return agent


engine_storage = ChatStorage[UUID, LlmEngine]()


@contextmanager
def get_engine(engine_id: UUID):
    yield engine_storage.get(engine_id)


@contextmanager
def add_engine(*, engine_id: UUID, collection_name: str, data: List[str] | None = None):
    engine = LlmEngine(collection_name)

    for _d in data or ():
        engine.add_documents(_d)

    engine_storage.add(engine_id, engine)
    yield engine_storage.get(engine_id)
