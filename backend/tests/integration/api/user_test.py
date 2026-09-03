import pytest

from sqlalchemy import select
from app.infrastructure.models.user import UserModel

def test_should_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Senha@123",
            "password_confirmation": "Senha@123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"]
    assert data["name"] == "Maria Silva"
    assert data["preferred_name"] == "Maria"
    assert data["email"] == "maria@example.com"
    assert "password" not in data
    assert "password_confirmation" not in data

def test_should_reject_empty_name(client):
    response = client.post(
        "/users",
        json={
            "name": "   ",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Senha@123",
            "password_confirmation": "Senha@123",
        },
    )

    assert response.status_code == 400


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
def test_should_reject_invalid_email(client, email):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": email,
            "password": "Senha@123",
            "password_confirmation": "Senha@123",
        },
    )

    assert response.status_code == 400


def test_should_reject_different_password_confirmation(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Senha@123",
            "password_confirmation": "Senha@456",
        },
    )

    print(response.json())

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request"
    assert data["details"]["password_confirmation"] == "Passwords do not match"


def test_should_reject_password_shorter_than_8_characters(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Sen@123",
            "password_confirmation": "Sen@123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["details"]["password"] == "Password must be at least 8 characters long"

def test_should_reject_password_without_uppercase(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "senha@123",
            "password_confirmation": "senha@123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["details"]["password"] == "Password must contain at least one uppercase letter"

def test_should_reject_password_without_lowercase(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "SENHA@123",
            "password_confirmation": "SENHA@123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["details"]["password"] == "Password must contain at least one lowercase letter"

def test_should_reject_password_without_number(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Senha@abc",
            "password_confirmation": "Senha@abc",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["details"]["password"] == "Password must contain at least one number"

def test_should_reject_password_without_symbol(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "Maria@Example.com",
            "password": "Senha123",
            "password_confirmation": "Senha123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["error"] == "validation_error"
    assert data["details"]["password"] == "Password must contain at least one symbol"

def test_should_reject_duplicate_email(client, db_session):
    first_response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "preferred_name": "Maria",
            "email": "maria@example.com",
            "password": "Senha@123",
            "password_confirmation": "Senha@123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users",
        json={
            "name": "Amanda Silva",
            "preferred_name": "Amanda",
            "email": "MARIA@example.com",
            "password": "Senha@456",
            "password_confirmation": "Senha@456",
        },
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["error"] == "email_already_registered"
    assert data["message"] == "This email is already registered"

def test_should_persist_password_as_hash(client, db_session):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "email": "maria@example.com",
            "password": "Password1!",
            "password_confirmation": "Password1!",
        },
    )

    assert response.status_code == 201

    user = db_session.scalar(
        select(UserModel).where(
            UserModel.email == "maria@example.com"
        )
    )

    assert user is not None
    assert user.password_hash is not None
    assert user.password_hash != "Password1!"

def test_should_not_return_password_or_password_hash(client):
    response = client.post(
        "/users",
        json={
            "name": "Maria Silva",
            "email": "maria@example.com",
            "password": "Password1!",
            "password_confirmation": "Password1!",
        },
    )

    assert response.status_code == 201
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
    