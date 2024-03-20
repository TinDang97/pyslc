from __future__ import annotations

from llama_index.agent.runner.base import BaseAgentRunner
from llama_index.chat_engine.types import StreamingAgentChatResponse

from app.core.storage import Storage
from app.core.types import UIDType


class Agent:
    def __init__(self, engine: BaseAgentRunner, **agent_config):
        self.engine = engine
        self.agent_config = agent_config

    def chat(self, message: str, chat_history=None):
        return self.engine.chat(message, chat_history)

    def stream(self, message: str, chat_history=None):
        stream_msg: StreamingAgentChatResponse = self.engine.stream_chat(message, chat_history)
        for msg in stream_msg.response_gen:
            if msg is None:
                break
            yield msg


class AgentService:
    def __init__(
        self,
        agent_storage: Storage[UIDType, Agent],
        **agent_config,
    ):
        self.agent_storage = agent_storage
        self.agent_config = agent_config

    def get_agent(self, session_id: UIDType) -> Agent:
        agent = self.agent_storage.get(session_id=session_id)
        if agent is None:
            raise ValueError("Chat agent not found")
        return agent

    def add_agent(self, session_id: UIDType, chat_agent: Agent):
        if session_id in self.agent_storage:
            raise ValueError("Chat agent already exists")
        self.agent_storage.add(session_id, chat_agent)

    def init_chat_agent(self, engine: BaseAgentRunner) -> Agent:
        return Agent(engine, **self.agent_config)

    def __call__(self, session_id: UIDType, engine: BaseAgentRunner) -> Agent:
        if session_id in self.agent_storage:
            return self.get_agent(session_id)

        agent = self.init_chat_agent(engine)
        self.add_agent(session_id, agent)
        return agent
