import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class DataPurgeRequest(BaseModel):
    wa_phone_hash: str = Field(..., min_length=16, description="SHA-256 hash of user phone number")


class DataPurgeResponse(BaseModel):
    status: Literal["purged"] = "purged"
    purged_records: list[str]


class SendOtpRequest(BaseModel):
    phone: str = Field(..., description="10-digit Indian phone number (or with +91)")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Strip spaces, dashes, +91 prefix
        cleaned = re.sub(r"[\s\-+]", "", v)
        if cleaned.startswith("91") and len(cleaned) == 12:
            cleaned = cleaned[2:]
        if not re.fullmatch(r"[6-9]\d{9}", cleaned):
            raise ValueError("Must be a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9.")
        return cleaned


class SendOtpResponse(BaseModel):
    status: str = "success"
    message: str
    phone: str
    demo_otp: str | None = None


class VerifyOtpRequest(BaseModel):
    phone: str = Field(...)
    otp: str = Field(..., min_length=4, max_length=6)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-+]", "", v)
        if cleaned.startswith("91") and len(cleaned) == 12:
            cleaned = cleaned[2:]
        if not re.fullmatch(r"[6-9]\d{9}", cleaned):
            raise ValueError("Must be a valid 10-digit Indian mobile number.")
        return cleaned


class LoginPasswordRequest(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)


class UserProfile(BaseModel):
    id: str
    name: str
    phone: str | None = None
    email: str | None = None
    role: Literal["patient", "caregiver", "clinician", "guest"] = "patient"
    preferred_language: Literal["en", "kn"] = "en"
    token: str


class AuthResponse(BaseModel):
    status: str = "success"
    message: str
    user: UserProfile
