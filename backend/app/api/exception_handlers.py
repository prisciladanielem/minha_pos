from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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
