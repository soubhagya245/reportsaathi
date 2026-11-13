# System Architecture Specification
## ReportSaathi: Plain-Language Medicine & Lab Report Explainer
*Document Version: 1.0 — Architecture & Technology Design*  
*Derived from `docs/01-problem.md` through `docs/05-prd.md`*

---

## 1. Architectural Philosophy & Principles

1. **Deterministic Core, Constrained Periphery:** Medical calculations (normal vs. abnormal lab values), drug identity resolution, and safety gates must be **100% deterministic code**. AI models are never permitted to touch numbers, diagnose conditions, or determine clinical significance.
2. **Free & Open-Source Software (FOSS) First:** Every component in the architecture utilizes open-source software, permissive community models, or zero-cost developer tiers.
3. **Extreme Simplicity & Edge-Viability:** The system must be deployable on minimal infrastructure (a single low-cost virtual private server or local edge container) without distributed microservice complexity.
4. **Transient & Privacy-Preserving:** Patient images and raw extracted parameters exist only in memory during the request lifecycle. No persistent patient electronic health records (EHR) are maintained.

---

## 2. Deterministic vs. AI Model Responsibility Matrix

To prevent hallucinations, regulatory breach (CDSCO SaMD), and clinical harm, the boundaries between deterministic software logic and AI are strictly enforced:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          INCOMING USER INPUT                           │
│                 (Text: Drug Name  OR  Image: Lab Report)               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DETERMINISTIC CODE (Python / Regex)                  │
│ • Fuzzy string matching on Indian drug brand names                     │
│ • Image pre-processing (OpenCV: binarize, deskew, contrast)            │
│ • Text extraction routing                                              │
│ • Handwriting detection heuristics                                     │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
      [Image File]  ▼                                ▼  [Medicine Text]
┌───────────────────────────────┐  ┌─────────────────────────────────────┐
│    OPEN-SOURCE OCR ENGINE     │  │   CLINICIAN-REVIEWED CARD ENGINE    │
│  (Tesseract OCR / EasyOCR)    │  │ • Exact match in verified SQLite DB │
│  • Reads printed tabular data │  │ • Formats pre-written Kannada cards │
│  • Extracts Value, Unit, Range│  │ • Inserts named clinician metadata  │
└───────────────┬───────────────┘  └─────────────────┬───────────────────┘
                │                                    │
                ▼                                    │
┌───────────────────────────────────────────────┐    │
│       DETERMINISTIC VERIFICATION & GATING     │    │
│ 1. User Confirmation UX (WhatsApp interactive)│    │
│ 2. Mathematical Range Comparison:             │    │
│    is_low  = value < range_min                │    │
│    is_high = value > range_max                │    │
│ 3. Critical-Alert Table Lookup:               │    │
│    IF value in CRITICAL_TABLE -> TRIGGER W8   │    │
│    (HALT ALL AI PIPELINES IMMEDIATELY)        │    │
└───────────────┬───────────────────────────────┘    │
                │                                    │
                ▼                                    │
┌───────────────────────────────────────────────┐    │
│     AI MODEL (OPTIONAL / STRICTLY BOUNDED)    │    │
│ • Input: ONLY normalized parameters + status  │    │
│   e.g. {"test": "TSH", "status": "HIGH"}      │    │
│ • Task: Synthesize friendly Kannada phrasing  │    │
│   adhering to strict system prompt guardrails │    │
│ • Fallback: Rule-based template (zero AI)     │    │
└───────────────┬───────────────────────────────┘    │
                │                                    │
                └─────────────────┬──────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 DETERMINISTIC COMPLIANCE POST-FILTER                   │
