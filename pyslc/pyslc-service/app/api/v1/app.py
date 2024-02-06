from app.api.v1.builder import AppBuilder

builder = AppBuilder()
app = builder.build()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
