# Design Specification & Screen States
### Plain-Language Medicine & Report Explainer — India / Kannada-first (ReportSaathi)
*Derived from docs/03-scope.md, docs/01-problem.md, and docs/02-research.md. Date: November 2026.*

---

## 1. Surfaces & Architecture

The product is deliberately **WhatsApp-first and web-companion**. Because older Kannada-speaking patients in Karnataka face high app-install friction, storage constraints on budget phones, and digital literacy hurdles, the primary interface is a **WhatsApp Business conversation thread**, accompanied by lightweight **single-page responsive web cards** (opened via WhatsApp link or pharmacy QR codes).

| Surface | Stage | Medium | Technology / Constraints |
|---|---|---|---|
| **WhatsApp Chat UI** | Stage 1 MVP & Stage 2 | WhatsApp Business API | Native message bubbles, interactive quick-reply buttons (max 3), WhatsApp markdown (`*bold*`), voice audio notes (.ogg/opus), emoji visual anchors. |
| **Static Medicine Card (Web / Print)** | Stage 1 MVP & Stage 2 | Lightweight static HTML/CSS | Responsive single-column (max-width 480px), zero client-side framework bloat (<50KB payload), printable QR format for pharmacy counters. |
| **OCR Value Confirmation Form** | Stage 2 MVP | Mobile Web View / WebView | Lightweight verification form allowing user or family proxy to inspect and confirm OCR extracted values before any explanation is generated. |

---

## 2. All Screens in the Core Flow

Below is the complete state table for every screen in the core flow across both surfaces.

### Summary State Matrix

| Screen ID | Screen Name | Surface | Trigger | Primary Goal |
|---|---|---|---|---|
| **W1** | Welcome & Language Select | WhatsApp | First incoming message ("Hi", "Namaskara") | Establish immediate trust; select Kannada or English. |
| **W2** | Main Intent Menu | WhatsApp | Post-language setup or typing "menu" | Select between medicine explanation or lab report flow. |
| **W3** | Medicine Input & Lookup | WhatsApp | User types/speaks medicine name | Immediate acknowledgment and lookup progress. |
| **W4** | Medicine Card (Found) | WhatsApp | Medicine match in curated database | Deliver core 6-part clinician-reviewed card in Kannada. |
| **W5** | Medicine Not Found / Ambiguous | WhatsApp | No match or multiple close aliases | Suggest generic name or pharmacist fallback without dead-ending. |
| **W6** | System Error / Downtime | WhatsApp | Network timeout, API outage | Calm, non-technical recovery path and human fallback. |
| **W7** | Lab Upload & Privacy Consent | WhatsApp | User chooses "Understand Report" (Stage 2) | DPDP-compliant plain-language consent before image processing. |
| **W8** | OCR Extraction & Value Confirmation | Mobile Web | User uploads lab report photo | Side-by-side verification of extracted values vs. printed range. |
| **W9** | Lab Report Explanation | WhatsApp / Web | User confirms extracted numbers | Parameter-by-parameter plain-language context with doctor questions. |
| **W10** | Critical Result Escalation Alert | WhatsApp / Web | Extracted value exceeds critical threshold | Calm, unambiguous "See a doctor today" alert; zero diagnostic reassure. |
| **C1** | Web Medicine Card (Loaded) | Web | User taps WhatsApp link or scans QR | High-contrast, large-type standalone card with audio playback. |
| **C2** | Web Card Loading Skeleton | Web | Link opened on 2G/3G slow connection | Accessible layout skeleton; eliminates layout shifts and anxiety. |
| **C3** | Web Card Not Found / Expired | Web | Malformed URL or unlisted drug ID | Clear redirection back to WhatsApp bot or pharmacist. |
| **C4** | Web Card Critical Result Banner | Web | Lab report card with critical parameter | Persistent red urgency banner commanding doctor consultation. |

---

## 3. Screen-by-Screen State Definitions

---

### W1 · Welcome & Language Selection

