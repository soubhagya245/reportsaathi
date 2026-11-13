export interface LabPrintedRange {
  min: number | null;
  max: number | null;
}

export type LabParameterStatus =
  | 'WITHIN_RANGE'
  | 'ABOVE_RANGE'
  | 'BELOW_RANGE'
  | 'RANGE_NOT_SPECIFIED_ON_REPORT';

export interface ExtractedLabParameter {
  test_id: string;
  name: string;
  found_value: number;
  unit: string;
  lab_printed_range: LabPrintedRange;
  status: LabParameterStatus;
  is_critical: boolean;
  critical_escalation_message?: string | null;
}

export interface LabExtractResponse {
  status: 'success';
  document_type: string;
  confidence_score: number;
  extracted_parameters: ExtractedLabParameter[];
}

export interface LabExtractErrorResponse {
  status: 'rejected';
  code: 'HANDWRITING_OR_ILLEGIBLE_DETECTED';
  message: string;
}
