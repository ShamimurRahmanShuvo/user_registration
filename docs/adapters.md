# Adapters

Adapters connect the core package to external frameworks and infrastructure.

## Dependency Direction

```text
                 user-registration
                         ^
                         |
             +-----------+-----------+
             |                       |
             |                       |
      FastAPI Adapter        SQLAlchemy Adapter