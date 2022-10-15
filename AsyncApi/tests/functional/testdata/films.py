import uuid


def create_data(id=None, name: str=None):
    return {
        "id": id or str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "title": name,
        "description": "New World",
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'b92cc01c-e0a1-448d-97b4-c1ff3e5f0e75', 'name': 'Ann'},
            {'id': '3302d318-d6d4-4fe9-a345-e29f9e8c62f6', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '35d147db-1f2c-4894-b40d-09333a2c0f99', 'name': 'Ben'},
            {'id': 'cb1697e5-06e0-4cb6-a474-1e9f52e09d5c', 'name': 'Howard'}
        ],
    }
