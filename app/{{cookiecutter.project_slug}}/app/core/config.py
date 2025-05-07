import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "local"
    LOG_LEVEL: int = logging.INFO
    LOG_NAME: str = "fastapi-base"
    PROJECT_NAME: str = "FastAPI Base Environment"

    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

{%- if cookiecutter.database == "mongodb (motor)" %}
    DB_ADDRESS: str = "localhost"       # or host.docker.internal from containerized env
    MONGO_DB_NAME : str = "test_db"
    MONGO_DB_URI: str = f"mongodb://{DB_ADDRESS}:27017/"
{%- elif cookiecutter.database == "postgresql (asyncpg)" %}
    POSTGRES_DB_NAME: str = "{{cookiecutter.project_slug}}_db"
    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://postgres:postgres@localhost:5436/{POSTGRES_DB_NAME}"
{%- endif %}


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
