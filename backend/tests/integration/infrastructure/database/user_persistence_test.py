import pytest

from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from app.infrastructure.models.user import UserModel


def test_should_persist_user(db_session):
    user_id = uuid4()

    user = UserModel(
        id=user_id,
        name="Maria Silva",
        email="maria@example.com",
        preferred_name="Maria",
        password_hash="hashed_password_123",
    )

    db_session.add(user)
    db_session.commit()

    persisted_user = db_session.get(UserModel, user_id)

    assert persisted_user is not None
    assert persisted_user.id == user_id
    assert persisted_user.name == "Maria Silva"
    assert persisted_user.email == "maria@example.com"
    assert persisted_user.preferred_name == "Maria"


def test_should_persist_user_without_preferred_name(db_session):
    user_id = uuid4()

    user = UserModel(
        id=user_id,
        name="Amanda Silva",
        email="amanda@example.com",
        password_hash="hashed_password_123",
    )

    db_session.add(user)
    db_session.commit()

    persisted_user = db_session.get(UserModel, user_id)

    assert persisted_user is not None
    assert persisted_user.preferred_name is None


def test_should_reject_duplicate_email(db_session):
    first_user = UserModel(
        id=uuid4(),
        name="Maria",
        email="same@example.com",
        password_hash="hashed_password_123",
    )

    second_user = UserModel(
        id=uuid4(),
        name="Amanda",
        email="same@example.com",
        password_hash="hashed_password_123",
    )

    db_session.add(first_user)
    db_session.commit()

    db_session.add(second_user)

    with pytest.raises(IntegrityError):
        db_session.commit()
def test_should_persist_password_as_hash(db_session):
    user = UserModel(
        id=uuid4(),
        name="Maria Silva",
        email="maria@example.com",
        password_hash="hashed_password_123",
    )

    db_session.add(user)
    db_session.commit()

    persisted_user = db_session.get(UserModel, user.id)

    assert persisted_user is not None
    assert persisted_user.password_hash == "hashed_password_123"
