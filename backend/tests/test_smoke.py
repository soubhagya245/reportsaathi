import aiosqlite
import pytest
from httpx import AsyncClient

from backend.app.config import settings


@pytest.mark.asyncio
async def test_smoke_database_and_health_roundtrip(async_client: AsyncClient) -> None:
    """Automated Smoke Test: Verifies DB WAL mode, custom seed writes, and API readback."""
    # 1. Directly mutate/insert a dynamic verification record into SQLite
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO system_metadata (key, value)
            VALUES ('system_health_seed', 'SMOKE_TEST_DB_VALUE_VERIFIED_2026');
            """
        )
        await db.commit()

        # Verify PRAGMA journal_mode is WAL
        async with db.execute("PRAGMA journal_mode;") as cursor:
            row = await cursor.fetchone()
            assert row is not None
            assert str(row[0]).lower() == "wal"

    # 2. Call GET /api/health to confirm backend reads that exact value back
    response = await async_client.get("/api/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["database"] == "connected"
    assert payload["db_value"] == "SMOKE_TEST_DB_VALUE_VERIFIED_2026"
