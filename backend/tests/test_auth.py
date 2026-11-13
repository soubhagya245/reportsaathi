import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app


@pytest.mark.asyncio
async def test_send_and_verify_otp():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Send OTP
        res = await ac.post("/api/auth/send-otp", json={"phone": "9876543210"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "success"
        assert data["phone"] == "9876543210"
        assert data["demo_otp"] == "123456"

        # 2. Verify with wrong OTP
        res_fail = await ac.post("/api/auth/verify-otp", json={"phone": "9876543210", "otp": "999999"})
        assert res_fail.status_code == 400

        # 3. Verify with correct OTP
        res_ok = await ac.post("/api/auth/verify-otp", json={"phone": "9876543210", "otp": "123456"})
        assert res_ok.status_code == 200
        auth_data = res_ok.json()
        assert auth_data["status"] == "success"
        user = auth_data["user"]
        assert user["phone"] == "9876543210"
        token = user["token"]

        # 4. Check /me with token
        res_me = await ac.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res_me.status_code == 200
        assert res_me.json()["phone"] == "9876543210"

        # 5. Logout
        res_logout = await ac.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
        assert res_logout.status_code == 200


@pytest.mark.asyncio
async def test_login_password_demo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Invalid password
        res_fail = await ac.post(
            "/api/auth/login-password",
            json={"email": "caregiver@reportsaathi.in", "password": "WrongPassword"}
        )
        assert res_fail.status_code == 401

        # Valid demo login
        res_ok = await ac.post(
            "/api/auth/login-password",
            json={"email": "caregiver@reportsaathi.in", "password": "Password123"}
        )
        assert res_ok.status_code == 200
        data = res_ok.json()
        assert data["user"]["name"] == "Rajesh Kumar (Caregiver)"
        assert data["user"]["role"] == "caregiver"


@pytest.mark.asyncio
async def test_guest_session():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/auth/guest")
        assert res.status_code == 200
        data = res.json()
        assert data["user"]["role"] == "guest"
        assert data["user"]["name"] == "Private Guest"
