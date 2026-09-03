from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.exception_handlers import validation_exception_handler

from app.api.routes.user import router as user_router

app = FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user_router)