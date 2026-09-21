"""
Registration service foundation.
"""
from __future__ import annotations

from password_validator.models import ValidationResult

from user_registration.config import RegistrationConfig
from user_registration.exceptions import RegistrationPersistenceError
from user_registration.models import RegistrationRequest, User
from user_registration.password import PasswordHasher, PasswordPolicyValidator
from user_registration.registration.hooks import RegistrationHook
from user_registration.registration.result import RegistrationResult
from user_registration.repository import DuplicateUserError, UserRepository
from user_registration.validation import ValidationRegistry, create_default_validation_registry


class RegistrationService:
    """
    Coordinates the user registration workflow.
    The service is independent of web frameworks, databases, ORMs, and authentication/session mechanism.
    """
    def __init__(self, *,
                 repository: UserRepository,
                 password_hasher: PasswordHasher,
                 password_validator: PasswordPolicyValidator,
                 config: RegistrationConfig | None = None,
                 validation_registry: ValidationRegistry | None = None,
                 hooks: tuple[RegistrationHook, ...] = ()
                 ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher
        self._password_validator = password_validator
        self._config = config or RegistrationConfig()

        self._validation_registry = (
            validation_registry if validation_registry is not None
            else create_default_validation_registry(self._config)
        )
        self._hooks = hooks

    def register(self, request: RegistrationRequest) -> RegistrationResult:
        """
        Register a new user.
        Workflow:
            1. Validate required fields.
            2. Normalize username/email.
            3. Validate username/email.
            4. Check for duplicates.
            5. Validate password policy.
            6. Hash password.
            7. Create domain User.
            8. Persist User.
            9. Execute registration hooks.
        """
        errors = self._validate_required_fields(request)

        if errors:
            return RegistrationResult.validation_failed(*errors)

        username = self._normalize_username(request.username)
        email = self._normalize_email(request.email)

        validation_errors = self._validate_fields(
            username=username,
            email=email
        )

        if validation_errors:
            return RegistrationResult.validation_failed(*validation_errors)

        duplicate_errors = self._check_duplicates(
            username=username,
            email=email,
        )

        if duplicate_errors:
            return RegistrationResult.duplicate(*duplicate_errors)

        assert request.password is not None

        password_result = self._password_validator.validate(request.password)

        if not password_result.valid:
            return RegistrationResult.validation_failed(*self._password_errors(password_result))

        password_hash = self._password_hasher.hash(request.password)

        user = User.create(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        try:
            persisted_user = self._repository.create(user)
        except DuplicateUserError:
            return RegistrationResult.duplicate(
                "Username or email is already registered"
            )
        except Exception as exc:
            raise RegistrationPersistenceError(
                "Unable to persist registered user"
            ) from exc

        self._execute_hooks(persisted_user)

        return RegistrationResult.successful(persisted_user.id)

    def _validate_required_fields(self, request: RegistrationRequest) -> list[str]:
        errors: list[str] = []

        if self._config.username_required and not request.username:
            errors.append("Username is required")

        if self._config.email_required and not request.email:
            errors.append("Email is required")

        if self._config.password_required and not request.password:
            errors.append("Password is required")

        return errors

    def _normalize_username(self, username: str | None) -> str:
        value = username or ""

        if self._config.normalize_username:
            return value.strip().lower()

        return value.strip()

    def _normalize_email(self, email: str | None) -> str:
        value = email or ""

        if self._config.normalize_email:
            return value.strip().lower()

        return value.strip()

    def _validate_fields(self, *, username: str, email: str) -> list[str]:
        errors: list[str] = []

        if self._config.username_required:
            errors.extend(
                self._validation_registry.validate(
                    "username", username,
                )
            )

        if self._config.email_required:
            errors.extend(
                self._validation_registry.validate(
                    "email", email,
                )
            )

        return errors

    def _check_duplicates(self, *, username: str, email: str) -> list[str]:
        errors: list[str] = []

        if self._config.username_required and self._repository.exists_by_username(username):
            errors.append("Username is already registered")

        if self._config.email_required and self._repository.exists_by_email(email):
            errors.append("Email is already registered")

        return errors

    def _password_errors(self, password_result: ValidationResult) -> list[str]:
        """
        Convert password-validator-s validation failures into registration errors.
        This method is intentionally defensive until the exact public
        ValidationResult error representation is finalized.
        """
        if password_result.errors:
            return [str(error) for error in password_result.errors]

        return ["Password does not satisfy the configured policy"]

    def _execute_hooks(self, user: User) -> None:
        for hook in self._hooks:
            hook.after_registration(user)

