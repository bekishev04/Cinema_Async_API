import uuid

import pytest


@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genre": ["Action", "Sci-Fi"],
            "title": "The Computer game",
            "description": "New World",
            "director": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        }
        for _ in range(50)
    ]

    await es_write_data(es_data, "movies")

    query_data = {"title": "The Computer game"}
    response = await make_get_request("api/v1/film-work/movie", query_data)

    assert response.status == 200
    assert len(response.body["items"]) == 50
