export interface HealthResponse {
  status: 'healthy';
  database: 'connected';
  db_value: string;
  app_env?: string;
}
