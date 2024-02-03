# Created by tindang at 04/02/2024

from pydantic import BaseModel


class QueryParams(BaseModel):
    limit: int = 10
    offset: int = 0
