# Product Requirements Document (PRD)
## ReportSaathi: Plain-Language Medicine & Lab Report Explainer (Kannada-First)
*Document Version: 1.0 — Stage 1 & Stage 2 Scope*  
*Derived from `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`, and `docs/04-design.md`*

---

## 1. Product Overview & Purpose

**ReportSaathi** is a regional-language patient empowerment tool designed for chronic illness patients (and their family caregivers) in India, beginning with Kannada speakers in Karnataka. It bridges the critical communication gap left by short outpatient department (OPD) visits (<10 minutes) and English-only diagnostic/pharmaceutical materials. 

The product explains **why** patients take specific chronic medications, clarifies **what** standard lab values mean relative to the laboratory's printed reference ranges, generates **actionable questions for their doctor**, and provides **audio playback** for elderly and low-literacy users.

It operates strictly as an **educational and informational aid**. It never diagnoses, never prescribes, and never alters medical treatments.

---

## 2. Goals & Non-Goals

### 2.1 Goals
1. **Explain Purpose & Administration:** Help Kannada-speaking patients understand the plain-language purpose, proper intake timing, common side effects, and warning signs for their chronic medications (Hypertension, Type 2 Diabetes, Thyroid disorders).
2. **Contextualize Lab Results (Stage 2):** Parse printed lab reports deterministically and explain whether results fall within or outside the lab’s printed normal range, without diagnostic labeling.
3. **Empower Doctor Visits:** Equip patients with 1–3 specific, relevant questions to ask their Registered Medical Practitioner (RMP) at their next consultation.
4. **Accessible to Elderly & Low-Cost Hardware:** Deliver the experience via familiar channels (WhatsApp Business and lightweight responsive web cards) with high-contrast text, 18sp+ typography in Noto Sans Kannada, and clear Kannada audio playback.
5. **Zero Regulatory Ambiguity (SaMD Safe Harbor):** Maintain strict boundaries as an educational tool to remain outside CDSCO Medical Device Rules (MDR 2017) and Telemedicine Practice Guidelines restrictions.
6. **Privacy-by-Design:** Adhere strictly to the Digital Personal Data Protection (DPDP) Act 2023 with unbundled consent, zero secondary data monetization, and transient data storage.

### 2.2 Non-Goals
1. **No Medical Diagnosis:** The product will never infer, predict, or state a clinical diagnosis (e.g., it will state "Your fasting blood sugar of 165 mg/dL is above your lab's reference range (70–100 mg/dL)", never "You have diabetes").
2. **No Treatment or Dose Modification:** The product will never recommend altering dosages, skipping doses, substituting brands, or stopping medications.
3. **No Unlicensed Drug Interaction Claims:** The product will not evaluate multi-drug combinations or declare them "safe" or "unsafe" unless an accredited, licensed Indian clinical drug-interaction database is integrated in future stages.
4. **No Telemedicine or Prescriptions:** The product will not issue prescriptions, connect to on-demand teleconsultations, or replace an RMP.
5. **No Handwritten Prescription Deciphering:** The product will explicitly reject unreadable handwritten scripts and redirect the user to their local pharmacist.
6. **No Health Data Monetization:** Patient reports, phone numbers, and queries will never be sold to diagnostic labs, pharmaceutical advertisers, or insurance brokers.

---

## 3. User Personas & User Stories

### 3.1 User Personas
* **Primary Patient: "Appaji" (Age 64, Retired, Belagavi/Bengaluru).** Speaks and reads Kannada; struggles with small English text on medicine strips; has hypertension and diabetes; carries printed lab reports in plastic bags; uses WhatsApp daily for voice notes and family messages.
* **Family Caregiver: "Soumya" (Age 32, Tech Professional, Bengaluru).** Manages her aging father’s doctor visits; receives lab PDF reports on WhatsApp; needs a safe, trustworthy explanation in Kannada so her parents understand why they are taking each pill.
* **Community Pharmacist: "Manjunath" (Age 41, Retail Chemist, Hubballi).** Dispenses 150+ prescriptions daily; lacks time to explain mechanisms of action to elderly patients; desires printed, clinician-verified reference cards to hand out.

### 3.2 User Stories

