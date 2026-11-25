"""Foundation tests: the app starts, is healthy, and exposes nothing extra."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import Settings


def test_healthz_returns_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_api_docs_are_disabled(client: TestClient, path: str) -> None:
    assert client.get(path).status_code == 404


def test_unknown_route_returns_404(client: TestClient) -> None:
    assert client.get("/does-not-exist").status_code == 404


def test_production_rejects_http_base_url() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production", base_url="http://example.com", _env_file=None)


def test_production_accepts_https_base_url() -> None:
    settings = Settings(
        environment="production", base_url="https://jasonmorrissette.com", _env_file=None
    )
    assert settings.is_production