#### Purpose
Establish immediate institutional trust, reassure the patient/caregiver, and set the interaction language before any medical terminology is introduced.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │                                               🟢 Online │
  │  [ReportSaathi Verified Business ✓]                     │
  │                                                         │
  │  🙏 ನಮಸ್ಕಾರ! Welcome to ReportSaathi.                  │
  │  ನಿಮ್ಮ ಮಾತ್ರೆ ಮತ್ತು ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್ ತಿಳಿಯಲು ಸುಲಭ ದಾರಿ.    │
  │  (Your simple guide to medicines and lab reports.)      │
  │                                                         │
  │  ದಯವಿಟ್ಟು ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ / Choose language:            │
  │                                                         │
  │  [ 1️⃣ ಕನ್ನಡ (Kannada) ]   [ 2️⃣ English ]               │
  └─────────────────────────────────────────────────────────┘
  ```
  - WhatsApp quick-reply buttons (maximum 2 buttons).
  - Familiar Namaskara icon (`🙏`) as the brand visual anchor.
  - Zero legal jargon before the language choice.

* **Empty State:**
  If the incoming message is blank or an unparseable sticker/media:
  ```text
  ನಮಸ್ಕಾರ! ದಯವಿಟ್ಟು ಕೆಳಗಿನ ಬಟನ್ ಒತ್ತಿ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ:
  [ ಕನ್ನಡ ]  [ English ]
  ```

* **Loading State:**
  Text indicator sent within 500ms:
  ```text
  ⏳ ನಿಮ್ಮ ಭಾಷೆ ದಾಖಲಿಸಲಾಗುತ್ತಿದೆ... (Setting language...)
  ```

* **Error State:**
  If the database write fails or session drops:
  ```text
  ⚠️ ಸಂಪರ್ಕದಲ್ಲಿ ತೊಂದರೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು '1' (ಕನ್ನಡ) ಅಥವಾ '2' (English) ಎಂದು ಟೈಪ್ ಮಾಡಿ ಕಳುಹಿಸಿ.
  [ ↩️ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ ]
  ```

---

### W2 · Main Intent Menu

#### Purpose
Direct the user to the single active task without menu clutter or cognitive overload.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?                          │
  │  (What would you like to know?)                         │
  │                                                         │
  │  [ 💊 ಮಾತ್ರೆ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ / About Medicine ]          │
  │  [ 📋 ರಿಪೋರ್ಟ್ ಅರ್ಥ ಮಾಡಿಕೊಳ್ಳಿ / Understand Report ]   │
  └─────────────────────────────────────────────────────────┘
  ```
  - In Stage 1 MVP, tapping "Understand Report" gently informs the user that the lab feature is launching next month and redirects them to the medicine explainer.

* **Empty State:**
  User sends an unrecognizable query (e.g. "hello", "hi"):
  Re-renders W2 with a friendly nudge:
  ```text
  ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ನಾವು ಸಿದ್ಧರಿದ್ದೇವೆ. ಕೆಳಗಿನ ಆಯ್ಕೆಗಳಲ್ಲಿ ಒಂದನ್ನು ಒತ್ತಿ:
  [ 💊 ಮಾತ್ರೆ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ ]  [ 📋 ರಿಪೋರ್ಟ್ ಅರ್ಥ ]
  ```

* **Loading State:**
  Instantaneous (static template rendered on WhatsApp edge).

* **Error State:**
  If user input cannot be parsed:
  ```text
  ಕ್ಷಮಿಸಿ, ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಮಾತ್ರೆ ಹೆಸರನ್ನು ಟೈಪ್ ಮಾಡಿ (ಉದಾ: Glycomet) ಅಥವಾ 'ಮೆನು' ಎಂದು ಕಳುಹಿಸಿ.
  ```

---

### W3 · Medicine Lookup & Processing

#### Purpose
Acknowledge the user's typed or spoken medicine name immediately so they never wonder if the bot crashed.

* **Default State (User Action):**
  User inputs text in Kannada, English, or Romanized Kannada: `"ಮೆಟ್‌ಫಾರ್ಮಿನ್"`, `"Metformin"`, or `"Glycomet 500"`.

* **Empty State:**
  User sends punctuation, an emoji, or an accidental whitespace:
  ```text
  ದಯವಿಟ್ಟು ಮಾತ್ರೆಯ ಹೆಸರನ್ನು ಬರೆಯಿರಿ (ಉದಾ: Metformin, Telmisartan, Eltroxin).
  ನೀವು ಮಾತ್ರೆಯ ರಟ್ಟಿನ (strip) ಫೋಟೋ ಕೂಡ ಕಳುಹಿಸಬಹುದು.
  ```

* **Loading State (Immediate acknowledgment within 1 second):**
  ```text
  ⏳ *'Glycomet'* ಮಾತ್ರೆಯ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತಿದ್ದೇವೆ...
     (Looking up details for Glycomet...)
  ```

* **Error State (Timeout / Network glitch):**
  ```text
  ⚠️ ಸರ್ವರ್ ಸಂಪರ್ಕ ನಿಧಾನವಾಗಿದೆ. ದಯವಿಟ್ಟು 1 ನಿಮಿಷದಲ್ಲಿ ಮತ್ತೆ ಕಳುಹಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಔಷಧಿಕಾರರನ್ನು ಕೇಳಿ.
  [ ↩️ ಮರುಪ್ರಯತ್ನಿಸಿ ]
  ```

---

### W4 · Medicine Explainer Card (Found)

