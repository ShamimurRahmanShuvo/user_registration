from user_registration import ConfigurationError, RegistrationConfig


def test_public_api() -> None:
    config = RegistrationConfig()

    assert config is not None
    assert ConfigurationError is not None


def test_package_versions():
    import user_registration
    assert user_registration.__version__ == "0.1.0"
