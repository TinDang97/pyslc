# Created by tindang at 04/02/2024
from enum import Enum
from typing import Annotated, Generic, List, Optional, TypeVar

from pydantic import BaseModel, computed_field, Field

T = TypeVar("T")
BaseT = TypeVar("BaseT", bound=BaseModel)


class ListOrderOptions(str, Enum):
    desc = "desc"
    asc = "asc"


class QueryParams(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field(ge=1, le=100)] = 10
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
    class Config:
        arbitrary_types_allowed = True

    items: List[T]
    total: Optional[int] = None
    next_page: Optional[QueryParams] = None
    current_page: QueryParams

    @computed_field  # type: ignore[misc]
    @property
    def max_page(self) -> Optional[int]:
        if self.next_page is None or self.total is None or self.total == 0:
            return self.current_page.page

        return self.total // self.next_page.page_size + 1

    def __len__(self):
        return len(self.items)

    def __contains__(self, item) -> bool:
        return item in self.items
