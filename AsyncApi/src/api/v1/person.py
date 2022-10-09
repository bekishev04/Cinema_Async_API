import http
import uuid

from fastapi import APIRouter, Depends, HTTPException

from src import schemas, strings
from src.schemas import ArgsPerson
from src.services.service import PersonService

router = APIRouter(prefix="/persons")
tag = 'Persons'


@router.get(
    "/person/{person_id}",
    status_code=http.HTTPStatus.OK,
    response_model=schemas.ItemPerson,
    tags=[tag],
    summary=strings.PERSONS_GET_SUMMARY,
    description=strings.PERSONS_GET_DESCRIPTION
)
async def get_person(
        person_id: uuid.UUID,
        person_service: PersonService = Depends(PersonService),
):
    resp = await person_service.get_by(person_id)
    if not resp:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail=strings.ITEM_NOT_FOUND)
    return resp


@router.get(
    "/persons",
    status_code=http.HTTPStatus.OK,
    response_model=schemas.ItemsPerson,
    tags=[tag],
    summary=strings.PERSONS_SEARCH_SUMMARY,
    description=strings.PERSONS_SEARCH_DESCRIPTION
)
async def search_person(
        query: ArgsPerson = Depends(ArgsPerson),
        person_service: PersonService = Depends(PersonService),
):
    resp = await person_service.find_by(query)
    return resp
