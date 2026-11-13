# Safety Rules & Clinical Governance Specification
## ReportSaathi: Patient Safety, Regulatory Safe Harbors & Guardrails
*Document Version: 1.0 — Safety & Clinical Protocol*  
*Derived from `docs/01-problem.md` through `docs/06-architecture.md`*

---

## 1. Safety Core Philosophy: "Do No Harm, Never Substitute the Physician"

ReportSaathi operates under the principle that **an incorrect or misleading medical explanation is significantly worse than no explanation at all**. For vulnerable chronic-disease patients (particularly elderly individuals managing hypertension, diabetes, and heart disease), misinterpreting a lab value or prematurely stopping a medication can lead to severe clinical events (stroke, diabetic ketoacidosis, thyroid storm).

Every software boundary, content workflow, and interface state must strictly adhere to this safety document.

---

## 2. Regulatory Safe Harbor Strategy (India Context)

To operate legally within India without requiring classification as a regulated medical device under CDSCO or violating the Telemedicine Practice Guidelines, ReportSaathi strictly adheres to three distinct safe harbors:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REGULATORY BOUNDARY MAP                         │
├──────────────────────────────────┬─────────────────────────────────────┤
│ 🚫 FORBIDDEN CLINICAL DOMAIN     │ ✅ PERMISSIBLE EDUCATIONAL DOMAIN   │
│ (Regulated SaMD / Telemedicine)  │ (ReportSaathi Safe Harbor)          │
├──────────────────────────────────┼─────────────────────────────────────┤
│ • Stating a specific diagnosis   │ • Explaining physiological purpose  │
│   ("Your test shows diabetes")   │   ("This test measures sugar")      │
│                                  │                                     │
│ • Evaluating clinical risk       │ • Direct arithmetic comparison      │
│   ("Your high sugar is alarming")│   ("This value is above the printed │
│                                  │    normal range: 70–100 mg/dL")     │
│                                  │                                     │
│ • Directing clinical management  │ • Deferring to human physician      │
│   ("Increase your Metformin")    │   ("Please discuss this reading     │
│                                  │    with your doctor")               │
│                                  │                                     │
│ • Independent AI prescribing     │ • Clinician-verified static text    │
│   ("Take 500mg daily")           │   ("Commonly taken once or twice    │
│                                  │    daily as prescribed by a doctor")│
└──────────────────────────────────┴─────────────────────────────────────┘
```

### 2.1 CDSCO Medical Device Rules (MDR 2017) Safe Harbor
Under the Central Drugs Standard Control Organization (CDSCO) and International Medical Device Regulators Forum (IMDRF) standards:
* **The Rule:** Software is classified as **Software as a Medical Device (SaMD)** (Class B or C) if it *drives or informs clinical management by interpreting physiological data to diagnose or monitor conditions*.
* **The Safe Harbor:** Pure medical reference tools, patient education materials, and digital representations of laboratory-printed data that do **not** calculate individualized diagnostic conclusions fall outside medical device licensing.
* **Implementation:** The software compares values *only* to the printed reference range provided by the certifying diagnostic laboratory. The output states whether the value is "within range", "above range", or "below range", followed immediately by: *"Only your doctor can determine what this reading means for your health."*

### 2.2 Telemedicine Practice Guidelines 2020 Compliance
* **The Rule:** Clause 1.4.2 explicitly mandates that **Artificial Intelligence / Machine Learning tools are strictly prohibited from independently counseling patients or prescribing medications**. Only a Registered Medical Practitioner (RMP) can practice medicine.
* **The Safe Harbor:** ReportSaathi does not conduct consultations. It acts as an interactive digital pamphlet. It never issues prescriptions, never assesses new symptoms, and never mimics a doctor-patient consultation.

### 2.3 Drugs & Magic Remedies Act 1954 & Drugs and Cosmetics Act 1940
* **The Rule:** Section 3 prohibits advertisements that make false or misleading claims regarding the treatment or cure of specified chronic diseases (including Diabetes, Heart Disease, and Blood Pressure disorders).
* **The Safe Harbor:** ReportSaathi never uses promotional language, never endorses specific pharmaceutical brands, never claims a medicine "cures" a chronic condition, and presents generic pharmacological names alongside trade names with equal prominence.

---

## 3. Deterministic Safety Guards & The Critical-Result Gate

### 3.1 The Critical-Result Escalation Gate (Mandatory Execution)
When a diagnostic lab report is parsed in Stage 2, the extracted numerical values are checked against a hardcoded, non-overridable **Critical Values Escalation Table** developed with an MBBS/MD clinician.

If any parameter crosses the critical threshold:
1. **Immediate Execution Halt:** All explanation generators, conversational bots, and standard card views are terminated immediately.
2. **Zero Reassurance:** The system is strictly forbidden from outputting words like *"normal", "minor", "fine", or "manageable"*.
3. **Trigger Alert Screen W8:** Deliver the urgent, calm escalation message instructing the user to see a doctor or emergency clinic today.

### 3.2 Critical Lab Values Reference Table (Standard Adult Chronic Care)

| Test Name | Standard Unit | Critical Low Threshold (Immediate Escalation) | Critical High Threshold (Immediate Escalation) | Clinical Rationale |
|---|---|---|---|---|
| **Fasting Blood Glucose** | mg/dL | **< 55** (Severe Hypoglycemia) | **> 350** (Hyperglycemic Crisis / DKA risk) | Neuroglycopenia / Coma risk |
| **Postprandial / Random Glucose**| mg/dL | **< 60** | **> 400** | Hyperosmolar state risk |
| **HbA1c** | % | **< 4.0%** (Artifact / Hypoglycemia risk)| **> 12.0%** | Uncontrolled severe chronic hyperglycemia |
| **Potassium (K+)** | mEq/L | **< 2.8** (Severe Hypokalemia) | **> 6.2** (Severe Hyperkalemia) | Fatal cardiac arrhythmia risk |
| **Sodium (Na+)** | mEq/L | **< 120** | **> 155** | Cerebral edema / Seizure risk |
| **Serum Creatinine** | mg/dL | N/A | **> 3.5** (or >2.0 in acute rise) | Acute kidney injury (AKI) |
| **Platelet Count** | /µL | **< 30,000** | **> 1,000,000** | Spontaneous hemorrhage risk |
| **Hemoglobin (Hb)** | g/dL | **< 6.5** | **> 19.0** | Tissue hypoxia / Heart failure risk |
| **Thyroid Stimulating Hormone (TSH)**| µIU/mL | **< 0.01** | **> 20.0** | Severe thyroid dysfunction |

*Note: The exact operational values must be formally signed off by the pilot partner clinician before Stage 2 deployment.*

---

## 4. Clinician-in-the-Loop Content Governance Protocol

No medicine card or educational summary may be published to the production database without passing the **Four-Eye Clinical Verification Workflow**:

```
[ Medical Writer / Pharmacist drafts Card in JSON ]
                       │
                       ▼
[ Primary Review: Named MBBS / MD Clinician verifies:
  1. Clinical accuracy of "Why", "How", and "Side Effects"
  2. Red flags cover all critical acute toxicities
  3. Doctor questions are realistic for an Indian OPD ]
                       │
                       ▼
[ Linguistic Review: Native Kannada Translator verifies:
  1. Medical terms translated into colloquial Kannada (not literal Sanskritized text)
  2. Respectful tone ("ನೀವು")
  3. No confusing grammatical ambiguities ]
                       │
                       ▼
[ Cryptographic Sign-Off:
  Clinician attaches Name, Medical Council Registration Number (e.g. KMC Reg 12345),
  and timestamp. Entry marked IS_ACTIVE=1 in cards.db ]
                       │
                       ▼
[ Annual Expiration: Content expires automatically after 365 days unless re-certified ]
```

---

## 5. Standard Disclaimer Copy (Immutable Formats)

The following disclaimer blocks are hardcoded constants in the application source code. They cannot be suppressed, hidden, or minimized by any user preference.

### 5.1 Card Footer Disclaimer (Bilingual)

**Kannada:**
> ℹ️ **ಗಮನಿಸಿ:** ಇದು ಸಾಮಾನ್ಯ ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ, ವೈದ್ಯಕೀಯ ಸಲಹೆ ಅಥವಾ ರೋಗನಿರ್ಣಯವಲ್ಲ. ನಿಮ್ಮ ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಯಾವುದೇ ಮಾತ್ರೆಯನ್ನು ಪ್ರಾರಂಭಿಸಬೇಡಿ ಅಥವಾ ನಿಲ್ಲಿಸಬೇಡಿ.  
> *ಪರಿಶೀಲಿಸಿದ ವೈದ್ಯರು:* ಡಾ. [ವೈದ್ಯರ ಹೆಸರು], [ನೋಂದಣಿ ಸಂಖ್ಯೆ] | *ದಿನಾಂಕ:* [ದಿನಾಂಕ]  
> *ಔಷಧ ಪರಸ್ಪರ ಪರಿಣಾಮಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ.*

**English:**
> ℹ️ **Notice:** This is for general informational purposes only and is not medical advice or a diagnosis. Never start, stop, or change any medication without consulting your doctor.  
> *Reviewed by:* Dr. [Clinician Name], Reg No: [Reg Number] | *Date:* [Date]  
> *Drug-drug interactions are not checked.*

### 5.2 Critical Escalation Disclaimer (Screen W8)

**Kannada:**
> 🚨 **ತಕ್ಷಣ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ**  
> ನಿಮ್ಮ ವರದಿಯಲ್ಲಿರುವ ಒಂದು ಅಥವಾ ಹೆಚ್ಚು ಮಾಪನಗಳು ಲ್ಯಾಬ್‌ನ ಸಾಮಾನ್ಯ ಮಿತಿಗಿಂತ ತುಂಬಾ ಹೊರಗಿವೆ. ಇದು ತಕ್ಷಣದ ವೈದ್ಯಕೀಯ ಗಮನವನ್ನು ಬಯಸಬಹುದು. ದಯವಿಟ್ಟು ಇಂದೇ ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಅಥವಾ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಯನ್ನು ಭೇಟಿ ಮಾಡಿ. ನಾವು ಯಾವುದೇ ಔಷಧಿ ಬದಲಾವಣೆಯನ್ನು ಶಿಫಾರಸು ಮಾಡುವುದಿಲ್ಲ.

**English:**
> 🚨 **Consult a Doctor Today**  
> One or more measurements in your report are significantly outside the laboratory's standard range. This may require immediate medical attention. Please consult your doctor or visit a nearby clinic today. We do not recommend any changes to your medication.

---

## 6. Illegible Input & Handwriting Fallback Protocol

Handwritten doctor prescriptions are notoriously variable in legibility. Attempting to parse them with optical character recognition introduces unacceptable clinical risk.

### 6.1 Handwriting Detection Rules
1. If the OCR confidence score across the document is **< 70%**, or
2. If the document classifier detects cursive, handwritten script rather than printed diagnostic typography:
   * **Action:** Immediately halt processing.
   * **Message Delivered:**
     > ✍️ **ಕ್ಷಮಿಸಿ, ಕೈಬರಹದ ಚೀಟಿಯನ್ನು ಓದಲು ಸಾಧ್ಯವಿಲ್ಲ.**  
     > *(Sorry, we cannot read handwritten prescriptions reliably.)*  
     > ತಪ್ಪಾದ ಮಾಹಿತಿ ರೋಗಿಯ ಆರೋಗ್ಯಕ್ಕೆ ಹಾನಿ ಮಾಡಬಹುದು. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸಮೀಪದ ಔಷಧಿಕಾರರನ್ನು (Pharmacist) ಭೇಟಿ ಮಾಡಿ.  
     > *(Incorrect readings can harm your health. Please show this prescription to your local pharmacist.)*

---

## 7. Data Privacy, Dignity & DPDP Act 2023 Guardrails

Medical documents contain sensitive personal health information (SPHI). In accordance with the Digital Personal Data Protection (DPDP) Act 2023 and the SPDI Rules 2011:

1. **Explicit Unbundled Consent:** No image processing begins without user consent (Screen W7). Consent cannot be bundled into terms of service.
2. **Transient Processing Only:** Uploaded photos are stored strictly in volatile RAM (`tmpfs`) during OCR parsing. Upon message delivery or within **10 minutes**, the image file is destroyed using secure file shredding (`find /tmp/scratch -type f -delete`).
3. **Zero Third-Party Model Leakage:** No patient names, hospital names, doctor names, or contact numbers are passed to external AI models. All internal logging hashes user identifiers using `SHA-256(phone + DATA_SALT)`.
4. **Instant Right to Erasure:** Users can text `"DELETE"` or `"ಅಳಿಸು"` at any point. The backend executes a complete wipe of active session tokens, temporary files, and interaction metadata.
5. **Zero Commercial Data Sharing:** Medical inquiries and lab parameters are **never** sold, monetized, or shared with pharmaceutical manufacturers, insurance underwriters, or targeted advertising networks.

---

## 8. Emergency Exclusions & Boundary Limits

ReportSaathi is **not** an emergency response system. 

If a user texts words indicating acute emergency distress (e.g., *"chest pain"*, *"ಎದೆ ನೋವು"*, *"unconscious"*, *"ತಲೆಸುತ್ತು ಬಿದ್ದುಹೋದರು"*, *"poison"*):
1. **Immediate Auto-Response:**
   > 🚨 **ತುರ್ತು ಪರಿಸ್ಥಿತಿ / Emergency**  
   > ನೀವು ಅಥವಾ ನಿಮ್ಮವರು ತೀವ್ರ ಎದೆ ನೋವು, ಉಸಿರಾಟದ ತೊಂದರೆ, ಅಥವಾ ಪ್ರಜ್ಞಾಹೀನತೆಯಿಂದ ಬಳಲುತ್ತಿದ್ದರೆ, ತಕ್ಷಣ **108 ಅಥವಾ 112** ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ ಹತ್ತಿರದ ತುರ್ತು ಚಿಕಿತ್ಸಾ ವಿಭಾಗಕ್ಕೆ (Emergency Hospital) ತೆರಳಿ. ಈ ಬಾಟ್ ತುರ್ತು ಸಂದರ್ಭಗಳಿಗೆ ಸೂಕ್ತವಲ್ಲ.  
   > *(If experiencing severe chest pain, breathing difficulty, or unconsciousness, call 108 / 112 immediately or visit an emergency room. This bot cannot assist in emergencies.)*

---
*End of Safety & Governance Document. All technical and clinical participants must maintain strict adherence to these boundaries.*
