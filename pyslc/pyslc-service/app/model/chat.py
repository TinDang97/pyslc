from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import ModelBase, TimestampMixin, UserMixin

if TYPE_CHECKING:
    from app.model.collection import Collection


class Message(ModelBase, TimestampMixin, UserMixin):
    __tablename__ = "message"

    content: Mapped[str] = mapped_column(String, nullable=False)

    previous_message_id: Mapped[str] = mapped_column(
        ForeignKey("message.uid"), nullable=True
    )
    previous_message: Mapped["Message"] = relationship(
        uselist=False,
        foreign_keys=[previous_message_id],
        remote_side=[previous_message_id],
    )

    next_message_id: Mapped[str] = mapped_column(
        ForeignKey("message.uid"), nullable=True
    )
    next_message: Mapped["Message"] = relationship(
        uselist=False,
        foreign_keys=[next_message_id],
        remote_side=[next_message_id],
    )

    chat_id = mapped_column(ForeignKey("chat.uid"), nullable=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return (
            f"<Message(content={self.content}, "
            f"previous_chat_id={self.previous_message_id}, "
            f"next_chat_id={self.previous_message_id})>"
        )


class Chat(ModelBase, TimestampMixin, UserMixin):
    __tablename__ = "chat"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    messages: Mapped[List[Message]] = relationship(back_populates="chat")

    collection_id = mapped_column(ForeignKey("collection.uid"), nullable=False)
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="chats"
    )
    session_id: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<Chat(name={self.title}, description={self.description})>"
