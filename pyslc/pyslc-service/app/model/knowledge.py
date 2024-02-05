from uuid import UUID

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING

from app.model.base import ModelBase, TimestampMixin, UserMixin

if TYPE_CHECKING:
    from app.model.collection import Collection


class Knowledge(ModelBase, TimestampMixin, UserMixin):
    __tablename__ = "knowledge"

    content: Mapped[str] = mapped_column(String, nullable=False)
    collection_id: Mapped[UUID] = Column(ForeignKey("collection.id"), nullable=False)
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="knowledge_parts"
    )

    def __repr__(self):
        return f"<Knowledge(content={self.content}, metadata={self.metadata}, collection_id={self.collection_id})>"
