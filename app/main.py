"""Application factory: builds and configures the FastAPI app."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Settings, get_settings
from app.errors import register_error_handlers
from app.middleware.security_headers import SecurityHeadersMiddleware, build_security_headers
from app.routes import health, pages
from app.templating import STATIC_DIR


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

    app.add_middleware(SecurityHeadersMiddleware, headers=build_security_headers(settings))
    register_error_handlers(app)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.include_router(health.router)
    app.include_router(pages.router)
    return app
    return app


app = create_app()
