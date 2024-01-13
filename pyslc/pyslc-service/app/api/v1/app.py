from fastapi import FastAPI

from app.api.v1 import router
from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

for api_router in router.__dict__:
    if isinstance(api_router, str):
        app.include_router(api_router, prefix=settings.api_v1_str)
