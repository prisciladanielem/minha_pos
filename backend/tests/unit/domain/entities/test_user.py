import pytest
from app.domain.entities.user import User

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


def test_should_reject_empty_id():
    with pytest.raises(ValueError):
        User(
            id="",
            name="Maria",
            email="maria@example.com",
        )


@pytest.mark.parametrize(
    "email",
    [
        "",
        "@",
        "a@",
        "@example.com",
        "mariaexample.com",
        "maria@",
        "maria@example",
        "maria @example.com",
        "maria@example .com",
        "maria@@example.com",
    ],
)
def test_should_reject_invalid_email(email):
    with pytest.raises(ValueError, match="Invalid email"):
        User(
            id="user-1",
            name="Maria",
            email=email,
        )

@pytest.mark.parametrize(
    "email",
    [
        "maria@example.com",
        "maria.silva@example.com",
        "maria+test@example.com",
        "maria@sub.example.com",
    ],
)
def test_should_accept_valid_email(email):
    user = User(
        id="user-1",
        name="Maria",
        email=email,
    )

    assert user.email == email

@pytest.mark.parametrize("preferred_name", ["", "   "])
def test_should_reject_empty_preferred_name(preferred_name):
    with pytest.raises(ValueError, match="Preferred name cannot be empty"):
        User(
            id="user-1",
            name="Maria",
            email="maria@example.com",
            preferred_name=preferred_name,
        )
