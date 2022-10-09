import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.config import AppSettings
from src.api import router as api_router
from src.database import redis, elastic
from src.errorhandler import (
    http_error_handler,
    http422_error_handler,
)


def get_application() -> FastAPI:
    settings = AppSettings()

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

    @application.on_event("shutdown")
    async def shutdown():
        await redis.redis.close()
        await elastic.es.close()

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
