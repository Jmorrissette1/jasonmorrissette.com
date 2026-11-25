"""Application factory: builds and configures the FastAPI app."""

from fastapi import FastAPI

from app.config import Settings, get_settings
from app.routes import health


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a configured FastAPI instance.

    Tests pass their own Settings; production uses environment variables.
    """
    settings = settings or get_settings()

    app = FastAPI(
        title="jasonmorrissette.com",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.state.settings = settings

    app.include_router(health.router)
    return app


app = create_app()