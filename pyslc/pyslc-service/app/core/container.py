# Created by tindang at 17/03/2024

import logging

from dependency_injector import containers, providers

from app.core.agents.llama import LlamaAgentService
from app.core.interfaces.llm import Agent
from app.core.llms.zep import ZepLLMEngine, ZepLLMService
from app.core.storage import Storage
from app.databases.database import Database
from app.repository import (
    ChatRepository,
    CollectionRepository,
    KnowledgeRepository,
    MessageRepository,
)
from app.services import (
    ChatService,
    CollectionService,
    KnowledgeService,
)
from app.settings import settings


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(logging.getLogger, name="pyslc-service")

    # config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.deps",
            "app.api.v1.endpoint.chat",
            "app.api.v1.endpoint.collection",
            "app.api.v1.endpoint.knowledge",
        ]
    )

    # database
    database = providers.Singleton(Database, db_url=settings.db.uri, logger=logger)

    # repositories
    chat_repository = providers.Factory(
        ChatRepository,
        session_factory=database.provided.session,
        logger=logger,
    )
    message_repository = providers.Factory(
        MessageRepository,
        session_factory=database.provided.session,
        logger=logger,
    )
    collection_repository = providers.Factory(
        CollectionRepository,
        session_factory=database.provided.session,
        logger=logger,
    )
    knowledge_repository = providers.Factory(
        KnowledgeRepository,
        session_factory=database.provided.session,
        logger=logger,
    )

    # core service
    llm_storage = providers.Singleton(Storage[str, ZepLLMEngine])

    llm_service = providers.Factory(
        ZepLLMService,
        zep_url=settings.zep_url,
        openai_api_key=settings.openai_api_key,
        llm_storage_dir=settings.llm_storage_dir,
        logger=logger,
        storage=llm_storage,
    )

    agent_storage = providers.Singleton(Storage[str, Agent])
    agent_service = providers.Factory(
        LlamaAgentService,
        storage=agent_storage,
        llm_service=llm_service,
    )

    # services
    collection_service = providers.Factory(
        CollectionService,
        collection_repository=collection_repository,
        knowledge_repository=knowledge_repository,
    )
    chat_service = providers.Factory(
        ChatService,
        collection_service=collection_service,
        chat_repository=chat_repository,
        knowledge_repository=knowledge_repository,
        message_repository=message_repository,
        agent_service=agent_service,
    )
    knowledge_service = providers.Factory(
        KnowledgeService,
        knowledge_repository=knowledge_repository,
        collection_repository=collection_repository,
    )