│ • Regex assertion: Disallow any diagnostic phrasing or therapy words  │
│ • Append mandatory doctor-question bullets (F4.1)                     │
│ • Append mandatory legal disclaimer & review date (F5.1, F5.2)         │
│ • Generate audio file via Kannada TTS (Indic-TTS / gTTS)               │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       OUTGOING WHATSAPP MESSAGE                        │
└────────────────────────────────────────────────────────────────────────┘
```

| Pipeline Step | Mechanism | Justification |
|---|---|---|
| **Drug Name Resolution** | **Deterministic** (Levenshtein fuzzy matching) | Zero risk of LLM inventing non-existent drug compositions. |
| **Lab Value Extraction** | **Deterministic Code + OCR** (Tesseract / EasyOCR) | Bounded pattern matching (`Regex`: `(\d+(\.\d+)?)\s*(mg/dL|g/dL|mEq/L|%)`). |
| **Normal vs. Abnormal** | **Deterministic** (`val < min` / `val > max`) | Arithmetic cannot be left to probabilistic neural networks. |
| **Critical Escalation** | **Deterministic** (Static Python Dictionary) | Safety-critical; must execute in 0 milliseconds without network dependence. |
| **Explanation Assembly** | **Template-First / AI Constrained** | Deterministic string templates for Stage 1. Small LLM only for Kannada linguistic smoothing in Stage 2. |
| **Doctor Questions** | **Deterministic** (Database Lookup per Drug/Test) | Clinically verified questions linked to specific conditions. |
| **Safety Disclaimers** | **Deterministic** (Hardcoded constants) | Legal immunity requires immutable compliance text. |

---

## 3. Technology Stack Comparison & Recommendation

We evaluate two distinct, fully open-source technology stacks suitable for low-cost execution:

### 3.1 Stack Comparison

| Component | Option 1: Python-Centric (FastAPI + Tesseract + SQLite) | Option 2: Node.js-Centric (TypeScript + Express + Tesseract.js) |
|---|---|---|
| **Core Backend** | Python 3.11 + FastAPI (Async, Pydantic validation) | Node.js 20 LTS + Express / Fastify (TypeScript) |
| **Database** | SQLite3 (WAL mode enabled) + SQLModel / SQLAlchemy | SQLite3 + Prisma ORM |
| **OCR Engine** | Native C++ `tesseract-ocr` via `pytesseract` + `OpenCV` | `tesseract.js` (WebAssembly port) |
| **Indic NLP & Script** | `indic-nlp-library` + `AI4Bharat` tools natively in Python | Limited; requires calling external Python scripts or basic JS regex |
| **Audio / TTS** | `gTTS` / `piper-tts` (offline Indic support) | External API calls or heavy WebAudio wrappers |
| **WhatsApp Gateway** | Meta WhatsApp Cloud API (Free tier) OR `wppconnect`/`baileys` sidecar | Native integration with `@whiskeysockets/baileys` library |
| **Memory Footprint** | ~250 MB base RAM | ~180 MB base RAM |
| **Developer Ergonomics** | Exceptional for data manipulation, image processing, and scientific units | Good for async I/O and JSON streaming |

### 3.2 Recommended Stack: Option 1 (Python-Centric with FastAPI)

**Rationale:**
1. **Computer Vision & OCR Superiority:** Image parsing of low-quality lab photos taken on budget smartphones requires pre-processing (grayscale thresholding, deskewing, noise reduction). Python’s `OpenCV` (`cv2`) and native `tesseract-ocr` are significantly faster and more accurate than JavaScript WebAssembly ports.
2. **Indic Language Ecosystem:** The open-source Indian language ecosystem (IIT Madras AI4Bharat, Bhashini, Indic-NLP) is written exclusively in Python.
3. **Strict Schema Integrity:** FastAPI with Pydantic v2 guarantees strict type safety on medical values, preventing string-to-float conversion bugs in reference ranges.

---

## 4. System Architecture & Components

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLIENT ACCESS SURFACES                          │
│                                                                        │
│   [ Patient WhatsApp (Android/KaiOS) ]    [ Mobile Browser Web Card ] │
└───────────────────┬───────────────────────────────────┬────────────────┘
                    │                                   │
                    ▼ HTTPS Webhook                     ▼ HTTPS
┌────────────────────────────────────────────────────────────────────────┐
│                     REVERSE PROXY & GATEWAY (Caddy)                    │
│   • Auto-HTTPS (Let's Encrypt)       • Rate Limiting (10 req/min/IP)   │
│   • Static file caching              • IP filtering                    │
└───────────────────┬────────────────────────────────────────────────────┘
                    │
                    ▼ HTTP (Port 8000)
┌────────────────────────────────────────────────────────────────────────┐
│                    APPLICATION BACKEND (FastAPI)                       │
│                                                                        │
│  ┌───────────────────────┐ ┌────────────────────────────────────────┐  │
│  │  Webhook Router       │ │  Session State Machine                 │  │
│  │  (/api/v1/whatsapp)   │ │  (In-Memory / SQLite Session Store)    │  │
│  └───────────┬───────────┘ └───────────────────┬────────────────────┘  │
│              │                                 │                       │
│              ▼                                 ▼                       │
│  ┌───────────────────────┐ ┌────────────────────────────────────────┐  │
│  │ Medicine Query Engine │ │  Lab Parser & Verification Engine      │  │
│  │ • Levenshtein Search  │ │  • OpenCV Image Pipeline               │  │
│  │ • Generic/Brand Map   │ │  • Tesseract OCR Worker (Celery/Async) │  │
│  └───────────┬───────────┘ └───────────────────┬────────────────────┘  │
│              │                                 │                       │
│              ▼                                 ▼                       │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Safety Filter & Range Gate (Deterministic Table Lookup)          │  │
│  └───────────────────────────┬──────────────────────────────────────┘  │
│                              │                                         │
│                              ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Audio Synthesizer (Local piper-tts / gTTS - Kannada kn-IN)       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────┬────────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     LOCAL STORAGE ENGINE (SQLite)                      │
│   • cards.db (Clinician-reviewed medicine & test cards - Read Only)    │
│   • audit.db (Anonymized error logs & consent timestamps)              │
│   • /tmp/scratch/ (Transient image cache - Cron auto-purge 10 mins)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Model & Schema Specifications

The system utilizes **SQLite3** in WAL (Write-Ahead Logging) mode. Medical content is stored as immutable, version-controlled records.

### 5.1 Database Schema (DDL)

```sql
-- 1. Clinician Verified Medicine Repository
CREATE TABLE medicines (
    id TEXT PRIMARY KEY,                       -- e.g. "med_metformin_500"
    generic_name TEXT NOT NULL,               -- e.g. "Metformin Hydrochloride"
    brand_names_json TEXT NOT NULL,           -- JSON array: ["Glycomet", "Glucophage", "Obimet"]
    therapeutic_category TEXT NOT NULL,       -- e.g. "Blood Glucose Regulator"
    
    -- Bilingual Explanations (Kannada & English)
    purpose_kn TEXT NOT NULL,                 -- ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ನಿಯಂತ್ರಿಸಲು
    purpose_en TEXT NOT NULL,
    how_to_take_kn TEXT NOT NULL,             -- ಊಟದ ಜೊತೆ ಅಥವಾ ನಂತರ
    how_to_take_en TEXT NOT NULL,
    side_effects_mild_kn TEXT NOT NULL,       -- ಹೊಟ್ಟೆ ನೋವು, ವಾಕರಿಕೆ
    side_effects_mild_en TEXT NOT NULL,
    red_flags_kn TEXT NOT NULL,               -- ತೀವ್ರ ಹೊಟ್ಟೆ ನೋವು, ಉಸಿರಾಟ ತೊಂದರೆ
    red_flags_en TEXT NOT NULL,
    dont_stop_warning_kn TEXT NOT NULL,       -- ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ನಿಲ್ಲಿಸಬೇಡಿ
    dont_stop_warning_en TEXT NOT NULL,
    
    -- Doctor Questions (JSON arrays)
    doctor_questions_kn TEXT NOT NULL,        -- JSON array of 3 questions
    doctor_questions_en TEXT NOT NULL,
    
    -- Clinical Governance Metadata
    reviewed_by_clinician_name TEXT NOT NULL, -- e.g. "Dr. Ramesh K., MBBS, MD"
    clinician_reg_number TEXT NOT NULL,       -- KMC Reg: 45291
    version_tag TEXT NOT NULL,                -- "v1.2.2026"
    reviewed_at TIMESTAMP NOT NULL,
    next_review_due TIMESTAMP NOT NULL,
    is_active INTEGER DEFAULT 1
);

