from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.model.base import ModelBase, ModelMixin, TimestampMixin, UserMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Collection(ModelBase, ModelMixin, TimestampMixin, UserMixin):
    __tablename__ = "collection"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    documents = relationship("Document", back_populates="collection")
    knowledge = relationship("Knowledge", back_populates="collection")

    def __repr__(self):
        return f"<Collection(name={self.name}, description={self.description})>"
