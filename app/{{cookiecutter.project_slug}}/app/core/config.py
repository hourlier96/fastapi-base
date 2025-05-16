import logging

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = "local"
    LOG_LEVEL: str = Field(default=logging.INFO)
    LOG_NAME: str = "fastapi-base"
    PROJECT_NAME: str = "FastAPI Base Environment"

    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

{%- if cookiecutter.database == "mongodb (motor)" %}
    DB_ADDRESS: str = "host.docker.internal"    # or 'localhost' from direct host access
    MONGO_DB_NAME : str = "test_db"
    MONGO_DB_URI: str = f"mongodb://{DB_ADDRESS}:27017/"
{%- elif cookiecutter.database == "postgresql (asyncpg)" %}
    POSTGRES_SERVER: str = Field(...)
    POSTGRES_DB_NAME: str = Field(...)
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"
{%- endif %}

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
