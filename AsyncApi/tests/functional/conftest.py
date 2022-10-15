import json
from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@dataclass
class HTTPResponse:
    body: dict
    status: int


@pytest.fixture
def es_write_data():
    async def inner(data: list[dict], index: str):
        bulk_query = []
        for row in data:
            bulk_query.extend(
                [
                    json.dumps(
                        {
                            "index": {
                                "_index": index,
                                "_id": row["id"],
                            }
                        }
                    ),
                    json.dumps(row),
                ]
            )
        str_query = "\n".join(bulk_query) + "\n"
        client = AsyncElasticsearch(hosts=test_settings.elastic_uri, verify_certs=False)
        response = await client.bulk(body=str_query, index=index, refresh=True)

        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def make_get_request():
    async def inner(url: str, query_data: dict = None):
        session = aiohttp.ClientSession()
        async with session.get(
            f"{test_settings.service_url}/" + url, params=query_data
        ) as response:
            body = await response.json()
            status = response.status
        await session.close()

        return HTTPResponse(body=body, status=status)

    return inner
