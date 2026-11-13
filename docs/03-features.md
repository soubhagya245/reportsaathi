# Feature Prioritisation
### Plain-Language Medicine & Report Explainer — India / Kannada-first
*Derived from docs/01-problem.md and docs/02-research.md. Written: November 2026.*

---

## The Single Core Flow

**In one sentence:**
A patient — or a family member on their behalf — sends a medicine name on WhatsApp in Kannada,
gets a short clinician-reviewed card that says why they take it, what to watch for, and what
to ask their doctor, and nothing else happens.

That is the entire product. Every feature below is judged against one test:

> **"Does removing this break the core flow, or just make it nicer?"**
> If the answer is "nicer," it is not in the Stage 1 MVP.

```
[Patient or family member]
        |
        | sends medicine name via WhatsApp (text, any script)
        v
[Name matched to curated card — generic name + Indian brand aliases]
        |
        | match found?
        |-- NO  → "We don't have this yet. Try the generic name or ask your pharmacist."
        |
        v
[Plain-language card returned in Kannada (+ English companion)]
        |
        | card always contains, in this fixed order:
        |   1. Why you take it
        |   2. How to take it
        |   3. Common effects (what is normal)
        |   4. Red flags — see a doctor if you notice these
        |   5. "Don't stop without asking your doctor"
        |   6. 1–3 questions to ask at next appointment
        |   7. "This is information, not medical advice" + reviewer name + date
        v
[Done — user has what they needed without travelling or waiting]
```

**What the flow deliberately does not do:**
- It does not look at the user's other medicines.
- It does not interpret numbers or test results (Stage 2 only, if Stage 1 passes).
- It does not say whether the user's dose is right.
- It does not connect the medicine to the user's specific diagnosis.
- It does not diagnose anything.

---

## Feature Tree

### F1 · Medicine Explainer

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F1.1 | Lookup by medicine name (text, any script) | Core action |
| F1.2 | Card content: why / how / effects / red flags | Core value |
| F1.3 | "Don't stop without asking your doctor" line | Safety-critical |
| F1.4 | Clinician review + named reviewer + version date on every card | Keeps product educational, not diagnostic |
| F1.5 | Generic name + common Indian brand names as lookup aliases | Patients ask by brand name |
| F1.6 | Drug-interaction check | See prioritisation — this is a Never without a licensed DB |

### F2 · Lab Report Explainer

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F2.1 | Photo input (printed report) | Stage 2 |
| F2.2 | OCR extraction of values | Stage 2 |
| F2.3 | User confirmation of extracted text before explanation | Stage 2 — cannot be skipped |
| F2.4 | Comparison to lab's own printed reference range only | Stage 2 — never use product's own thresholds |
| F2.5 | Plain-language explanation of what the value means | Stage 2 |
| F2.6 | Critical-result gate — "see a doctor today," never "this is normal" | Stage 2 |
| F2.7 | Handwritten prescription detection + "ask your pharmacist" response | Stage 2 |
| F2.8 | AI-inferred diagnosis from values | NEVER |

### F3 · Language & Delivery

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F3.1 | Kannada text output | The differentiator |
| F3.2 | English text companion (below Kannada, same card) | Bilingual users; clinician review |
| F3.3 | Voice playback — Kannada (TTS or pre-recorded) | High value; infrastructure needed |
| F3.4 | Voice playback — English | Lower priority than Kannada voice |
| F3.5 | WhatsApp delivery channel | Only channel reaching this demographic without an app |
| F3.6 | Hindi output | Real demand; Stage 3 |
| F3.7 | Other regional languages | Stage 3 |
| F3.8 | Dedicated mobile app | Nobody asked for it |

### F4 · Doctor Questions

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F4.1 | 1–3 questions per card, per medicine | Directly in the problem statement |
| F4.2 | Questions personalised to this user's other conditions | Later — Stage 1 uses per-medicine generic questions |

