from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.model.base import ModelBase, ModelMixin, TimestampMixin, UserMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.model.document import Document
    from app.model.knowledge import Knowledge


class Collection(ModelBase, ModelMixin, TimestampMixin, UserMixin):
    __tablename__ = "collection"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    documents: Mapped[Document] = relationship(back_populates="collection")
    knowledge: Mapped[Knowledge] = relationship(back_populates="collection")

    def __repr__(self):
        return f"<Collection(name={self.name}, description={self.description})>"
