from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["healthy"] = "healthy"
    database: Literal["connected"] = "connected"
    db_value: str
    app_env: str = "development"
