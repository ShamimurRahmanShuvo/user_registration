from fastapi import FastAPI

from user_registration_fastapi import (
    get_registration_service,
    router,
)

from example_app.dependencies import get_registration_service as application_registration_service


app = FastAPI(
    title="User Registration API",
)


app.dependency_overrides[
    get_registration_service
] = application_registration_service


app.include_router(router)
