# Created by tindang at 04/02/2024
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.core.types import UIDType
from app.schema.chat import (
    AgentChatCreatePayload,
    AgentChatResponse,
    ChatCreatePayload,
    ChatResponsePayload,
    ChatListResponsePayload,
)
from app.schema.collection import CollectionResponse
from app.schema.query import QueryParams

if TYPE_CHECKING:
    from app.services.collection import CollectionService
    from app.repository.chat import ChatRepository
    from app.repository.knowledge import KnowledgeRepository
    from app.core.llm.base import LLMService
    from app.core.chat.chat import AgentService


class ChatService:
    def __init__(
        self,
        *,
        collection_service: "CollectionService",
        chat_repository: "ChatRepository",
        knowledge_repository: "KnowledgeRepository",
        # core
        llm_service: "LLMService",
        agent_service: "AgentService",
    ):
        self.collection_service = collection_service
        self.knowledge_repository = knowledge_repository
        self.chat_repository = chat_repository
        self.llm_service = llm_service
        self.agent_service = agent_service

    @staticmethod
    def create_chat_session():
        return uuid4()

    @staticmethod
    def get_engine_id(
        collection_id: UIDType,
        user_id: UIDType,
    ):
        engine_id = f"{collection_id}_{user_id}"
        return engine_id

    def get_chats_by_user(self, user_id: UIDType, query: QueryParams):
        chats = self.chat_repository.get_by_user_id(
            user_id,
            query,
        )
        return ChatListResponsePayload.model_validate(chats, from_attributes=True)

    def chat(self, payload: ChatCreatePayload) -> ChatResponsePayload:
        chat_agent = self.agent_service.get_agent(payload.session_id)
        if chat_agent is None:
            raise ValueError("Chat agent not found")

        response = chat_agent.chat(payload.message)
        return ChatResponsePayload(
            message=response.response,
            session_id=payload.session_id,
        )

    def stream_chat(self, payload: ChatCreatePayload):
        chat_agent = self.agent_service.get_agent(payload.session_id)
        if chat_agent is None:
            raise ValueError("Chat agent not found")

        response = chat_agent.stream(payload.message)
        return response

    def refresh_engine(self, engine_id: UIDType, collection_id):
        collection: CollectionResponse = self.collection_service.get(collection_id)
        if not collection:
            raise ValueError("Collection not found")

        knowledges = self.knowledge_repository.get_knowledge_by_collection(
            collection_id=collection_id
        )
        llm_engine = self.llm_service.get_engine(engine_id)
        llm_engine.refresh_index(knowledges.raw())

    def get_engine(self, collection_id: UIDType, user_id: UIDType):
        engine_id = self.get_engine_id(collection_id, user_id)
        llm_engine = self.llm_service.get_engine(engine_id)
        if llm_engine is None:
            raise ValueError("Engine not found")
        return llm_engine

    def create_engine(self, collection_uid: UIDType, user_id: UIDType):
        collection: CollectionResponse = self.collection_service.get(collection_uid)
        if not collection:
            raise ValueError("Collection not found")

        knowledges = self.knowledge_repository.get_knowledge_by_collection(
            collection_id=collection_uid
        )
        return self.llm_service.__call__(
            engine_uid=self.get_engine_id(collection_uid, user_id),
            collection_uid=collection_uid,
            docs=knowledges.raw(),
        )

    def create_chat_agent(
        self, payload: AgentChatCreatePayload, user_id: str
    ) -> AgentChatResponse:
        llm_engine = self.get_engine(payload.collection_id, user_id)
        session_id = self.create_chat_session()
        self.agent_service(session_id, llm_engine.agent())
        return AgentChatResponse(session_id=session_id)

    def get_chat_agent(self, session_id: UUID):
        return self.agent_service.get_agent(session_id)