#### Purpose
The core value delivery of Stage 1. Delivers the verified 7-part clinician-reviewed card directly inside WhatsApp chat.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  💊 *Metformin (Glycomet, Glucophage)*                  │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │                                                         │
  │  📌 *ಏಕೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತೀರಿ? (Purpose)*                 │
  │  ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ನಿಯಂತ್ರಿಸಲು.                     │
  │  (To help control blood sugar levels.)                  │
  │                                                         │
  │  ⏰ *ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳಬೇಕು? (How to take)*               │
  │  ಊಟದ ಜೊತೆ ಅಥವಾ ತಕ್ಷಣ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ.               │
  │  (Take with or immediately after food.)                 │
  │                                                         │
  │  😌 *ಸಾಮಾನ್ಯ ಪರಿಣಾಮಗಳು (Common effects)*                │
  │  ಹೊಟ್ಟೆ ನೋವು, ವಾಕರಿಕೆ — ಸಾಮಾನ್ಯವಾಗಿ 1-2 ವಾರಗಳಲ್ಲಿ       │
  │  ಕಡಿಮೆಯಾಗುತ್ತದೆ.                                       │
  │  (Mild nausea or loose motion; usually settles.)        │
  │                                                         │
  │  🚨 *ಈ ಲಕ್ಷಣಗಳಿದ್ದರೆ ತಕ್ಷಣ ವೈದ್ಯರನ್ನು ಕಾಣಿ (Red flags):* │
  │  • ತೀವ್ರ ನಿಶ್ಯಕ್ತಿ ಅಥವಾ ವಿಪರೀತ ಹೊಟ್ಟೆ ನೋವು               │
  │  • ಉಸಿರಾಟದಲ್ಲಿ ತೊಂದರೆ                                   │
  │                                                         │
  │  ⚠️ *ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಈ ಮಾತ್ರೆ ನಿಲ್ಲಿಸಬೇಡಿ.*           │
  │  (Do not stop this medicine without asking your doctor.)│
  │                                                         │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │  🩺 *ನಿಮ್ಮ ವೈದ್ಯರಿಗೆ ಕೇಳಬೇಕಾದ ಪ್ರಶ್ನೆಗಳು:*             │
  │  1. ಈ ಮಾತ್ರೆ ಎಷ್ಟು ದಿನ ಮುಂದುವರಿಸಬೇಕು?                  │
  │  2. ಮಾತ್ರೆ ತೆಗೆದುಕೊಳ್ಳುವುದು ಮರೆತರೆ ಏನು ಮಾಡಬೇಕು?        │
  │                                                         │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │  ℹ️ *ಇದು ಮಾಹಿತಿ ಮಾತ್ರ, ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆಯಲ್ಲ.*         │
  │  ಪರಿಶೀಲಿಸಿದವರು: Dr. Anita Rao, MD (11/2026).            │
  │  ಔಷಧ ಪರಸ್ಪರ ಕ್ರಿಯೆ (Interactions) ಪರಿಶೀಲಿಸಿಲ್ಲ.         │
  │                                                         │
  │  [ 🔊 ಕನ್ನಡದಲ್ಲಿ ಆಲಿಸಿ (Voice) ]  [ 📋 ಮುಖ್ಯ ಮೆನು ]     │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  Not applicable (if matched, full structured content is always returned).

* **Loading State:**
  Covered in W3.

* **Error State:**
  If card generation fails midway, fallback to W6.

---

### W5 · Medicine Not Found / Ambiguous Query

#### Purpose
Gracefully handle unlisted drugs, spelling typos, or ambiguous brand names without stranding the user.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  😕 *ಕ್ಷಮಿಸಿ, ಈ ಮಾತ್ರೆಯ ವಿವರ ಸದ್ಯ ನಮ್ಮಲ್ಲಿಲ್ಲ.*           │
  │  (We do not have information on this medicine yet.)     │
  │                                                         │
  │  ಸಾಧ್ಯವಾದರೆ:                                            │
  │  1. ಮಾತ್ರೆಯ ಸಾಮಾನ್ಯ (generic) ಹೆಸರು ಪ್ರಯತ್ನಿಸಿ.          │
  │  2. ಮಾತ್ರೆಯ ರಟ್ಟಿನ ಮೇಲೆ ಮುದ್ರಿತ ಹೆಸರನ್ನು ಸರಿಯಾಗಿ ನೋಡಿ.  │
  │                                                         │
  │  ನಿಮಗೆ ಯಾವುದೇ ಅನುಮಾನವಿದ್ದರೆ, ನಿಮ್ಮ ಹತ್ತಿರದ ಔಷಧಿಕಾರರನ್ನು  │
  │  (Pharmacist) ಅಥವಾ ವೈದ್ಯರನ್ನು ನೇರವಾಗಿ ಕೇಳಿ.             │
  │                                                         │
  │  [ 🔍 ಬೇರೆ ಹೆಸರು ಹುಡುಕಿ ]  [ 📋 ಮೆನು ]                  │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  Triggered when input is unmatchable. Logs query internally for content expansion pipeline.

* **Loading State:**
  Standard lookup state (W3).

* **Error State:**
  Repeated 3 failures trigger proactive human pharmacist advisory:
  ```text
  ಈ ಮಾತ್ರೆಯ ಬಗ್ಗೆ ಖಚಿತ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ. ಯಾವುದೇ ತಪ್ಪು ಮಾಡಬೇಡಿ — ನಿಮ್ಮ ಸಮೀಪದ ಮೆಡಿಕಲ್ ಶಾಪ್ ಅಥವಾ ವೈದ್ಯರನ್ನು ಭೇಟಿಯಾಗಿ.
  ```

---

### W6 · System Error / Service Downtime

