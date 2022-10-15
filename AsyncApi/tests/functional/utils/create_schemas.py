import json
import os

from tests.functional.settings import test_settings
import elasticsearch

from tests.functional.utils.index import index_dict

es = elasticsearch.Elasticsearch([test_settings.elastic_uri], request_timeout=300)

for index in index_dict:
    dir = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(dir, index_dict[index]["index_schema"])
    if not es.indices.exists(index=index):
        es.indices.create(body=json.load(open(file, "r")), index=index)
