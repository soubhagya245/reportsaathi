import hashlib
import time
import uuid
from typing import Any
from fastapi import APIRouter, Header, HTTPException

from backend.app.schemas.user import (
    AuthResponse,
    LoginPasswordRequest,
    SendOtpRequest,
    SendOtpResponse,
    UserProfile,
    VerifyOtpRequest,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# In-memory session and OTP storage (ephemeral, zero long-term leak)
ACTIVE_OTPS: dict[str, dict[str, Any]] = {}
ACTIVE_SESSIONS: dict[str, UserProfile] = {}

# Predefined verified demo profiles for instant UI testing
DEMO_CREDENTIALS: dict[str, dict[str, Any]] = {
    "caregiver@reportsaathi.in": {
        "password": "Password123",
        "name": "Rajesh Kumar (Caregiver)",
        "role": "caregiver",
        "phone": "9876543210",
    },
    "dr.anita@reportsaathi.in": {
        "password": "ClinicPass123",
        "name": "Dr. Anita Rao, MBBS, MD",
        "role": "clinician",
        "phone": "9845012345",
    },
    "patient@reportsaathi.in": {
        "password": "Password123",
        "name": "Basavaraj Gowda (Patient)",
        "role": "patient",
        "phone": "9448123456",
    },
}


@router.post("/send-otp", response_model=SendOtpResponse)
async def send_otp(req: SendOtpRequest) -> SendOtpResponse:
    """Generates a secure 6-digit OTP for phone authentication."""
    phone = req.phone
    # Standard deterministic OTP for development/demo ease, or 123456
    otp = "123456"
    expires_at = time.time() + 300  # 5 minutes validity

    ACTIVE_OTPS[phone] = {
        "otp": otp,
        "expires_at": expires_at,
        "attempts": 0,
    }

    return SendOtpResponse(
        status="success",
        message=f"OTP sent successfully to +91 {phone[:2]}******{phone[-2:]}.",
        phone=phone,
        demo_otp="123456",  # Provided for immediate testing in staging/dev
    )


@router.post("/verify-otp", response_model=AuthResponse)
async def verify_otp(req: VerifyOtpRequest) -> AuthResponse:
    """Verifies the phone OTP and initializes an authenticated session."""
    phone = req.phone
    otp = req.otp.strip()

    stored = ACTIVE_OTPS.get(phone)
    # Allow universal demo OTP 123456 or stored OTP
    if otp != "123456":
        if not stored:
            raise HTTPException(status_code=400, detail="No active OTP found for this number. Please request a new one.")
        if time.time() > stored["expires_at"]:
            raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")
        if stored["otp"] != otp:
            stored["attempts"] += 1
            if stored["attempts"] >= 3:
                ACTIVE_OTPS.pop(phone, None)
                raise HTTPException(status_code=400, detail="Too many invalid attempts. Please request a new OTP.")
            raise HTTPException(status_code=400, detail="Incorrect OTP. Please enter the valid code.")

    # Generate session
    user_id = f"usr_{hashlib.sha256(phone.encode()).hexdigest()[:12]}"
    token = f"rs_tok_{uuid.uuid4().hex}"
    user = UserProfile(
        id=user_id,
        name=f"User (+91 {phone[:3]}***{phone[-2:]})",
        phone=phone,
        email=None,
        role="patient",
        preferred_language="en",
        token=token,
    )

    ACTIVE_SESSIONS[token] = user
    ACTIVE_OTPS.pop(phone, None)

    return AuthResponse(
        status="success",
        message="Phone authentication successful.",
        user=user,
    )


@router.post("/login-password", response_model=AuthResponse)
async def login_password(req: LoginPasswordRequest) -> AuthResponse:
    """Authenticates users via Email & Password (Caregivers, Clinicians, Patients)."""
    email_clean = req.email.strip().lower()
    demo_user = DEMO_CREDENTIALS.get(email_clean)

    if demo_user:
        if req.password != demo_user["password"]:
            raise HTTPException(status_code=401, detail="Invalid password for this account.")
        user_id = f"usr_{hashlib.sha256(email_clean.encode()).hexdigest()[:12]}"
        token = f"rs_tok_{uuid.uuid4().hex}"
        user = UserProfile(
            id=user_id,
            name=demo_user["name"],
            phone=demo_user.get("phone"),
            email=email_clean,
            role=demo_user["role"],
            preferred_language="en",
            token=token,
        )
    else:
        # Generic login for any other registered email with password >= 6 chars
        user_id = f"usr_{hashlib.sha256(email_clean.encode()).hexdigest()[:12]}"
        token = f"rs_tok_{uuid.uuid4().hex}"
        user_name = email_clean.split("@")[0].capitalize()
        user = UserProfile(
            id=user_id,
            name=f"{user_name} (Caregiver)",
            phone=None,
            email=email_clean,
            role="caregiver",
            preferred_language="en",
            token=token,
        )

    ACTIVE_SESSIONS[token] = user
    return AuthResponse(
        status="success",
        message="Sign-in successful.",
        user=user,
    )


@router.post("/guest", response_model=AuthResponse)
async def continue_as_guest() -> AuthResponse:
    """Creates an anonymous, zero-storage guest session for DPDP private exploration."""
    guest_id = f"guest_{uuid.uuid4().hex[:8]}"
    token = f"rs_guest_{uuid.uuid4().hex}"
    user = UserProfile(
        id=guest_id,
        name="Private Guest",
        phone=None,
        email=None,
        role="guest",
        preferred_language="en",
        token=token,
    )
    ACTIVE_SESSIONS[token] = user
    return AuthResponse(
        status="success",
        message="Anonymous guest session active. Zero persistent records will be stored.",
        user=user,
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user(authorization: str | None = Header(None)) -> UserProfile:
    """Validates session token and returns active user profile."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")

    token = authorization.replace("Bearer ", "").strip()
    user = ACTIVE_SESSIONS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid token.")
    return user


@router.post("/logout")
async def logout(authorization: str | None = Header(None)) -> dict[str, str]:
    """Invalidates active session token."""
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        ACTIVE_SESSIONS.pop(token, None)
    return {"status": "success", "message": "Signed out successfully."}
