import time

from loguru import logger
from redis import Redis, ConnectionError

from src.backoff import backoff
from tests.functional.settings import test_settings


@backoff()
def wait():
    logger.debug(f"waiting for redis on {test_settings.redis_uri}")
    r = Redis(host=test_settings.redis_uri.host, port=test_settings.redis_uri.port)
    r.ping()


if __name__ == "__main__":
    wait()