### F5 · Safety & Compliance

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F5.1 | "Not medical advice" disclaimer on every output | Non-negotiable |
| F5.2 | Named clinician reviewer listed on content | CDSCO educational-tool positioning |
| F5.3 | Content version date + scheduled review interval | Prevents dangerous content staleness |
| F5.4 | Critical-result escalation list (doctor-defined thresholds) | Stage 2 prerequisite |
| F5.5 | "Interactions not checked" statement | One-line footer; cheap; removes regulatory ambiguity |
| F5.6 | Explicit data consent before any upload | DPDP Act + WhatsApp Business policy |
| F5.7 | Minimal storage policy + deletion on request | DPDP Act; strongest privacy signal |
| F5.8 | Data Processing Agreements with third-party OCR/AI vendors | Mandatory before Stage 2 goes live |
| F5.9 | Health-tech lawyer sign-off before public launch | Cannot launch without it |

### F6 · Content Management

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F6.1 | Starter set: 5–10 cards (blood pressure, diabetes, thyroid) | Without this there is no product |
| F6.2 | Clinician card editing + approval workflow tool | Manual Google Docs review is fine in Stage 1 |
| F6.3 | Card coverage expansion beyond starter set | Only after starter set is validated |
| F6.4 | User-submitted questions feeding card updates | Needs moderation + legal review before it influences content |

### F7 · User Management

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F7.1 | WhatsApp opt-in and opt-out mechanism | WhatsApp Business API policy requirement |
| F7.2 | User accounts / health history / longitudinal tracking | Adds storage burden and login friction |
| F7.3 | Family-member-as-proxy-uploader consent flow | Required before lab photo feature goes live |
| F7.4 | Personalised dose and refill reminders | Useful but not the core flow |

### F8 · Advanced / Later Scope

| ID | Sub-feature | Notes |
|----|-------------|-------|
| F8.1 | Handwriting recognition for prescriptions | OCR accuracy on Indian handwritten scripts is poor today |
| F8.2 | ABDM / ABHA health record integration | Increases trust; adds integration complexity |
| F8.3 | Pharmacist-supported human explanation desk | High safety value; requires staffing and operating model |
| F8.4 | Clinician-facing analytics dashboard | Build once usage data exists |
| F8.5 | Licensed drug-interaction database (Mims India, DrFirst) | Correct to do only with a licensed DB |
| F8.6 | B2B white-label for pharmacies or clinics | Requires product-market fit first |

---

## Prioritisation

---

### Stage 1 MVP — Weeks 1–4, pre-software
**What it is:** Printed cards at one pharmacy + a WhatsApp number that returns the same card as text when someone messages a medicine name. A human (or simple keyword bot) handles the matching. No app, no backend, no OCR, no accounts.

| Feature | In MVP? | Reason |
|---------|---------|--------|
| F1.1 Lookup by medicine name | ✅ YES | The core action. Without this there is no explainer. |
| F1.2 Card content (why / how / effects / red flags) | ✅ YES | The actual value delivered. |
| F1.3 "Don't stop without asking your doctor" | ✅ YES | Safety-critical; core product position. Without it the product might imply a user can self-taper. |
| F1.4 Clinician review + named reviewer + version date | ✅ YES | Required to maintain educational (not diagnostic) status under CDSCO. Without it the product is an unaccountable WhatsApp forward. |
| F1.5 Generic name + common Indian brand names | ✅ YES | Patients ask by brand name (Glycomet, not Metformin). Without aliases the lookup fails most of the time. |
| F3.1 Kannada text output | ✅ YES | The primary differentiator. Without it the product is indistinguishable from 1mg. |
| F3.2 English text companion | ✅ YES | Bilingual families; clinician review is easier in English; makes cards auditable. |
| F3.5 WhatsApp delivery | ✅ YES | The only channel that reaches older Kannada-speaking patients without requiring them to install anything. |
| F4.1 Doctor questions (1–3 per card) | ✅ YES | Explicitly in the problem statement; converts passive reading into an action the user can take at the next appointment. |
| F5.1 "Not medical advice" disclaimer | ✅ YES | Non-negotiable legally and ethically. |
| F5.2 Named clinician reviewer on content | ✅ YES | Required for CDSCO educational-tool positioning; also the strongest trust signal. |
| F5.3 Version date + review schedule | ✅ YES | A card written today and never updated can become dangerous. The review date forces accountability. |
| F5.5 "Interactions not checked" statement | ✅ YES | One-line footer; costs nothing to add; removes regulatory ambiguity and sets honest user expectations. |
| F5.9 Health-tech lawyer sign-off | ✅ YES | DPDP Act, DMRA 1954, and WhatsApp Business API all have obligations that need a lawyer's review before any public number is live. Cannot launch without it. |
| F6.1 Starter 5–10 cards | ✅ YES | Without content there is no product. |
| F7.1 WhatsApp opt-in/opt-out | ✅ YES | WhatsApp Business API policy requirement. No opt-out = account ban. |

