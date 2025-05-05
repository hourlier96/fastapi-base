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
    DB_ADDRESS: str = "host.docker.internal"       # or localhost without container
    MONGO_DB_NAME : str = "test_db"
    MONGO_DB_URI: str = f"mongodb://{DB_ADDRESS}:27017/"  
{%- endif %}    

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
