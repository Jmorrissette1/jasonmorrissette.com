"""Visitor-facing HTML pages."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import templates

router = APIRouter()

# FastAPI does not add HEAD automatically; monitors and link checkers use it.
PAGE_METHODS = ["GET", "HEAD"]


@router.api_route("/", methods=PAGE_METHODS, response_class=HTMLResponse, include_in_schema=False)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "pages/home.html")
