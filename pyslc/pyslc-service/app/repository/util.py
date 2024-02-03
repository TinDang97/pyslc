from app.model.base import Base
from typing import Type


def map_dict_to_entity(base: Type[Base], *, data, collection_name) -> Base:
    return base(data=data, collection_name=collection_name)
