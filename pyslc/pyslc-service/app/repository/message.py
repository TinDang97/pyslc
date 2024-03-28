# Created by tindang at 26/3/24
from typing import Optional

from sqlalchemy import select

from app.core.types import UIDType
from app.core.types.message import MessageRole
from app.model.message import Message
from app.repository.base import BaseRepository
from app.repository.util import paginate
from app.schema.query import ListResponse, QueryParams


class MessageRepository(BaseRepository[Message]):
    """
    Message repository class.
    """

    _entity = Message

    def create_message(
        self,
        chat_uid: UIDType,
        content: str,
        role: MessageRole,
        created_by: UIDType,
        previous_message_id: Optional[UIDType] = None,
    ) -> Message:
        """
        Create a message.
        """
        with self.session_factory() as session:
            message = Message(
                chat_uid=chat_uid,
                content=content,
                role=role,
                created_by=created_by,
                previous_message_id=previous_message_id,
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message

    def get_messages_by_chat_id(
        self, chat_uid: UIDType, query: QueryParams
    ) -> ListResponse[Message]:
        """
        Get messages by chat ID.
        """
        with self.session_factory() as session:
            smt = select(Message).filter(
                Message.chat_uid == chat_uid, Message.is_deleted.__eq__(False)
            )
            return paginate(smt, query, session)

    def get_last_message_by_chat_id(self, chat_uid: UIDType) -> Optional[Message]:
        """
        Get the last message by chat ID.
        """
        with self.session_factory() as session:
            smt = (
                select(Message)
                .filter(Message.chat_uid == chat_uid, Message.is_deleted.__eq__(False))
                .order_by(Message.created_at.desc())
            )
            return session.execute(smt).scalars().first()
