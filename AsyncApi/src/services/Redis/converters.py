import abc

from elastic_transport import ObjectApiResponse

from src.schemas import (
    ItemPerson,
    ItemsPerson,
    ItemsGenre,
    BaseModelSchema,
    BaseModel,
    ItemGenre,
    ItemsFilmWork,
    ItemFilmWork,
    DetailFilmWork,
)


class AbstractConverter(abc.ABC):
    _model: BaseModelSchema

    @abc.abstractmethod
    def one(self, data: ObjectApiResponse) -> BaseModelSchema:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, data: ObjectApiResponse) -> BaseModel:
        raise NotImplementedError


class PersonConverter(AbstractConverter):
    def list(self, data: ObjectApiResponse) -> ItemsPerson:
        return ItemsPerson.parse_raw(data)

    def one(self, data: ObjectApiResponse) -> ItemPerson:
        return ItemPerson.parse_raw(data)


class GenreConverter(AbstractConverter):
    def list(self, data: ObjectApiResponse) -> ItemsGenre:
        return ItemsGenre.parse_raw(data)

    def one(self, data: ObjectApiResponse) -> ItemGenre:
        return ItemGenre.parse_raw(data)


class FilmConverter(AbstractConverter):
    def list(self, data: ObjectApiResponse) -> ItemsFilmWork:
        return ItemsFilmWork.parse_raw(data)

    def one(self, data: ObjectApiResponse) -> DetailFilmWork:
        return DetailFilmWork.parse_raw(data)
