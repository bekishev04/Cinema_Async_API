import json
import os

from tests.functional.settings import test_settings
import elasticsearch

from tests.functional.utils.index import index_dict

if __name__ == "__main__":
    es = elasticsearch.Elasticsearch(hosts=test_settings.elastic_uri, request_timeout=300)

    for index in index_dict:
        es.options(ignore_status=[400, 404]).indices.delete(index=index)
