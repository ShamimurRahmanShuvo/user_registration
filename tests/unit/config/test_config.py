import pytest

from user_registration import ConfigurationError, RegistrationConfig


def test_default_configuration() -> None:
    config = RegistrationConfig()
    
    assert config.username_min_length == 4
    assert config.username_max_length == 50
    assert config.email_required is True
    assert config.username_required is True
    assert config.password_required is True
    assert config.normalize_email is True
    assert config.normalize_username is True


def test_customize_configuration() -> None:
    config = RegistrationConfig(
        username_min_length=5,
        username_max_length=30,
        email_required=True,
        username_required=True,
        password_required=True,
        normalize_email=False,
        normalize_username=False
    )

    assert config.username_min_length == 5
    assert config.username_max_length == 30
    assert config.email_required is True
    assert config.username_required is True
    assert config.password_required is True
    assert config.normalize_email is False
    assert config.normalize_username is False


def test_configuration_is_immutable() -> None:
    config = RegistrationConfig()

    with pytest.raises(AttributeError):
        config.username_min_length = 10


def test_configuration_uses_slots() -> None:
    config = RegistrationConfig()

    assert not hasattr(config, "__dict__")


def test_username_min_length_must_be_positive() -> None:
    with pytest.raises(ConfigurationError, match="greater than 0"):
        RegistrationConfig(username_min_length=0)

    with pytest.raises(ConfigurationError, match="greater than 0"):
        RegistrationConfig(username_min_length=-1)


def test_username_max_length_cannot_be_less_than_minimum() -> None:
    with pytest.raises(ConfigurationError, match="greater than or equal to"):
        RegistrationConfig(
            username_min_length=20,
            username_max_length=10
        )


def test_username_lengths_can_be_equal() -> None:
    config = RegistrationConfig(
        username_min_length=10,
        username_max_length=10
    )

    assert config.username_min_length == 10
    assert config.username_max_length == 10


def test_from_env_reads_integer_and_boolean_values() -> None:
    environ = {
        "USER_REGISTRATION_USERNAME_MIN_LENGTH": "5",
        "USER_REGISTRATION_USERNAME_MAX_LENGTH": "25",
        "USER_REGISTRATION_EMAIL_REQUIRED": "true",
        "USER_REGISTRATION_USERNAME_REQUIRED": "yes",
        "USER_REGISTRATION_PASSWORD_REQUIRED": "1",
        "USER_REGISTRATION_NORMALIZE_EMAIL": "off",
        "USER_REGISTRATION_NORMALIZE_USERNAME": "0",
    }

    config = RegistrationConfig.from_env(environ)

    assert config.username_min_length == 5
    assert config.username_max_length == 25

    assert config.email_required is True
    assert config.username_required is True
    assert config.password_required is True

    assert config.normalize_email is False
    assert config.normalize_username is False


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("true", True),
        ("TRUE", True),
        ("True", True),
        ("1", True),
        ("yes", True),
        ("YES", True),
        ("on", True),
        ("ON", True),
    ]
)
def test_from_env_boolean_formats(value: str, expected: bool) -> None:
    config = RegistrationConfig.from_env(
        {
            "USER_REGISTRATION_EMAIL_REQUIRED": value,
        }
    )

    assert config.email_required is expected


def test_from_env_uses_defaults_for_missing_variables() -> None:
    config = RegistrationConfig.from_env({})

    assert config == RegistrationConfig()


def test_from_env_rejects_invalid_integer() -> None:
    with pytest.raises(
            ConfigurationError,
            match="USER_REGISTRATION_USERNAME_MIN_LENGTH must be integer; got 'abc'"
    ):
        RegistrationConfig.from_env(
            {
                "USER_REGISTRATION_USERNAME_MIN_LENGTH": "abc",
            }
        )


def test_from_env_rejects_empty_integer() -> None:
    with pytest.raises(
            ConfigurationError,
            match="USER_REGISTRATION_USERNAME_MIN_LENGTH must be integer; got ''"
    ):
        RegistrationConfig.from_env(
            {
                "USER_REGISTRATION_USERNAME_MIN_LENGTH": "",
            }
        )


def test_from_env_rejects_invalid_boolean() -> None:
    with pytest.raises(ConfigurationError, match="must be a boolean"):
        RegistrationConfig.from_env(
            {
                "USER_REGISTRATION_EMAIL_REQUIRED": "maybe",
            }
        )


def test_from_env_can_use_os_environment(monkeypatch) -> None:
    monkeypatch.setenv(
        "USER_REGISTRATION_USERNAME_MIN_LENGTH",
        "8",
    )
    monkeypatch.setenv(
        "USER_REGISTRATION_USERNAME_MAX_LENGTH",
        "40",
    )
    monkeypatch.setenv(
        "USER_REGISTRATION_EMAIL_REQUIRED",
        "true",
    )

    config = RegistrationConfig.from_env()

    assert config.username_min_length == 8
    assert config.username_max_length == 40
    assert config.email_required is True
