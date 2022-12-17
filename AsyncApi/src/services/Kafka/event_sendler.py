import abc
import uuid
from abc import ABC
from typing import Optional

from src import schemas
from src.services.Kafka.event_producer import EventProducer, KafkaEventProducer


class EventSendler(ABC):
    event_producer: EventProducer

    @abc.abstractmethod
    def post_event(self, event_obj, topic, user_id):
        pass


class KafkaEventSendler(EventSendler):
    event_producer: KafkaEventProducer

    def __init__(self, event_producer):
        self.event_producer = event_producer

    def post_event(self, event_obj: schemas.ReqKafkaFilmTimeStamp, topic: str, user_id: uuid.UUID):
        return self.event_producer.send(
            topic=topic, value=schemas.KafkaFilmTimeStamp(user_id=user_id, **event_obj.dict()).json().encode()
        )


kafka_event_sendler: Optional[KafkaEventSendler] = None


def get_kafka_event_sendler() -> KafkaEventSendler:
    return kafka_event_sendler
