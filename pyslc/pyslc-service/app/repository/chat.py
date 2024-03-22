from logging import Logger
from typing import Callable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.types import UIDType
from app.model.chat import Chat
from app.repository.base import BaseRepository
from app.repository.util import paginate
from app.schema.chat import ChatListResponsePayload
from app.schema.query import ListResponse, QueryParams


class ChatRepository(BaseRepository[Chat]):
    """
    Chat repository class.
    """

    def __init__(self, session_factory: Callable[[], Session], logger: Logger):
        """
        Constructor.
        """
        super().__init__(Chat, session_factory, logger)

    def get_by_session_id(self, session_id: UIDType) -> Optional[Chat]:
        """
        Get a single chat by its session ID.

        :param session_id: session ID
        :return: chat
        """
        with self.session_factory() as session:
            chat = select(Chat).filter(Chat.session_id == session_id, Chat.is_deleted.__eq__(False))
            Chat.is_deleted.__eq__(False)
        return session.execute(chat).scalar_one_or_none()

    def get_by_collection_id(self, collection_id: UIDType, query: QueryParams) -> ChatListResponsePayload:
        """
        Get a single chat by its collection ID.

        :param collection_id: collection ID
        :param query: query parameters
        :return: chats
        """
        with self.session_factory() as session:
            smt = select(Chat).filter(Chat.collection_id == collection_id, Chat.is_deleted.__eq__(False))
            page: ListResponse[Chat] = paginate(smt, query, session)
            return ChatListResponsePayload.model_validate(page, from_attributes=True)

    def get_by_user_id(
        self, user_id: UIDType, query: QueryParams
    ) -> ChatListResponsePayload:
        """
        Get all chats by user ID.
        """
        with self.session_factory() as session:
            smt = select(Chat).filter(
                Chat.created_by == user_id,
                Chat.is_deleted.__eq__(False)
            )
            page: ListResponse[Chat] = paginate(smt, query, session)
            return ChatListResponsePayload.model_validate(page, from_attributes=True)
