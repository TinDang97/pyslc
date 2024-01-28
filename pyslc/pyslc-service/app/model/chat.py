from sqlalchemy import Column, String
from app.model.base import ModelBase
from app.model.base import ModelMixin, TimestampMixin, UserMixin


class Chat(ModelBase, ModelMixin, TimestampMixin, UserMixin):
    __tablename__ = "chat"

    session_id = Column(String, nullable=False)
    model = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    status = Column(String, nullable=False)
    error = Column(String, nullable=True)
