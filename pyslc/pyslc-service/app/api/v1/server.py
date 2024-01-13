from fastapi import FastAPI

from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Welcome to pyslc-service!"}


# health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# include the router


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api.server:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
