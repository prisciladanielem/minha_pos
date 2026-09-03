from app.application.security.password import hash_password
from app.domain.entities.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.exceptions.registration import EmailAlreadyRegisteredError


def create_user(
    name: str,
    email: str,
    preferred_name: str | None,
    password: str,
    repository: UserRepository,
) -> User:
    user = User(
        name=name,
        email=email,
        preferred_name=preferred_name,
    )
        
    password_hash = hash_password(password)

    existing_user = repository.get_by_email(user.email)

    if existing_user is not None:
        raise EmailAlreadyRegisteredError()

    return repository.create(
        user,
        password_hash=password_hash,
    )
