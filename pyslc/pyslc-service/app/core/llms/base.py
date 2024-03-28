# Created by tindang at 28/3/24
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger
import os
from typing import Generic, List, Optional, TypeVar
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
from llama_index.vector_stores.types import VectorStore
import openai

from app.core.storage.storage import Storage
from app.core.types import DocParam, UIDType
from app.core.util import hash_string
from app.core.types import ChatHistory

COL_LIMIT_RANGE = 30


class LlamaEngineBase(ABC):
    """
    LlamaEngineBase is a class that manages the lifecycle of the LLM index.
    supper class: LLMEngine (app.core.interfaces.llms.engine.LLMEngine)
    """

    def __init__(
        self,
        collection_name: UIDType,
        docs: DocParam,
        *,
        openai_api_key: str,
        llm_storage_dir: str,
        logger: Logger,
    ):
        self.docs = docs
        self.openai_api_key = openai_api_key
        self.logger = logger

        self.load_openai_config(openai_api_key)
        if isinstance(collection_name, uuid.UUID):
            collection_name = collection_name.hex[:COL_LIMIT_RANGE]

        if collection_name.__len__() > COL_LIMIT_RANGE:
            warn(
                f"Collection name is too long, will be truncated to {COL_LIMIT_RANGE} characters"
            )

        collection_name = hash_string(collection_name)[:COL_LIMIT_RANGE]
        self.collection_name = collection_name
        self.vector_store: VectorStore = self.get_vector_store()

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
            documents=self.to_documents(texts=self.docs),
            storage_context=self.storage_context,
            show_progress=True,
            service_context=self.service_context,
        )

    @abstractmethod
    def get_vector_store(
        self,
    ) -> VectorStore:
        pass

    @staticmethod
    def to_document(text: str) -> Document:
        return Document(doc_id=hash_string(text), text=text)  # noqa

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
            doc = Document(doc_id=hash_string(doc), text=doc)  # noqa
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

    def agent(self, chat_history: Optional[ChatHistory] = None) -> BaseChatEngine:
        _agent = self.index.as_chat_engine(chat_history=chat_history)
        return _agent


T = TypeVar("T", bound=LlamaEngineBase)


class LlamaLLMService(ABC, Generic[T]):
    """
    LlamaLLMService is a service class that manages the lifecycle of LlamaEngineBase instances.
    super class: LLMService (app.core.interfaces.llms.service.LLMService)
    """

    def __init__(
        self,
        openai_api_key: str,
        llm_storage_dir: str,
        logger: Logger,
        storage: Storage[UIDType, T],
    ):
        self.openai_api_key: str = openai_api_key
        self.llm_storage_dir: str = llm_storage_dir
        self.logger: Logger = logger
        self.storage: Storage[uuid.UUID | str, T] = storage

    @staticmethod
    def _get_engine_uid(engine_uid: UIDType) -> UIDType:
        if isinstance(engine_uid, uuid.UUID):
            engine_uid = engine_uid.hex
        return engine_uid[:COL_LIMIT_RANGE]

    def get_engine(self, engine_uid: UIDType) -> T | None:
        engine_uid = self._get_engine_uid(engine_uid)
        engine = self.storage.get(engine_uid)
        return engine

    def add_engine(self, engine_uid: UIDType, engine: T):
        engine_uid = self._get_engine_uid(engine_uid)
        self.storage.add(engine_uid, engine)

    def delete_engine(self, engine_uid: UIDType):
        engine_uid = self._get_engine_uid(engine_uid)
        self.storage.delete(engine_uid)

    @abstractmethod
    def init_engine(self, collection_uid: UIDType, docs: DocParam) -> T:
        ...

    def refresh_engine(self, engine_uid: UIDType, docs: DocParam):
        engine_uid = self._get_engine_uid(engine_uid)
        engine = self.get_engine(engine_uid=engine_uid)
        if not engine:
            raise ValueError("Engine not found")

        engine.refresh_index(docs=docs)

    def __call__(
        self,
        engine_uid: UIDType,
        collection_uid: UIDType,
        docs: Optional[DocParam] = None,
    ) -> T:
        if collection_uid not in self.storage:
            new_engine = self.init_engine(
                collection_uid=collection_uid, docs=docs or []
            )
            self.add_engine(engine_uid=engine_uid, engine=new_engine)
        elif docs:
            self.refresh_engine(engine_uid=engine_uid, docs=docs)

        engine = self.get_engine(engine_uid=engine_uid)
        if engine is None:
            raise ValueError("Engine not found")
        return engine
