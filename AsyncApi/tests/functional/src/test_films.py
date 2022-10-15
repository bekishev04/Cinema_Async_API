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


async def test_not_found(make_get_request):
    uuid_key = uuid.uuid4()

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == 404