-- Index for instant brand/generic search
CREATE INDEX idx_medicines_generic ON medicines(generic_name);

-- 2. Standard Lab Test Definitions (Stage 2)
CREATE TABLE lab_tests (
    id TEXT PRIMARY KEY,                       -- e.g. "lab_fbs"
    standard_name TEXT NOT NULL,              -- e.g. "Fasting Blood Sugar"
    aliases_json TEXT NOT NULL,               -- JSON array: ["FBS", "Fasting Glucose", "Blood Sugar Fasting"]
    standard_unit TEXT NOT NULL,              -- "mg/dL"
    
    -- Adult Reference Bounds (Default fallback if lab's own range unreadable)
    default_ref_min REAL,                     -- 70.0
    default_ref_max REAL,                     -- 100.0
    
    -- Plain Language Explanation
    explanation_kn TEXT NOT NULL,             -- ದೇಹದಲ್ಲಿ ಖಾಲಿ ಹೊಟ್ಟೆಯಲ್ಲಿರುವ ಸಕ್ಕರೆಯ ಪ್ರಮಾಣ
    explanation_en TEXT NOT NULL,
    
    -- Questions for Doctor
    doctor_questions_kn TEXT NOT NULL,
    doctor_questions_en TEXT NOT NULL,
    
    -- Safety metadata
    reviewed_by TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 3. Hardcoded Critical Abnormality Escalation Table
CREATE TABLE critical_lab_thresholds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id TEXT NOT NULL,
    critical_low REAL,                        -- If value < critical_low -> TRIGGER W8
    critical_high REAL,                       -- If value > critical_high -> TRIGGER W8
    unit TEXT NOT NULL,
    escalation_message_kn TEXT NOT NULL,      -- ಇಂದೇ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ
    escalation_message_en TEXT NOT NULL,
    FOREIGN KEY(test_id) REFERENCES lab_tests(id)
);

-- Seed critical values (Sample)
-- Glucose < 50 mg/dL (Severe Hypoglycemia) OR > 400 mg/dL (Hyperglycemic Crisis)
-- Potassium < 2.5 mEq/L (Cardiac Arrhythmia risk) OR > 6.5 mEq/L

-- 4. Ephemeral User Sessions & DPDP Consent Records
CREATE TABLE user_sessions (
    wa_phone_hash TEXT PRIMARY KEY,           -- SHA-256 hash of user phone number (Never store raw phone)
    preferred_language TEXT DEFAULT 'kn',     -- 'kn' or 'en'
    consent_granted INTEGER DEFAULT 0,        -- 0 = No, 1 = Explicit Consent Given
    consent_timestamp TIMESTAMP,
    active_step TEXT DEFAULT 'MAIN_MENU',     -- 'MAIN_MENU', 'AWAITING_MED_NAME', 'AWAITING_REPORT_PHOTO', 'CONFIRM_OCR'
    pending_payload_json TEXT,                -- Temporary storage for OCR confirmation (auto-purged)
    last_interaction TIMESTAMP NOT NULL
);
```

---

## 6. API Route & Interface Specifications

### 6.1 WhatsApp Webhook Interface

#### `GET /api/v1/whatsapp/webhook`
* **Purpose:** Verification handshake for Meta WhatsApp Cloud API / webhook registration.
* **Query Parameters:** `hub.mode`, `hub.verify_token`, `hub.challenge`.
* **Behavior:** Returns `hub.challenge` if `hub.verify_token` matches `WHATSAPP_VERIFY_TOKEN`.

#### `POST /api/v1/whatsapp/webhook`
* **Purpose:** Ingests incoming messages, button clicks, and media from users.
* **Payload Structure:** Standard Meta WhatsApp Webhook JSON format.
* **Internal Routing:**
  1. Hashes user phone number: `user_hash = SHA256(From + SALT)`.
  2. Retrieves session from `user_sessions`.
  3. Evaluates commands (`"DELETE"` -> trigger immediate purge).
  4. Dispatches to matching handler:
     - `interactive.button_reply`: Handle language choice, consent agreement, OCR verification.
     - `text.body`: Match against medicine database via fuzzy search.
     - `image`: Check consent. If granted, download media to `/tmp/scratch/`, spawn async OCR worker.

### 6.2 Static Web Card Endpoint (Lightweight HTML)

#### `GET /c/{card_id}`
* **Purpose:** View static medicine card in browser (for QR codes on printed pharmacy cards or WhatsApp link shares).
* **Response:** Pre-rendered, semantic HTML5 page with zero external JS frameworks.
* **Headers:** `Cache-Control: public, max-age=86400` (Aggressively cached; static content).
* **Payload:** Sub-100KB HTML with embedded CSS and base64 SVG icons.

### 6.3 Health & Operations Endpoints

#### `GET /healthz`
* **Purpose:** System monitoring and container health check.
* **Response:** `200 OK` `{ "status": "healthy", "database": "connected", "tesseract": "available" }`.

---

## 7. Third-Party Services & Open-Source Tools Specification

All components are strictly free, open-source, or zero-cost:

| Capability | Tool / Library Selected | Cost / License | Operational Deployment |
|---|---|---|---|
| **Messaging Engine** | **Meta WhatsApp Cloud API (Free Tier)** *(Primary)*<br>OR **Baileys (Open-Source WS)** *(Alternative)* | Free (1,000 service convos/mo free) / MPL-2.0 | Hosted webhook listener on FastAPI. Baileys runs as Node.js sidecar if zero-Meta path chosen. |
| **Optical Character Recognition (OCR)** | **Tesseract OCR v5.3+** with `tessdata_fast` (`kan` + `eng` language models) | Open Source (Apache 2.0) | Installed at OS level on the container. Invoked via `pytesseract`. |
| **Image Pre-processing** | **OpenCV (cv2 headless)** | Open Source (Apache 2.0) | Deskewing, adaptive Otsu thresholding for printed thermal lab paper. |
| **Kannada Text-to-Speech (TTS)** | **piper-tts** (offline lightweight neural TTS) OR **gTTS** (Google TTS Python) | Open Source (MIT) / Free Python wrapper | Pre-generates cached `.ogg` voice notes for the 10 starter cards. Zero runtime latency. |
| **LLM / Linguistic Smoothing (Stage 2 only)** | **Rule-based templating (0% AI)** *(Default)*<br>OR **Ollama + Llama-3.2-3B / IndicLLM** *(Optional)* | 100% Free / Open Weights | Run locally on VPS CPU or zero-cost Hugging Face Inference API. Templating preferred for zero cost. |
| **Reverse Proxy** | **Caddy v2** | Open Source (Apache 2.0) | Automates Let's Encrypt TLS certificates, enforces rate limits and gzip/brotli compression. |
| **Maps / Geolocation** | **None (Excluded)** | N/A | Excluded to preserve privacy and minimize scope. Users directed to their existing doctor. |

---

## 8. Deployment, Hosting & Infrastructure Architecture

### 8.1 Single-Node Minimal Deployment (Docker Compose)

The entire architecture is containerized and deployable on a single \$5/month virtual server (e.g., Hetzner, DigitalOcean, or an existing on-premises hospital PC):

```yaml
version: '3.8'

services:
  caddy:
    image: caddy:2-alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    environment:
      - APP_ENV=production
      - DB_PATH=/app/data/reportsaathi.db
      - SCRATCH_DIR=/tmp/scratch
      - WHATSAPP_TOKEN=${WHATSAPP_TOKEN}
      - WHATSAPP_PHONE_ID=${WHATSAPP_PHONE_ID}
      - WHATSAPP_VERIFY_TOKEN=${WHATSAPP_VERIFY_TOKEN}
      - DATA_SALT=${DATA_SALT}
    volumes:
      - app_data:/app/data
      - scratch_data:/tmp/scratch
    tmpfs:
      - /tmp/scratch:size=100M,uid=1000

volumes:
  caddy_data:
  caddy_config:
  app_data:
  scratch_data:
```

### 8.2 Ephemeral Storage & Data Retention Daemon
A lightweight Linux cron task runs every 5 minutes inside the container:
```bash
# Delete all uploaded patient images older than 10 minutes
find /tmp/scratch -type f -mmin +10 -delete
```

---

## 9. Environment Variables & Configuration

| Variable | Description | Example / Default | Mandatory? |
|---|---|---|---|
| `APP_ENV` | Application environment | `production` / `development` | Yes |
| `PORT` | Internal HTTP listening port | `8000` | Yes |
| `DB_PATH` | Absolute path to SQLite database file | `/app/data/reportsaathi.db` | Yes |
| `SCRATCH_DIR` | Directory for transient image processing | `/tmp/scratch` | Yes |
| `DATA_SALT` | Cryptographic salt for hashing phone numbers | `s9f82k3j!_salt_reportsaathi_2026` | Yes |
| `WHATSAPP_TOKEN` | Meta WhatsApp Cloud API permanent bearer token | `EAAx...` | Yes (for Meta Cloud) |
| `WHATSAPP_PHONE_ID` | Meta WhatsApp Business registered Phone Number ID | `1048291048123` | Yes (for Meta Cloud) |
| `WHATSAPP_VERIFY_TOKEN` | Custom webhook challenge verification string | `rep_saathi_verify_secure_token` | Yes |
| `MAX_UPLOAD_SIZE_MB` | Maximum permitted file upload size | `5` | Yes |
| `ENABLE_AI_SMOOTHING` | Toggle whether to use LLM smoothing or pure templates | `false` (default: pure templates) | Yes |
| `LOCAL_TTS_ENGINE` | Audio generation backend | `piper` / `gtts` | Yes |

---

## 10. Open Architectural & Technical Questions

Rather than assuming unverified operational parameters, the following questions are flagged for resolution during Stage 1 pilot testing:

1. **Meta WhatsApp API Approval vs. Baileys Risk:**
   * *Question:* Will Meta’s Cloud API approve a health-related informational bot without requiring a Registered Commercial Pharmacy license?
   * *Implication:* If Meta rejects the template messages during review, the project must pivot to an open-source WhatsApp Web bridge (`Baileys` / `WPPConnect`). However, `Baileys` carries a non-zero risk of WhatsApp phone number banning if message velocity exceeds anti-spam limits.
2. **Kannada OCR Accuracy on Thermal Printouts:**
   * *Question:* What is the real-world character error rate (CER) of Tesseract OCR on degraded thermal paper receipts from Tier-2 Karnataka diagnostic labs?
   * *Implication:* If OCR accuracy on numerical ranges is below 90%, the confirmation UX must require the user to manually verify both the test value and the reference numbers before any explanation is presented.
3. **Audio Pre-generation vs. Dynamic Voice Synthesis:**
   * *Question:* Is it better to pre-record professional human Kannada voice notes for the 10 starter cards, or generate them via synthetic TTS?
   * *Implication:* Human voice recordings in authentic regional dialects (e.g., North Karnataka vs. Old Mysore Kannada) elicit significantly higher trust among 60+ adults than synthetic robotic TTS, but do not scale to Stage 2 lab reports.
4. **Offline Pharmacy Terminal Alternative:**
   * *Question:* If patients lack active 4G data packs at the pharmacy counter, can the system deploy as an offline static QR code linking to pre-cached content via the chemist’s local Wi-Fi?

---
*End of Architecture Specification. Next: Detailed Safety Rules & Guardrails (docs/06b-safety-rules.md).*
