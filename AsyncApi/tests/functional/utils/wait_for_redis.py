import time

from redis import Redis, ConnectionError

if __name__ == '__main__':
    r = Redis('127.0.0.1', socket_connect_timeout=1)
    while True:
        try:
            r.ping()
            break
        except ConnectionError:
            time.sleep(1)
            pass
