"""Jinja2 template configuration shared by all routes."""

from pathlib import Path

from fastapi.templating import Jinja2Templates

APP_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

# (label, path) pairs rendered by partials/header.html.
NAV_ITEMS: list[tuple[str, str]] = [
    ("Home", "/"),
    ("About", "/about"),
    ("Projects", "/projects"),
    ("Research", "/research"),
    ("Certifications", "/certifications"),
    ("Résumé", "/resume"),
]


def static_url(path: str) -> str:
    """Return a root-relative URL for a file in app/static/."""
    return f"/static/{path.lstrip('/')}"


templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates.env.globals["static_url"] = static_url
templates.env.globals["nav_items"] = NAV_ITEMS