from typing import Type

from sqlalchemy import func, Select
from sqlalchemy.orm import Session

from app.model.base import Base
from app.schema.query import ListResponse, QueryParams


def map_dict_to_entity(base: Type[Base], *_, **kwargs) -> Base:
    return base(**kwargs)


def paginate(smt: Select, query: QueryParams, session: Session) -> ListResponse:
    """Paginate the query."""
    paginated_query = smt.offset(query.offset).limit(query.limit)
    total = session.query(func.count()).select_from(smt.subquery()).scalar()
    return ListResponse(
        total=total,
        items=list(session.execute(paginated_query).unique().scalars().all()),
        next_page=QueryParams(
            page=query.page + 1,
            page_size=query.page_size,
            order=query.order,
            order_by=query.order_by,
        )
        if query.offset + query.page_size <= total
        else None,
        current_page=query,
    )
