import json
import time
from contextlib import contextmanager

import elasticsearch
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

import constants, config
from backoff import backoff
from state import State, JsonFileStorage


@contextmanager
def _conn_text_psycopg2(**kwargs):
    """Контекстный менеджер для postgresql."""
    conn = psycopg2.connect(**kwargs, cursor_factory=DictCursor)
    yield conn
    conn.close()


class PsqlLoader:
    def __init__(self, size, index="movies"):
        self.index = index
        self.size = size

    @backoff()
    def load_batch(self, last_row_crated_at) -> list[dict]:
        with _conn_text_psycopg2(**config.AppSettings().postgres_kwargs) as pg_conn:
            pg_conn: _connection
            cursor = pg_conn.cursor()

            if not last_row_crated_at:
                last_row_crated_at = constants.MIN_DATE

            cursor.execute("SET search_path TO content,public; ")

            cursor.execute(constants.options[self.index], (last_row_crated_at,))
            rows = cursor.fetchmany(self.size)

            return [dict(row) for row in rows]


class ESLoader:
    def __init__(self, index="movies", index_schema="schemas/index_schema_movies.json"):
        self.index = index
        self.index_schema = index_schema
        self.es = elasticsearch.Elasticsearch(
            [config.AppSettings().es_kwargs], request_timeout=300
        )

    @backoff()
    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(
                index=self.index, body=json.load(open(self.index_schema, "r"))
            )

    @backoff()
    def save_to_es(self, data: list[dict]):
        self.es.bulk(index=self.index, body=data)


class PostgresToES:
    def __init__(
        self,
        *,
        index_dict,
        size=100,
        storage_file=None,
    ):
        self.state = State(JsonFileStorage(storage_file))
        self.size = size
        self.index_dict = index_dict

    def migrate(self):
        for index, index_params in self.index_dict.items():
            es_loader = ESLoader(index, index_params.get("index_schema"))
            es_loader.create_index()

            psql_loader = PsqlLoader(self.size, index)
            while rows := psql_loader.load_batch(
                self.state.get_state(f"{index}_last_updated_at")
            ):
                last_row_crated_at = rows[-1]["updated_at"]

                rows = self.prepare_data_for_es(
                    index, index_params.get("model_schema"), rows
                )

                es_loader.save_to_es(rows)
                self.state.retrieve_state(
                    f"{index}_last_updated_at", str(last_row_crated_at)
                )
        time.sleep(60)

    def prepare_data_for_es(self, index: str, model_schema, rows: list[dict]):
        data = []
        for row in rows:
            data.append({"index": {"_index": index, "_id": str(row["id"])}})
            data.append(model_schema(**row).dict())
        return data
