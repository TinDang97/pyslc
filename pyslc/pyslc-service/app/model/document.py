from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING

from app.model.base import ModelBase

if TYPE_CHECKING:
    from app.model.collection import Collection


class Document(ModelBase):
    __tablename__ = "document"

    name: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_extension = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[str] = mapped_column(Integer, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)
    file_hash: Mapped[str] = mapped_column(String, nullable=False)

    collection_id = mapped_column(ForeignKey("collection.id"), nullable=False)
    collection: Mapped[Collection] = relationship(
        "Collection", back_populates="documents"
    )

    def __repr__(self):
        return f"<Document(name={self.name}, file_name={self.file_name}, file_hash={self.file_hash})>"
