from __future__ import annotations

from contextlib import contextmanager
import logging
import os
import sys
from typing import List
from uuid import UUID

from llama_index import (
    Document,
    load_index_from_storage,
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.chat_engine.context import BaseChatEngine
from llama_index.embeddings import OpenAIEmbedding
from llama_index.vector_stores.zep import ZepVectorStore
import openai

from app.core.llm.storage import ChatStorage
from app.core.util import hash_string
from app.settings import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

openai.api_key = settings.openai_api_key


class LlmEngine:
    def __init__(
        self,
        collection_name: str,
        data: List[str],
    ):
        collection_name = hash_string(collection_name)[:30]
        self.vector_store = ZepVectorStore(
            api_url=settings.zep_url,
            collection_name=collection_name,
            embedding_dimensions=1536,
        )

        docs = [Document(id_=hash_string(d), text=d) for d in data]

        if not os.path.exists(settings.llm_storage_dir):
            os.makedirs(settings.llm_storage_dir)

        try:
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
                persist_dir=settings.llm_storage_dir,
            )
        except FileNotFoundError:
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

        self.index: VectorStoreIndex = VectorStoreIndex.from_documents(
            documents=docs,
            storage_context=self.storage_context,
            show_progress=True,
            service_context=self.service_context,
        )

    def load_storage(self, path: str):
        load_index_from_storage(self.storage_context, path)

    def load_index(self, index_id: str):
        return load_index_from_storage(self.storage_context, index_id)

    def add_document(self, doc: str | Document):
        if isinstance(doc, str):
            doc = Document(id_=hash_string(doc), text=doc)
        self.index.insert(doc)

    def refresh_index(self, docs: List[str]):
        docs = [Document(id_=hash_string(d), text=d) for d in docs]
        self.index.refresh(docs)

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
def add_engine(*, engine_id: UUID, collection_name: str, data: List[str]):
    engine = LlmEngine(collection_name, data)
    engine_storage.add(engine_id, engine)
    yield engine_storage.get(engine_id)
