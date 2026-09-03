from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.exception_handlers import validation_exception_handler

from app.api.routes.user import router as user_router
from app.api.exception_handlers import domain_validation_exception_handler
from app.domain.exceptions.validations import DomainValidationError

app = FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user_router)

app.add_exception_handler(
    DomainValidationError,
    domain_validation_exception_handler,
)