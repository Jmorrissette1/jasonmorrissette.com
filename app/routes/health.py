"""Operational endpoints used by the hosting platform, not by visitors."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", include_in_schema=False)
def healthz() -> dict[str, str]:
    """Liveness check. Deliberately reveals nothing about the app or its environment."""
    return {"status": "ok"}