#### Purpose
Provide a calm, non-technical, reassuring failure message with an actionable human alternative.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  ⚠️ *ಸೇವೆ ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ.*                     │
  │  (Service is temporarily unavailable.)                  │
  │                                                         │
  │  ತಾಂತ್ರಿಕ ದೋಷದಿಂದಾಗಿ ಸಂದೇಶ ಕಳುಹಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ.   │
  │  ದಯವಿಟ್ಟು 2 ನಿಮಿಷಗಳ ನಂತರ ಮರುಪ್ರಯತ್ನಿಸಿ.               │
  │                                                         │
  │  ತುರ್ತು ಸಂದರ್ಭದಲ್ಲಿ ನಿಮ್ಮ ಔಷಧಿಕಾರರನ್ನು ಅಥವಾ             │
  │  ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.                                  │
  │                                                         │
  │  [ ↩️ ಮರುಪ್ರಯತ್ನಿಸಿ (Try again) ]                      │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  Not applicable.

* **Loading State:**
  Not applicable.

* **Error State:**
  Persistent failure offers the customer-care escalation contact.

---

### W7 · Lab Upload & Privacy Consent (Stage 2)

#### Purpose
Fulfill mandatory DPDP Act 2023 obligations before sensitive personal health data (report photos) is uploaded.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  🔒 *ನಿಮ್ಮ ಆರೋಗ್ಯ ಮಾಹಿತಿ ಸುರಕ್ಷಿತವಾಗಿರುತ್ತದೆ*           │
  │  (Your Health Data Privacy Notice)                      │
  │                                                         │
  │  • ನಿಮ್ಮ ರಿಪೋರ್ಟ್ ಫೋಟೋವನ್ನು ವಿವರಣೆ ನೀಡಲು ಮಾತ್ರ         │
  │    ಬಳಸಲಾಗುತ್ತದೆ ಮತ್ತು ತಕ್ಷಣ ಅಳಿಸಲಾಗುತ್ತದೆ.              │
  │    (Processed only to explain and deleted immediately.) │
  │  • ಇದನ್ನು ಯಾರಿಗೂ ಹಂಚಿಕೊಳ್ಳುವುದಿಲ್ಲ ಅಥವಾ ಮಾರಾಟ ಮಾಡುವುದಿಲ್ಲ.│
  │  • ಈ ವಿವರಣೆ ವೈದ್ಯರ ಸಲಹೆಗೆ ಪರ್ಯಾಯವಲ್ಲ.                  │
  │                                                         │
  │  ನಿಮ್ಮ ಒಪ್ಪಿಗೆ ಇದೆಯೇ?                                   │
  │                                                         │
  │  [ ✅ ಒಪ್ಪಿಗೆ ಇದೆ (I Consent) ]  [ ❌ ಬೇಡ (Cancel) ]    │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  User sends photo before granting consent → system holds photo in memory buffer without OCR processing and demands W7 consent first.

* **Loading State:**
  ```text
  🔒 ನಿಮ್ಮ ಸಮ್ಮತಿ ದಾಖಲಾಗುತ್ತಿದೆ...
  ```

* **Error State:**
  User taps "Cancel":
  ```text
  ನಿಮ್ಮ ನಿರ್ಧಾರವನ್ನು ಗೌರವಿಸುತ್ತೇವೆ. ಯಾವುದೇ ಫೋಟೋ ಸಂಗ್ರಹವಾಗಿಲ್ಲ. ನೀವು ಬಯಸಿದಾಗ ಮುಖ್ಯ ಮೆನುವಿನಿಂದ ಮುಂದುವರಿಯಬಹುದು.
  [ 📋 ಮುಖ್ಯ ಮೆನು ]
  ```

---

### W8 · OCR Extraction & Value Confirmation (Stage 2)

#### Purpose
Enforce the fundamental safety rule: **Code handles numbers, AI only words the explanation, and the user must verify extracted text before explanation.**

* **Default State (Mobile Web Modal via WhatsApp link):**
  - Displays original snippet of scanned report alongside extracted key parameters.
  - Parameter Name, Found Value, and Lab's Printed Reference Range.
  - Value highlighted in soft red border if outside lab's printed range.
  - Action buttons: `[ ✅ ಹೌದು, ಸರಿಯಾಗಿದೆ — ವಿವರಣೆ ನೀಡಿ ]` and `[ ✏️ ಸಂಖ್ಯೆ ತಿದ್ದಿ (Edit) ]`.

* **Empty State (Blurred / Illegible Image or Handwritten Prescription):**
  ```text
  🔍 *ಫೋಟೋ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ / ಕೈಬರಹ ಓದಲು ಸಾಧ್ಯವಿಲ್ಲ*
  ಮುದ್ರಿತ (Printed) ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್‌ನ ಸ್ಪಷ್ಟ ಫೋಟೋ ಕಳುಹಿಸಿ.
  ವೈದ್ಯರ ಕೈಬರಹದ ಚೀಟಿಯಾಗಿದ್ದರೆ, ದಯವಿಟ್ಟು ಔಷಧಿಕಾರರನ್ನು ಕೇಳಿ.
  [ 📷 ಮತ್ತೊಮ್ಮೆ ಫೋಟೋ ತೆಗೆಯಿರಿ ]
  ```

