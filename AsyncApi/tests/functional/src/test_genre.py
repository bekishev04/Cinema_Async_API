import json
import uuid

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.helpers import generate_doc, delete_doc
from tests.functional.settings import test_settings


@pytest.mark.asyncio
async def test_search_genre():
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "test",
        }
        for _ in range(50)
    ]

    bulk_query = []
    for row in es_data:
        bulk_query.extend(
            [
                json.dumps(
                    {
                        "index": {
                            "_index": "genres",
                            "_id": row["id"],
                        }
                    }
                ),
                json.dumps(row),
            ]
        )

    str_query = "\n".join(bulk_query) + "\n"

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)
    response = await es_client.bulk(index="genres", body=str_query, refresh=True)
    await es_client.close()

    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")

    session = aiohttp.ClientSession()
    url = test_settings.service_url + "/api/v1/genres/genre"
    query_data = {"name": "test"}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
    await session.close()

    assert status == 200
    assert len(body["items"]) == body["total"] == 50


@pytest.mark.asyncio
async def test_cache_genre(make_get_request):

    uuid_key = uuid.uuid4()
    data = {"id": uuid_key, "name": "Test"}

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)

    await helpers.async_bulk(es_client, generate_doc([data], "genres"))

    response_first = await make_get_request(f"api/v1/genres/genre/{uuid_key}/")
    assert response_first.status == 200

    await helpers.async_bulk(es_client, delete_doc([data], "genres"))

    response_second = await make_get_request(f"api/v1/genres/genre/{uuid_key}/")
    assert response_second.status == 200
    assert response_first.body == response_second.body
