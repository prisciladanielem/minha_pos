import pytest
from argon2 import PasswordHasher

from app.application.security.password import (
    hash_password,
    verify_password,
)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def test_should_verify_password_hash():
    password = "Password1!"
    password_hash = hash_password(password)

    hasher = PasswordHasher()

    assert hasher.verify(password_hash, password)

def test_should_reject_incorrect_password():
    password_hash = hash_password("Password1!")

    hasher = PasswordHasher()

    with pytest.raises(VerifyMismatchError):
        hasher.verify(password_hash, "WrongPassword1!")

def test_should_generate_different_hashes_for_same_password():
    password = "Password1!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash

def test_should_verify_correct_password():
    password = "Password1!"
    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True

def test_should_reject_incorrect_password():
    password_hash = hash_password("Password1!")

    assert verify_password("WrongPassword1!", password_hash) is False
