import os
from collections.abc import AsyncGenerator

import aiosqlite

from backend.app.config import settings


async def init_db() -> None:
    """Initialize SQLite database with WAL mode and create health/seed tables."""
    db_dir = os.path.dirname(settings.db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    async with aiosqlite.connect(settings.db_path) as db:
        # Enable Write-Ahead Logging (WAL) per architecture specification
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA foreign_keys=ON;")

        # Create system_metadata table for health and migration status
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS system_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # Seed initial system health entry if not present
        seed_value = "ReportSaathi DB Core Initialized - SQLite WAL Mode Active"
        await db.execute(
            """
            INSERT OR IGNORE INTO system_metadata (key, value)
            VALUES ('system_health_seed', ?);
            """,
            (seed_value,),
        )
        await db.commit()


async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Dependency / context helper yielding an active database connection."""
    async with aiosqlite.connect(settings.db_path) as conn:
        conn.row_factory = aiosqlite.Row
        yield conn


async def read_health_status() -> str:
    """Reads the health seed value from the database to prove live DB reads."""
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT value FROM system_metadata WHERE key = 'system_health_seed';"
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return str(row["value"])
            return "No health record found"
