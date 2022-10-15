import uuid


def create_data(id=None, name: str=None):
    return {
        "id": id or str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "title": name,
        "description": "New World",
        "director": [],
        "actors_names": [],
        "writers_names": [],
        "genre": [],
        "actors": [],
        "writers": [],
    }
