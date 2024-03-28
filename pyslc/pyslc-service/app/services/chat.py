# Created by tindang at 04/02/2024
from typing import TYPE_CHECKING, Any, Generator

from ..model.message import Message
from app.core.types import UIDType, ChatMessage
from app.schema.chat import (
    ChatCreatePayload,
    ChatCreateResponse,
    ChatListResponsePayload,
)
from app.schema.collection import CollectionResponse
from app.schema.message import MessageResponsePayload, MessageSendPayload
from app.schema.query import QueryParams
from app.core.types.message import MessageRole

if TYPE_CHECKING:
    from app.services.collection import CollectionService
    from app.repository.chat import ChatRepository
    from app.repository.knowledge import KnowledgeRepository
    from app.repository.message import MessageRepository
    from app.core.interfaces.llm import AgentService
    from app.core.interfaces.llm.agent import Agent


class ChatService:
    def __init__(
        self,
        *,
        collection_service: "CollectionService",
        chat_repository: "ChatRepository",
        knowledge_repository: "KnowledgeRepository",
        message_repository: "MessageRepository",
        # core
        agent_service: "AgentService[Agent]",
    ):
        self.collection_service = collection_service
        self.knowledge_repository = knowledge_repository
        self.chat_repository = chat_repository
        self.agent_service = agent_service
        self.message_repository = message_repository

    def get_chats_by_user(self, user_id: UIDType, query: QueryParams):
        chats = self.chat_repository.get_by_user_id(user_id, query)
        return ChatListResponsePayload.model_validate(chats, from_attributes=True)

    def _create_chat_user_message(
        self, payload: MessageSendPayload, user_id: str
    ) -> Message:
        last_message = self.message_repository.get_last_message_by_chat_id(
            payload.chat_uid
        )

        user_message: Message = self.message_repository.create_message(
            chat_uid=payload.chat_uid,
            content=payload.content,
            role=MessageRole.USER,
            created_by=user_id,
            previous_message_id=last_message.uid if last_message else None,
        )
        return user_message

    def chat(self, payload: MessageSendPayload, user_id: str) -> MessageResponsePayload:
        chat_agent = self.agent_service.get_agent(payload.chat_uid)
        if chat_agent is None:
            chat = self.chat_repository.get_chat_by_uid(payload.chat_uid)
            if not chat:
                raise ValueError("Chat not found")

            chat_agent = self.create_chat_agent(chat.uid, chat.collection_uid)

        # Chat with the agent
        response = chat_agent.chat(payload.content)

        # Create user message
        user_message: Message = self._create_chat_user_message(payload, user_id)

        # Create agent message
        response_msg = ""
        for msg in response:
            self.message_repository.create_message(
                chat_uid=payload.chat_uid,
                content=msg.content,
                role=msg.role,
                created_by=user_id,
                previous_message_id=user_message.uid,
            )
            if msg.role == MessageRole.ASSISTANT:
                response_msg = msg.content

        return MessageResponsePayload(
            chat_uid=payload.chat_uid,
            content=payload.content,
            reply_content=response_msg,
        )

    def stream_chat(self, payload: MessageSendPayload, user_id: str):
        chat_agent = self.agent_service.get_agent(payload.chat_uid)
        if chat_agent is None:
            chat = self.chat_repository.get_chat_by_uid(payload.chat_uid)
            if not chat:
                raise ValueError("Chat not found")
            chat_agent = self.create_chat_agent(chat.uid, chat.collection_uid)

        # Chat with the agent
        user_message: Message = self._create_chat_user_message(payload, user_id)

        # Stream chat with the agent
        response = chat_agent.stream(payload.content)

        def response_wrapper() -> Generator[str, Any, None]:
            assistance_response: str = ""
            for chunk in response:
                yield chunk.content

                if chunk.role == MessageRole.ASSISTANT:
                    assistance_response += chunk.content
                else:
                    self.message_repository.create_message(
                        chat_uid=payload.chat_uid,
                        content=chunk.content,
                        role=chunk.role,
                        created_by=user_id,
                        previous_message_id=user_message.uid,
                    )

            self.message_repository.create_message(
                chat_uid=payload.chat_uid,
                content=assistance_response,
                role=MessageRole.ASSISTANT,
                created_by=user_id,
                previous_message_id=user_message.uid,
            )

        return response_wrapper()

    def refresh_engine(self, engine_id: UIDType, collection_uid: UIDType):
        # TODO: Implement this method that refreshes the engine and chat agent
        ...

    def create_chat_agent(self, chat_uid: UIDType, collection_uid: UIDType):
        docs = self.knowledge_repository.get_knowledges_by_collection_uid(
            collection_uid=collection_uid, query=QueryParams(page_size=100)
        )
        messages = self.message_repository.get_messages_by_chat_id(
            chat_uid=chat_uid, query=QueryParams(page_size=100)
        )
        agent = self.agent_service(
            session_id=chat_uid,
            collection_uid=collection_uid,
            docs=[item.content for item in docs.items],
            chat_history=[
                ChatMessage.model_validate(item, from_attributes=True)
                for item in messages.items
            ],
        )
        return agent

    def create_chat(self, payload: ChatCreatePayload, user_id: str):
        collection: CollectionResponse = self.collection_service.get(
            payload.collection_uid
        )
        if not collection:
            raise ValueError("Collection not found")

        chat = self.chat_repository.create_chat(
            title=payload.title,
            description=payload.description,
            collection_uid=payload.collection_uid,
            created_by=user_id,
        )
        self.create_chat_agent(chat.uid, payload.collection_uid)
        return ChatCreateResponse.model_validate(chat, from_attributes=True)
