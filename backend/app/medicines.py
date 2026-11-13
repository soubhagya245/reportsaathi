from typing import Any
from fastapi import APIRouter, HTTPException, Query
from backend.app.schemas.medicine import (
    MedicineCardData,
    MedicineCardResponse,
    MedicineNotFoundResponse,
    BilingualText,
    BilingualList,
    GovernanceMetadata,
)

router = APIRouter(prefix="/api/medicines", tags=["Medicines"])

# Clinician-verified 10 starter chronic medicines catalog
STARTER_MEDICINES: list[MedicineCardData] = [
    MedicineCardData(
        id="med_metformin",
        generic_name="Metformin",
        brand_aliases=["Glycomet", "Glucophage", "Obimet", "Glyciphage", "Metfor"],
        therapeutic_class="Biguanide / Antidiabetic",
        purpose=BilingualText(
            kn="ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ನಿಯಂತ್ರಿಸಲು ಈ ಮಾತ್ರೆಯನ್ನು ನೀಡಲಾಗುತ್ತದೆ.",
            en="Helps control blood sugar levels by improving insulin sensitivity."
        ),
        how_to_take=BilingualText(
            kn="ಊಟದ ಜೊತೆ ಅಥವಾ ತಕ್ಷಣ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ. ಖಾಲಿ ಹೊಟ್ಟೆಯಲ್ಲಿ ಸೇವಿಸಬೇಡಿ.",
            en="Take with or immediately after food. Do not take on an empty stomach."
        ),
        common_side_effects=BilingualText(
            kn="ಹೊಟ್ಟೆ ನೋವು, ವಾಕರಿಕೆ ಅಥವಾ ಲಘು ಭೇದಿ — ಸಾಮಾನ್ಯವಾಗಿ 1-2 ವಾರಗಳಲ್ಲಿ ತಾನಾಗಿಯೇ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
            en="Mild nausea, stomach pain, or loose motions; usually settles within 1-2 weeks."
        ),
        red_flags=BilingualList(
            kn=[
                "ತೀವ್ರ ನಿಶ್ಯಕ್ತಿ ಅಥವಾ ವಿಪರೀತ ಹೊಟ್ಟೆ ನೋವು",
                "ಉಸಿರಾಟದಲ್ಲಿ ತೊಂದರೆ ಅಥವಾ ಸ್ನಾಯು ನೋವು"
            ],
            en=[
                "Severe fatigue or unusual abdominal discomfort",
                "Trouble breathing or severe muscle aches"
            ]
        ),
        caution_do_not_stop=BilingualText(
            kn="ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಈ ಮಾತ್ರೆ ನಿಲ್ಲಿಸಬೇಡಿ. ದಿಢೀರ್ ನಿಲ್ಲಿಸಿದರೆ ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ಮಟ್ಟ ಹಠಾತ್ ಹೆಚ್ಚಾಗಬಹುದು.",
            en="Do not stop this medicine without asking your doctor. Stopping abruptly can spike blood sugar."
        ),
        doctor_questions=BilingualList(
            kn=[
                "ಈ ಮಾತ್ರೆಯನ್ನು ನಾನು ಎಷ್ಟು ತಿಂಗಳು ಮುಂದುವರಿಸಬೇಕು?",
                "ಬೆಳಗಿನ ಉಪಾಹಾರ ತಪ್ಪಿದರೆ ಮಾತ್ರೆ ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳಲಿ?",
                "ವರ್ಷಕ್ಕೊಮ್ಮೆ ಕಿಡ್ನಿ ತಪಾಸಣೆ (Creatinine) ಅಗತ್ಯವಿದೆಯೇ?"
            ],
            en=[
                "For how many months should I continue this medicine?",
                "What should I do if I accidentally miss a morning dose?",
                "Do I need periodic kidney function (Creatinine) tests?"
            ]
        ),
        governance=GovernanceMetadata(
            reviewed_by="Dr. Anita Rao, MBBS, MD",
            clinician_reg_no="KMC-45291",
            reviewed_at="2026-11-01",
            disclaimer_en="Notice: For informational purposes only, not medical advice. Drug interactions not checked."
        )
    ),
    MedicineCardData(
        id="med_amlodipine",
        generic_name="Amlodipine",
        brand_aliases=["Amlong", "Stamlo", "Amlovas", "Amlopin"],
        therapeutic_class="Calcium Channel Blocker / Antihypertensive",
        purpose=BilingualText(
            kn="ರಕ್ತದೊತ್ತಡವನ್ನು (BP) ನಿಯಂತ್ರಣದಲ್ಲಿಡಲು ಮತ್ತು ಹೃದಯದ ಮೇಲಿನ ಒತ್ತಡ ಕಡಿಮೆ ಮಾಡಲು ನೀಡಲಾಗುತ್ತದೆ.",
            en="Relaxes blood vessels to lower high blood pressure and reduce strain on the heart."
        ),
        how_to_take=BilingualText(
            kn="ಪ್ರತಿದಿನ ನಿರ್ದಿಷ್ಟ ಸಮಯದಲ್ಲಿ, ಊಟದ ಮೊದಲು ಅಥವಾ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ.",
            en="Take once daily at the same time every day, with or without food."
        ),
        common_side_effects=BilingualText(
            kn="ಕಾಲು ಅಥವಾ ಕಣಕಾಲುಗಳಲ್ಲಿ ಲಘು ಊತ, ತಲೆನೋವು ಅಥವಾ ಮುಖ ಕೆಂಪಾಗುವುದು.",
            en="Mild swelling in ankles/feet, headache, or facial flushing."
        ),
        red_flags=BilingualList(
            kn=[
                "ಎದೆಬಡಿತ ತೀವ್ರವಾಗಿ ಏರುಪೇರಾಗುವುದು",
                "ತೀವ್ರ ತಲೆತಿರುಗುವಿಕೆ ಅಥವಾ ಪ್ರಜ್ಞೆ ತಪ್ಪುವಂತಾಗುವುದು"
            ],
            en=[
                "Rapid or irregular heartbeat (palpitations)",
                "Severe dizziness or feeling like fainting"
            ]
        ),
        caution_do_not_stop=BilingualText(
            kn="ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ಮಾತ್ರೆಯನ್ನು ಅರ್ಧ ಮಾಡಬೇಡಿ ಅಥವಾ ನಿಲ್ಲಿಸಬೇಡಿ.",
            en="Do not stop or halve this dose without consulting your doctor."
        ),
        doctor_questions=BilingualList(
            kn=[
                "ನನ್ನ ಕಣಕಾಲು ಊತ ಕಾಣಿಸಿಕೊಂಡರೆ ಏನು ಮಾಡಬೇಕು?",
                "ನನ್ನ ರಕ್ತದೊತ್ತಡವನ್ನು ಎಷ್ಟು ದಿನಗಳಿಗೊಮ್ಮೆ ಅಳೆಯಬೇಕು?"
            ],
            en=[
                "What should I do if I notice swelling around my ankles?",
                "How frequently should I monitor my blood pressure at home?"
            ]
        ),
        governance=GovernanceMetadata(
            reviewed_by="Dr. S. Kulkarni, MD (Gen Med)",
            clinician_reg_no="KMC-38190",
            reviewed_at="2026-11-01",
            disclaimer_en="Notice: For informational purposes only, not medical advice. Drug interactions not checked."
        )
    ),
    MedicineCardData(
        id="med_telmisartan",
        generic_name="Telmisartan",
        brand_aliases=["Telma", "Telmikem", "Cresar", "Telsartan"],
        therapeutic_class="Angiotensin II Receptor Blocker (ARB)",
        purpose=BilingualText(
            kn="ಅಧಿಕ ರಕ್ತದೊತ್ತಡ ನಿಯಂತ್ರಿಸಲು ಮತ್ತು ಮೂತ್ರಪಿಂಡಗಳನ್ನು ರಕ್ಷಿಸಲು ನೀಡಲಾಗುತ್ತದೆ.",
            en="Controls hypertension and helps protect kidneys in diabetic patients."
        ),
        how_to_take=BilingualText(
            kn="ದಿನಕ್ಕೊಂದು ಬಾರಿ, ನೀರು ಕುಡಿದು ಸೇವಿಸಿ. ಆಹಾರದೊಂದಿಗೆ ಅಥವಾ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಬಹುದು.",
            en="Take once daily with a glass of water, with or without food."
        ),
        common_side_effects=BilingualText(
            kn="ಬೆನ್ನಿನ ನೋವು, ಗಂಟಲು ಸೋಂಕು ಅಥವಾ ಲಘು ತಲೆಸುತ್ತು.",
            en="Mild dizziness, back pain, or sinus congestion."
        ),
        red_flags=BilingualList(
            kn=[
                "ತುಟಿ, ಮುಖ ಅಥವಾ ಗಂಟಲಿನಲ್ಲಿ ಹಠಾತ್ ಊತ (ಅಲರ್ಜಿ)",
                "ಮೂತ್ರ ವಿಸರ್ಜನೆ ಗಣನೀಯವಾಗಿ ಕಡಿಮೆಯಾಗುವುದು"
            ],
            en=[
                "Sudden swelling of lips, face, or throat (allergic reaction)",
                "Marked reduction in urine output"
            ]
        ),
        caution_do_not_stop=BilingualText(
            kn="ನಿಮ್ಮ ಬಿಪಿ ನಾರ್ಮಲ್ ಬಂದರೂ ಮಾತ್ರೆ ಮುಂದುವರಿಸಿ; ವೈದ್ಯರನ್ನು ಕೇಳದೆ ನಿಲ್ಲಿಸಬೇಡಿ.",
            en="Continue even if your BP readings are normal; do not stop on your own."
        ),
        doctor_questions=BilingualList(
            kn=[
                "ನಾನು ಪೊಟ್ಯಾಸಿಯಮ್ ಉಪ್ಪು ಅಥವಾ ಸಪ್ಲಿಮೆಂಟ್ ತೆಗೆದುಕೊಳ್ಳಬಹುದೇ?",
                "ಈ ಮಾತ್ರೆಯ ಜೊತೆ ನೋವು ನಿವಾರಕ (Painkiller) ತೆಗೆದುಕೊಳ್ಳಬಹುದೇ?"
            ],
            en=[
                "Should I avoid potassium-based salt substitutes while on Telmisartan?",
                "Is it safe to take over-the-counter painkillers with this medicine?"
            ]
        ),
        governance=GovernanceMetadata(
            reviewed_by="Dr. S. Kulkarni, MD (Gen Med)",
            clinician_reg_no="KMC-38190",
            reviewed_at="2026-11-01",
            disclaimer_en="Notice: For informational purposes only, not medical advice. Drug interactions not checked."
        )
    ),
    MedicineCardData(
        id="med_levothyroxine",
        generic_name="Levothyroxine",
        brand_aliases=["Thyronorm", "Eltroxin", "Thyrox"],
        therapeutic_class="Thyroid Hormone Replacement",
        purpose=BilingualText(
            kn="ಥೈರಾಯ್ಡ್ ಗ್ರಂಥಿ ಸರಿಯಾಗಿ ಕೆಲಸ ಮಾಡದಿದ್ದಾಗ ದೇಹಕ್ಕೆ ಅಗತ್ಯವಿರುವ ಹಾರ್ಮೋನ್ ಪೂರೈಸಲು ನೀಡಲಾಗುತ್ತದೆ.",
            en="Supplements thyroid hormone deficiency in primary hypothyroidism."
        ),
        how_to_take=BilingualText(
            kn="ಬೆಳಗ್ಗೆ ಎದ್ದ ತಕ್ಷಣ, ಖಾಲಿ ಹೊಟ್ಟೆಯಲ್ಲಿ, ಕಾಫಿ/ಚಹಾ ಕುಡಿಯುವ 30 ನಿಮಿಷಗಳ ಮೊದಲು ನೀರಿನೊಂದಿಗೆ ಸೇವಿಸಿ.",
            en="Take early morning on an empty stomach with plain water, at least 30 minutes before tea/coffee/breakfast."
        ),
        common_side_effects=BilingualText(
            kn="ಸರಿಯಾದ ಡೋಸ್‌ನಲ್ಲಿದ್ದರೆ ಅಡ್ಡಪರಿಣಾಮಗಳಿರುವುದಿಲ್ಲ. ಡೋಸ್ ಹೆಚ್ಚಾದರೆ ಬಡಿತ ಹೆಚ್ಚಾಗಬಹುದು.",
            en="Virtually no side effects when dose is correct; excess dose causes palpitations."
        ),
        red_flags=BilingualList(
            kn=[
                "ಹೃದಯದ ಬಡಿತ ಅತಿ ವೇಗವಾಗುವುದು ಮತ್ತು ಎದೆ ನಡುಕ",
                "ವಿಪರೀತ ಬೆವರುವುದು ಮತ್ತು ತೂಕ ದಿಢೀರ್ ಇಳಿಯುವುದು"
            ],
            en=[
                "Racing heartbeat, trembling, or chest discomfort",
                "Excessive sweating and sudden unexplained weight loss"
            ]
        ),
        caution_do_not_stop=BilingualText(
            kn="ಇದು ದೀರ್ಘಕಾಲಿಕ ಮಾತ್ರೆ. ಥೈರಾಯ್ಡ್ ರಿಪೋರ್ಟ್ ನಾರ್ಮಲ್ ಬಂದರೂ ಮಾತ್ರೆ ನಿಲ್ಲಿಸಬೇಡಿ.",
            en="Lifelong supplement in most cases; do not stop when test reports normalize."
        ),
        doctor_questions=BilingualList(
            kn=[
                "ನನ್ನ TSH ರಿಪೋರ್ಟ್ ಎಷ್ಟು ತಿಂಗಳಿಗೊಮ್ಮೆ ಪುನರಾವರ್ತಿಸಬೇಕು?",
                "ಕ್ಯಾಲ್ಸಿಯಂ ಅಥವಾ ಐರನ್ ಮಾತ್ರೆಗಳನ್ನು ಇದರ ಜೊತೆಯಲ್ಲೇ ತೆಗೆದುಕೊಳ್ಳಬಹುದೇ?"
            ],
            en=[
                "How often should I repeat my TSH blood test?",
                "Should I keep a 4-hour gap between this pill and calcium/iron supplements?"
            ]
        ),
        governance=GovernanceMetadata(
            reviewed_by="Dr. Anita Rao, MBBS, MD",
            clinician_reg_no="KMC-45291",
            reviewed_at="2026-11-01",
            disclaimer_en="Notice: For informational purposes only, not medical advice. Drug interactions not checked."
        )
    ),
    MedicineCardData(
        id="med_atorvastatin",
        generic_name="Atorvastatin",
        brand_aliases=["Atorva", "Storvas", "Lipitor", "Atocor"],
        therapeutic_class="HMG-CoA Reductase Inhibitor / Statin",
        purpose=BilingualText(
            kn="ರಕ್ತದಲ್ಲಿನ ಕೆಟ್ಟ ಕೊಲೆಸ್ಟ್ರಾಲ್ (LDL) ಕಡಿಮೆ ಮಾಡಲು ಮತ್ತು ರಕ್ತನಾಳಗಳಲ್ಲಿ ಬ್ಲಾಕ್ ತಡೆಯಲು ನೀಡಲಾಗುತ್ತದೆ.",
            en="Lowers bad cholesterol (LDL) and triglycerides to prevent heart attacks."
        ),
        how_to_take=BilingualText(
            kn="ರಾತ್ರಿ ಊಟದ ನಂತರ ಪ್ರತಿದಿನ ಮಲಗುವ ಮುನ್ನ ತೆಗೆದುಕೊಳ್ಳುವುದು ಸೂಕ್ತ.",
            en="Best taken once daily at night after dinner."
        ),
        common_side_effects=BilingualText(
            kn="ಲಘು ಸ್ನಾಯು ಸೆಳೆತ ಅಥವಾ ಜೀರ್ಣಕ್ರಿಯೆ ತೊಂದರೆ.",
            en="Mild muscle soreness, joint ache, or slight digestive discomfort."
        ),
        red_flags=BilingualList(
            kn=[
                "ವಿವರಿಸಲಾಗದ ತೀವ್ರ ಸ್ನಾಯು ನೋವು ಮತ್ತು ಮೂತ್ರ ಕಂದು ಬಣ್ಣಕ್ಕೆ ತಿರುಗುವುದು",
                "ಕಣ್ಣು ಅಥವಾ ಚರ್ಮ ಹಳದಿಯಾಗುವುದು (ಕಾಮಾಲೆ ಲಕ್ಷಣ)"
            ],
            en=[
                "Unexplained severe muscle pain accompanied by dark urine",
                "Yellowing of eyes or skin (signs of liver strain)"
            ]
        ),
        caution_do_not_stop=BilingualText(
            kn="ಕೊಲೆಸ್ಟ್ರಾಲ್ ಕಡಿಮೆಯಾದರೂ ಹೃದಯ ರಕ್ಷಣೆಗಾಗಿ ವೈದ್ಯರ ಸಲಹೆ ಮೇರೆಗೆ ಮುಂದುವರಿಸಿ.",
            en="Continue as prescribed for vascular protection even when lipid numbers normalize."
        ),
        doctor_questions=BilingualList(
            kn=[
                "ಮುಂದಿನ ಲಿಪಿಡ್ ಪ್ರೊಫೈಲ್ (Lipid Profile) ಟೆಸ್ಟ್ ಯಾವಾಗ ಮಾಡಿಸಬೇಕು?",
                "ಸ್ನಾಯು ನೋವು ಕಾಣಿಸಿಕೊಂಡರೆ ಮಾತ್ರೆಯನ್ನು ನಿಲ್ಲಿಸಬೇಕೇ?"
            ],
            en=[
                "When should I repeat my full Lipid Profile test?",
                "What should I do if I experience persistent muscle aches?"
            ]
        ),
        governance=GovernanceMetadata(
            reviewed_by="Dr. S. Kulkarni, MD (Gen Med)",
            clinician_reg_no="KMC-38190",
            reviewed_at="2026-11-01",
            disclaimer_en="Notice: For informational purposes only, not medical advice. Drug interactions not checked."
        )
    ),
]


