import abc
import uuid
from typing import Optional

from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src import schemas
from src.database.elastic import get_elastic
from src.backoff import backoff


class AbstractRepo(abc.ABC):
    def __init__(self, es: get_elastic = Depends(get_elastic)):
        self._es: AsyncElasticsearch = es

    @abc.abstractmethod
    def get_by(self, id: uuid.UUID) -> ObjectApiResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, query: schemas.ArgsPaginate) -> ObjectApiResponse:
        raise NotImplementedError


class FilmWorkRepo(AbstractRepo):

    _index = "movies"

    @backoff()
    async def get_by(self, id: uuid.UUID) -> ObjectApiResponse:
        try:
            resp = await self._es.get(id=str(id), index=self._index)
        except NotFoundError:
            resp = None

        return resp

    @backoff()
    async def find_by(self, query: schemas.ArgsFilmWork) -> ObjectApiResponse:
        filter_ = []
        sort_ = []
        bool_ = {}

        if query.rating:
            filter_.append({"term": {"imdb_rating": query.rating}})

        if query.title:
            bool_["must"] = {"match": {"title": query.title}}

        if filter_:
            bool_["filter"] = filter_

        if query.sort_by and query.sort:
            sort_.append([{query.sort_by: query.sort}])

        body = {
            "query": {"bool": bool_},
        }

        resp = await self._es.search(
            index=self._index,
            body=body,
            size=query.limit,
            sort=sort_ or None,
            from_=query.offset,
        )

        return resp


class GenreRepo(AbstractRepo):

    _index = "genres"

    @backoff()
    async def get_by(self, id: uuid.UUID) -> ObjectApiResponse:
        try:
            resp = await self._es.get(id=str(id), index=self._index)
        except NotFoundError:
            resp = None

        return resp

    @backoff()
    async def find_by(self, query: schemas.ArgsGenre) -> ObjectApiResponse:
        sort_ = []
        bool_ = {}

        if query.name:
            bool_["must"] = {"match": {"name": query.name}}

        if query.sort_by and query.sort:
            if query.sort_by == "name":
                query.sort_by = "name.raw"
            sort_.append({query.sort_by: query.sort})

        body = {
            "query": {"bool": bool_},
        }

        resp = await self._es.search(
            index=self._index,
            body=body,
            size=query.limit,
            sort=sort_ or None,
            from_=query.offset,
        )

        return resp


class PersonRepo(AbstractRepo):

    _index = "persons"

    @backoff()
    async def get_by(self, id: uuid.UUID) -> Optional[dict]:
        try:
            person_data = await self._es.get(index="persons", id=str(id))
        except NotFoundError:
            return None
        return person_data

    @backoff()
    async def find_by(self, query: schemas.ArgsPerson) -> dict:
        filter_ = []
        sort_ = []
        bool_ = {}

        if query.full_name:
            bool_["must"] = {"match": {"full_name": query.full_name}}

        if filter_:
            bool_["filter"] = filter_

        if query.sort_by and query.sort:
            sort_.append([{query.sort_by: query.sort}])

        body = {
            "query": {"bool": bool_},
        }

        resp = await self._es.search(
            index=self._index,
            body=body,
            size=query.limit,
            sort=sort_ or None,
            from_=query.offset,
        )
        return resp
