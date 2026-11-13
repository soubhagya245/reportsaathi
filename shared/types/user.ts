export interface DataPurgeRequest {
  wa_phone_hash: string;
}

export interface DataPurgeResponse {
  status: 'purged';
  purged_records: string[];
}
