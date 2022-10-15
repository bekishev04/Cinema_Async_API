import http
import uuid

import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.helpers import generate_doc, delete_doc
from tests.functional.settings import test_settings
from tests.functional.testdata.genres import create_data

pytestmark = pytest.mark.asyncio



async def test_search_genre(make_get_request, es_write_data):
    name = "test"
    es_data = [
        create_data(name=name)
        for _ in range(50)
    ]

    await es_write_data(es_data, "genres")

    query_data = {"name": name}
    response = await make_get_request("api/v1/genres/genre", query_data)

    assert response.status == http.HTTPStatus.OK
    assert len(response.body["items"]) == response.body["total"] == 50



async def test_cache_genre(make_get_request):

    uuid_key = uuid.uuid4()
    data = create_data(name="Test", id=uuid_key)

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    await helpers.async_bulk(es_client, generate_doc([data], "genres"))

    response_first = await make_get_request(f"api/v1/genres/genre/{uuid_key}")
    assert response_first.status == http.HTTPStatus.OK

    await helpers.async_bulk(es_client, delete_doc([data], "genres"))

    response_second = await make_get_request(f"api/v1/genres/genre/{uuid_key}")
    assert response_second.status == http.HTTPStatus.OK
    assert response_first.body == response_second.body


async def test_not_found(make_get_request):
    uuid_key = uuid.uuid4()

    response_first = await make_get_request(f"api/v1/genres/genre/{uuid_key}")
    assert response_first.status == http.HTTPStatus.NOT_FOUND