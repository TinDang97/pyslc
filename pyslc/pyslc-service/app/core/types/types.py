# Created by tindang at 20/03/2024
from typing import List, Union
from uuid import UUID

from app.core.types.message import ChatMessage

DocParam = List[str]
UIDType = Union[UUID, str]
ChatMessages = List[ChatMessage]
ChatHistory = List[ChatMessage]
