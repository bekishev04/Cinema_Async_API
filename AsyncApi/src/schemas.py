import uuid
from typing import Literal

import orjson
from pydantic import BaseModel as PydanticBaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    """Base Schema"""

    class Config:
        anystr_strip_whitespace = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseModelSchema(PydanticBaseModel):
    """Base Model Schema"""

    id: uuid.UUID

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ArgsPaginate(BaseModel):
    """Args Schema paginate"""

    offset: int = Field(0, ge=0, description="Номер сдвига") #todo нужно переносить в strings?
    limit: int = Field(50, gt=0, description="Кол-во элементов")


class ArgsFilmWork(ArgsPaginate):
    """Args Schema paginate For FilmWork"""

    title: str | None
    rating: float | None
    sort_by: Literal[
        "rating",
    ] | None
    sort: Literal[
        "asc",
        "desc",
    ] | None


class ArgsPerson(ArgsPaginate):
    full_name: str | None
    sort_by: Literal["full_name"] | None
    sort: Literal["asc", "desc"] | None


class ArgsGenre(ArgsPaginate):
    """Args Schema paginate For Genre"""

    name: str | None
    sort_by: Literal[
        "name",
    ] | None
    sort: Literal[
        "asc",
        "desc",
    ] | None


class ItemPerson(BaseModelSchema):
    full_name: str


class ItemsPerson(BaseModel):
    total: int
    items: list[ItemPerson]


class ItemGenre(BaseModelSchema):
    name: str
    description: str | None


class ItemsGenre(BaseModel):
    total: int
    items: list[ItemGenre]


class ItemFilmWork(BaseModelSchema):
    title: str
    description: str | None
    imdb_rating: float


class ItemWithName(BaseModelSchema):
    name: str


class DetailFilmWork(ItemFilmWork):
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[ItemWithName]
    writers: list[ItemWithName]


class ItemsFilmWork(BaseModel):
    total: int
    items: list[ItemFilmWork]
