import abc
import uuid

from aioredis import Redis
from elastic_transport import ObjectApiResponse
from fastapi import Depends

from src.database.redis import get_redis
from src.schemas import BaseModelSchema, ArgsPerson, BaseModel, ArgsGenre, ArgsFilmWork
from src.backoff import backoff

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # todo перенести в конфиг


class AbstractRepo(abc.ABC):
    def __init__(self, redis: get_redis = Depends(get_redis)):
        self._redis: Redis = redis

    @backoff()
    async def get_by_id(self, index: str, id: uuid.UUID) -> ObjectApiResponse | None:
        data = await self._redis.get(f"{index}_{id}")
        if not data:
            return None
        return data

    @backoff()
    async def put_by_id(self, index: str, item: BaseModelSchema):
        await self._redis.set(
            f"{index}_{item.id}", item.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    @abc.abstractmethod
    def get_by_query(self, query: ArgsPerson) -> ObjectApiResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def put_by_query(self, query: ArgsPerson, item: BaseModel | BaseModelSchema):
        raise NotImplementedError


class PersonRepo(AbstractRepo):
    @backoff()
    async def get_by_query(self, query: ArgsPerson) -> ObjectApiResponse | None:
        data = await self._redis.get(query.json())
        if not data:
            return None
        return data

    @backoff()
    async def put_by_query(self, query: ArgsPerson, item: BaseModel | BaseModelSchema):
        await self._redis.set(
            query.json(), item.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS
        )


class GenreRepo(AbstractRepo):
    @backoff()
    async def get_by_query(self, query: ArgsGenre) -> ObjectApiResponse | None:
        data = await self._redis.get(query.json())
        if not data:
            return None
        return data

    @backoff()
    async def put_by_query(self, query: ArgsGenre, item: BaseModel | BaseModelSchema):
        await self._redis.set(
            query.json(), item.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS
        )


class FilmWorkRepo(AbstractRepo):
    @backoff()
    async def get_by_query(self, query: ArgsFilmWork) -> ObjectApiResponse | None:
        data = await self._redis.get(query.json())
        if not data:
            return None
        return data

    @backoff()
    async def put_by_query(
        self, query: ArgsFilmWork, item: BaseModel | BaseModelSchema
    ):
        await self._redis.set(
            query.json(), item.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS
        )
