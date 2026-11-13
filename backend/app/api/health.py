from backend.app.config import settings
from backend.app.database import read_health_status
from backend.app.schemas.health import HealthResponse
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/api/health", response_model=HealthResponse)
@router.get("/healthz", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """System health check that verifies live database read connectivity."""
    db_value = await read_health_status()
    return HealthResponse(
        status="healthy",
        database="connected",
        db_value=db_value,
        app_env=settings.app_env,
    )
