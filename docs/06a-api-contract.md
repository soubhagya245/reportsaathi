# API Contract & Schema Specification
## ReportSaathi: REST & Webhook Interfaces
*Document Version: 1.0 — Stage 1 & Stage 2 API Contracts*  
*Derived from `docs/05-prd.md`, `docs/06-architecture.md`, and `docs/06b-safety-rules.md`*

---

## 1. Overview & Conventions

All endpoints adhere to standard REST and JSON conventions over HTTPS (TLS 1.3).
- **Base URL:** `https://api.reportsaathi.in/api/v1`
- **Authentication:** Webhook signatures via HMAC-SHA256 (`X-Hub-Signature-256`), Internal Service JWTs where applicable.
- **Data Minimization:** Raw phone numbers are never stored or accepted in request bodies; only ephemeral webhook payloads containing user communication IDs are handled.

---

## 2. API Endpoints

### 2.1 WhatsApp Cloud API Webhook Handshake
* **Path:** `GET /whatsapp/webhook`
* **Query Parameters:**
  * `hub.mode` (string, required): Must equal `"subscribe"`
  * `hub.verify_token` (string, required): Pre-shared secret token
  * `hub.challenge` (string, required): Challenge string to echo back
* **Responses:**
  * `200 OK`: Returns the raw `hub.challenge` string
  * `403 Forbidden`: If `hub.verify_token` does not match

### 2.2 WhatsApp Cloud API Inbound Webhook Event
* **Path:** `POST /whatsapp/webhook`
* **Headers:** `X-Hub-Signature-256: sha256=<signature>`
* **Request Schema (Meta Webhook Envelope):**
```json
{
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
              "phone_number_id": "1048291048123"
            },
            "contacts": [
              {
                "profile": { "name": "Appaji" },
                "wa_id": "9198XXXXXXXX"
              }
            ],
            "messages": [
              {
                "from": "9198XXXXXXXX",
                "id": "wamid.HBgMOTE5...",
                "timestamp": "1731485640",
                "type": "text",
                "text": { "body": "Glycomet 500" }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```
* **Supported `type` Payloads:**
  * `text`: Body containing medicine name, command ("MENU", "DELETE", "ಕನ್ನಡ").
  * `interactive`: Button reply payload (`id`: `btn_lang_kn`, `btn_consent_yes`, `btn_confirm_ocr`).
  * `image`: Photo of lab report (contains `id`, `mime_type`, `sha256`).

### 2.3 Medicine Card Lookup API
* **Path:** `GET /medicines/lookup`
* **Query Parameters:**
  * `q` (string, required): Drug trade name or generic name (e.g., `Glycomet`, `Metformin`, `ಥೈರೋನಾರ್ಮ್`)
  * `lang` (string, optional, default: `kn`): `kn` or `en`
* **Responses:**
  * `200 OK`:
  ```json
  {
    "status": "success",
    "data": {
      "id": "med_metformin",
      "generic_name": "Metformin",
      "brand_aliases": ["Glycomet", "Glucophage", "Obimet", "Glyciphage"],
      "therapeutic_class": "Biguanide / Antidiabetic",
      "purpose": {
        "kn": "ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ನಿಯಂತ್ರಿಸಲು.",
        "en": "To help control blood sugar levels."
      },
      "how_to_take": {
        "kn": "ಊಟದ ಜೊತೆ ಅಥವಾ ತಕ್ಷಣ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ.",
        "en": "Take with or right after food."
      },
      "common_side_effects": {
        "kn": "ಹೊಟ್ಟೆ ನೋವು, ವಾಕರಿಕೆ — ಸಾಮಾನ್ಯವಾಗಿ 1-2 ವಾರಗಳಲ್ಲಿ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
        "en": "Mild nausea or loose motion; usually settles in 1-2 weeks."
      },
      "red_flags": {
        "kn": ["ತೀವ್ರ ನಿಶ್ಯಕ್ತಿ ಅಥವಾ ವಿಪರೀತ ಹೊಟ್ಟೆ ನೋವು", "ಉಸಿರಾಟದಲ್ಲಿ ತೊಂದರೆ"],
        "en": ["Severe fatigue or abdominal pain", "Difficulty breathing"]
      },
      "caution_do_not_stop": {
        "kn": "ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಈ ಮಾತ್ರೆ ನಿಲ್ಲಿಸಬೇಡಿ.",
        "en": "Do not stop this medicine without consulting your doctor."
      },
      "doctor_questions": {
        "kn": [
          "ಈ ಮಾತ್ರೆ ಎಷ್ಟು ದಿನ ಮುಂದುವರಿಸಬೇಕು?",
          "ಮಾತ್ರೆ ತೆಗೆದುಕೊಳ್ಳುವುದು ಮರೆತರೆ ಏನು ಮಾಡಬೇಕು?"
        ],
        "en": [
          "For how many months should I continue this medicine?",
          "What should I do if I miss a dose?"
        ]
      },
      "governance": {
        "reviewed_by": "Dr. Anita Rao, MBBS, MD",
        "clinician_reg_no": "KMC-45291",
        "reviewed_at": "2026-11-01T00:00:00Z",
        "disclaimer_en": "Notice: Information only, not medical advice. Drug-drug interactions not checked."
      }
    }
  }
  ```
  * `404 Not Found`:
  ```json
  {
    "status": "not_found",
    "message": "Medicine not found in catalog",
    "fallback_action": "PHARMACIST_FALLBACK"
  }
  ```

### 2.4 Lab Report Processing API (Stage 2)
* **Path:** `POST /lab-reports/ocr-extract`
* **Content-Type:** `multipart/form-data`
* **Request:** `file` (image/jpeg, image/png, application/pdf, max 5MB), `consent_token` (string, required)
* **Responses:**
  * `200 OK`:
  ```json
  {
    "status": "success",
    "document_type": "PRINTED_LAB_REPORT",
    "confidence_score": 0.94,
    "extracted_parameters": [
      {
        "test_id": "lab_fbs",
        "name": "Fasting Blood Sugar (FBS)",
        "found_value": 168.0,
        "unit": "mg/dL",
        "lab_printed_range": { "min": 70.0, "max": 100.0 },
        "status": "ABOVE_RANGE",
        "is_critical": false
      },
      {
        "test_id": "lab_potassium",
        "name": "Serum Potassium",
        "found_value": 6.4,
        "unit": "mEq/L",
        "lab_printed_range": { "min": 3.5, "max": 5.0 },
        "status": "ABOVE_RANGE",
        "is_critical": true,
        "critical_escalation_message": "Consult a doctor today immediately."
      }
    ]
  }
  ```
  * `422 Unprocessable Entity` (Handwriting Detected / Blurry):
  ```json
  {
    "status": "rejected",
    "code": "HANDWRITING_OR_ILLEGIBLE_DETECTED",
    "message": "Cannot parse handwritten prescriptions reliably. Please consult your local pharmacist."
  }
  ```

### 2.5 Ephemeral Data Purge API (DPDP Erasure)
* **Path:** `POST /user/erase`
* **Request Body:**
```json
{
  "wa_phone_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```
* **Responses:**
  * `200 OK`: `{ "status": "purged", "purged_records": ["sessions", "scratch_files", "cache"] }`

---
*End of API Contract Specification.*
