import http
import uuid

from fastapi import APIRouter, Depends
from src import schemas, strings
from src.config import settings
from src.services.Kafka.event_sendler import KafkaEventSendler, get_kafka_event_sendler
from src.tokens.tokens import JWTBearer

router = APIRouter(prefix="/kafka")
TAG = "Kafka"


@router.post(
    "/genre",
    response_model=schemas.ItemsGenre,
    status_code=http.HTTPStatus.OK,
    tags=[TAG],
    summary=strings.KAFKA_SEARCH_SUMMARY,
    description=strings.KAFKA_SEARCH_DESCRIPTION,
)
async def film_timestamp(
    film_timestamp: schemas.ReqKafkaFilmTimeStamp,
    kafka_event_sendler: KafkaEventSendler = Depends(get_kafka_event_sendler),
    payload: dict = Depends(JWTBearer().payload),
) -> http.HTTPStatus.OK:
    await kafka_event_sendler.post_event(
        topic=settings.kafka_topic,
        event_obj=film_timestamp,
        user_id=payload.get("id"),
    )
    return http.HTTPStatus.OK
