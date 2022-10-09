from pydantic import BaseModel, validator


def set_default_list(val):
    return val or []


class Item(BaseModel):
    id: str = ""
    name: str


class Movie(BaseModel):
    id: str
    imdb_rating: float | None
    genre: list[str] | None
    title: str
    description: str | None = ""
    director: list[str] | None = []
    actors_names: list[str] | None = []
    writers_names: list[str] | None = []
    actors: list[Item] | None = []
    writers: list[Item] | None = []

    _validate_genre = validator("genre", allow_reuse=True)(set_default_list)
    _validate_director = validator("director", allow_reuse=True)(set_default_list)
    _validate_actors_names = validator("actors_names", allow_reuse=True)(
        set_default_list
    )
    _validate_writers_names = validator("writers_names", allow_reuse=True)(
        set_default_list
    )
    _validate_actors = validator("actors", allow_reuse=True)(set_default_list)
    _validate_writers = validator("writers", allow_reuse=True)(set_default_list)


class Genre(BaseModel):
    id: str
    name: str


class Person(BaseModel):
    id: str
    full_name: str
