from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import desc, func, Select
from sqlalchemy.orm import Session

from app.model.base import Base
from app.schema.query import ListResponse, QueryParams

T = TypeVar("T", bound=BaseModel)


def map_dict_to_entity(base: Type[Base], *_, **kwargs) -> Base:
    return base(**kwargs)


def paginate(smt: Select, query: QueryParams, session: Session) -> ListResponse[T]:
    """Paginate the query."""
    if query.order_by:
        smt = smt.order_by(query.order_by) if not query.desc else smt.order_by(desc(query.order_by))

    paginated_query = smt.offset((query.page - 1) * query.page_size).limit(query.page_size)
    return ListResponse(
        total=session.query(func.count()).select_from(smt.subquery()).scalar(),
        items=list(session.execute(paginated_query).scalars().all()),
        pagination=QueryParams(
            page=query.page + 1,
            page_size=query.page_size,
            order=query.order,
            order_by=query.order_by,
        ),
    )
