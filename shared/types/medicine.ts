export interface BilingualText {
  kn: string;
  en: string;
}

export interface BilingualList {
  kn: string[];
  en: string[];
}

export interface GovernanceMetadata {
  reviewed_by: string;
  clinician_reg_no: string;
  reviewed_at: string;
  disclaimer_en: string;
}

export interface MedicineCardData {
  id: string;
  generic_name: string;
  brand_aliases: string[];
  therapeutic_class: string;
  purpose: BilingualText;
  how_to_take: BilingualText;
  common_side_effects: BilingualText;
  red_flags: BilingualList;
  caution_do_not_stop: BilingualText;
  doctor_questions: BilingualList;
  governance: GovernanceMetadata;
}

export interface MedicineCardResponse {
  status: 'success';
  data: MedicineCardData;
}

export interface MedicineNotFoundResponse {
  status: 'not_found';
  message: string;
  fallback_action: 'PHARMACIST_FALLBACK';
}
