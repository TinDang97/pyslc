# Created by tindang at 28/3/24
from llama_index.agent.runner.base import BaseAgentRunner
from llama_index.chat_engine.types import StreamingAgentChatResponse
from llama_index.core.llms.types import (
    ChatMessage as _ChatMessage,
    MessageRole as _MessageRole,
)

from app.core.storage import Storage
from app.core.types import ChatHistory, DocParam, UIDType, MessageRole, ChatMessage

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.interfaces.llm import LLMService


def _parse_chat_history(chat_history: ChatHistory):
    return [
        _ChatMessage(role=_MessageRole(msg.role), content=msg.content)
        for msg in chat_history
        if not msg.role == MessageRole.TOOL
    ]


class LlamaAgent:
    """
    This class is a wrapper around the BaseAgentRunner class. It is used to
    interact with the chat engine.

    super class: app.core.interfaces.llms.agent.LlamaAgent
    """

    def __init__(self, engine: BaseAgentRunner, **agent_config):
        self.engine = engine
        self.agent_config = agent_config

    def chat(self, message: str, chat_history: Optional[ChatHistory] = None):
        _chat_history = None
        if chat_history:
            _chat_history = _parse_chat_history(chat_history)

        response = self.engine.chat(message, _chat_history)
        return [
            ChatMessage(role=MessageRole.ASSISTANT, content=response.response),
            *[
                ChatMessage(
                    role=MessageRole.TOOL, content=msg.content, name=msg.tool_name
                )
                for msg in response.sources
            ],
        ]

    def stream(self, message: str, chat_history: Optional[ChatHistory] = None):
        _chat_history = None
        if chat_history:
            _chat_history = _parse_chat_history(chat_history)

        stream_msg: StreamingAgentChatResponse = self.engine.stream_chat(
            message, _chat_history
        )
        for msg in stream_msg.response_gen:
            if msg is None:
                break
            yield ChatMessage(role=MessageRole.ASSISTANT, content=msg)

        for tool_msg in stream_msg.sources:
            yield ChatMessage(
                role=MessageRole.TOOL, content=tool_msg.content, name=tool_msg.tool_name
            )


class LlamaAgentService:
    """
    This class is a service class for the LlamaAgent class. It is used
    to manage the agent storage.

    super class: app.core.interfaces.llms.service.AgentService
    """

    def __init__(
        self,
        llm_service: "LLMService",
        storage: Storage[UIDType, LlamaAgent],
        **agent_config,
    ):
        self.storage = storage
        self.agent_config = agent_config
        self.llm_service = llm_service

    def get_agent(self, session_id: UIDType) -> LlamaAgent | None:
        agent = self.storage.get(session_id=session_id)
        return agent

    def add_agent(self, session_id: UIDType, chat_agent: LlamaAgent):
        if session_id in self.storage:
            raise ValueError("Chat agent already exists")
        self.storage.add(session_id, chat_agent)

    def init_chat_agent(
        self,
        collection_uid: UIDType,
        docs: DocParam,
        chat_history: Optional[ChatHistory] = None,
    ) -> LlamaAgent:
        engine = self.llm_service.__call__(collection_uid, collection_uid, docs)
        _chat_history = None
        if chat_history:
            _chat_history = _parse_chat_history(chat_history)
        return LlamaAgent(engine.agent(_chat_history), **self.agent_config)

    def __call__(
        self,
        session_id: UIDType,
        collection_uid: UIDType,
        docs: DocParam,
        chat_history: Optional[ChatHistory] = None,
    ) -> LlamaAgent:
        if session_id in self.storage:
            agent = self.storage.get(session_id)
            if agent is None:
                raise ValueError("Chat agent not found")
            return agent

        agent = self.init_chat_agent(collection_uid, docs, chat_history)
        self.add_agent(session_id, agent)
        return agent