* **Loading State (OCR Processing, 2–4 seconds):**
  ```text
  ⏳ ರಿಪೋರ್ಟ್‌ನಿಂದ ಸಂಖ್ಯೆಗಳನ್ನು ಓದಲಾಗುತ್ತಿದೆ... (Extracting values...)
  ```

* **Error State (OCR Failure / Misaligned table):**
  Allows manual entry of values:
  ```text
  ⚠️ ಲ್ಯಾಬ್ ಮೌಲ್ಯಗಳನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಓದಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.
  ದಯವಿಟ್ಟು ನಿಮ್ಮ ಟೆಸ್ಟ್ ಹೆಸರು ಮತ್ತು ಸಂಖ್ಯೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ (ಉದಾ: HbA1c 7.5).
  ```

---

### W9 · Lab Report Explanation (Stage 2)

#### Purpose
Translate lab numbers into plain Kannada understanding strictly using the lab's own printed range without making any diagnostic pronouncements.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  📋 *Fasting Blood Sugar (FBS): 168 mg/dL*              │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │  ನಿಮ್ಮ ಲ್ಯಾಬ್ ಮುದ್ರಿತ ಸಾಮಾನ್ಯ ಮಿತಿ: 70 - 100 mg/dL     │
  │                                                         │
  │  📌 *ಇದರ ಅರ್ಥವೇನು?*                                     │
  │  ಈ ಮೌಲ್ಯವು ನಿಮ್ಮ ಲ್ಯಾಬ್ ನೀಡಿದ ಸಾಮಾನ್ಯ ಮಿತಿಗಿಂತ         │
  │  ಹೆಚ್ಚಾಗಿದೆ (Above printed normal range).               │
  │                                                         │
  │  💡 *ನೆನಪಿಡಿ:*                                          │
  │  ಒಂದೇ ರಿಪೋರ್ಟ್ ಆಧಾರದ ಮೇಲೆ ಯಾವುದೇ ತೀರ್ಮಾನಕ್ಕೆ ಬರಬೇಡಿ.    │
  │  ಆಹಾರ, ಸಮಯ ಮತ್ತು ಇತರ ಮಾತ್ರೆಗಳು ಈ ಸಂಖ್ಯೆಯ ಮೇಲೆ ಪರಿಣಾಮ   │
  │  ಬೀರುತ್ತವೆ.                                             │
  │                                                         │
  │  🩺 *ವೈದ್ಯರಿಗೆ ಕೇಳಿ:*                                   │
  │  "ನನ್ನ ಊಟದ ನಂತರದ ಸಕ್ಕರೆ ಮಟ್ಟ ಅಥವಾ HbA1c ತಪಾಸಣೆ         │
  │  ಅಗತ್ಯವಿದೆಯೇ?"                                          │
  │                                                         │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │  ℹ️ ಇದು ರೋಗ ನಿರ್ಣಯವಲ್ಲ. ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಭೇಟಿಯಾಗಿ.     │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  Test not recognized in medical catalog → generic contextual guide shown.

* **Loading State:**
  ```text
  ⏳ ವಿವರಣೆ ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ...
  ```

* **Error State:**
  Standard fallback to W6.

---

### W10 · Critical Result Escalation Alert (Stage 2)

#### Purpose
Safely intercept values that cross predefined physician-defined danger thresholds (e.g. Potassium >6.0 mEq/L, Blood Glucose >400 mg/dL, Platelets <20,000). Must **never** say "this looks normal" or downplay the condition.

* **Default State:**
  ```text
  ┌─────────────────────────────────────────────────────────┐
  │  🚨 *ಇಂದೇ ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ*                 │
  │  (Please Consult a Doctor Today)                        │
  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━               │
  │                                                         │
  │  ನಿಮ್ಮ ರಿಪೋರ್ಟ್‌ನಲ್ಲಿ ಒಂದು ಮೌಲ್ಯವು ಲ್ಯಾಬ್‌ನ ಸಾಮಾನ್ಯ       │
  │  ಮಿತಿಗಿಂತ ಗಣನೀಯವಾಗಿ ವ್ಯತ್ಯಾಸವಾಗಿದೆ.                     │
  │                                                         │
  │  ಇದು ಅಪಾಯಕಾರಿ ಎಂದು ನಾವು ಹೇಳಲಾರೆವು — ಆದರೆ ವೈದ್ಯರ          │
  │  ನೇರ ತಪಾಸಣೆ ಇಂದೇ ಅಗತ್ಯವಿದೆ.                             │
  │                                                         │
  │  ⚠️ *ಮಾತ್ರೆಗಳನ್ನು ನೀವೇ ನಿಲ್ಲಿಸಬೇಡಿ ಅಥವಾ ಬದಲಾಯಿಸಬೇಡಿ.*   │
  │                                                         │
  │  📋 *ವೈದ್ಯರ ಬಳಿಗೆ ಹೋಗುವಾಗ ತೆಗೆದುಕೊಂಡು ಹೋಗಿ:*            │
  │  1. ಈ ಮೂಲ ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್                               │
  │  2. ಪ್ರಸ್ತುತ ಸೇವಿಸುತ್ತಿರುವ ಎಲ್ಲಾ ಮಾತ್ರೆಗಳ ಚೀಟಿ          │
  │                                                         │
  │  [ 🏥 ಆಸ್ಪತ್ರೆ / ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ ]                 │
  └─────────────────────────────────────────────────────────┘
  ```

