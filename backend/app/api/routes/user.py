from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.domain.exceptions.registration import EmailAlreadyRegisteredError
from app.application.schemas.user import CreateUserRequest, CreateUserResponse
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.database.dependencies import get_db
from app.application.services.user import create_user as create_user_service


router = APIRouter()

@router.post(
        "/users", 
        status_code=status.HTTP_201_CREATED,
        response_model=CreateUserResponse,
    )
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)

    try:
        user = create_user_service(
            name=request.name,
            email=request.email,
            preferred_name=request.preferred_name,
            password=request.password,
            repository=repository,
        )


    except EmailAlreadyRegisteredError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "email_already_registered",
                "message": "This email is already registered",
            },
        )

    return user

