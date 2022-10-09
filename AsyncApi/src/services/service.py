import abc
import uuid

from fastapi import Depends

from src import schemas
from src.services.ElasticSearch import repositories as es_repositories
from src.services.ElasticSearch import converters as es_converters
from src.services.Redis import repositories as redis_repositories
from src.services.Redis import converters as redis_converters


class AbstractService(abc.ABC):
    @abc.abstractmethod
    def get_by(self, id: uuid.UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, query: schemas.ArgsPaginate):
        raise NotImplementedError


class PersonService(AbstractService):
    _index = "persons"

    def __init__(
        self,
        es_repo: es_repositories.PersonRepo = Depends(es_repositories.PersonRepo),
        es_converter: es_converters.PersonConverter = Depends(
            es_converters.PersonConverter
        ),
        redis_repo: redis_repositories.PersonRepo = Depends(
            redis_repositories.PersonRepo
        ),
        redis_converter: redis_converters.PersonConverter = Depends(
            redis_converters.PersonConverter
        ),
    ):
        self.es_repo = es_repo
        self.es_converter = es_converter
        self.redis_repo = redis_repo
        self.redis_converter = redis_converter

    async def get_by(self, id: uuid.UUID):
        raw_data = await self.redis_repo.get_by_id(self._index, id)
        if raw_data:
            return self.redis_converter.one(raw_data)
        raw_data = await self.es_repo.get_by(id)
        if not raw_data:
            return None
        item = self.es_converter.one(raw_data)
        await self.redis_repo.put_by_id(self._index, item)
        return item

    async def find_by(self, query: schemas.ArgsPerson):
        raw_data = await self.redis_repo.get_by_query(query)
        if raw_data:
            return self.redis_converter.list(raw_data)
        raw_data = await self.es_repo.find_by(query)
        result = self.es_converter.list(raw_data)
        await self.redis_repo.put_by_query(query, result)
        return result


class FilmWorkService(AbstractService):
    _index = "movies"

    def __init__(
        self,
        es_repo: es_repositories.FilmWorkRepo = Depends(es_repositories.FilmWorkRepo),
        es_converter: es_converters.FilmWorkConverter = Depends(
            es_converters.FilmWorkConverter
        ),
        redis_repo: redis_repositories.FilmWorkRepo = Depends(
            redis_repositories.FilmWorkRepo
        ),
        redis_converter: redis_converters.FilmConverter = Depends(
            redis_converters.FilmConverter
        ),
    ):
        self.es_repo = es_repo
        self.es_converter = es_converter
        self.redis_repo = redis_repo
        self.redis_converter = redis_converter

    async def get_by(self, id: uuid.UUID):
        raw_data = await self.redis_repo.get_by_id(self._index, id)
        if raw_data:
            return self.redis_converter.one(raw_data)
        row = self.es_converter.one(await self.es_repo.get_by(id=id))
        if row:
            await self.redis_repo.put_by_id(self._index, row)
        return row

    async def find_by(self, query: schemas.ArgsFilmWork):
        raw_data = await self.redis_repo.get_by_query(query)
        if raw_data:
            return self.redis_converter.list(raw_data)
        rows = self.es_converter.list(await self.es_repo.find_by(query=query))
        await self.redis_repo.put_by_query(query, rows)
        return rows


class GenreService(AbstractService):
    _index = "genres"

    def __init__(
        self,
        es_repo: es_repositories.GenreRepo = Depends(es_repositories.GenreRepo),
        es_converter: es_converters.GenreConverter = Depends(
            es_converters.GenreConverter
        ),
        redis_repo: redis_repositories.GenreRepo = Depends(
            redis_repositories.GenreRepo
        ),
        redis_converter: redis_converters.GenreConverter = Depends(
            redis_converters.GenreConverter
        ),
    ):
        self.es_repo = es_repo
        self.es_converter = es_converter
        self.redis_repo = redis_repo
        self.redis_converter = redis_converter

    async def get_by(self, id: uuid.UUID):
        raw_data = await self.redis_repo.get_by_id(self._index, id)
        if raw_data:
            return self.redis_converter.one(raw_data)
        row = self.es_converter.one(await self.es_repo.get_by(id=id))
        if row:
            await self.redis_repo.put_by_id(self._index, row)
        return row

    async def find_by(self, query: schemas.ArgsGenre):
        raw_data = await self.redis_repo.get_by_query(query)
        if raw_data:
            return self.redis_converter.list(raw_data)
        rows = self.es_converter.list(await self.es_repo.find_by(query=query))
        await self.redis_repo.put_by_query(query, rows)
        return rows
