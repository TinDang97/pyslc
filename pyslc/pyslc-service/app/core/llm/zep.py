from typing import List


from app.settings import settings
from llama_index import VectorStoreIndex, StorageContext, Document, ServiceContext
from llama_index.readers import StringIterableReader
from llama_index.vector_stores.zep import ZepVectorStore
from llama_index.embeddings import OpenAIEmbedding

import openai
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

openai.api_key = settings.openai_api_key


class ZepEngine:
    def __init__(
        self,
        collection_name: str,
        data: List[str] = [],
        documents: List[Document] = [],
    ):
        self.vector_store = ZepVectorStore(
            api_url=settings.zep_url,
            collection_name=collection_name,
            embedding_dimensions=1536,
        )
        if documents:
            self.doc = documents
        else:
            self.doc = StringIterableReader().load_data(data)
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
            self.doc,
            storage_context=self.storage_context,
            show_progress=True,
            service_context=self.service_context,
        )
        self.query_engine = self.index.as_query_engine()
        self.rag_engine = self.index.as_retriever()

    def query(self, query: str):
        return self.query_engine.query(query)

    def retrieve(self, query: str):
        return self.rag_engine.retrieve(query)
