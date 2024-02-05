from app.model.base import Base
from typing import Type


def map_dict_to_entity(base: Type[Base], *_, **kwargs) -> Base:
    return base(**kwargs)
