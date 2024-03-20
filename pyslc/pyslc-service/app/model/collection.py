from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.model.base import ModelBase, TimestampMixin, UserMixin
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.model.document import Document
    from app.model.knowledge import Knowledge
    from app.model.chat import Chat


class Collection(ModelBase, TimestampMixin, UserMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)

    documents: Mapped[List["Document"]] = relationship(back_populates="collection")
    knowledge_parts: Mapped[List["Knowledge"]] = relationship(
        back_populates="collection"
    )
    chats: Mapped[List["Chat"]] = relationship(back_populates="collection")

    def __repr__(self):
        return f"<Collection(name={self.name}, description={self.description})>"