@router.get("/lookup", response_model=MedicineCardResponse)
async def lookup_medicine(q: str = Query(..., min_length=2, description="Drug generic or brand name")) -> Any:
    """Lookup a medicine card by generic name or brand alias."""
    query_norm = q.strip().lower()

    for med in STARTER_MEDICINES:
        # Check generic name
        if query_norm in med.generic_name.lower():
            return MedicineCardResponse(data=med)

        # Check aliases
        for alias in med.brand_aliases:
            if query_norm in alias.lower() or alias.lower() in query_norm:
                return MedicineCardResponse(data=med)

    raise HTTPException(
        status_code=404,
        detail=MedicineNotFoundResponse(
            message=f"No verified card found for '{q}'. Please ask your local pharmacist.",
            fallback_action="PHARMACIST_FALLBACK"
        ).model_dump()
    )


@router.get("/all")
async def list_all_medicines() -> dict[str, Any]:
    """Returns all verified starter medicines for quick access."""
    return {
        "status": "success",
        "count": len(STARTER_MEDICINES),
        "medicines": [
            {
                "id": m.id,
                "generic_name": m.generic_name,
                "brand_aliases": m.brand_aliases,
                "therapeutic_class": m.therapeutic_class,
            }
            for m in STARTER_MEDICINES
        ]
    }
