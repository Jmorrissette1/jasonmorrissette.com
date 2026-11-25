"""Page rendering, navigation and static-file safety."""

import re

from fastapi.testclient import TestClient

from app.templating import templates


def test_home_renders_html(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Cloud Security. Identity. Zero Trust." in response.text


def test_base_layout_accessibility_landmarks(client: TestClient) -> None:
    html = client.get("/").text
    assert '<html lang="en">' in html
    assert 'href="#main"' in html  # skip link
    assert '<main id="main"' in html
    assert 'aria-label="Primary"' in html


def test_current_page_is_marked_in_nav(client: TestClient) -> None:
    html = client.get("/").text
    # Whitespace-tolerant: assert the markup's meaning, not its formatting.
    assert re.search(r'aria-current="page"\s*>\s*Home\s*</a', html)
    assert html.count('aria-current="page"') == 1


def test_stylesheet_uses_root_relative_url(client: TestClient) -> None:
    assert 'href="/static/css/site.css"' in client.get("/").text


def test_html_templates_autoescape() -> None:
    # Starlette enables autoescaping for .html templates; guard against regressions.
    assert templates.env.autoescape("pages/home.html") is True


def test_static_path_traversal_is_blocked(client: TestClient) -> None:
    response = client.get("/static/%2e%2e/main.py")
    assert response.status_code == 404
    assert "create_app" not in response.text
