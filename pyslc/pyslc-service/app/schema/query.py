# Created by tindang at 04/02/2024
from typing import Generic, Iterator, List, Optional, TypeVar, Annotated

from pydantic import BaseModel, computed_field, Field
from enum import Enum

T = TypeVar("T")


class ListOrderOptions(str, Enum):
    desc = "desc"
    asc = "asc"


class QueryParams(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field()] = 10
    order: ListOrderOptions = ListOrderOptions.desc
    order_by: str = "updated_at"

    @computed_field  # type: ignore[misc]
    @property
    def limit(self) -> int:
        return self.page_size

    @computed_field  # type: ignore[misc]
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
    def max_page(self) -> Optional[int]:
        if self.pagination is None or self.total is None or self.total == 0:
            return None

        return self.total // self.pagination.page_size + 1

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index) -> T:
        return self.items[index]

    def __contains__(self, item) -> bool:
        return item in self.items

    def __reversed__(self) -> Iterator[T]:
        return reversed(self.items)
