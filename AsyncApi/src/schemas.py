import uuid
import datetime
from typing import Literal

import orjson
from pydantic import BaseModel as PydanticBaseModel, Field



class BaseModel(PydanticBaseModel):
    """Base Schema"""

    class Config:
        anystr_strip_whitespace = True


class BaseModelSchema(PydanticBaseModel):
    """Base Model Schema"""

    id: uuid.UUID

    class Config:
        orm_mode = True


class JWTPayload(BaseModelSchema):
    """Item Schema For JWTPayload"""

    login: str
    full_name: str
    role: str
    valid_through: datetime.datetime


class ArgsPaginate(BaseModel):
    """Args Schema paginate"""

    offset: int = Field(0, ge=0, description="Номер сдвига")
    limit: int = Field(50, gt=0, description="Кол-во элементов")


class ArgsFilmWork(ArgsPaginate):
    """Args Schema paginate For FilmWork"""

    title: str | None
    rating: float | None
    sort_by: Literal[
        "imdb_rating",
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


class ReqKafkaFilmTimeStamp(BaseModel):
    film_id: uuid.UUID
    film_timestamp: datetime.datetime
    event_time: datetime.datetime


class KafkaFilmTimeStamp(ReqKafkaFilmTimeStamp):
    user_id: uuid.UUID
