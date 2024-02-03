from starlette.responses import RedirectResponse
from starlette.types import ASGIApp


# create middleware to fix redirect 307 with endpoint without trailing slash
class NonTrailingSlashRedirectMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, request, call_next):
        if request.url.path.endswith("/"):
            return await call_next(request)
        return RedirectResponse(request.url.path + "/", status_code=307)
