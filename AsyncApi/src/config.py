import os
from typing import Any

from fastapi.responses import ORJSONResponse
from loguru import logger
from pydantic import RedisDsn, SecretStr
from pydantic.env_settings import BaseSettings

from src import strings


class AppSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/doc"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = strings.APP_TITLE
    version: str = "1.0"

    redis_uri: RedisDsn = "redis://127.0.0.1:6379"
    elastic_uri: str = ""

    secret_key: SecretStr = ""

    allowed_hosts: list[str] = ["*"]

    default_response_class = ORJSONResponse

    jwt_secret: str
    jwt_algorithm: str

    class Config:
        validate_assignment = True
        env_file = ".env"

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "default_response_class": self.default_response_class,
        }

    def configure_logging(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))

        logger.add(
            os.path.join(os.path.dirname(basedir), "logs", "app.log"),
            level="DEBUG" if self.debug else "ERROR",
        )


settings = AppSettings()
