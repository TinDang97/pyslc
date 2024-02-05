from starlette.types import ASGIApp, Scope, Receive, Send


# create middleware to fix redirect 307 with endpoint without trailing slash
class NonTrailingSlashRedirectMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)
