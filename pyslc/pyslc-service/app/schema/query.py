# Created by tindang at 04/02/2024
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, computed_field
from enum import Enum


T = TypeVar("T")


class ListOrderOptions(str, Enum):
    desc = "desc"
    asc = "asc"


class QueryParams(BaseModel):
    page: int = 1
    page_size: int = 10
    order: ListOrderOptions = ListOrderOptions.desc
    order_by: str = "updated_at"

    @computed_field  # type: ignore[misc]
    @property
    def limit(self) -> int:
        return self.page_size

    @computed_field   # type: ignore[misc]
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @computed_field  # type: ignore[misc]
    @property
    def desc(self) -> bool:
        return self.order == ListOrderOptions.desc

    def next_query_params(self) -> "QueryParams":
        return QueryParams(
            page=self.page + 1,
            page_size=self.page_size,
            order=self.order,
            order_by=self.order_by,
        )


class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    total: Optional[int] = None
    pagination: Optional[QueryParams] = None

    @computed_field  # type: ignore[misc]
    @property
    def count(self) -> int:
        return len(self.items)

    @computed_field  # type: ignore[misc]
    @property
    def max_page(self) -> Optional[int]:
        if self.pagination is None or self.total is None or self.total == 0:
            return None

        return self.total // self.pagination.page_size + 1
