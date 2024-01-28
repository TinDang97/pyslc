from fastapi import FastAPI
from llama_index import SimpleDirectoryReader

from app.core.llm.zep import ZepEngine
from app.settings import settings
from app.api.v1.endpoint.chat import router as chat_router, storage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    print("injecting demo")
    # load the model
    doc = SimpleDirectoryReader("./demo").load_data()
    storage.get("demo", ZepEngine("pauldemo", documents=doc))


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


# include the endpoint
app.include_router(chat_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api.server:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
