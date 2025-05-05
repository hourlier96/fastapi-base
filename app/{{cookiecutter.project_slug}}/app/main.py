import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_PREFIX)

{% if cookiecutter.database == "mongodb (motor)" %}
from fastapi.concurrency import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    from app.core.mongodb import MongoDB
    from pymongo.errors import ConnectionFailure

    print("Connecting to MongoDB...")
    try:
        mongo = MongoDB(settings.MONGO_DB_URI, settings.MONGO_DB_NAME)
        app.state.mongo = mongo
        print(
            f"Application startup: Successfully connected to MongoDB database {os.getenv('MONGO_DB_NAME')}!"
        )
    except ConnectionFailure as e:
        if mongo.client:
            mongo.client.close()
        raise RuntimeError("Database connection failed during startup") from e
    yield
    if hasattr(app.state, "mongo_client") and app.state.mongo.client:
        app.state.mongo.client.close()
{%- endif %}

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
