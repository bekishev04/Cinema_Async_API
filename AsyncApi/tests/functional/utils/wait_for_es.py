import sys
import time

from elasticsearch import Elasticsearch
from loguru import logger

from tests.functional.settings import test_settings

if __name__ == '__main__':
    logger.debug('waiting for es')
    logger.debug(test_settings.elastic_uri)
    es_client = Elasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)
    while True:
        if es_client.ping():
            logger.debug('es answered')
            break
        logger.debug('es doesn\'t answer yet')
        time.sleep(1)