#### Epic 1: Medicine Explanation (Stage 1 MVP)
* **US-1.1 (Medicine Lookup):** As a patient or caregiver, I want to send a common brand or generic medicine name (e.g., "Glycomet" or "Metformin") via WhatsApp, so that I immediately receive a verified plain-language card explaining what it is for.
* **US-1.2 (Clear Administration Instructions):** As a patient, I want to know whether to take my medicine before or after meals in simple Kannada, so that I take it correctly and avoid stomach upset.
* **US-1.3 (Side Effect Reassurance):** As an anxious patient, I want to know which mild side effects are normal during the first week, so that I do not panic and stop taking my pill prematurely.
* **US-1.4 (Red-Flag Symptoms):** As an elderly patient, I want clear bullet points of severe symptoms that require immediate medical attention, so that I know when to visit an emergency clinic.
* **US-1.5 (Doctor Consultation Questions):** As a patient, I want 1–3 specific questions at the bottom of the card, so that I know what to ask my doctor during my 5-minute consultation.
* **US-1.6 (Audio Playback):** As an older user with failing eyesight, I want to tap an audio button to hear the card read out in clear, natural Kannada voice, so that I do not have to strain to read small text.

#### Epic 2: Lab Report Comprehension (Stage 2 MVP)
* **US-2.1 (Printed Report Upload):** As a caregiver, I want to photograph a printed lab report (e.g., Lipid Profile or HbA1c) and send it to the WhatsApp bot, so that my parents can understand the numbers.
* **US-2.2 (Verification & Confirmation):** As a user, I want the bot to show me the extracted test name, extracted number, and printed reference range to confirm before explaining, so that OCR errors do not mislead me.
* **US-2.3 (Critical Value Alert):** As a patient whose lab value is dangerously abnormal, I want to receive an immediate, calm alert advising me to see a doctor today, rather than an automated explanation that delays urgent care.
* **US-2.4 (Illegible/Handwritten Fallback):** As a user who uploads a handwritten doctor's note or blurry photo, I want the system to honestly tell me it cannot read it reliably and advise me to ask a pharmacist, rather than guessing.

#### Epic 3: Safety & Governance
* **US-3.1 (Clinician Accountability):** As a patient, I want to see the name and registration number of the verifying doctor and the review date on every card, so that I know the information is medically vetted and current.
* **US-3.2 (Data Consent & Erasure):** As a privacy-conscious user, I want to give explicit consent before sending health documents and have the ability to delete my history by texting "DELETE", so that my medical records remain private.

---

## 4. Functional Requirements

### 4.1 Medicine Information & Card Engine (Stage 1 & Stage 2)

| Req ID | Requirement Description | Stage | Deterministic vs AI |
|---|---|---|---|
| **FR-1** | **Drug Name Matching:** System must accept text queries matching generic drug names (e.g., Metformin, Amlodipine, Levothyroxine) and common Indian trade brand names (e.g., Glycomet, Telma, Thyronorm, Eltroxin) via exact and fuzzy string matching. | MVP-1 | Deterministic Code |
| **FR-2** | **Clinician-Reviewed Card Repository:** System must store static, pre-approved JSON cards written by registered doctors/pharmacists covering the 10 most common chronic drugs. | MVP-1 | Deterministic Code |
| **FR-3** | **Structured Card Layout:** Every medicine card must contain 7 mandatory sections in fixed order: (1) Drug identity + aliases, (2) Why you take it (Purpose), (3) How to take it (Timing/food), (4) Common mild side effects, (5) Red-flag symptoms (See doctor now), (6) "Do not stop without doctor" warning, (7) 1–3 doctor questions. | MVP-1 | Deterministic Code |
| **FR-4** | **Bilingual Output:** All text cards must render in natural Kannada first, accompanied by English translations in parentheses or bilingual toggles. | MVP-1 | Deterministic Code |
| **FR-5** | **Mandatory Legal & Clinical Footer:** Every card must output: "ℹ️ Information only, not medical advice. Reviewed by Dr. [Name], [Date]. Drug interactions not checked." | MVP-1 | Deterministic Code |
| **FR-6** | **Audio Voice Note Generation:** System must provide an audio file (.ogg/.mp3) reading the verified Kannada card text aloud upon user button click. | MVP-2 | Deterministic (Pre-recorded) / AI TTS |
| **FR-7** | **Missed Query Logging:** If a medicine query fails to match the database, system must output Screen W5 (Pharmacist fallback) and log the query for clinician backlog. | MVP-1 | Deterministic Code |

