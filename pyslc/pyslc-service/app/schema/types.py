# Created by tindang at 28/3/24
from pydantic import AfterValidator
from typing import Annotated
from app.core.types import UIDType as UIDTypeBase
from uuid import UUID


def cast2uuid(value: str) -> UIDTypeBase:
    try:
        if isinstance(value, UUID):
            return value
        return UUID(value)
    except ValueError:
        return value


UIDType = Annotated[UIDTypeBase, AfterValidator(cast2uuid)]
