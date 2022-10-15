from typing import Generator


def generate_doc(docs: list[dict], index: str) -> Generator:
    for doc in docs:
        yield {"_index": index, "_id": doc["id"], "_source": doc}


def delete_doc(docs: list[dict], index: str) -> Generator:
    for doc in docs:
        yield {
            "_op_type": "delete",
            "_index": index,
            "_id": doc["id"],
        }
