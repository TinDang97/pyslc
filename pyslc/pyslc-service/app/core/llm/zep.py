from __future__ import annotations

from logging import Logger
import os
from typing import List, Union
import uuid
from warnings import warn

from llama_index import (
    Document,
    load_index_from_storage,
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.chat_engine.types import BaseChatEngine
from llama_index.embeddings import OpenAIEmbedding
from llama_index.vector_stores.zep import ZepVectorStore
import openai

from app.core.llm.base import LLMEngine, LLMService
from app.core.storage.storage import Storage
from app.core.types import UIDType
from app.core.util import hash_string

COL_LIMIT_RANGE = 30
DocParam = Union[List[str], str]


class ZepLLMEngine(LLMEngine):
    def __init__(
        self,
        collection_name: UIDType,
        docs: DocParam,
        *,
        zep_url: str,
        openai_api_key: str,
        llm_storage_dir: str,
        logger: Logger,
    ):
        super().__init__(docs, openai_api_key, logger)
        self.load_openai_config(openai_api_key)

        if isinstance(collection_name, uuid.UUID):
            collection_name = collection_name.hex[:COL_LIMIT_RANGE]

        if collection_name.__len__() > COL_LIMIT_RANGE:
            warn(
                f"Collection name is too long, will be truncated to {COL_LIMIT_RANGE} characters"
            )
        collection_name = hash_string(collection_name)[:COL_LIMIT_RANGE]

        self.vector_store = ZepVectorStore(
            api_url=zep_url,
            collection_name=str(collection_name),
            embedding_dimensions=1536,
        )

        if isinstance(docs, str):
            self.docs = [docs]

        data: List[Document] = self.to_documents(texts=self.docs)

        if not os.path.exists(llm_storage_dir):
            os.makedirs(llm_storage_dir)

        try:
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
                persist_dir=llm_storage_dir,
            )
        except FileNotFoundError:
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store,
            )

        self.embed_model = OpenAIEmbedding(
            api_key=openai_api_key,
            embed_batch_size=16,
        )
        self.service_context = ServiceContext.from_defaults(
            embed_model=self.embed_model
        )

        self.index: VectorStoreIndex = VectorStoreIndex.from_documents(
            documents=data,
            storage_context=self.storage_context,
            show_progress=True,
            service_context=self.service_context,
        )

    @staticmethod
    def to_document(text: str) -> Document:
        return Document(doc_id=hash_string(text), text=text)

    def to_documents(self, texts: List[str]) -> List[Document]:
        return [self.to_document(text) for text in texts]

    @staticmethod
    def load_openai_config(api_key: str):
        openai.api_key = api_key

    def load_storage(self, path: str):
        load_index_from_storage(self.storage_context, path)

    def load_index(self, index_id: str):
        return load_index_from_storage(self.storage_context, index_id)

    def add_document(self, doc: str | Document):
        if isinstance(doc, str):
            doc = Document(doc_id=hash_string(doc), text=doc)
        self.index.insert(doc)

    def refresh_index(self, docs: DocParam):
        if isinstance(docs, str):
            docs = [docs]

        data = self.to_documents(texts=docs)
        self.index.refresh(data)

    def query_engine(self):
        return self.index.as_query_engine()

    def retriever(self):
        return self.index.as_retriever()

    def agent(self, chat_history=None) -> BaseChatEngine:
        _agent = self.index.as_chat_engine(chat_history=chat_history)
        return _agent


class ZepLLMService(LLMService[ZepLLMEngine]):
    def __init__(
        self,
        zep_url: str,
        openai_api_key: str,
        llm_storage_dir: str,
        logger: Logger,
        storage: Storage[UIDType, ZepLLMEngine],
    ):
        self.zep_url = zep_url
        self.openai_api_key = openai_api_key
        self.llm_storage_dir = llm_storage_dir
        self.logger = logger
        self.storage = storage

    def get_engine(self, engine_uid: UIDType) -> ZepLLMEngine:
        engine = self.storage.get(engine_uid)
        if engine is None:
            raise ValueError("Engine not found")
        return engine

    def add_engine(self, engine_uid: UIDType, engine: ZepLLMEngine):
        self.storage.add(engine_uid, engine)

    def init_llm_engine(self, collection_uid: UIDType, docs: DocParam) -> ZepLLMEngine:
        engine = ZepLLMEngine(
            docs=docs,
            zep_url=self.zep_url,
            openai_api_key=self.openai_api_key,
            llm_storage_dir=self.llm_storage_dir,
            logger=self.logger,
            collection_name=collection_uid,
        )
        return engine

    def __call__(
        self, engine_uid: UIDType, collection_uid: UIDType, docs: DocParam
    ) -> ZepLLMEngine:
        if collection_uid not in self.storage:
            engine = self.init_llm_engine(collection_uid, docs)
            self.add_engine(engine_uid, engine)
        else:
            engine = self.get_engine(collection_uid)
        return engine