**Intentionally excluded from Stage 1 MVP:**

| Feature | Excluded because |
|---------|-----------------|
| F5.6 Explicit data consent (upload) | No uploads happen in Stage 1. The medicine name typed in chat is not sensitive health data under DPDP Act. If the bot ever processes anything identifiable, re-evaluate. |
| F5.7 Minimal storage / deletion on request | No personal health data is stored in Stage 1 (messages go to WhatsApp Business inbox; no backend DB). Re-evaluate before Stage 2. |
| F3.3 Voice playback | High value, but adds infrastructure (AI4Bharat / Google TTS integration). Stage 1 is explicitly "pre-software." Prove demand via text first. |

---

### Challenges — Things That Appear in the MVP But Were Questioned

The following are in the MVP, but were challenged. The challenge and the reason for keeping them are both recorded.

| Feature | Challenge | Why it stays |
|---------|-----------|--------------|
| **F1.4 Clinician review + version date** | "Can we just launch with AI-generated cards and add a reviewer later? It doubles the work." | No. Without a named clinician, the product is an unreviewed AI health claim — CDSCO's SaMD boundary becomes much harder to stay on the right side of, and a single factual error on a medicine card causes direct patient harm. This is the safety layer, not a polish layer. |
| **F5.9 Lawyer sign-off** | "It's a pilot at one pharmacy. Does it really need a lawyer before week 1?" | Yes, for a public WhatsApp number. The moment a number is live, WhatsApp Business API terms, DPDP Act consent obligations, and DMRA 1954 advertising rules all apply. A quiet internal test with 10 invited participants could proceed without it; a WhatsApp number open to the public cannot. |
| **F4.1 Doctor questions** | "This adds length to the card. Can we cut it and just give the explanation?" | The doctor-questions section is what makes this product different from a Wikipedia page. It converts the user's confusion into a concrete action at their next consultation. Research finding #3 in docs/02-research.md is "no why am I taking this answer" — the follow-on failure is that patients don't know what to do with the answer either. Keep it. |
| **F1.5 Brand name aliases** | "Maintaining brand-name aliases for every generic is ongoing work. Can users just learn to send generic names?" | No. The target user is a Kannada-speaking older adult who bought "Glycomet" from a pharmacy. They will not know that Glycomet is Metformin. If the lookup fails, they get nothing. Brand aliases are the lookup reliability layer. |
| **F3.2 English companion text** | "Isn't this a Kannada-first product? Why are we cluttering cards with English?" | Two reasons. First, the clinician reviewer needs to audit the clinical accuracy of the card — reviewing Kannada content requires a Kannada-literate clinician, which may not always be available. The English companion makes review accessible. Second, many families include English-comfortable members who help older relatives; the bilingual card serves both. Keep it, but Kannada is always first and larger. |

---

### Stage 2 MVP — Only if Stage 1 passes all five thresholds
**What it adds:** Photo of a lab report → OCR → user confirms extracted values → plain-language Kannada explanation → critical-result gate. Voice playback added here.

