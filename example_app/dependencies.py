from collections.abc import Generator

from user_registration import (
    Argon2Hasher,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationService,
    create_default_validation_registry,
)

from user_registration_sqlalchemy import SQLAlchemyUserRepository

from example_app.database import SessionLocal


def get_registration_service() -> Generator[RegistrationService, None, None]:
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        config = RegistrationConfig()

        validation_registry = (
            create_default_validation_registry(
                config,
            )
        )

        service = RegistrationService(
            repository=repository,
            password_hasher=Argon2Hasher(),
            password_validator=PasswordValidatorAdapter(),
            config=config,
            validation_registry=validation_registry,
        )

        yield service

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
