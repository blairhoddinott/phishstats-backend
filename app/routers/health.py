from fastapi import APIRouter

from app.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment)


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.app_name}"}
