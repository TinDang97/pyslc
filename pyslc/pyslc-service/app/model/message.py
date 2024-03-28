# Created by tindang at 26/3/24
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import ModelBase, TimestampMixin, UserMixin
from app.core.types.message import MessageRole

if TYPE_CHECKING:
    from app.model.chat import Chat


class Message(ModelBase, TimestampMixin, UserMixin):
    __tablename__ = "message"

    content: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[MessageRole] = mapped_column(String, nullable=False)

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

    chat_uid = mapped_column(ForeignKey("chat.uid"), nullable=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return (
            f"<Message(content={self.content}, "
            f"previous_chat_id={self.previous_message_id}, "
            f"next_chat_id={self.previous_message_id})>"
        )
