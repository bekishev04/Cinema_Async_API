import uuid

import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.helpers import generate_doc, delete_doc
from tests.functional.settings import test_settings


@pytest.mark.asyncio
async def test_search_person(es_write_data, make_get_request):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "full_name": "test",
        }
        for _ in range(50)
    ]

    await es_write_data(es_data, "persons")

    query_data = {"full_name": "test"}
    response = await make_get_request("api/v1/persons/person", query_data)

    assert response.status == 200
    assert len(response.body["items"]) == response.body["total"] == 50


@pytest.mark.asyncio
async def test_cache_person(make_get_request):

    uuid_key = uuid.uuid4()
    data = {"id": uuid_key, "full_name": "Test"}

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    await helpers.async_bulk(es_client, generate_doc([data], "persons"))

    response_first = await make_get_request(f"api/v1/persons/person/{uuid_key}/")
    assert response_first.status == 200
    await helpers.async_bulk(es_client, delete_doc([data], "persons"))

    await es_client.close()

    response_second = await make_get_request(f"api/v1/persons/person/{uuid_key}/")
    assert response_second.status == 200
    assert response_first.body == response_second.body
