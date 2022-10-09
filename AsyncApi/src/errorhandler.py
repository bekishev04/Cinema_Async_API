import http

from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


async def http422_error_handler(
    _: Request,
    exc: RequestValidationError| ValidationError,
) -> JSONResponse:
    return JSONResponse(
        {"message": exc.errors()},
        status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
    )
