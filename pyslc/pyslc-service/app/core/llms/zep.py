from __future__ import annotations

from logging import Logger

from llama_index.vector_stores.zep import ZepVectorStore

from app.core.llms.base import LlamaEngineBase, LlamaLLMService
from app.core.storage.storage import Storage
from app.core.types import DocParam, UIDType

COL_LIMIT_RANGE = 30


class ZepLLMEngine(LlamaEngineBase):
    """
    ZepLLMEngine is a class that manages the lifecycle of the LLM index.
    """

    __slots__ = [
        "docs",
        "openai_api_key",
        "logger",
        "vector_store",
        "storage_context",
        "embed_model",
        "service_context",
        "index",
        "collection_name" "zep_url",
    ]

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
        self.zep_url: str = zep_url
        super().__init__(
            collection_name=collection_name,
            docs=docs,
            openai_api_key=openai_api_key,
            llm_storage_dir=llm_storage_dir,
            logger=logger,
        )

    def get_vector_store(
        self,
    ):
        return ZepVectorStore(
            api_url=self.zep_url,
            collection_name=self.collection_name,
            embedding_dimensions=1536,
        )


class ZepLLMService(LlamaLLMService):
    """
    ZepLLMService is a service class that manages the lifecycle of ZepLLMEngine instances.
    super class: LLMService (app.core.llms.service.LLMService)
    """

    __slots__ = [
        "zep_url",
        "openai_api_key",
        "llm_storage_dir",
        "logger",
        "storage",
    ]

    def __init__(
        self,
        zep_url: str,
        openai_api_key: str,
        llm_storage_dir: str,
        logger: Logger,
        storage: Storage[UIDType, ZepLLMEngine],
    ):
        self.zep_url: str = zep_url
        super().__init__(
            openai_api_key=openai_api_key,
            llm_storage_dir=llm_storage_dir,
            logger=logger,
            storage=storage,
        )

    def init_engine(self, collection_uid: UIDType, docs: DocParam) -> ZepLLMEngine:
        engine = ZepLLMEngine(
            docs=docs,
            zep_url=self.zep_url,
            openai_api_key=self.openai_api_key,
            llm_storage_dir=self.llm_storage_dir,
            logger=self.logger,
            collection_name=collection_uid,
        )
        return engine
