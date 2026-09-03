from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.validations import DomainValidationError


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    details = {}

    for error in exc.errors():
        if error["type"] == "password_confirmation":
            details["password_confirmation"] = error["msg"]
            continue

        field = error["loc"][-1]
        details[field] = error["msg"]

    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": "Invalid request",
            "details": details,
        },
    )

async def domain_validation_exception_handler(
    request: Request,
    exc: DomainValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": "Invalid request",
            "details": {
                exc.field: exc.message,
            },
        },
    )
