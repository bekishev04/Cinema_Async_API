import time

from redis import Redis, ConnectionError

from functional.settings import test_settings

if __name__ == '__main__':
    r = Redis(test_settings.redis_uri, socket_connect_timeout=1)
    while True:
        try:
            r.ping()
            break
        except ConnectionError:
            time.sleep(1)
            pass
