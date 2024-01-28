from uuid import uuid4

from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.zep import ZepVectorStore
from llama_index.storage.storage_context import StorageContext

zep_api_url = "http://localhost:8000"
collection_name = f"graham{uuid4().hex}"

vector_store = ZepVectorStore(
    api_url=zep_api_url,
    collection_name=collection_name,
    embedding_dimensions=1536,
)

documents = SimpleDirectoryReader("../data/paul_graham/").load_data()

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()

response = query_engine.query("What did the author do growing up?")
