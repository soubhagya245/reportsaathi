from typing import Literal

from pydantic import BaseModel, Field


class BilingualText(BaseModel):
    kn: str
    en: str


class BilingualList(BaseModel):
    kn: list[str]
    en: list[str]


class GovernanceMetadata(BaseModel):
    reviewed_by: str
    clinician_reg_no: str
    reviewed_at: str
    disclaimer_en: str


class MedicineCardData(BaseModel):
    id: str
    generic_name: str
    brand_aliases: list[str] = Field(default_factory=list)
    therapeutic_class: str
    purpose: BilingualText
    how_to_take: BilingualText
    common_side_effects: BilingualText
    red_flags: BilingualList
    caution_do_not_stop: BilingualText
    doctor_questions: BilingualList
    governance: GovernanceMetadata


class MedicineCardResponse(BaseModel):
    status: Literal["success"] = "success"
    data: MedicineCardData


class MedicineNotFoundResponse(BaseModel):
    status: Literal["not_found"] = "not_found"
    message: str
    fallback_action: Literal["PHARMACIST_FALLBACK"] = "PHARMACIST_FALLBACK"