### 4.2 Lab Report Processing Engine (Stage 2)

| Req ID | Requirement Description | Stage | Deterministic vs AI |
|---|---|---|---|
| **FR-8** | **Printed Document Ingestion:** Accept user image uploads (.jpg, .png, .pdf) of printed diagnostic test reports via WhatsApp. | MVP-2 | Deterministic Code |
| **FR-9** | **Handwriting Detection & Rejection:** System must analyze image input. If identified as a handwritten prescription or cursive clinic note, reject processing and respond: *"I cannot read handwritten notes reliably. Please ask your local pharmacist."* | MVP-2 | Deterministic / Heuristic Code |
| **FR-10** | **OCR Parsing:** Extract test names, numerical patient values, units (mg/dL, %, etc.), and the lab's printed reference range. | MVP-2 | Code + Open-Source OCR Engine |
| **FR-11** | **User Confirmation Step:** Before generating any explanation, display extracted values back to user: *"We detected: Fasting Blood Sugar = 145 mg/dL (Reference Range: 70–100 mg/dL). Is this correct? [Yes] [No]"*. | MVP-2 | Deterministic Code |
| **FR-12** | **Deterministic Range Comparison:** Normal/Abnormal status must be calculated solely by mathematical comparison (`value < min`, `value > max`, `min <= value <= max`) against the lab's printed range. Never use an LLM to determine if a number is in-range. | MVP-2 | Deterministic Code |
| **FR-13** | **Critical-Result Escalation Gate:** System must match extracted values against a hardcoded, clinician-defined Critical Abnormality Table (e.g., Blood Glucose < 50 mg/dL or > 400 mg/dL; Potassium < 2.5 or > 6.5 mEq/L). If triggered, halt standard explanation and deliver Screen W8: *"🚨 See a doctor today."* | MVP-2 | Deterministic Code |
| **FR-14** | **Plain-Language Explanation Framing:** An AI model may be used *only* to assemble conversational Kannada explanations adhering to strict prompt templates, using only the code-verified range status. It must never add unsolicited medical diagnoses. | MVP-2 | Constrained AI / Template Engine |

### 4.3 WhatsApp Channel & User Management

| Req ID | Requirement Description | Stage | Deterministic vs AI |
|---|---|---|---|
| **FR-15** | **Consent Architecture (DPDP):** Before ingesting any lab photo or health history, display unbundled consent notice (Screen W7). User must tap "[✅ I Agree]" before processing begins. | MVP-1/2 | Deterministic Code |
| **FR-16** | **Session State Machine:** Maintain user state across 3 conversation steps: Language Selection → Mode Selection (Medicine vs Report) → Card Delivery. Reset session after 15 minutes of inactivity. | MVP-1 | Deterministic Code |
| **FR-17** | **Interactive UI Controls:** WhatsApp messages must utilize native Interactive Reply Buttons (up to 3 options) and List Menus to minimize typing for elderly users. | MVP-1 | Deterministic Code |
| **FR-18** | **Data Erasure Command:** When user texts "DELETE" or "ಅಳಿಸು", immediately purge all associated chat logs, uploaded images, and session tokens from storage. | MVP-1 | Deterministic Code |

---

## 5. Non-Functional Requirements (NFRs)

### 5.1 Performance & Responsiveness
* **NFR-1 (Lookup Latency):** Static medicine card lookups on WhatsApp must deliver the reply message within **2.0 seconds** over 3G/4G connections.
* **NFR-2 (OCR & Processing Latency):** Stage 2 lab report image extraction, confirmation prompt, and explanation must complete within **8.0 seconds**.
* **NFR-3 (Audio Latency):** Kannada voice note delivery must initiate playback within **3.0 seconds** of user tap.