| Feature | Reason to include now |
|---------|----------------------|
| F2.1 Photo input | The Stage 2 job. |
| F2.2 OCR extraction | Required for the lab report flow. |
| F2.3 User confirmation of extracted text | Cannot be skipped. OCR on printed Indian lab reports has known error rates; a wrong number explained confidently causes harm. The user confirms what was extracted before anything is explained. |
| F2.4 Comparison to lab's own reference range | The safety boundary. The product never uses its own clinical thresholds — only what the lab itself printed. This keeps the product out of SaMD diagnostic territory. |
| F2.5 Plain-language explanation of values | The Stage 2 value. |
| F2.6 Critical-result gate | A patient who gets "this looks fine" for a critically abnormal value is harmed. The gate must exist before the lab report feature launches. |
| F2.7 Handwritten detection + pharmacist fallback | OCR on handwritten Indian prescriptions is unreliable. The product must gracefully fail rather than confidently misread. |
| F3.3 Voice playback (Kannada) | Research is clear: older users prefer voice over text; WhatsApp voice notes are native behaviour. This is the highest-value addition for the core demographic. AI4Bharat (Bhashini) is the implementation path for Kannada TTS. |
| F3.4 Voice playback (English) | Follows naturally from F3.3; lower priority but low marginal cost once F3.3 is built. |
| F4.2 Personalised doctor questions | In Stage 2 the system knows the specific test and value — questions can be tailored ("Ask your doctor what a TSH of 6.2 means for you") rather than generic. |
| F5.6 Explicit consent before upload | DPDP Act kicks in the moment a user uploads a photo. Consent UI must exist and be recorded before any image is processed. |
| F5.7 Minimal storage + deletion on request | Photos must not be retained server-side after explanation is delivered. DPDP Act requires erasure to be possible on request. |
| F5.8 DPA with third-party OCR/AI vendors | Before any lab photo is sent to a third-party OCR or AI service, a Data Processing Agreement (or equivalent) must be in place. This is a DPDP Act and IT Act SPDI Rules requirement. |
| F7.3 Family-proxy consent flow | A family member photographing and uploading a patient's report is processing that patient's health data. The consent must cover the actual data subject (the patient), not just the person with the phone. |

---

### Later — Build only if Stage 2 shows real use

| Feature | Reason to defer |
|---------|----------------|
| F3.6 Hindi | Real demand; expand only after Kannada is proven. |
| F3.7 Other regional languages | Stage 3. |
| F3.8 Mobile app | No user asked for it. WhatsApp removes the friction of a separate app. Build only if WhatsApp proves insufficient for a specific use case. |
| F5.4 Critical-result escalation list | Needed in Stage 2; listed here because the *curating and maintaining* of this doctor-defined list is ongoing work, not a one-time build. |
| F6.2 Clinician card editing + approval workflow tool | Manual Google Docs / sheets review by one clinician is fine through Stage 1 and early Stage 2. Build the tool when card count exceeds what one person can manage manually. |
| F6.3 Card coverage expansion | Expand only after the starter 5–10 cards have been validated for accuracy and usefulness. |
| F6.4 User-submitted questions feeding card updates | High value for improving content quality. Requires moderation pipeline and a legal review of the process before user input can influence medical content. |
| F7.2 User accounts / health history / longitudinal tracking | Adds login friction to a single-explanation interaction. Also adds significant DPDP Act obligations (purpose limitation, storage limits, audit logs). Build only if users explicitly request it. |
| F7.4 Personalised dose and refill reminders | Useful; not the core flow. Also risks crossing into clinical management territory if not carefully scoped. |
| F8.1 Handwriting recognition | OCR accuracy on handwritten Indian prescriptions is poor today. Stage 3 — wait for model quality to improve. |
| F8.2 ABDM / ABHA integration | Increases institutional trust and opens government health system distribution. Adds integration complexity. Stage 3. |
| F8.3 Pharmacist-supported human explanation desk | High safety value as a human fallback. Requires staffing, operating model, and training. Stage 3. |
| F8.4 Clinician analytics dashboard | Useful for sustaining clinician buy-in. Build once usage data exists and there is something worth showing. |
| F8.5 Licensed drug-interaction database | Correct to do only with a licensed Indian database (Mims India, DrFirst). Without a licensed DB, any interaction claim made by the product is a liability. The "interactions not checked" disclaimer (F5.5) is the correct interim position. |
| F8.6 B2B white-label | Requires product-market fit before the product can be packaged for another business. |

