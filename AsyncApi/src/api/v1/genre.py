import http
import uuid

from fastapi import APIRouter, Depends, HTTPException
from src import schemas, strings
from src.schemas import ArgsGenre
from src.services.service import GenreService


router = APIRouter(prefix="/genres")
Items = "Items"


@router.get(
    "/genre",
    response_model=schemas.ItemsGenre,
    status_code=http.HTTPStatus.OK,
    tags=[Items],
    summary=strings.GENRES_SEARCH_SUMMARY,
    description=strings.GENRES_SEARCH_DESCRIPTION,
)
async def genres_get(
    query: ArgsGenre = Depends(ArgsGenre),
    service: GenreService = Depends(GenreService),
):
    resp = await service.find_by(query=query)

    return resp


@router.get(
    "/genre/{id}",
    response_model=schemas.ItemGenre,
    status_code=http.HTTPStatus.OK,
    tags=[Items],
    summary=strings.GENRES_GET_SUMMARY,
    description=strings.GENRES_GET_DESCRIPTION,
)
async def genre_get(
    id: uuid.UUID,
    service: GenreService = Depends(GenreService),
):
    resp = await service.get_by(id=id)

    if not resp:
        raise HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail=strings.ITEM_NOT_FOUND
        )

    return resp
