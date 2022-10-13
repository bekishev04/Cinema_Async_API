import os

from loguru import logger
from pydantic import RedisDsn
from pydantic.env_settings import BaseSettings


class TestSettings(BaseSettings):
    debug: bool = False
    redis_uri: RedisDsn = "redis://127.0.0.1:6379"
    elastic_uri: str = "https://127.0.0.1:9200"
    es_index = 'movies'
    es_id_field = 'id'

    class Config:
        validate_assignment = True
        env_file = ".env"

    def configure_logging(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))

        logger.add(
            os.path.join(os.path.dirname(basedir), "logs", "app.log"),
            level="DEBUG" if self.debug else "ERROR",
        )


test_settings = TestSettings()
