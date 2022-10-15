import http
import uuid

import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.helpers import generate_doc, delete_doc
from tests.functional.settings import test_settings
from tests.functional.testdata.films import create_data

pytestmark = pytest.mark.asyncio


async def test_search(es_write_data, make_get_request):
    name = "The Computer game"

    es_data = [
        create_data(name=name)
        for _ in range(50)
    ]
    es_data_dict = {d['id']: d for d in es_data}

    await es_write_data(es_data, "movies")

    query_data = {"title": name}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    assert response.status == http.HTTPStatus.OK
    assert len(response.body["items"]) == 50

    # test limit/offset
    query_data = {"title": name, "limit": 10, "offset": 10}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    for item in response.body["items"]:
        reference_item = es_data_dict.get(item["id"], None)
        if not reference_item:
            raise AssertionError
        for k, v in item.items():
            assert reference_item.get(k, None) == v

    assert response.status == http.HTTPStatus.OK
    assert len(response.body["items"]) == 10
    assert response.body["total"] == 50


async def test_not_found(make_get_request):
    uuid_key = uuid.uuid4()

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == http.HTTPStatus.NOT_FOUND


async def test_cache_person(make_get_request):
    uuid_key = uuid.uuid4()
    data = create_data(name="Test", id=uuid_key)

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    await helpers.async_bulk(es_client, generate_doc([data], "movies"))

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == http.HTTPStatus.OK
    await helpers.async_bulk(es_client, delete_doc([data], "movies"))

    await es_client.close()

    response_second = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_second.status == http.HTTPStatus.OK
    assert response_first.body == response_second.body


async def test_accordance(es_write_data, make_get_request):
    name = "The Accordance test"
    es_data = [
        create_data(name=name)
        for _ in range(50)
    ]

    data = []
    for k, i in enumerate(es_data):
        i["imdb_rating"] = k
        data.append(i)

    await es_write_data(es_data, "movies")

    query_data = {"title": name, "sort_by": "imdb_rating", "sort": "asc"}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    assert response.status == http.HTTPStatus.OK

    for i in range(len(data)):
        assert response.body["items"][i]["imdb_rating"] == i
