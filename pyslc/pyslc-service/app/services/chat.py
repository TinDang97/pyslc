# Created by tindang at 04/02/2024
import uuid

from app.schema.chat import (
    ChatCreatePayload,
    ChatResponsePayload,
    AgentChatCreatePayload,
    AgentChatResponse,
)
from app.schema.collection import CollectionResponse
from app.schema.knowledge import KnowledgeBaseListPayloadResponse
from app.services.base import ServiceBase
from app.services.collection import CollectionService
from app.core.llm.llm import get_engine, add_engine
from app.core.chat.chat import get_chat_storage, add_chat_storage


class ChatService(ServiceBase):
    def __init__(self, collection_service: CollectionService):
        super().__init__()
        self.collection_service: CollectionService = collection_service

    def get(self, id):
        pass

    def list(self, limit, offset):
        pass

    def create(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    @staticmethod
    def create_chat_session():
        return uuid.uuid4()

    def chat(self, payload: ChatCreatePayload) -> ChatResponsePayload:
        with get_chat_storage(payload.session_id) as chat_agent:
            if chat_agent is None:
                raise ValueError("Chat agent not found")

            response = chat_agent.chat(payload.message)
            return ChatResponsePayload(
                message=response.response,
                session_id=payload.session_id,
            )

    @staticmethod
    def stream_chat(session_id, message: str):
        with get_chat_storage(session_id) as chat_agent:
            if chat_agent is None:
                raise ValueError("Chat agent not found")

            response = chat_agent.stream(message)
            return response

    def get_engine(self, collection_id: str, auto_create: bool = True):
        collection: CollectionResponse = self.collection_service.get(collection_id)
        if not collection:
            raise ValueError("Collection not found")

        with get_engine(collection.id) as zep_engine:
            if zep_engine is not None:
                return zep_engine
            elif not auto_create:
                raise ValueError("Engine not found")

        knowledge_parts: KnowledgeBaseListPayloadResponse = (
            self.collection_service.knowledge_service.get_knowledge_bases_by_collection(
                collection_id
            )
        )
        if not knowledge_parts.data:
            raise ValueError("No knowledge base found for this collection")

        with add_engine(
            engine_id=collection.id,
            collection_name=collection.name,
            data=knowledge_parts.data,
        ) as zep_engine:
            return zep_engine

    def create_chat_agent(self, payload: AgentChatCreatePayload) -> AgentChatResponse:
        zep_engine = self.get_engine(payload.collection_id)
        session_id = self.create_chat_session()
        with add_chat_storage(
            engine_id=session_id,
            engine=zep_engine.chat_agent(),
        ):
            return AgentChatResponse(
                session_id=session_id,
            )

    @staticmethod
    def get_chat_agent(session_id: uuid.UUID):
        with get_chat_storage(session_id) as chat_agent:
            if chat_agent is None:
                raise ValueError("Chat agent not found")
            return chat_agent
