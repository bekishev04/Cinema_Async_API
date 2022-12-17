import socket

import aioredis
import uvicorn as uvicorn
from aiokafka import AIOKafkaProducer
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from kafka import KafkaAdminClient
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.api import router as api_router
from src.database import redis, elastic, kafka
from src.errorhandler import (
    http_error_handler,
    http422_error_handler,
)
from src.services.Kafka import event_producer, event_sendler


def get_application() -> FastAPI:
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router)

    @application.on_event("startup")
    async def startup():
        redis.redis = await aioredis.from_url(settings.redis_uri)
        elastic.es = AsyncElasticsearch(hosts=[settings.elastic_uri])

        # kafka
        kafka.kafka_admin = KafkaAdminClient(
            bootstrap_servers=settings.kafka_url, client_id=socket.gethostname()
        )
        kafka.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=[settings.kafka_url], client_id=socket.gethostname()
        )
        await kafka.kafka_producer.start()
        event_producer.kafka_event_producer = event_producer.KafkaEventProducer(
            event_producer=kafka.kafka_producer,
            kafka_admin=kafka.kafka_admin,
            topics=set(
                settings.kafka_topic,
            ),
        )
        event_sendler.kafka_event_sendler = event_sendler.KafkaEventSendler(
            event_producer=event_producer.kafka_event_producer
        )

    @application.on_event("shutdown")
    async def shutdown():
        await redis.redis.close()
        await elastic.es.close()

        # kafka
        await kafka.kafka_producer.stop()
        kafka.kafka_admin.close()

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