---

### Never — The Hard Wall

These features would cause the product to diagnose, prescribe, or change a patient's treatment.
They are excluded permanently, regardless of technical feasibility or user demand.
Crossing this wall changes the product's regulatory classification under CDSCO Medical Devices Rules 2017
from an educational tool to a Software as a Medical Device — a category that requires
ISO 13485 certification, DCGI registration, and clinical validation, none of which this
staged product is designed or resourced for.

| Feature | Why it is Never |
|---------|----------------|
| **AI-inferred diagnosis from lab values** | "Your TSH of 8.5 suggests hypothyroidism" is a diagnostic statement. This is exactly what CDSCO MDR 2017 classifies as SaMD Class B/C. The safe and correct language is: "This value is above your lab's printed reference range — please discuss with your doctor." |
| **Drug-interaction check without a licensed DB** | Incorrect interaction information is clinically worse than no information. The product must state "interactions not checked" until a licensed Indian drug database (Mims India, DrFirst, or equivalent) is contractually secured and integrated correctly. |
| **Recommending a dose change** | The product explains what a medicine is for. It never says "take half a tablet" or "take it twice a day instead." Dose decisions are clinical decisions that require knowing the patient's full history. |
| **Recommending starting a new medicine** | Entirely outside scope. No circumstances. |
| **Recommending stopping a medicine** | The card says the opposite: "Don't stop without asking your doctor." The product actively contradicts self-discontinuation. |
| **Saying a critical result "looks normal" or "looks fine"** | If a result matches the critical-result gate (F2.6), the response is always "see a doctor today" — never reassurance. There is no scenario in which the product should reassure a patient about a lab result. |
| **AI-generated content without clinician review** | An AI-written card that has not been reviewed by a named clinician is an unaccountable health claim. It removes the safety layer that keeps the product educational. |
| **Differential diagnosis from symptoms** | The product does not accept symptoms as input. Responding to "I have chest pain, what could it be?" immediately classifies the product as a symptom checker and SaMD Class B/C. |
| **Prescription generation or modification** | Illegal under Telemedicine Practice Guidelines 2020. Only a registered medical practitioner can prescribe. The product is not a practitioner. |
| **Connecting medicine dosage to a specific patient's diagnosis** | "You are taking Metformin because you have Type 2 diabetes" personalises and implies clinical knowledge of the user's condition. The product does not know the user's diagnosis and must never state or imply it. |

---

## Decision Summary

```
Stage 1 MVP (Weeks 1–4, pre-software — printed cards + WhatsApp keyword bot):
  F1.1  F1.2  F1.3  F1.4  F1.5
  F3.1  F3.2  F3.5
  F4.1
  F5.1  F5.2  F5.3  F5.5  F5.9
  F6.1
  F7.1

Stage 2 MVP (only if Stage 1 passes all five thresholds):
  F2.1  F2.2  F2.3  F2.4  F2.5  F2.6  F2.7
  F3.3  F3.4
  F4.2
  F5.6  F5.7  F5.8
  F7.3

Later (only if Stage 2 shows real use):
  F3.6  F3.7  F3.8
  F5.4  F6.2  F6.3  F6.4
  F7.2  F7.4
  F8.1  F8.2  F8.3  F8.4  F8.6
  F1.6 / F8.5 — only if a licensed Indian drug interaction DB is contractually secured

Never (permanent exclusion):
  F2.8
  Drug-interaction check without licensed DB
  Dose recommendations
  Diagnosis from symptoms or values
  Prescription generation or modification
  AI-generated content without clinician review
  Any reassurance about a critical lab result
```

---

*Derived from docs/01-problem.md (problem statement, staged solution, safety rules, success thresholds) and docs/02-research.md (competitive gap analysis, regulatory framework). To be revisited after Stage 1 field data is collected.*
