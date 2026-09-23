# Testing

## Unit Tests

Unit tests cover:

- configuration
- domain models
- validators
- validation registry
- password hashing
- registration result
- registration service
- hooks
- repository behavior using fakes

## Integration Tests

Integration tests cover:

- SQLAlchemy repository
- FastAPI registration endpoint
- persistence behavior
- duplicate handling
- HTTP status mapping

## Test Commands

All tests:

```bash
.venv/bin/python -m pytest -v