from typing import Literal

from pydantic import BaseModel

LabParameterStatus = Literal[
    "WITHIN_RANGE",
    "ABOVE_RANGE",
    "BELOW_RANGE",
    "RANGE_NOT_SPECIFIED_ON_REPORT",
]


class LabPrintedRange(BaseModel):
    min: float | None = None
    max: float | None = None


class ExtractedLabParameter(BaseModel):
    test_id: str
    name: str
    found_value: float
    unit: str
    lab_printed_range: LabPrintedRange
    status: LabParameterStatus
    is_critical: bool
    critical_escalation_message: str | None = None


class LabExtractResponse(BaseModel):
    status: Literal["success"] = "success"
    document_type: str = "PRINTED_LAB_REPORT"
    confidence_score: float
    extracted_parameters: list[ExtractedLabParameter]


class LabExtractErrorResponse(BaseModel):
    status: Literal["rejected"] = "rejected"
    code: Literal["HANDWRITING_OR_ILLEGIBLE_DETECTED"] = "HANDWRITING_OR_ILLEGIBLE_DETECTED"
    message: str
