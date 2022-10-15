import uuid


def create_data(id=None, name=None):
    return {
        "id": id or str(uuid.uuid4()),
        "name": name,
    }
