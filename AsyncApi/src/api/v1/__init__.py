from fastapi import APIRouter

from src.api.v1.welcome import router as welcome_router
from src.api.v1.film_work import router as film_work_router
from src.api.v1.person import router as person_router
from src.api.v1.genre import router as genre_router
from src.api.v1.kafka import router as kafka_router


router = APIRouter(prefix="/v1")

router.include_router(welcome_router)
router.include_router(film_work_router)
router.include_router(person_router)
router.include_router(genre_router)
router.include_router(kafka_router)
