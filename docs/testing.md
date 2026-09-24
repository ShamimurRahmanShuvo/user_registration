# Testing

Use the project virtual environment:

```bash
.venv/bin/python -m pytest -v
```

Do not rely on a globally installed pytest.

## Unit coverage

Cover configuration, domain models, repositories/fakes, password hashing, password policy, validators, registry, registration results, registration service, and hooks.

## Adapter integration coverage

### SQLAlchemy

- persistence and retrieval
- duplicate username/email
- update
- delete
- mapper round trip

### FastAPI

- successful registration → 201
- duplicate registration → 409
- invalid registration → 422
- persistence failure → 500
- dependency override

## Quality checks

```bash
.venv/bin/python -m pytest -v
.venv/bin/python -m mypy src
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
```

## Wheel verification

```bash
.venv/bin/python -m build
.venv/bin/python -m venv /tmp/user-registration-release-test
/tmp/user-registration-release-test/bin/python -m pip install dist/user_registration-*.whl
/tmp/user-registration-release-test/bin/python -c "import user_registration; print('Package import successful')"
```