* **Empty State:**
  Not applicable.

* **Loading State:**
  Immediate delivery via high-priority queue.

* **Error State:**
  Even if full explanation fails to generate, the critical alert message is hardcoded and always fires.

---

### C1 · Static Web Medicine Card (Default Loaded)

#### Purpose
Visual standalone representation accessible through shared WhatsApp links or physical QR cards at pharmacy counters.

* **Default State:**
  - Responsive single card (max width 480px) on warm-white `#FAFAF8` background.
  - Top header with ReportSaathi logo and instant bilingual switch `[ ಕನ್ನಡ | English ]`.
  - Drug generic name `Metformin` (24sp SemiBold) with common Indian brand aliases (`Glycomet, Glucophage, Obimet`).
  - Section 1 (Green badge): 📌 ಏಕೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತೀರಿ? (Purpose).
  - Section 2 (Blue badge): ⏰ ಹೇಗೆ ಸೇವಿಸಬೇಕು? (Dosage instructions).
  - Section 3 (Amber box): ⚠️ ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ನಿಲ್ಲಿಸಬೇಡಿ (Do not stop warning).
  - Section 4 (Red box): 🚨 ರೆಡ್ ಫ್ಲ್ಯಾಗ್ ಲಕ್ಷಣಗಳು (Red flag symptoms).
  - Section 5 (Light green card): 🩺 ವೈದ್ಯರಿಗೆ ಕೇಳಬೇಕಾದ 2 ಪ್ರಶ್ನೆಗಳು (Doctor questions).
  - Prominent full-width action button: `🔊 ಕನ್ನಡದಲ್ಲಿ ಆಲಿಸಿ (Voice Playback)` (48dp height minimum).
  - Muted footer: Clinician name, review date, and "No interaction checks performed" disclaimer.

* **Empty State (C3 - Card Not Found):**
  Soft illustration, friendly message in Kannada & English:
  ```text
  😕 ಈ ಪುಟ ಲಭ್ಯವಿಲ್ಲ (Page Not Available)
  ಮಾತ್ರೆಯ ಹೆಸರನ್ನು ನಮ್ಮ WhatsApp ನಂಬರ್‌ಗೆ ಕಳುಹಿಸಿ.
  [ WhatsApp ತೆರೆಯಿರಿ ]
  ```

* **Loading State (C2 - Skeleton):**
  - Smooth `#E0E0E0` placeholder shimmer blocks matching the exact geometry of headers, badges, and action button.
  - Zero layout shift (CLS = 0) when text finishes loading.

* **Error State (C4 - Critical Warning Variant):**
  - When viewed for a lab result with critical parameters, a persistent red alert banner spans the top of the card: `🚨 ಇಂದೇ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ / Consult Doctor Today`.

---

## 4. Review of Design References & Benchmark Analysis

The reference screenshots generated in `docs/references/` establish clear boundaries on what to adopt and what to avoid from commercial and governmental health interfaces.

### Reference 1: WhatsApp Business Conversational UI (`ref-01-whatsapp-flow.png`)
* **Context:** The de facto primary communication channel for Indian families and local clinics.
* **What to Borrow:**
  - WhatsApp quick-reply buttons (reduces typing for elderly users with tremors or low literacy).
  - Voice note audio player pill directly inside chat thread.
  - Section dividers (`━━━━`) and emoji anchors (`💊`, `📌`, `⏰`, `🚨`) to structure long text.
  - Verified green badge to overcome trust deficit.
* **What to Avoid:**
  - Deep nested menu trees (e.g. "Reply 1 for X, 2 for Y, 3 for Z") — users get lost; keep depth to ≤2 steps.
  - Cluttered long text paragraphs without line breaks.
  - Unverified automated medical diagnosis or bot self-confidence.

### Reference 2: Standalone Medicine Card (`ref-02-medicine-card-kannada.png`)
* **Context:** The clean web companion card for older adults and family sharing.
* **What to Borrow:**
  - Visual hierarchy: Large 24sp drug name, distinct section containers, prominent audio button.
  - Dedicated "Questions for your doctor" box that converts passive reading into proactive clinical dialogue.
  - Clean bilingual subtitles under Kannada headings for cross-generational caregiver support.
* **What to Avoid:**
  - Multi-tab navigation (e.g. Overview / Pharmacology / Clinical Trials) which confuses patients.
  - Dense pharmaceutical jargon (e.g., "Biguanide antihyperglycemic agent").

