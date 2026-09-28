# Release Guide

This project publishes three distributions:

```text
user-registration
user-registration-fastapi
user-registration-sqlalchemy
```

## 1. Verify the Working Tree
```bash
git status
```

The working tree should contain only intentional release changes.

## 2. Update Versions

Update the version in:

```markdown
pyproject.toml
adapters/fastapi/pyproject.toml
adapters/sqlalchemy/pyproject.toml
```
For example:

`0.1.3`

Also keep:

```python
user_registration.__version__
```

consistent with the core package version.

## 3. Update CHANGELOG

Add the release entry to:

`CHANGELOG.md`

Document:
- Added functionality
- Changed functionality
- Fixed issues
- Packaging changes
- Breaking changes, if any

## 4. Run Unit Tests
```bash
.venv/bin/python -m pytest -v
```
## 5. Run Type Checking
```bash
.venv/bin/python -m mypy src
```
## 6. Run Ruff
```bash
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
```
For adapter code:

```bash
.venv/bin/python -m ruff check adapters/fastapi adapters/sqlalchemy
.venv/bin/python -m ruff format --check adapters/fastapi adapters/sqlalchemy
```
## 7. Build All Distributions

Clean previous build artifacts:

```bash
rm -rf dist build *.egg-info
rm -rf adapters/fastapi/dist adapters/fastapi/build adapters/fastapi/*.egg-info
rm -rf adapters/sqlalchemy/dist adapters/sqlalchemy/build adapters/sqlalchemy/*.egg-info
```
Build all packages into one directory:

```bash
mkdir -p dist

.venv/bin/python -m build --outdir dist .

.venv/bin/python -m build \
    --outdir dist \
    adapters/fastapi

.venv/bin/python -m build \
    --outdir dist \
    adapters/sqlalchemy
```
#### Verify:

```bash
ls -lh dist/
```
Expected artifacts:

```bash
user_registration-<version>-py3-none-any.whl
user_registration-<version>.tar.gz

user_registration_fastapi-<version>-py3-none-any.whl
user_registration_fastapi-<version>.tar.gz

user_registration_sqlalchemy-<version>-py3-none-any.whl
user_registration_sqlalchemy-<version>.tar.gz
```
## 8. Validate Package Metadata

Install Twine if required:

```bash
.venv/bin/python -m pip install twine
```

Run:

```bash
.venv/bin/python -m twine check dist/*
```

The output should report: `PASSED` for all distributions.

## 9. Test the Core Wheel

Create a clean environment:

```bash 
.venv/bin/python -m venv /tmp/user-registration-release-test
```

Install the wheel:

```bash
/tmp/user-registration-release-test/bin/python \
    -m pip install dist/user_registration-*.whl
```
Verify:

```bash
/tmp/user-registration-release-test/bin/python \
    -c "import user_registration; print(user_registration.__version__)"
```
## 10. Test Adapter Installation

### FastAPI:

```bash
/tmp/user-registration-release-test/bin/python \
    -m pip install dist/user_registration_fastapi-*.whl
```
Verify:

```bash
/tmp/user-registration-release-test/bin/python \
    -c "import user_registration_fastapi; print('FastAPI adapter OK')"
```
### SQLAlchemy:

```bash
/tmp/user-registration-release-test/bin/python \
    -m pip install dist/user_registration_sqlalchemy-*.whl
```
Verify:

```bash
/tmp/user-registration-release-test/bin/python \
    -c "import user_registration_sqlalchemy; print('SQLAlchemy adapter OK')"
```
## 11. Commit the Release
```bash
git add .
git commit -m "Release user-registration 0.1.3"
```
Verify:

```bash
git status
```
## 12. Create the Git Tag

Use a new tag for every published version.

```bash
git tag -a v0.1.3 -m "Release user-registration 0.1.3"
```
Verify:

```bash
git show v0.1.3
```
## 13. Push
```bash
git push origin main
git push origin v0.1.3
```
The tag should trigger the publishing workflow.

## 14. Verify GitHub Actions

Confirm that:
- CI passes.
- Package build succeeds.
- Twine validation succeeds.
- Publishing succeeds.
- All three distributions are uploaded.

## 15. Verify PyPI

Verify the three project pages:
```markdown
- user-registration
- user-registration-fastapi
- user-registration-sqlalchemy
```
Confirm:
- Version number
- Project description
- README rendering
- Python requirements
- Dependencies
- Project URLs
- Package files

##16. Verify Clean Installation from PyPI

After publication:

```bash
python3.14 -m venv /tmp/user-registration-pypi-test
```
Install:
```bash
/tmp/user-registration-pypi-test/bin/python \
    -m pip install user-registration
```
Verify:
```bash
/tmp/user-registration-pypi-test/bin/python \
    -c "import user_registration; print(user_registration.__version__)"
```
For FastAPI:
```bash
/tmp/user-registration-pypi-test/bin/python \
    -m pip install user-registration-fastapi
```
For SQLAlchemy:
```bash
/tmp/user-registration-pypi-test/bin/python \
    -m pip install user-registration-sqlalchemy
```
### Versioning Policy

Before `1.0.0`, the project is considered pre-stable.

For `1.0.0`:

- Public imports must be deliberately stabilized.
- Public protocols must be documented.
- Repository contracts must be documented.
- Transaction behavior must be documented.
- Error behavior must be documented.
- Supported Python versions must be explicit.
- Adapter compatibility must be explicit.
- Breaking changes should require a major version after stabilization.

### Release Checklist
- [ ] Working tree clean
- [ ] Version updated
- [ ] __version__ updated
- [ ] CHANGELOG updated
- [ ] Tests pass
- [ ] mypy passes
- [ ] Ruff passes
- [ ] Formatting passes
- [ ] All three distributions build
- [ ] twine check passes
- [ ] Core wheel tested
- [ ] FastAPI adapter tested
- [ ] SQLAlchemy adapter tested
- [ ] Git commit created
- [ ] Git tag created
- [ ] GitHub Actions succeeds
- [ ] PyPI packages verified
- [ ] Clean PyPI installation verified
