import { useEffect, useState } from 'react';

interface HealthData {
  status: string;
  database: string;
  db_value: string;
  app_env?: string;
}

export default function App() {
  const [data, setData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const endpoint = `${apiUrl}/api/health`;
      const res = await fetch(endpoint);
      if (!res.ok) {
        throw new Error(`HTTP error ${res.status}`);
      }
      const json: HealthData = await res.json();
      setData(json);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <main className="card" role="main">
      <h1>ReportSaathi System Health</h1>
      <p>Plain-Language Medicine & Lab Report Explainer — Foundation Skeleton</p>

      {loading && (
        <div>
          <span className="status-badge loading" data-testid="status-loading">
            Checking backend & database...
          </span>
        </div>
      )}

      {error && (
        <div>
          <span className="status-badge error" data-testid="status-error">
            Error: {error}
          </span>
          <div style={{ marginTop: '1rem' }}>
            <button onClick={fetchHealth}>Retry</button>
          </div>
        </div>
      )}

      {data && !loading && (
        <section aria-label="Backend status" data-testid="health-data">
          <div>
            <strong>Service Status: </strong>
            <span
              className={`status-badge ${data.status === 'healthy' ? 'healthy' : 'error'}`}
              data-testid="service-status"
            >
              {data.status}
            </span>
          </div>

          <div style={{ marginTop: '0.75rem' }}>
            <strong>Database Connection: </strong>
            <span data-testid="db-status">{data.database}</span>
          </div>

          <div style={{ marginTop: '0.75rem' }}>
            <strong>Value Read From Database: </strong>
            <div className="db-output" data-testid="db-value">
              {data.db_value}
            </div>
          </div>

          {data.app_env && (
            <div style={{ marginTop: '0.75rem' }}>
              <strong>Environment: </strong>
              <span data-testid="app-env">{data.app_env}</span>
            </div>
          )}

          <div style={{ marginTop: '1.25rem' }}>
            <button onClick={fetchHealth} data-testid="refresh-button">
              Refresh Health Check
            </button>
          </div>
        </section>
      )}
    </main>
  );
}