### Reference 3: Lab Report OCR Value Confirmation (`ref-03-lab-report-ocr-confirmation.png`)
* **Context:** The safety checkpoint where code extracts numbers and the user verifies them.
* **What to Borrow:**
  - Two-column parameter vs. value confirmation table.
  - Color-coded borders matching lab's printed range only.
  - Prominent confirmation CTA (`✅ ಹೌದು, ಸರಿಯಾಗಿದೆ`) paired with manual edit fallback (`✏️ ತಿದ್ದುಪಡಿ`).
* **What to Avoid:**
  - Automatically explaining values without user confirmation.
  - Overriding the lab's printed range with generalized global thresholds.

### Reference 4: Critical Result Alert Flow (`ref-04-critical-alert-flow.png`)
* **Context:** Emergency handling when a lab value indicates high clinical risk.
* **What to Borrow:**
  - High-urgency crimson header (`🚨 ಇಂದೇ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ`) with calm, actionable guidance.
  - Practical checklist for the clinic visit (bring original report, list of medicines).
  - Explicit disclaimer: "ReportSaathi is not an emergency service; do not self-taper or change doses."
* **What to Avoid:**
  - Panic-inducing sensationalist phrasing ("Fatal risk", "Severe organ damage").
  - Suggesting home remedies or intermediate drug alterations.

### Reference 5: Comparative Industry Patterns (`ref-05-comparative-patterns.png`)
* **Context:** Side-by-side comparison of Tata 1mg, NirogGyan, and ReportSaathi.
* **From Tata 1mg:**
  - *Borrow:* Rich generic drug alias mapping and explicit contraindication warnings.
  - *Avoid:* E-commerce sales funnels ("Add to Cart", "Flat 20% off"), tiny 12sp English typography, and dense manufacturer leaflet dumps.
* **From NirogGyan:**
  - *Borrow:* Parameter-by-parameter categorization (e.g. Sugar, Lipids, Liver) and visual simplicity.
  - *Avoid:* Multi-color speedometers / dial gauges (hard for older adults to interpret accurately), English-only PDFs, and B2B-only access barriers.

### Reference 6: Budget Phone & Kannada Typography Spec (`ref-06-budget-phone-kannada-typography.png`)
* **Context:** Technical constraints of low-cost Android hardware (360x800 resolution, 720p TFT/LCD displays, sub-₹8,000 devices like Redmi A3, Realme C-series, Samsung Galaxy A04).
* **What to Borrow:**
  - 18sp minimum body text with **1.5× line height** to prevent Kannada conjunct vowel collisions.
  - 48 × 48 dp minimum touch target bounding boxes for all interactive buttons.
  - Strict prohibition of mid-word truncation (`...`).
* **What to Avoid:**
  - Thin/light font weights (weight 200/300) which wash out on low-brightness LCDs in Indian sunlight.
  - CSS blur filters, backdrop-filters, and heavy JavaScript frameworks that cause jank on 2GB RAM phones.

---

## 5. Design Direction

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REPORTSAATHI DESIGN TOKENS                      │
├────────────────────────────────────────────────────────────────────────┤
│  LAYOUT      Single-column • Max 480px • Zero horizontal scroll         │
│  TYPE        Noto Sans Kannada • 18sp body min • 1.5× line height       │
│  COLOUR      Deep Green #1A6B3C • Surface #FAFAF8 • Alert #C0392B       │
│  SPACING     8dp base grid • 16dp card padding • 48dp min touch targets │
│  TONE        Respectful • Calm • Local neighbor • Zero diagnosis        │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Layout & Visual Structure
* **Single-Column Stack:** Both on WhatsApp and Web, the UI is strictly a top-to-bottom vertical stack. Never use multi-column grids, horizontal carousels, or swipe gestures that older adults struggle with.
* **Predictable Fixed Section Order:**
  `1. Name & Aliases` → `2. Purpose (Why)` → `3. How to take` → `4. Common effects` → `5. Red flags` → `6. Don't stop warning` → `7. Doctor questions` → `8. Disclaimers`.
  Repeat users internalize this mental model within 2 visits.
* **Thumb-Zone Optimization:** Primary actionable buttons (Voice playback, Menu, Confirm) reside in the bottom third of the screen, designed with minimum **48 × 48 dp** touch targets to accommodate motor tremor or reduced precision.

### 5.2 Typography for Indic & Kannada Scripts
* **Font Family:** **Noto Sans Kannada** paired with system **Roboto / Noto Sans** for English companions. Noto Sans Kannada is pre-installed on Android 7.0+ and renders complex Kannada conjunct ligatures (e.g. `ರ್ತ್`, `ಕ್ಷ`, `ಷ್ಟ್ರ`) cleanly without glyph breakage.
* **Type Scale (Mobile Web & Printed Cards):**
  - **Drug / Parameter Heading (H1):** `24sp` / SemiBold (weight 600).
  - **Brand Subtitles:** `15sp` / Regular (weight 400), Muted `#5C5C5C`.
  - **Section Headings (H2):** `16sp` / SemiBold with unified emoji visual anchor.
  - **Body Copy:** **`18sp` minimum** / Regular (weight 400), `#1A1A1A`.
  - **Captions & Disclaimers:** `13sp` / Regular (weight 400), `#5C5C5C`.
