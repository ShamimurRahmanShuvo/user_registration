# Release Guide

Run all checks:

```bash
.venv/bin/python -m pytest -v
.venv/bin/python -m mypy src
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
```

Clean build:

```bash
rm -rf dist build *.egg-info
.venv/bin/python -m build
```

Test the wheel in a clean environment:

```bash
.venv/bin/python -m venv /tmp/user-registration-release-test
/tmp/user-registration-release-test/bin/python   -m pip install dist/user_registration-*.whl

/tmp/user-registration-release-test/bin/python   -c "import user_registration; print('Package import successful')"
```

Git release example:

```bash
git status
git diff
git add .
git commit -m "Prepare user-registration 0.1.0 release"
git tag -a v0.1.0 -m "Release user-registration 0.1.0"
git push origin main
git push origin v0.1.0
```

Keep the project in the `0.x` series until the public API is deliberately stabilized.

Recommended distributions:

```text
user-registration
user-registration-fastapi
user-registration-sqlalchemy
```
