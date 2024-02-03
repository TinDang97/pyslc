from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING

from app.model.base import ModelBase, ModelMixin, TimestampMixin, UserMixin

if TYPE_CHECKING:
    from app.model.collection import Collection


class Knowledge(ModelBase, ModelMixin, TimestampMixin, UserMixin):
    __tablename__ = "knowledge"

    content: Mapped[str] = mapped_column(Column(String, nullable=False))
    collection_id = Column(String, nullable=False)
    collection: Mapped[Collection] = relationship(
        "Collection", back_populates="knowledge"
    )

    def __repr__(self):
        return f"<Knowledge(content={self.content}, metadata={self.metadata}, collection_id={self.collection_id})>"
