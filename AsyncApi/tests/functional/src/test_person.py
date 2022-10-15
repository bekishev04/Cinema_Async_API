import pytest
from elasticsearch import AsyncElasticsearch
import aiohttp
import json
from tests.functional.utils.models import Person

# Напишите функциональные тесты для метода /person:
# все граничные случаи по валидации данных;
# поиск с учётом кеша в Redis.


@pytest.fixture(scope='session')
async def es_write_data():
    file_path = 'tests/functional/testdata/person_testdata.json'
    with open(file_path) as json_file:
        data = json.load(json_file)
    obj_list = [Person.parse_obj(item) for item in data]
    bulk_query = []
    for each in obj_list:
        bulk_query.append(
            {"index": {"_index": "persons", "_id": each.id}})
        bulk_query.append(each.dict())
    str_query = '\n'.join([json.dumps(line) for line in bulk_query]) + '\n'

    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200')
    await client.bulk(body=str_query, index='persons')
    await client.close()


async def make_get_request(method: str, params: dict = None):
    method = method
    params = params or {}
    url = f'http://127.0.0.1:8000/api/v1/{method}'
    session = aiohttp.ClientSession()
    async with session.get(url, params=params) as response:
        body = await response.json()
    await session.close()
    return body


@pytest.mark.asyncio
async def test_certain_person_search(es_write_data):
    """Тест поиска конкретного человека."""
    response_list = await make_get_request('persons/persons')
    persons_list = [Person.parse_obj(person) for person in response_list['items']]
    person_id = persons_list[0].id
    response_one = await make_get_request(f'persons/person/{person_id}')
    person = Person.parse_obj(response_one)
    assert person.id == person_id
