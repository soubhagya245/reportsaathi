import pytest
from pydantic import ValidationError

from backend.app.schemas.lab_report import (
    LabExtractErrorResponse,
    LabExtractResponse,
)
from backend.app.schemas.medicine import (
    MedicineCardResponse,
    MedicineNotFoundResponse,
)
from backend.app.schemas.user import DataPurgeRequest, DataPurgeResponse
from backend.app.schemas.whatsapp import (
    WhatsAppWebhookPayload,
)

# ==============================================================================
# WhatsApp Webhook Contract Tests (TASK-01 / TC-API-01)
# ==============================================================================


def test_whatsapp_text_webhook_payload_valid() -> None:
    raw_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "9180XXXXXXXX",
                                "phone_number_id": "1048291048123",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Appaji"},
                                    "wa_id": "9198XXXXXXXX",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "9198XXXXXXXX",
                                    "id": "wamid.HBgMOTE5...",
                                    "timestamp": "1731485640",
                                    "type": "text",
                                    "text": {"body": "Glycomet 500"},
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }
    model = WhatsAppWebhookPayload.model_validate(raw_payload)
    assert model.object == "whatsapp_business_account"
    assert len(model.entry) == 1
    msg = model.entry[0].changes[0].value.messages[0]  # type: ignore[index]
    assert msg.from_ == "9198XXXXXXXX"
    assert msg.type == "text"
    assert msg.text is not None
    assert msg.text.body == "Glycomet 500"


def test_whatsapp_interactive_button_payload_valid() -> None:
    raw_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WABA_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "918012345678",
                                "phone_number_id": "1048291048123",
                            },
                            "messages": [
                                {
                                    "from": "919876543210",
                                    "id": "wamid.12345",
                                    "timestamp": "1731485650",
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "button_reply",
                                        "button_reply": {
                                            "id": "btn_lang_kn",
                                            "title": "ಕನ್ನಡ",
                                        },
                                    },
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }
    model = WhatsAppWebhookPayload.model_validate(raw_payload)
    msg = model.entry[0].changes[0].value.messages[0]  # type: ignore[index]
    assert msg.type == "interactive"
    assert msg.interactive is not None
    assert msg.interactive.button_reply.id == "btn_lang_kn"


def test_whatsapp_webhook_malformed_raises_error() -> None:
    # Missing required 'object' and malformed changes
    bad_payload = {"entry": [{"id": "123", "changes": []}]}
    with pytest.raises(ValidationError):
        WhatsAppWebhookPayload.model_validate(bad_payload)


# ==============================================================================
# Medicine Card Response Contract Tests (TASK-01 / TC-API-02)
# ==============================================================================


def test_medicine_card_response_valid() -> None:
    raw_response = {
        "status": "success",
        "data": {
            "id": "med_metformin",
            "generic_name": "Metformin",
            "brand_aliases": ["Glycomet", "Glucophage", "Obimet", "Glyciphage"],
            "therapeutic_class": "Biguanide / Antidiabetic",
            "purpose": {
                "kn": "ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ನಿಯಂತ್ರಿಸಲು.",
                "en": "To help control blood sugar levels.",
            },
            "how_to_take": {
                "kn": "ಊಟದ ಜೊತೆ ಅಥವಾ ತಕ್ಷಣ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ.",
                "en": "Take with or right after food.",
            },
            "common_side_effects": {
                "kn": "ಹೊಟ್ಟೆ ನೋವು, ವಾಕರಿಕೆ — ಸಾಮಾನ್ಯವಾಗಿ 1-2 ವಾರಗಳಲ್ಲಿ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
                "en": "Mild nausea or loose motion; usually settles in 1-2 weeks.",
            },
            "red_flags": {
                "kn": ["ತೀವ್ರ ನಿಶ್ಯಕ್ತಿ ಅಥವಾ ವಿಪರೀತ ಹೊಟ್ಟೆ ನೋವು", "ಉಸಿರಾಟದಲ್ಲಿ ತೊಂದರೆ"],
                "en": ["Severe fatigue or abdominal pain", "Difficulty breathing"],
            },
            "caution_do_not_stop": {
                "kn": "ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಈ ಮಾತ್ರೆ ನಿಲ್ಲಿಸಬೇಡಿ.",
                "en": "Do not stop this medicine without consulting your doctor.",
            },
            "doctor_questions": {
                "kn": [
                    "ಈ ಮಾತ್ರೆ ಎಷ್ಟು ದಿನ ಮುಂದುವರಿಸಬೇಕು?",
                    "ಮಾತ್ರೆ ತೆಗೆದುಕೊಳ್ಳುವುದು ಮರೆತರೆ ಏನು ಮಾಡಬೇಕು?",
                ],
                "en": [
                    "For how many months should I continue this medicine?",
                    "What should I do if I miss a dose?",
                ],
            },
            "governance": {
                "reviewed_by": "Dr. Anita Rao, MBBS, MD",
                "clinician_reg_no": "KMC-45291",
                "reviewed_at": "2026-11-01T00:00:00Z",
                "disclaimer_en": (
                    "Notice: Information only, not medical advice. "
                    "Drug-drug interactions not checked."
                ),
            },
        },
    }
    model = MedicineCardResponse.model_validate(raw_response)
    assert model.status == "success"
    assert model.data.id == "med_metformin"
    assert model.data.generic_name == "Metformin"
    assert "Glycomet" in model.data.brand_aliases
    assert len(model.data.doctor_questions.kn) == 2


