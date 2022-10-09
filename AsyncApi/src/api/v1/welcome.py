from fastapi import APIRouter

router = APIRouter(prefix="/welcome")


@router.get("")
def welcome():
    return "Welcome API"
