# Plain-Language Medicine and Report Explainer for Regional-Language Patients

## 1. Final Problem Statement

Adults on long-term medication, especially older patients who prefer a regional language such as Kannada, often leave a consultation unsure why they take each tablet or which side effects matter, and getting a second explanation takes time, travel, or someone who isn't available. We do not yet know how often this happens, what harm it causes, or whether patients would use a plain-language aid instead of asking a pharmacist or relative.

> **Evidence gap:** The cause ("the doctor explains too fast"), the frequency, current workarounds, and cost are all unmeasured. Treat them as hypotheses until interviews confirm them.

## 2. Final Proposed Solution

A staged plain-language medicine and report explainer, starting with a no-software test and adding AI only if the test shows real demand. It explains and educates only. It never diagnoses, recommends treatment, or changes a prescription.

### Stage 1: Low-software test (weeks 1 to 4)

- **Content:** Pharmacists and doctors write short cards for the 5 to 10 most common chronic medicines (start with blood pressure, diabetes, and thyroid), in Kannada and English. Each card covers:
  - what the medicine is for
  - how to take it
  - common effects
  - red flags, with what to do about them
  - a line saying "Don't stop this medicine without asking your doctor"
- **Delivery:** Printed cards at one or two pharmacies or clinics, plus pre-recorded Kannada voice notes sent by WhatsApp when someone messages the medicine name.
- **Scope:** Generic names with common Indian brand names listed, and no promotion of any brand.
- **Interviews first:** Talk to 10 people on long-term medicines about what they did the last time they doubted a tablet.

### Stage 2: Family-helper AI tool (only if Stage 1 passes)

- The patient or a family member photographs a printed lab report or prescription and gets a short explanation in Kannada or English, with voice playback.
- **Numbers and drug names are handled by code, not the AI.** OCR extracts values, ordinary code compares them to the lab's printed reference range, and drug names are matched against a drug database. The AI only words the explanation.
- The user confirms the extracted text before anything is explained.
- Handwritten prescriptions show: *"I can't read this reliably, please ask your pharmacist."*
- The tool also writes 3 to 5 questions to ask the doctor.

### Stage 3: Expansion (only if Stage 2 shows real use)

- Hindi and other languages
- More tests and drugs
- Handwriting support
- A pharmacist-supported explanation desk if users prefer a human

## 3. Safety Rules From Day One

- A named clinician reviews all content, with version dates and a review schedule.
- Every output says it is information, not medical advice, and sends the person back to their doctor.
- A doctor-set list of critical results triggers "see a doctor today," never "this is normal."
- No drug-interaction claims unless a proper interaction database is used. Otherwise the tool states that it doesn't check interactions.
- Consent for the patient's data, including a practical way to record it from the family member who uploads it. Minimal storage, deletion on request, and care with third-party AI and OCR services.
- A health-tech lawyer checks India's DPDP Act, medical device software rules, drug promotion rules, and WhatsApp Business policies before any public launch.

## 4. Success Thresholds for Stage 1

| Measure | Threshold |
|---|---|
| People offered a card who take one | At least 30% |
| Takers who say it answered a real doubt | At least half |
| Clinician-found errors in the cards | Zero |
| Pharmacist willing to continue without being chased | Yes |
| Interviewees who would pay or name a price | At least 3 of 10 |

If these fail, the problem is too small or the channel is wrong, and building the AI tool won't fix either.

## 5. Biggest Open Risks

1. The pain is not confirmed to be frequent or costly.
2. Pharmacists may have little reason to distribute the cards.
3. Nobody has been named as the payer yet.

---
