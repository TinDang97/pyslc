from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware as _TrustedHostMiddleware,
)
from starlette.types import ASGIApp

from app.settings import settings


class TrustedHostMiddleware(_TrustedHostMiddleware):
    def __init__(self, app: ASGIApp, allowed_hosts=None) -> None:
        super().__init__(app, allowed_hosts=allowed_hosts or settings.trusted_hosts)