def test_medicine_card_missing_governance_raises_error() -> None:
    bad_card = {
        "status": "success",
        "data": {
            "id": "med_metformin",
            "generic_name": "Metformin",
            # missing governance
        },
    }
    with pytest.raises(ValidationError):
        MedicineCardResponse.model_validate(bad_card)


def test_medicine_not_found_response_valid() -> None:
    raw_response = {
        "status": "not_found",
        "message": "Medicine not found in catalog",
        "fallback_action": "PHARMACIST_FALLBACK",
    }
    model = MedicineNotFoundResponse.model_validate(raw_response)
    assert model.status == "not_found"
    assert model.fallback_action == "PHARMACIST_FALLBACK"


# ==============================================================================
# Lab Extract Contract Tests (TASK-01 / API-4)
# ==============================================================================


def test_lab_extract_response_valid() -> None:
    raw_response = {
        "status": "success",
        "document_type": "PRINTED_LAB_REPORT",
        "confidence_score": 0.94,
        "extracted_parameters": [
            {
                "test_id": "lab_fbs",
                "name": "Fasting Blood Sugar (FBS)",
                "found_value": 168.0,
                "unit": "mg/dL",
                "lab_printed_range": {"min": 70.0, "max": 100.0},
                "status": "ABOVE_RANGE",
                "is_critical": False,
            },
            {
                "test_id": "lab_potassium",
                "name": "Serum Potassium",
                "found_value": 6.4,
                "unit": "mEq/L",
                "lab_printed_range": {"min": 3.5, "max": 5.0},
                "status": "ABOVE_RANGE",
                "is_critical": True,
                "critical_escalation_message": "Consult a doctor today immediately.",
            },
        ],
    }
    model = LabExtractResponse.model_validate(raw_response)
    assert model.status == "success"
    assert len(model.extracted_parameters) == 2
    assert model.extracted_parameters[1].is_critical is True
    assert model.extracted_parameters[1].critical_escalation_message is not None


def test_lab_extract_handwriting_rejected_response() -> None:
    raw_response = {
        "status": "rejected",
        "code": "HANDWRITING_OR_ILLEGIBLE_DETECTED",
        "message": "Cannot parse handwritten prescriptions reliably.",
    }
    model = LabExtractErrorResponse.model_validate(raw_response)
    assert model.status == "rejected"
    assert model.code == "HANDWRITING_OR_ILLEGIBLE_DETECTED"


# ==============================================================================
# DPDP Data Purge Contract Tests (TASK-01 / TC-API-03)
# ==============================================================================


def test_data_purge_models_valid() -> None:
    req = DataPurgeRequest(
        wa_phone_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert len(req.wa_phone_hash) == 64

    resp = DataPurgeResponse(
        status="purged",
        purged_records=["sessions", "scratch_files", "cache"],
    )
    assert resp.status == "purged"
    assert "scratch_files" in resp.purged_records


def test_data_purge_request_short_hash_rejected() -> None:
    with pytest.raises(ValidationError):
        DataPurgeRequest(wa_phone_hash="short")