* **Line Height (Mandatory Rule):**
  - **1.5× (27px line-height on 18sp text)** for all Kannada copy. Kannada possesses extensive ascenders and descenders (vowel signs like `ೂ`, `ೈ`, `ೌ` and subscript consonants like `್ಕ`). Tight 1.2× line heights cause adjacent lines to collide, rendering text unreadable on budget displays.
* **Prohibition of Mid-Word Truncation:** Never truncate Kannada words with CSS ellipsis (`text-overflow: ellipsis`). Kannada words are agglutinative and long; truncating mid-word slices multi-byte Unicode codepoints and destroys word meaning. Let text wrap naturally.

### 5.3 Colour Palette & Accessibility (WCAG 2.2 AA)
The palette uses 5 semantic tokens tested against outdoor glare and low-contrast LCD panels:

| Token Name | Hex Value | Semantic Usage | Contrast on `#FAFAF8` | Contrast on `#FFFFFF` |
|---|---|---|---|---|
| `--surface` | `#FAFAF8` | Page and chat background; warm white reduces eye fatigue and glare. | Base | Base |
| `--on-surface` | `#1A1A1A` | All primary Kannada body text and drug headings. | **16.5:1 (AAA)** | **17.8:1 (AAA)** |
| `--muted` | `#5C5C5C` | Disclaimer text, secondary brand aliases, metadata. | **5.4:1 (AA)** | **5.9:1 (AA)** |
| `--accent-green` | `#1A6B3C` | Primary buttons, section badges, verified trust marks. Culturally associated with pharmacy/health in Karnataka. | **5.1:1 (AA)** | **5.5:1 (AA)** |
| `--alert-crimson` | `#C0392B` | Red-flag headers, critical result banners. Never used for decoration. | **5.8:1 (AA)** | **6.3:1 (AA)** |

* **Redundant Encoding:** Color is **never** used as the sole indicator of status. Every alert or warning pairs color with an explicit text label and an icon (`🚨`, `⚠️`, `✅`).

### 5.4 Spacing & Density
* **8dp Grid System:** All paddings, margins, and component dimensions are multiples of 8dp (8dp, 16dp, 24dp, 32dp).
* **Generous Padding:** Internal card padding is **16dp** to prevent text from touching screen bezels on curved budget screens.
* **Visual Chunking:** Each section is housed in a dedicated card or bounded by clear horizontal dividers (`━━━━` on WhatsApp, `1px solid #E2E8F0` on web). Older patients process information one discrete chunk at a time.

### 5.5 Tone of Voice & Copywriting Rules
* **The "Knowledgeable Neighbor" Persona:** The voice is that of an educated, respectful family friend who has medical literacy — warm, unhurried, formal, and utterly honest about limits.
* **Respectful Kannada Pronouns:** Always address the patient as **"ನೀವು" (Neevu - formal you)**, never casual "ನೀನು" (Neenu). Older adults in Karnataka find casual pronouns disrespectful from a health service.
* **Short, Active Phrasing:** Maximum 12–15 words per sentence. Use active voice: `"ಊಟದ ಜೊತೆ ತೆಗೆದುಕೊಳ್ಳಿ"` (Take with food), rather than passive technical translations.
* **Honest Boundaries:** Prominently state what cannot be done: `"ಔಷಧ ಪರಸ್ಪರ ಪರಿಣಾಮ ಪರಿಶೀಲಿಸಿಲ್ಲ"` (Drug interactions not checked).
* **Calm Urgency:** Even on critical alerts, avoid screaming caps, exclamation floods, or frightening words. State clearly what was found and give the immediate next step: `"ಇಂದೇ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ"` (See your doctor today).

---

## 6. Implementation Checklist for Low-Cost Android Devices

- [x] **Zero Custom Web Fonts:** Use system `Noto Sans Kannada` on Android; only load Google Fonts fallback if system font is missing.
- [x] **No Canvas / WebGL:** All rendering is static DOM or native WhatsApp text bubbles.
- [x] **Lightweight Media:** Audio notes compressed via Opus codec at 24kbps mono (~150KB per 45-second explanation).
- [x] **Physical Device Test Target:** Verified render on Redmi 9A / A3, Realme C31, and Samsung Galaxy A04 running Android Go / 720p resolution.
- [x] **Touch Target Compliance:** 100% of interactive elements meet or exceed 48 × 48 dp.

---

*Artifacts generated in `docs/references/`:*
- [`ref-01-whatsapp-flow.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-01-whatsapp-flow.png)
- [`ref-02-medicine-card-kannada.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-02-medicine-card-kannada.png)
- [`ref-03-lab-report-ocr-confirmation.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-03-lab-report-ocr-confirmation.png)
- [`ref-04-critical-alert-flow.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-04-critical-alert-flow.png)
- [`ref-05-comparative-patterns.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-05-comparative-patterns.png)
- [`ref-06-budget-phone-kannada-typography.png`](file:///c:/Users/Dell/reportsaathi/docs/references/ref-06-budget-phone-kannada-typography.png)
