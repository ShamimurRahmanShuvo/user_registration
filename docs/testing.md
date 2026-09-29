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

## Coverage

Coverage uses pytest-cov.

Run:

```bash
  .venv/bin/python -m pytest \
    --cov=user_registration \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html
```
The HTML report is generated at:

`htmlcov/index.html`

## Coverage Policy

The core package has a minimum coverage threshold.

The target is:

`88%+`

Both line and branch coverage are considered.

## Repository Transaction Tests

Repository integration tests must verify:

- successful create
- successful update
- successful delete
- duplicate username
- duplicate email
- duplicate update
- missing user behavior
- repository does not commit
- repository does not rollback the caller's outer transaction
- failed uniqueness operations do not poison the outer transaction
- subsequent operations remain possible after a savepoint rollback