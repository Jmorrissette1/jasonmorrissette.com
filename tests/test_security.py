"""Security headers and safe error handling."""

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

EXPECTED_HEADERS = {
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "referrer-policy": "strict-origin-when-cross-origin",
    "cross-origin-opener-policy": "same-origin",
    "cross-origin-resource-policy": "same-origin",
}


@pytest.mark.parametrize(
    ("path", "expected_status"),
    [("/", 200), ("/healthz", 200), ("/static/.gitkeep", 200), ("/does-not-exist", 404)],
)
def test_security_headers_on_every_response(
    client: TestClient, path: str, expected_status: int
) -> None:
    response = client.get(path)
    assert response.status_code == expected_status
    for name, value in EXPECTED_HEADERS.items():
        assert response.headers.get(name) == value, f"{name} missing or wrong on {path}"
    assert "content-security-policy" in response.headers
    assert "permissions-policy" in response.headers


def test_csp_is_strict(client: TestClient) -> None:
    csp = client.get("/").headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "object-src 'none'" in csp
    assert "unsafe-inline" not in csp
    assert "unsafe-eval" not in csp


def test_dev_csp_does_not_upgrade_requests(client: TestClient) -> None:
    csp = client.get("/").headers["content-security-policy"]
    assert "upgrade-insecure-requests" not in csp


def test_hsts_is_off_by_default(client: TestClient) -> None:
    assert "strict-transport-security" not in client.get("/").headers


def test_production_settings_enable_hsts_and_upgrade() -> None:
    settings = Settings(
        environment="production",
        base_url="https://jasonmorrissette.com",
        hsts_max_age=300,
        _env_file=None,
    )
    with TestClient(create_app(settings)) as client:
        headers = client.get("/").headers
    assert headers["strict-transport-security"] == "max-age=300"
    assert "upgrade-insecure-requests" in headers["content-security-policy"]


def test_404_page_is_branded(client: TestClient) -> None:
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("text/html")
    assert "Page not found" in response.text


def test_405_keeps_allow_header(client: TestClient) -> None:
    response = client.post("/")
    assert response.status_code == 405
    assert "GET" in response.headers["allow"]


def test_500_page_hides_internals(settings: Settings) -> None:
    app = create_app(settings)

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("secret internal detail")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/boom")

    assert response.status_code == 500
    assert "Something went wrong" in response.text
    assert "secret internal detail" not in response.text
    assert "Traceback" not in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "content-security-policy" in response.headers
