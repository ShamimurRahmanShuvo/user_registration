from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RegisterUserRequest(BaseModel):
    """
    HTTP representation of RegistrationRequest
    """
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1)


class RegisterUserResponse(BaseModel):
    """
    HTTP representation of a successful registration.
    """
    user_id: UUID
