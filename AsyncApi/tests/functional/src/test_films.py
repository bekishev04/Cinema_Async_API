import uuid

import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.helpers import delete_doc, generate_doc
from tests.functional.settings import test_settings
from tests.functional.testdata.films import create_data


pytestmark = pytest.mark.asyncio



async def test_search(es_write_data, make_get_request):
    name = "The Computer game"
    es_data = [
        create_data(name=name)
        for _ in range(50)
    ]

    await es_write_data(es_data, "movies")

    query_data = {"title": name}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    assert response.status == 200
    assert len(response.body["items"]) == 50


async def test_cache_genre(make_get_request):

    uuid_key = uuid.uuid4()
    data = create_data(name="Test", id=uuid_key)

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    await helpers.async_bulk(es_client, generate_doc([data], "movies"))

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == 200

    await helpers.async_bulk(es_client, delete_doc([data], "movies"))

    response_second = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_second.status == 200
    assert response_first.body == response_second.body


async def test_not_found(make_get_request):
    uuid_key = uuid.uuid4()

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == 404
