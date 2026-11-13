Final problem statement

Patients who prefer regional languages, especially older adults, receive lab reports and prescriptions full of English medical terms and abbreviations, and many cannot understand them before or after seeing the doctor. This leads to confusion, anxiety, dependence on others, and a risk of misunderstanding instructions, so they need a safe, plain-language explanation in their own language.

Evidence gap: your document lists elderly, rural, and chronic-disease patients, but we only worked through one person (a 60-year-old Kannada speaker in Bengaluru). Treat the wider groups as a hypothesis until you interview them. Frequency, current workarounds, and cost are still unmeasured.

Final proposed solution

A multilingual AI explainer that turns an uploaded lab report or prescription into a plain-language explanation in Kannada, Hindi, or English, with optional voice playback. It explains and educates only. It never diagnoses, recommends treatment, or changes a prescription.

Key features
Upload a PDF or photo of a lab report or prescription.
Plain-language explanation of each test and what it measures.
Flag values outside the lab’s own printed reference range, with no disease labels.
Prescription explanation: medicine name, what it is generally used for, and the doctor’s written instructions restated simply.
Kannada, Hindi, and English output, with text-to-speech for users who can’t read well.
A list of 3 to 5 questions to ask the doctor.
Consent, encryption, and automatic deletion of uploaded images.
Design decisions I’d change from your draft
Don’t let the LLM read numbers or decide what’s abnormal. Extract values with OCR, compare them to the printed reference range in ordinary code, and use the LLM only to word the explanation. This avoids confident wrong answers.
Match drug names against a drug database instead of trusting the LLM’s memory.
Tesseract is weak on phone photos, Kannada script, and handwriting. For the first version, support printed lab reports and printed prescriptions only. For handwritten prescriptions, show “I can’t read this reliably, please ask your pharmacist.” A vision-capable model may beat Tesseract here, so test both on real reports.
Show the extracted text back to the user to confirm before explaining it.
Keep the stack simple: React frontend, FastAPI backend, PostgreSQL storing only minimal data, and a Kannada-capable text-to-speech service.
Build in phases
Phase 1 (MVP): printed lab reports only, English to Kannada, text plus voice, 10 to 15 common tests (CBC, sugar, lipids, thyroid, kidney, liver).
Phase 2: printed prescriptions with drug-database matching, then Hindi.
Phase 3: handwriting, more languages, and more tests, only if Phases 1 and 2 show real use.
Safety and legal rules
A doctor reviews the explanation templates and the “questions for your doctor” logic.
Every output carries “This is information, not medical advice. Please consult your doctor.”
Anything urgent-looking or unclear gets “discuss with your doctor soon” and never a reassuring “this is normal.”
Follow India’s DPDP Act: explicit consent, minimal storage, deletion on request.
Have a health-tech lawyer check whether this counts as medical device software before any public launch.
Validation before you invest heavily

Test the MVP with 10 real users (older Kannada speakers or their families) using anonymized reports. Measure whether they used it, whether it changed what they asked the doctor, and whether any explanation was wrong. If it fails on accuracy, no feature list will save it.

Expected outcome

Patients understand their reports and prescriptions in their own language, feel less anxious while waiting, depend less on others, and ask better questions at the visit.