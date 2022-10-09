import abc

from elastic_transport import ObjectApiResponse

from src import schemas


class AbstractConverter(abc.ABC):
    _model: schemas.BaseModelSchema

    @abc.abstractmethod
    def one(self, data: ObjectApiResponse) -> schemas.BaseModelSchema:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, data: ObjectApiResponse) -> schemas.BaseModel:
        raise NotImplementedError


class FilmWorkConverter(AbstractConverter):
    def one(self, data: ObjectApiResponse) -> schemas.DetailFilmWork | None:
        if not data:
            return None

        row = schemas.DetailFilmWork(**data["_source"])

        return row

    def list(self, data: ObjectApiResponse) -> schemas.ItemsFilmWork:
        return schemas.ItemsFilmWork(
            total=data["hits"]["total"]["value"],
            items=[hit["_source"] for hit in data["hits"]["hits"]],
        )


class GenreConverter(AbstractConverter):
    def one(self, data: ObjectApiResponse) -> schemas.ItemGenre | None:
        if not data:
            return None

        row = schemas.ItemGenre(**data["_source"])

        return row

    def list(self, data: ObjectApiResponse) -> schemas.ItemsGenre:
        return schemas.ItemsGenre(
            total=data["hits"]["total"]["value"],
            items=[hit["_source"] for hit in data["hits"]["hits"]],
        )


class PersonConverter(AbstractConverter):
    def one(self, data: dict) -> schemas.ItemPerson | None:
        if not data:
            return None
        row = schemas.ItemPerson(**data["_source"])
        return row

    def list(self, data: dict) -> schemas.ItemsPerson:
        return schemas.ItemsPerson(
            total=data["hits"]["total"]["value"],
            items=[hit["_source"] for hit in data["hits"]["hits"]],
        )
