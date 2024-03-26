import functools
import re
from hashlib import sha256
from typing import List, TypeVar, Type
import orjson

from pydantic import BaseModel

T = TypeVar("T")
BaseT = TypeVar("BaseT", bound=BaseModel)


def split_string(string) -> List[str]:
    return re.findall(r"\b\w+\b", string)


def hash_string(string: str):
    string = "".join(split_string(string))
    return sha256(string.encode()).hexdigest()


def json_serializer(obj):
    return orjson.dumps(obj).decode()


def json_deserializer(obj):
    return orjson.loads(obj)


def model_from_attrs(cls: Type[BaseT], strict=None, context=None):
    @functools.wraps(cls.model_validate)
    def wrapper(obj) -> BaseT:
        return cls.model_validate(
            obj, from_attributes=True, strict=strict, context=context
        )

    return wrapper
