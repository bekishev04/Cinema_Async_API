import time

from loguru import logger
from redis import Redis, ConnectionError

from tests.functional.settings import test_settings

if __name__ == '__main__':
    logger.debug(f'waiting for redis on {test_settings.redis_uri}')
    r = Redis(host=test_settings.redis_uri.host, port=test_settings.redis_uri.port)

    while True:
        try:
            r.ping()
            logger.debug('redis answered')
            break
        except ConnectionError:
            logger.debug('redis doesn\'t answer')
            time.sleep(1)
            pass
