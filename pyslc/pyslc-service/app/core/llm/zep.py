from typing import List


from app.settings import settings
from llama_index import VectorStoreIndex, StorageContext
from llama_index.readers import StringIterableReader
from llama_index.vector_stores.zep import ZepVectorStore
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = settings.openai_api_key


class ZepEngine:
    def __init__(self, collection_name: str, data: List[str]):
        self.vector_store = ZepVectorStore(
            api_url=settings.zep_url,
            collection_name=collection_name,
            embedding_dimensions=1536,
        )
        self.doc = StringIterableReader().load_data(data)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        self.index: VectorStoreIndex = VectorStoreIndex.from_documents(
            self.doc, storage_context=self.storage_context
        )
        self.query_engine = self.index.as_query_engine()
        self.rag_engine = self.index.as_retriever()

    def query(self, query: str):
        return self.query_engine.query(query)

    def retrieve(self, query: str):
        return self.rag_engine.retrieve(query)
