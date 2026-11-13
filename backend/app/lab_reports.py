"""Lab Report API endpoints

Provides:
- POST /api/lab-reports/ocr-extract  – accepts multipart file, returns extracted parameters.
- POST /api/lab-reports/process-fixture/{fixture_id} – returns a pre‑canned LabReportResult for demo fixtures.
- GET  /api/health – simple health check (already exists elsewhere).

The real OCR implementation is omitted for brevity; a placeholder deterministic parser is used.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/lab-reports", tags=["Lab Reports"])


class LabRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None


class ExtractedParam(BaseModel):
    test_id: str = Field(..., description="Internal test identifier")
    name: str
    name_kn: Optional[str] = None
    found_value: float
    unit: str
    lab_printed_range: LabRange
    status: str = Field(
        ..., description="WITHIN_RANGE | ABOVE_RANGE | BELOW_RANGE | RANGE_NOT_SPECIFIED_ON_REPORT"
    )
    is_critical: bool = False
    critical_escalation_message: Optional[str] = None
    desc_en: Optional[str] = None
    desc_kn: Optional[str] = None
    doctor_q_en: Optional[List[str]] = None
    doctor_q_kn: Optional[List[str]] = None


class LabReportResult(BaseModel):
    status: str
    document_type: str
    confidence_score: float
    is_critical: bool
    critical_alert: Optional[str] = None
    extracted_parameters: List[ExtractedParam]
    raw_text: Optional[str] = None
    message: Optional[str] = None
    governance: Optional[dict] = None


# ---------------------------------------------------------------------------
# Helper: very simple fake OCR – in real code replace with actual OCR engine.
# ---------------------------------------------------------------------------
def _fake_ocr(file_bytes: bytes) -> LabReportResult:
    # For demo we just return a static example of a high‑blood‑sugar report.
    params = [
        ExtractedParam(
            test_id="glucose_fasting",
            name="Fasting Blood Glucose",
            found_value=168,
            unit="mg/dL",
            lab_printed_range=LabRange(min=70, max=100),
            status="ABOVE_RANGE",
            is_critical=False,
            desc_en="Your fasting glucose is above the normal range.",
            doctor_q_en=[
                "Should my diabetes medication be adjusted?",
                "What target should I aim for?",
            ],
        ),
        ExtractedParam(
            test_id="hba1c",
            name="HbA1c (Glycated Hemoglobin)",
            found_value=8.4,
            unit="%",
            lab_printed_range=LabRange(min=4.0, max=5.6),
            status="ABOVE_RANGE",
            is_critical=False,
            desc_en="Your average blood sugar over the past 2‑3 months is high.",
            doctor_q_en=[
                "Do I need to change my Metformin dose?",
                "Any lifestyle changes recommended?",
            ],
        ),
    ]
    return LabReportResult(
        status="processed",
        document_type="lab_report",
        confidence_score=0.96,
        is_critical=False,
        extracted_parameters=params,
    )


# ---------------------------------------------------------------------------
# End‑point: OCR extract
# ---------------------------------------------------------------------------
@router.post("/ocr-extract", response_model=LabReportResult)
async def ocr_extract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    content = await file.read()
    # In production replace this with actual OCR processing.
    result = _fake_ocr(content)
    return result


# ---------------------------------------------------------------------------
# End‑point: fixture processing – useful for UI demo chips
# ---------------------------------------------------------------------------
FIXTURES = {
    "normal": "normal",
    "high_glucose": "high_glucose",
    "critical_k": "critical_k",
    "low_sugar": "low_sugar",
    "high_creatinine": "high_creatinine",
    "high_tsh": "high_tsh",
}


@router.post("/process-fixture/{fixture_id}", response_model=LabReportResult)
async def process_fixture(fixture_id: str):
    if fixture_id not in FIXTURES:
        raise HTTPException(status_code=404, detail="Fixture not found")
    # Return a hard‑coded result per fixture – only a couple shown for brevity.
    if fixture_id == "high_glucose":
        return _fake_ocr(b"")
    if fixture_id == "critical_k":
        param = ExtractedParam(
            test_id="potassium",
            name="Serum Potassium",
            found_value=6.4,
            unit="mEq/L",
            lab_printed_range=LabRange(min=3.5, max=5.1),
            status="CRITICAL_VALUE",
            is_critical=True,
            critical_escalation_message="Urgent medical evaluation required.",
            desc_en="Potassium is dangerously high.",
            doctor_q_en=["What immediate steps should I take?"],
        )
        return LabReportResult(
            status="processed",
            document_type="lab_report",
            confidence_score=0.99,
            is_critical=True,
            extracted_parameters=[param],
        )
    # default fallback – reuse normal example
    return _fake_ocr(b"")


# Export router for inclusion in main app
__all__ = ["router"]