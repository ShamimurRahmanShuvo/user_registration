# FastAPI Integration

Install:

```bash
pip install user-registration user-registration-fastapi
```

With SQLAlchemy:

```bash
pip install user-registration-sqlalchemy
```

The adapter exposes a dependency contract; the application supplies the actual service.

Correct:

```python
Depends(get_registration_service)
```

Incorrect:

```python
Depends(get_registration_service())
```

The application overrides the dependency:

```python
app.dependency_overrides[
    get_registration_service
] = application_registration_service
```

Then:

```python
app.include_router(router)
```

## Endpoint

```text
POST /users/register
```

Request:

```json
{
  "username": "shuvo",
  "email": "shuvo@example.com",
  "password": "StrongPassword123!"
}
```

Responses:

- `201 Created` on success
- `409 Conflict` for duplicate registration
- `422 Unprocessable Entity` for registration validation errors
- `500 Internal Server Error` for persistence failure

The application owns the database session and transaction.
