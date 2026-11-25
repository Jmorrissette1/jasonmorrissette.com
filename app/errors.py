"""Branded error pages that never reveal internal details."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.middleware.security_headers import build_security_headers
from app.templating import templates


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
    """Render 404s and other HTTP errors (405, etc.) with the site layout."""
    template = "errors/404.html" if exc.status_code == 404 else "errors/error.html"
    return templates.TemplateResponse(
        request,
        template,
        {"status_code": exc.status_code},
        status_code=exc.status_code,
        headers=exc.headers,  # keeps e.g. the "Allow" header on a 405
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    """Last-resort 500 page.

    Starlette runs this handler *outside* our middleware stack, so security
    headers are added here explicitly. Starlette re-raises the exception
    afterwards so it is logged server-side; the visitor never sees it.
    """
    return templates.TemplateResponse(
        request,
        "errors/error.html",
        {"status_code": 500},
        status_code=500,
        headers=build_security_headers(request.app.state.settings),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)