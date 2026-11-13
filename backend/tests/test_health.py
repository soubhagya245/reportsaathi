import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_api_health(async_client: AsyncClient) -> None:
    """Tests GET /api/health returns healthy status and reads seed value from DB."""
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "ReportSaathi DB Core Initialized - SQLite WAL Mode Active" in data["db_value"]
    assert data["app_env"] == "test"


@pytest.mark.asyncio
async def test_get_healthz_alias(async_client: AsyncClient) -> None:
    """Tests GET /healthz alias endpoint for container/orchestrator health checks."""
    response = await async_client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
