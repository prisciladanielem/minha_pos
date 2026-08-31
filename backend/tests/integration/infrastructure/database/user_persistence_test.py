import pytest
from sqlalchemy.exc import IntegrityError
from app.infrastructure.models.user import UserModel


def test_should_persist_user(db_session):
    user = UserModel(
        id="user-1",
        name="Maria Silva",
        email="maria@example.com",
        preferred_name="Maria",
    )

    db_session.add(user)
    db_session.commit()

    persisted_user = db_session.get(UserModel, "user-1")

    assert persisted_user is not None
    assert persisted_user.id == "user-1"
    assert persisted_user.name == "Maria Silva"
    assert persisted_user.email == "maria@example.com"
    assert persisted_user.preferred_name == "Maria"

def test_should_persist_user_without_preferred_name(db_session):
    user = UserModel(
        id="user-2",
        name="Amanda Silva",
        email="amanda@example.com",
    )

    db_session.add(user)
    db_session.commit()

    persisted_user = db_session.get(UserModel, "user-2")

    assert persisted_user is not None
    assert persisted_user.preferred_name is None

def test_should_reject_duplicate_email(db_session):
    first_user = UserModel(
        id="user-3",
        name="Maria",
        email="same@example.com",
    )

    second_user = UserModel(
        id="user-4",
        name="Amanda",
        email="same@example.com",
    )

    db_session.add(first_user)
    db_session.commit()

    db_session.add(second_user)

    with pytest.raises(IntegrityError):
        db_session.commit()
