from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import ModelBase, TimestampMixin, UserMixin

if TYPE_CHECKING:
    from app.model.collection import Collection
    from app.model.message import Message


class Chat(ModelBase, TimestampMixin, UserMixin):
    __tablename__ = "chat"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")

    collection_uid = mapped_column(ForeignKey("collection.uid"), nullable=False)
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="chats"
    )

    def __repr__(self):
        return f"<Chat(name={self.title}, description={self.description})>"
