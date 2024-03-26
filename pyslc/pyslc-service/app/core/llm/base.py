# Created by tindang at 17/03/2024
from logging import Logger
from typing import Protocol


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
