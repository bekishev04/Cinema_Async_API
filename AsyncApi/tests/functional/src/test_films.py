import http
import uuid

import pytest

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

    assert response.status == http.HTTPStatus.OK
    assert len(response.body["items"]) == 50

    # test limit/offset
    query_data = {"title": name, "limit":10, "offset": 10}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    assert response.status == http.HTTPStatus.OK
    assert len(response.body["items"]) == 10
    assert response.body["total"] == 50


async def test_not_found(make_get_request):
    uuid_key = uuid.uuid4()

    response_first = await make_get_request(f"api/v1/film-work/movie/{uuid_key}")
    assert response_first.status == http.HTTPStatus.NOT_FOUND
