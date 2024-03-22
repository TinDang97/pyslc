from typing import Optional
from fastapi import FastAPI

from app.core.container import Container
from app.settings import settings


async def startup_event():
    print("Starting up...")


async def shutdown_event():
    print("Shutting down...")


async def root():
    return {"message": "Welcome to pyslc-service!"}


# health check
async def health_check():
    return {"status": "ok"}


class ExtendedFastAPI(FastAPI):
    def __init__(self, container: Container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container


class AppBuilder:
    def __init__(
        self,
        app: Optional[FastAPI] = None,
    ):
        if app:
            self.app = app
            setattr(self.app, "container", Container())
        else:
            self.app = ExtendedFastAPI(
                title=settings.app_name,
                description=settings.app_description,
                version=settings.app_version,
                redirect_slashes=True,
                container=Container(),
            )

    def add_event(self, event: str, handler):
        self.app.on_event(event)(handler)
        return self

    def add_startup_event(self) -> "AppBuilder":
        self.add_event("startup", startup_event)
        return self

    def add_shutdown_event(self) -> "AppBuilder":
        self.add_event("shutdown", shutdown_event)
        return self

    def add_health_check(self) -> "AppBuilder":
        self.app.get("/health")(health_check)
        return self

    def add_root(self) -> "AppBuilder":
        self.app.get("/")(root)
        return self

    def add_middleware(self) -> "AppBuilder":
        from app.api.v1.middleware.redirect import NonTrailingSlashRedirectMiddleware
        from fastapi.middleware.cors import CORSMiddleware

        self.app.add_middleware(NonTrailingSlashRedirectMiddleware)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allow_origins,
            allow_credentials=settings.cors_allow_credentials,
            allow_methods=settings.cors_allow_methods,
            allow_headers=settings.cors_allow_headers,
        )
        return self

    def add_router(self) -> "AppBuilder":
        # include the endpoint
        from app.api.v1.endpoint.chat import router as chat_router
        from app.api.v1.endpoint.collection import router as collection_router
        from app.api.v1.endpoint.knowledge import router as knowledge_router

        self.app.include_router(chat_router, prefix="/chat", tags=["chat"])
        self.app.include_router(
            collection_router, prefix="/collection", tags=["collection"]
        )
        self.app.include_router(
            knowledge_router, prefix="/knowledge", tags=["knowledge"]
        )
        return self

    def build(self) -> FastAPI:
        return (
            self.add_startup_event()
            .add_shutdown_event()
            .add_root()
            .add_middleware()
            .add_router()
            .app
        )
