import http
import uuid

from fastapi import APIRouter, Depends, HTTPException

from src import schemas, strings
from src.schemas import ArgsFilmWork
from src.services.service import FilmWorkService
from src.tokens.tokens import JWTBearer

router = APIRouter(prefix="/film-work")
FilmWork = "FilmWork"


@router.get(
    "/movie",
    response_model=schemas.ItemsFilmWork,
    status_code=http.HTTPStatus.OK,
    tags=[FilmWork],
    summary=strings.MOVIE_SEARCH_SUMMARY,
    description=strings.MOVIE_SEARCH_DESCRIPTION,
)
async def film_works_get(
    query: ArgsFilmWork = Depends(ArgsFilmWork),
    service: FilmWorkService = Depends(FilmWorkService),
):
    resp = await service.find_by(query=query)

    return resp


@router.get(
    "/movie/{id}",
    response_model=schemas.DetailFilmWork,
    status_code=http.HTTPStatus.OK,
    tags=[FilmWork],
    summary=strings.MOVIE_GET_SUMMARY,
    description=strings.MOVIE_GET_DESCRIPTION,
    dependencies=[Depends(JWTBearer())]
)
async def film_work_get(
    id: uuid.UUID,
    service: FilmWorkService = Depends(FilmWorkService),
):
    resp = await service.get_by(id=id)

    if not resp:
        raise HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail=strings.ITEM_NOT_FOUND
        )

    return resp
