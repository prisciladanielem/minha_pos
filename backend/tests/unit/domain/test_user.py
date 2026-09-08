import pytest
from app.domain.user import User

def test_should_create_user():
    user = User(
        id="user-1",
        name="Maria Silva",
        email="maria@example.com",
    )

    assert user.id == "user-1"
    assert user.name == "Maria Silva"
    assert user.email == "maria@example.com"
    assert user.preferred_name is None

def test_should_create_user_with_preferred_name():
    user = User(
        id="user-1",
        name="Maria Fernanda Silva",
        email="maria@example.com",
        preferred_name="Fernanda",
    )

    assert user.preferred_name == "Fernanda"

def test_should_reject_empty_name():
    with pytest.raises(ValueError):
        User(
            id="user-1",
            name="   ",
            email="maria@example.com",
        )


def test_should_reject_wrong_email():
    with pytest.raises(ValueError):
        User(
            id="user-1",
            name="Amanda",
            email="mariaexample.com",
        )