### 5.2 Accessibility & Usability (Older Adults & Low-Cost Hardware)
* **NFR-4 (Typography Standards):** Web surfaces must enforce a minimum font size of **18sp / 18px** for body text and **1.5× line-height** for Kannada scripts (Noto Sans Kannada).
* **NFR-5 (Touch Targets):** All clickable web buttons must have a minimum touch bounding box of **48 × 48 dp**.
* **NFR-6 (Color Contrast):** All text-to-background combinations must meet or exceed **WCAG 2.2 Level AA** (minimum 4.5:1 for body text, 3:1 for large headers).
* **NFR-7 (Lightweight Payload):** Static web cards must have a total asset bundle size under **150 KB** (zero client-side JavaScript frameworks; pure semantic HTML/CSS).

### 5.3 Reliability & Availability
* **NFR-8 (Uptime):** Backend service must achieve **99.5% uptime** during operational hours (07:00 to 22:00 IST).
* **NFR-9 (Graceful Degradation):** Under network timeouts or API service disruptions, the system must trigger Screen W6 within 5 seconds with a fallback suggestion to speak with a pharmacist.

### 5.4 Privacy, Security & Legal Compliance
* **NFR-10 (DPDP Act 2023 Compliance):** No personal identifiable health data (prescriptions, test results) shall be stored long-term. Uploaded photos must be processed in RAM or transient scratch storage and deleted within **10 minutes** of processing.
* **NFR-11 (Data Localization & Encryption):** All user data in transit must use **TLS 1.3**. All persistent configuration and cached logs must be stored within Indian geographic jurisdiction (e.g., AWS/GCP/MeitY-empanelled India regions).
* **NFR-12 (No Third-Party AI Data Leaks):** Zero patient-identifying data (names, phone numbers, lab identifiers) may be transmitted to external LLM APIs. Only anonymized, normalized parameters may be sent.

---

## 6. Safety Requirements & Guardrails

1. **SR-1 (Hard Stop on Clinical Diagnoses):** The system is prohibited from using diagnostic phrases such as "You have [Condition]", "This means you are suffering from [Disease]", or "Signs of [Illness]".
2. **SR-2 (Unconditional Escalation on Critical Vitals):** The critical value table overrides all normal flows. No conversational explanation, reassurance, or secondary advice may be given when a critical threshold is breached.
3. **SR-3 (Mandatory Doctor Referral):** Every generated message must reiterate that treatment decisions must only be made with an RMP.
4. **SR-4 (Doctor Question Limit):** The system must generate a maximum of 3 doctor questions per interaction to prevent cognitive overload during brief consultations.
5. **SR-5 (Clinician-in-the-Loop Content Gate):** No medicine card can enter production storage without cryptographic or database sign-off from a named MBBS/MD doctor or registered pharmacist.

---

## 7. Success Metrics & Validation Thresholds

### 7.1 Stage 1 MVP Success Gates (Pre-Software / Low-Software Test)
As defined in `docs/01-problem.md`, the software build of Stage 2 is strictly contingent on passing these gates:

| Metric | Target Threshold | Validation Method |
|---|---|---|
| **Card Uptake Rate** | ≥ 30% of eligible pharmacy patients take/read a card | Physical counter at 2 pilot pharmacies in Karnataka |
| **Doubt Resolution Rate** | ≥ 50% of card recipients report it answered an active doubt | Structured 3-question exit interview |
| **Clinician Accuracy Rate** | 100% (Zero clinician-found errors) | Independent review by 2 external clinicians |
| **Pharmacist Buy-in** | Chemist willing to continue distribution without chasing | Qualitative pharmacist interview at Week 4 |
| **Willingness to Pay / Value Signal** | ≥ 3 of 10 interviewed patients state they would pay or name a price | Structured qualitative interview |

### 7.2 Stage 2 Product Metrics (AI & Digital Flow)
* **OCR Confirmation Accuracy:** ≥ 92% of users confirm extracted lab values without manual editing.
* **Drop-Off at Consent Screen:** < 20% drop-off when Screen W7 is presented.
* **Doctor Discussion Rate:** ≥ 40% of surveyed users report actually asking the generated question to their doctor.
* **Safety Incidents:** Exactly **0** instances of missed critical result escalation or unauthorized diagnostic statements.

---
*End of PRD. Next: Architectural Specification (docs/06-architecture.md) and Safety Rules (docs/06b-safety-rules.md).*
