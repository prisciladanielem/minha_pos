from pydantic import BaseModel, field_validator, model_validator
from pydantic_core import PydanticCustomError

from uuid import UUID

class CreateUserRequest(BaseModel):
    name: str
    preferred_name: str | None = None
    email: str
    password: str
    password_confirmation: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise PydanticCustomError(
                "password",
                "Password must be at least 8 characters long",
            )

        if not any(char.isupper() for char in password):
            raise PydanticCustomError(
                "password",
                "Password must contain at least one uppercase letter",
        )

        if not any(char.islower() for char in password):
            raise PydanticCustomError(
                "password",
                "Password must contain at least one lowercase letter",
        )

        if not any(char.isdigit() for char in password):
            raise PydanticCustomError(
                "password",
                "Password must contain at least one number",
        )

        if not any(not char.isalnum() for char in password):
            raise PydanticCustomError(
                "password",
                "Password must contain at least one symbol",
        )

        return password

    @model_validator(mode="after")
    def validate_password_confirmation(self):
        if self.password != self.password_confirmation:
            raise PydanticCustomError(
                "password_confirmation",
                "Passwords do not match",
            )

        return self

class CreateUserResponse(BaseModel):
    id: UUID
    name: str
    preferred_name: str | None
    email: str
    