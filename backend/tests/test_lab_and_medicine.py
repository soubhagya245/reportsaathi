import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app

@pytest.mark.asyncio
async def test_medicine_lookup_metformin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/medicines/lookup?q=Glycomet")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["generic_name"] == "Metformin"
        assert "Glycomet" in data["brand_aliases"]
        assert "kn" in data["purpose"]
        assert "en" in data["purpose"]

@pytest.mark.asyncio
async def test_medicine_lookup_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/medicines/lookup?q=NonExistentTablet999")
        assert response.status_code == 404
        assert response.json()["detail"]["fallback_action"] == "PHARMACIST_FALLBACK"

@pytest.mark.asyncio
async def test_lab_report_fixtures_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/lab-reports/fixtures")
        assert response.status_code == 200
        fixtures = response.json()
        assert len(fixtures) >= 5

@pytest.mark.asyncio
async def test_lab_report_process_critical_potassium():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/lab-reports/process-fixture/fixture_03_critical_hyperkalemia")
        assert response.status_code == 200
        data = response.json()
        assert data["is_critical"] is True
        assert "🚨" in data["critical_alert"]
        potassium = next(p for p in data["extracted_parameters"] if p["test_id"] == "lab_potassium")
        assert potassium["found_value"] == 6.4
        assert potassium["status"] == "ABOVE_RANGE"
        assert potassium["is_critical"] is True

@pytest.mark.asyncio
async def test_lab_report_process_handwriting_rejection():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/lab-reports/process-fixture/fixture_09_handwritten_prescription")
        assert response.status_code == 422
        detail = response.json()["detail"]
        assert detail["code"] == "HANDWRITING_OR_ILLEGIBLE_DETECTED"
        assert "pharmacist" in detail["message"].lower()
