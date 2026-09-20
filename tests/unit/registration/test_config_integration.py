from user_registration.config import RegistrationConfig
from user_registration.models import RegistrationRequest
from user_registration.password import Argon2Hasher, PasswordValidatorAdapter
from user_registration.registration import RegistrationService

from tests.fakes import InMemoryUserRepository


def create_service(
    config: RegistrationConfig,
) -> tuple[RegistrationService, InMemoryUserRepository]:
    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        config=config,
    )

    return service, repository


def test_custom_username_length_configuration() -> None:
    config = RegistrationConfig(
        username_min_length=5,
        username_max_length=20,
    )

    service, _ = create_service(config)

    result = service.register(
        RegistrationRequest(
            username="abcd",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Username must contain atleast 5 characters" in result.errors


def test_normalization_can_be_disabled() -> None:
    config = RegistrationConfig(
        normalize_username=False,
        normalize_email=False,
    )

    service, repository = create_service(config)

    result = service.register(
        RegistrationRequest(
            username="  Shuvo  ",
            email="  SHUVO@EXAMPLE.COM  ",
            password="StrongPassword123!",
        )
    )

    assert result.success is True
    assert result.user_id is not None

    user = repository.get_by_id(result.user_id)

    assert user is not None
    assert user.username == "Shuvo"
    assert user.email == "SHUVO@EXAMPLE.COM"
