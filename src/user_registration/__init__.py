"""Public API for the user-registration package."""

from user_registration._version import __version__
from user_registration.config import (
    ConfigurationError,
    RegistrationConfig,
)
from user_registration.exceptions import (
    RegistrationError,
    RegistrationHookError,
    RegistrationPersistenceError,
    UserAlreadyExistsError,
)
from user_registration.models import (
    RegistrationRequest,
    User,
)
from user_registration.password import (
    Argon2Config,
    Argon2Hasher,
    PasswordHasher,
    PasswordPolicyValidator,
    PasswordValidatorAdapter,
)
from user_registration.registration import (
    NoOpRegistrationHook,
    RegistrationHook,
    RegistrationResult,
    RegistrationService,
    RegistrationStatus,
)
from user_registration.repository import (
    DuplicateUserError,
    RepositoryError,
    UserRepository,
)
from user_registration.security import generate_token
from user_registration.validation import (
    EmailValidator,
    FieldValidator,
    UsernameValidator,
    ValidationError,
    ValidationRegistry,
    create_default_validation_registry,
)

__all__ = [
    "__version__",
    # Configuration
    "ConfigurationError",
    "RegistrationConfig",
    # Models
    "RegistrationRequest",
    "User",
    # Repository
    "UserRepository",
    "RepositoryError",
    "DuplicateUserError",
    # Password
    "PasswordHasher",
    "Argon2Config",
    "Argon2Hasher",
    "PasswordPolicyValidator",
    "PasswordValidatorAdapter",
    # Registration
    "RegistrationError",
    "UserAlreadyExistsError",
    "RegistrationPersistenceError",
    "RegistrationHookError",
    "RegistrationResult",
    "RegistrationStatus",
    "RegistrationService",
    "RegistrationHook",
    "NoOpRegistrationHook",
    # Validation
    "FieldValidator",
    "ValidationError",
    "UsernameValidator",
    "EmailValidator",
    "ValidationRegistry",
    "create_default_validation_registry",
    # Security
    "generate_token",
]
