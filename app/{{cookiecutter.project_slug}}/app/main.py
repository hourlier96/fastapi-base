import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

{% if cookiecutter.database == "mongodb (motor)" -%}
from fastapi.concurrency import asynccontextmanager
from pymongo.errors import ConnectionFailure
from app.core.mongodb import MongoDB
{% endif %}

{% if cookiecutter.database == "sqlite (aiosqlite)" or cookiecutter.database == "postgresql (asyncpg)"-%}
from fastapi.concurrency import asynccontextmanager
from app.core.db import engine, Base
from app.core.db import session_factory
from app.api.models.user import User
from app.api.models.todo import Todo
{% endif %}

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

{% if cookiecutter.database == "mongodb (motor)" -%}
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB...")
    try:
        mongo = MongoDB(settings.MONGO_DB_URI, settings.MONGO_DB_NAME)
        app.state.mongo = mongo
        print(
            "Application startup: Successfully connected to MongoDB database "
            f"{settings.MONGO_DB_NAME}!"
        )
    except ConnectionFailure as e:
        if mongo.client:
            mongo.client.close()
        raise RuntimeError("Database connection failed during startup") from e
    yield
    if hasattr(app.state, "mongo_client") and app.state.mongo.client:
        app.state.mongo.client.close()

{% elif cookiecutter.database == "sqlite (aiosqlite)" or cookiecutter.database == "postgresql (asyncpg)"-%}
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    async with session_factory() as db:
        async with db.begin():
            users_to_add = []
            for i in range(1, 10):
                email = f"user{i}@example.com"
                user = User(email=email)
                users_to_add.append(user)
                todo_to_add = []
                for j in range(1, 20):
                    title = f"Title n°{j}"
                    status = "PENDING"
                    user_id = i
                    todo = Todo(title=title, status=status, user_id=user_id)
                    todo_to_add.append(todo)
                db.add_all(todo_to_add)
            db.add_all(users_to_add)
    yield
    async with engine.begin() as conn:
        print("Purging database...")
        await conn.run_sync(Base.metadata.drop_all)
{%- endif %}

{% if cookiecutter.database != "none" -%}
app.router.lifespan_context = lifespan
{%- endif %}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
