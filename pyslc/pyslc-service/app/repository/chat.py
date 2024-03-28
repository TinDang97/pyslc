from typing import Optional

from sqlalchemy import desc, select

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

    _entity = Chat

    def create_chat(
        self, title: str, description: str, collection_uid: UIDType, created_by: str
    ):
        """
        Create a chat.
        """
        return self.create(
            {
                "title": title,
                "description": description,
                "collection_uid": collection_uid,
            },
            created_by,
        )

    def get_chat_by_uid(self, chat_uid: UIDType) -> Optional[Chat]:
        """
        Get a single chat by its session ID.

        :param chat_uid: chat ID
        :return: chat
        """
        return self.get(chat_uid)

    def get_by_collection_uid(
        self, collection_uid: UIDType, query: QueryParams
    ) -> ChatListResponsePayload:
        """
        Get a single chat by its collection ID.

        :param collection_uid: collection ID
        :param query: query parameters
        :return: chats
        """
        with self.session_factory() as session:
            smt = select(Chat).filter(
                Chat.collection_uid == collection_uid, Chat.is_deleted.__eq__(False)
            )

            if query.order_by:
                order_by = Chat.__dict__[query.order_by]
                smt = (
                    smt.order_by(order_by)
                    if not query.desc
                    else smt.order_by(desc(order_by))
                )

            page: ListResponse[Chat] = paginate(smt, query, session)
            return ChatListResponsePayload.model_validate(page, from_attributes=True)

    def get_by_user_id(
        self, user_id: UIDType, query: QueryParams
    ) -> ListResponse[Chat]:
        """
        Get all chats by user ID.
        """
        with self.session_factory() as session:
            smt = select(Chat).filter(
                Chat.created_by == user_id, Chat.is_deleted.__eq__(False)
            )
            if query.order_by:
                order_by = Chat.__dict__[query.order_by]
                smt = (
                    smt.order_by(order_by)
                    if not query.desc
                    else smt.order_by(desc(order_by))
                )
            return paginate(smt, query, session)
