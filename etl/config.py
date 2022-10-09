from loguru import logger
from dotenv import load_dotenv
from pydantic import BaseSettings, Field
from typing import Any, Dict
import os


load_dotenv()


class AppSettings(BaseSettings):
    debug: bool = False

    # настройки Postgres
    dbname: str = Field(env="DB_NAME")
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASSWORD")
    pg_host: str = Field(env="DB_HOST", default="127.0.0.1")
    pg_port: str = Field(env="DB_PORT", default="5432")

    # настройки Elasticsearch
    scheme: str = Field(env="SCHEME", default="127.0.0.1")
    es_host: str = Field(env="DB_HOST_ELASTIC", default="127.0.0.1")
    es_port: str = Field(env="ELASTIC_PORT", default="9200")

    @property
    def postgres_kwargs(self) -> Dict[str, Any]:
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.pg_host,
            "port": self.pg_port,
        }

    @property
    def es_kwargs(self) -> Dict[str, Any]:
        return {
            "scheme": self.scheme,
            "host": self.es_host,
            "port": self.es_port,
        }

    def configure_logging(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))

        logger.add(
            os.path.join(os.path.dirname(basedir), "logs", "app.log"),
            level="DEBUG" if self.debug else "ERROR",
        )


settings = AppSettings()
settings.configure_logging()
