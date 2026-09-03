from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.entities.user import User
from app.domain.exceptions.registration import EmailAlreadyRegisteredError
from app.infrastructure.models.user import UserModel

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User, password_hash: str) -> User:
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            preferred_name=user.preferred_name,
            password_hash=password_hash,
        )

        self.session.add(user_model)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise EmailAlreadyRegisteredError()

        self.session.refresh(user_model)

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            preferred_name=user_model.preferred_name,
        )

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)

        user_model = self.session.scalar(statement)

        if user_model is None:
            return None

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            preferred_name=user_model.preferred_name,
        )
