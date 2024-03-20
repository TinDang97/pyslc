from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import String, ForeignKey


from app.model.base import ModelBase
from app.model.base import ModelMixin, TimestampMixin, UserMixin

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.model.collection import Collection


class Message(ModelBase, ModelMixin, TimestampMixin, UserMixin):
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


class Chat(ModelBase, ModelMixin, TimestampMixin, UserMixin):
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    messages: Mapped[List[Message]] = relationship(back_populates="chat")

    collection_id = mapped_column(ForeignKey("collection.id"), nullable=False)
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="chats"
    )
    session_id: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<Chat(name={self.title}, description={self.description})>"
