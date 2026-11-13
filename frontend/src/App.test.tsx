import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';

describe('App component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders loading state initially', () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => new Promise(() => {}));
    render(<App />);
    expect(screen.getByTestId('status-loading')).toBeInTheDocument();
  });

  it('fetches and displays database value from GET /api/health', async () => {
    const mockHealth = {
      status: 'healthy',
      database: 'connected',
      db_value: 'ReportSaathi System Seed v1.0 - SQLite Verified',
      app_env: 'staging',
    };

    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => mockHealth,
    } as unknown as Response);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId('service-status')).toHaveTextContent('healthy');
    });

    expect(screen.getByTestId('db-status')).toHaveTextContent('connected');
    expect(screen.getByTestId('db-value')).toHaveTextContent(
      'ReportSaathi System Seed v1.0 - SQLite Verified'
    );
  });

  it('renders error badge when backend call fails', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new Error('Network error'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId('status-error')).toHaveTextContent('Error: Network error');
    });
  });
});
