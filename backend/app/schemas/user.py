from typing import Literal

from pydantic import BaseModel, Field


class DataPurgeRequest(BaseModel):
    wa_phone_hash: str = Field(..., min_length=16, description="SHA-256 hash of user phone number")


class DataPurgeResponse(BaseModel):
    status: Literal["purged"] = "purged"
    purged_records: list[str]
