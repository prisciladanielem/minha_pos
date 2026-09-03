from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.application.exceptions.registration import EmailAlreadyRegisteredError
from app.application.schemas.user import CreateUserRequest
from app.domain.entities.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.database.dependencies import get_db
from app.application.services.user import create_user as create_user_service

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
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

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    except EmailAlreadyRegisteredError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "email_already_registered",
                "message": "This email is already registered",
            },
        )

    return {
        "id": str(user.id),
        "name": user.name,
        "preferred_name": user.preferred_name,
        "email": user.email,
    }
