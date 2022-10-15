import sys
import time

from elasticsearch import Elasticsearch, exceptions
from loguru import logger

from src.backoff import backoff
from tests.functional.settings import test_settings


# @backoff()
def wait():
    logger.debug("waiting for es")
    logger.debug(test_settings.elastic_uri)
    es_client = Elasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    if not es_client.ping():
        raise exceptions.ConnectionError

if __name__ == "__main__":
    wait()