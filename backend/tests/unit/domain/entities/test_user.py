import pytest
from uuid import UUID, uuid4

from app.domain.entities.user import User


def test_should_create_user():
    user_id = uuid4()

    user = User(
        id=user_id,
        name="Maria Silva",
        email="maria@example.com",
    )

    assert user.id == user_id
    assert user.name == "Maria Silva"
    assert user.email == "maria@example.com"
    assert user.preferred_name is None


def test_should_create_user_with_preferred_name():
    user = User(
        id=uuid4(),
        name="Maria Fernanda Silva",
        email="maria@example.com",
        preferred_name="Fernanda",
    )

    assert user.preferred_name == "Fernanda"


def test_should_reject_empty_name():
    with pytest.raises(ValueError):
        User(
            id=uuid4(),
            name="   ",
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
            id=uuid4(),
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
        id=uuid4(),
        name="Maria",
        email=email,
    )

    assert user.email == email


@pytest.mark.parametrize("preferred_name", ["", "   "])
def test_should_reject_empty_preferred_name(preferred_name):
    with pytest.raises(ValueError, match="Preferred name cannot be empty"):
        User(
            id=uuid4(),
            name="Maria",
            email="maria@example.com",
            preferred_name=preferred_name,
        )


def test_should_normalize_email_to_lowercase():
    user = User(
        id=uuid4(),
        name="Maria",
        email="Maria@Example.COM",
    )

    assert user.email == "maria@example.com"


def test_should_generate_random_uuid():
    user = User(
        name="Maria Silva",
        email="maria@example.com",
    )

    assert isinstance(user.id, UUID)


def test_should_generate_different_ids():
    user1 = User(
        name="Maria Silva",
        email="maria1@example.com",
    )

    user2 = User(
        name="Maria Silva",
        email="maria2@example.com",
    )

    assert user1.id != user2.id