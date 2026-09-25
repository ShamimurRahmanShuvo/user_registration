from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from user_registration.registration import RegistrationService


def get_registration_service() -> RegistrationService:
    """
    Application must override this dependency.
    The adapter does not know how the repository, hasher, validator,
    or database are configured.
    """
    raise RuntimeError("RegistrationService dependency has not been configured")


RegistrationServiceDependency = Annotated[
    RegistrationService, Depends(get_registration_service)
]
