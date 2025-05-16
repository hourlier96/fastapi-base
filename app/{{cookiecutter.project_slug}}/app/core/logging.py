import logging
import sys
from logging.config import dictConfig
from typing import Any

from app.core.config import settings


def configure_logging(_settings: Any | None = None) -> None:
    """Configure basic logging for the application.

    This sets a console handler with an ISO timestamp and level coming from
    `settings.LOG_LEVEL` if available. Can be extended to JSON/structlog.
    """

    level = getattr(settings, "LOG_LEVEL", logging.INFO)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": "%(asctime)s %(levelname)s [%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {"level": level, "handlers": ["console"]},
    }

    dictConfig(config)


# Convenience alias so modules can `from app.core.logging import log` if desired
log = logging.getLogger(settings.LOG_NAME if hasattr(settings, "LOG_NAME") else "fastapi-base")
