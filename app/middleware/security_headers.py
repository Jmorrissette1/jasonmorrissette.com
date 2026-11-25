"""Security headers applied to every HTTP response.

Implemented as pure ASGI middleware: it wraps the app, watches outgoing
messages, and adds headers to the response-start message.
"""

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.config import Settings


def build_csp(*, production: bool) -> str:
    """Return a strict Content-Security-Policy: same-origin only, no inline code."""
    directives = [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
    if production:
        # Local dev runs on plain http://127.0.0.1, where this would break CSS.
        directives.append("upgrade-insecure-requests")
    return "; ".join(directives)


def build_security_headers(settings: Settings) -> dict[str, str]:
    """All security headers for this deployment, derived from settings."""
    headers = {
        "Content-Security-Policy": build_csp(production=settings.is_production),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Resource-Policy": "same-origin",
    }
    if settings.hsts_max_age > 0:
        headers["Strict-Transport-Security"] = f"max-age={settings.hsts_max_age}"
    return headers


class SecurityHeadersMiddleware:
    """Add security headers to every HTTP response, including errors and static files."""

    def __init__(self, app: ASGIApp, *, headers: dict[str, str]) -> None:
        self.app = app
        self.headers = headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = MutableHeaders(scope=message)
                for name, value in self.headers.items():
                    response_headers[name] = value
            await send(message)

        await self.app(scope, receive, send_with_headers)