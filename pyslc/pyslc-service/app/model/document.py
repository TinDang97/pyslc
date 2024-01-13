from sqlalchemy import Column, String, Integer

from app.model.base import ModelBase


class Document(ModelBase):
    __tablename__ = 'document'

    name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_extension = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)
    file_hash = Column(String, nullable=True)
