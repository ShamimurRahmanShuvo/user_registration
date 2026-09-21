from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from user_registration.models import RegistrationRequest
from user_registration.registration import RegistrationStatus

from user_registration_fastapi.dependencies import RegistrationServiceDependency
from user_registration_fastapi.schemas import RegisterUserRequest, RegisterUserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUserRequest, service: RegistrationServiceDependency) -> RegisterUserResponse:
    result = service.register(
        RegistrationRequest(
            username=payload.username,
            email=payload.email,
            password=payload.password
        )
    )

    if result.status is RegistrationStatus.VALIDATION_ERROR:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=list(result.errors)
        )

    if result.status is RegistrationStatus.DUPLICATE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=list(result.errors)
        )

    if result.status is RegistrationStatus.PERSISTENCE_ERROR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user"
        )

    if result.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration completed without a user ID"
        )

    return RegisterUserResponse(
        user_id=result.user_id
    )
