import { useEffect, useState, useRef } from 'react';
import './index.css';

/* ───────────── Types ───────────── */
interface HealthData {
  status: string;
  database: string;
  db_value: string;
  app_env?: string;
}
interface ExtractedParam {
  test_id: string;
  name: string;
  name_kn?: string;
  found_value: number;
  unit: string;
  lab_printed_range: { min?: number | null; max?: number | null };
  status: 'WITHIN_RANGE' | 'ABOVE_RANGE' | 'BELOW_RANGE' | 'RANGE_NOT_SPECIFIED_ON_REPORT' | 'CRITICAL_VALUE';
  is_critical: boolean;
  critical_escalation_message?: string;
  desc_kn?: string;
  desc_en?: string;
  doctor_q_kn?: string[];
  doctor_q_en?: string[];
}
interface LabReportResult {
  status: string;
  document_type: string;
  confidence_score: number;
  is_critical: boolean;
  critical_alert?: string | null;
  extracted_parameters: ExtractedParam[];
  raw_text?: string;
  message?: string;
  governance?: {
    reviewed_by: string;
    reg_number: string;
    disclaimer_kn: string;
    disclaimer_en: string;
  };
}
interface MedicineCard {
  id: string;
  generic_name: string;
  brand_aliases: string[];
  therapeutic_class: string;
  purpose: { kn: string; en: string };
  how_to_take: { kn: string; en: string };
  common_side_effects: { kn: string; en: string };
  red_flags: { kn: string[]; en: string[] };
  caution_do_not_stop: { kn: string; en: string };
  doctor_questions: { kn: string[]; en: string[] };
  governance: {
    reviewed_by: string;
    clinician_reg_no: string;
    reviewed_at: string;
    disclaimer_en: string;
  };
}

/* ───────────── Fixture Definitions ───────────── */
const FIXTURES = [
  { id: 'fixture_01', label: 'Normal Sugar & Lipids', labelKn: 'ಸಾಮಾನ್ಯ ಸಕ್ಕರೆ & ಲಿಪಿಡ್', indicator: 'green', critical: false },
  { id: 'fixture_02', label: 'High Blood Sugar (HbA1c 8.4%)', labelKn: 'ಅಧಿಕ ರಕ್ತ ಸಕ್ಕರೆ (HbA1c 8.4%)', indicator: 'yellow', critical: false },
  { id: 'fixture_03', label: 'Critical Potassium (6.4 mEq/L)', labelKn: 'ತೀವ್ರ ಪೊಟ್ಯಾಸಿಯಮ್ (6.4 mEq/L)', indicator: 'red', critical: true },
  { id: 'fixture_04', label: 'Severe Low Sugar (42 mg/dL)', labelKn: 'ತೀವ್ರ ಕಡಿಮೆ ಸಕ್ಕರೆ (42 mg/dL)', indicator: 'red', critical: true },
  { id: 'fixture_05', label: 'Elevated Creatinine (2.4 mg/dL)', labelKn: 'ಎತ್ತರಿಸಿದ ಕ್ರಿಯೇಟಿನಿನ್ (2.4 mg/dL)', indicator: 'yellow', critical: false },
  { id: 'fixture_06', label: 'High TSH (Thyroid 8.9 uIU)', labelKn: 'ಅಧಿಕ TSH (ಥೈರಾಯ್ಡ್ 8.9 uIU)', indicator: 'yellow', critical: false },
  { id: 'fixture_07', label: 'Low Platelets (42,000 /cumm)', labelKn: 'ಕಡಿಮೆ ಪ್ಲೇಟ್‌ಲೆಟ್ (42,000 /cumm)', indicator: 'yellow', critical: false },
  { id: 'fixture_09', label: 'Test Handwriting Rejection', labelKn: 'ಕೈಬರಹ ತಿರಸ್ಕರಣ ಪರೀಕ್ಷೆ', indicator: 'pencil', critical: false },
];

/* ───────────── Helpers ───────────── */
function StatusDot({ indicator, critical }: { indicator: string; critical: boolean }) {
  if (indicator === 'pencil') return <span className="fix-icon">✏️</span>;
  if (critical) return <span className="fix-dot fix-dot--red">🚨</span>;
  if (indicator === 'green') return <span className="fix-dot fix-dot--green">●</span>;
  return <span className="fix-dot fix-dot--yellow">●</span>;
}

function StatusBadge({ status }: { status: ExtractedParam['status'] }) {
  const map: Record<string, { label: string; cls: string }> = {
    WITHIN_RANGE: { label: 'Normal', cls: 'badge--green' },
    ABOVE_RANGE: { label: 'High', cls: 'badge--yellow' },
    BELOW_RANGE: { label: 'Low', cls: 'badge--yellow' },
    CRITICAL_VALUE: { label: 'CRITICAL', cls: 'badge--red' },
    RANGE_NOT_SPECIFIED_ON_REPORT: { label: 'Range N/A', cls: 'badge--gray' },
  };
  const { label, cls } = map[status] ?? { label: status, cls: 'badge--gray' };
  return <span className={`badge ${cls}`}>{label}</span>;
}

/* ───────────── Main App ───────────── */
export default function App() {
  const [activeTab, setActiveTab] = useState<'lab' | 'medicine' | 'health'>('lab');
  const [lang, setLang] = useState<'en' | 'kn'>('en');

  /* Health */
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  /* Lab */
  const [labResult, setLabResult] = useState<LabReportResult | null>(null);
  const [labLoading, setLabLoading] = useState(false);
  const [labError, setLabError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  /* Medicine */
  const [searchQuery, setSearchQuery] = useState('');
  const [medicineCard, setMedicineCard] = useState<MedicineCard | null>(null);
  const [medLoading, setMedLoading] = useState(false);
  const [medError, setMedError] = useState<string | null>(null);

  const apiUrl = import.meta.env.VITE_API_URL || '';

  /* Fetch health on mount */
  useEffect(() => { fetchHealth(); }, []);

  async function fetchHealth() {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const res = await fetch(`${apiUrl}/api/health`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setHealthData(await res.json());
    } catch (e: unknown) {
      setHealthError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setHealthLoading(false);
    }
  }

  async function analyseFixture(fixtureId: string) {
    setLabLoading(true);
    setLabError(null);
    setLabResult(null);
    setActiveTab('lab');
    try {
      const res = await fetch(`${apiUrl}/api/lab-reports/analyse-fixture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fixture_id: fixtureId }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail?.message ?? err.detail ?? `HTTP ${res.status}`);
      }
      setLabResult(await res.json());
    } catch (e: unknown) {
      setLabError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLabLoading(false);
    }
  }

  async function analyseFile(file: File) {
    setLabLoading(true);
    setLabError(null);
    setLabResult(null);
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await fetch(`${apiUrl}/api/lab-reports/analyse`, { method: 'POST', body: form });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail?.message ?? err.detail ?? `HTTP ${res.status}`);
      }
      setLabResult(await res.json());
    } catch (e: unknown) {
      setLabError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLabLoading(false);
    }
  }

  async function lookupMedicine(q: string) {
    if (!q.trim()) return;
    setMedLoading(true);
    setMedError(null);
    setMedicineCard(null);
    try {
      const res = await fetch(`${apiUrl}/api/medicines/lookup?q=${encodeURIComponent(q)}`);
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail?.message ?? 'Medicine not found');
      }
      const json = await res.json();
      setMedicineCard(json.data);
    } catch (e: unknown) {
      setMedError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setMedLoading(false);
    }
  }

  /* File drop */
  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) analyseFile(file);
  }

  const t = (en: string, kn: string) => lang === 'kn' ? kn : en;

  /* ═══════════════ RENDER ═══════════════ */
  return (
    <div className="app-shell">

      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-brand">
          <span className="header-leaf">🌿</span>
          <div>
            <div className="header-title">ReportSaathi</div>
            <div className="header-sub">{t('Plain-Language Medicine & Lab Report Explainer', 'ಸರಳ ಭಾಷೆಯ ಔಷಧ ಮತ್ತು ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್ ವಿವರಕ')}</div>
          </div>
        </div>
        <div className="lang-toggle">
          <button className={lang === 'en' ? 'lang-btn active' : 'lang-btn'} onClick={() => setLang('en')}>English</button>
          <button className={lang === 'kn' ? 'lang-btn active' : 'lang-btn'} onClick={() => setLang('kn')}>ಕನ್ನಡ</button>
        </div>
      </header>

      <div className="app-body">

        {/* ── Tabs ── */}
        <div className="tab-bar">
          <button className={activeTab === 'lab' ? 'tab active' : 'tab'} onClick={() => setActiveTab('lab')}>
            📋 {t('Upload Lab Report', 'ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್ ಅಪ್‌ಲೋಡ್')}
          </button>
          <button className={activeTab === 'medicine' ? 'tab active' : 'tab'} onClick={() => setActiveTab('medicine')}>
            💊 {t('Medicine Explainer', 'ಔಷಧ ವಿವರಕ')}
          </button>
          <button className={activeTab === 'health' ? 'tab active' : 'tab'} onClick={() => setActiveTab('health')}>
            ⚙️ {t('System Health', 'ಸಿಸ್ಟಮ್ ಆರೋಗ್ಯ')}
          </button>
        </div>

        {/* ── DPDP Banner ── */}
        <div className="dpdp-banner">
          🔒 {t(
            'DPDP Act 2023 Privacy: Your report is parsed transiently in memory and deleted within 10 minutes. Never stored or shared.',
            'DPDP ಕಾಯ್ದೆ 2023 ಗೌಪ್ಯತೆ: ನಿಮ್ಮ ರಿಪೋರ್ಟ್ ತಾತ್ಕಾಲಿಕವಾಗಿ ಮೆಮೊರಿಯಲ್ಲಿ ಪಾರ್ಸ್ ಆಗುತ್ತದೆ ಮತ್ತು 10 ನಿಮಿಷಗಳಲ್ಲಿ ಅಳಿಸಲ್ಪಡುತ್ತದೆ.'
          )}
        </div>

        {/* ════ TAB: Lab Report ════ */}
        {activeTab === 'lab' && (
          <div className="tab-content">

            {/* Upload Zone */}
            {!labResult && !labLoading && (
              <div
                className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".jpg,.jpeg,.png,.pdf"
                  style={{ display: 'none' }}
                  onChange={(e) => { const f = e.target.files?.[0]; if (f) analyseFile(f); }}
                />
                <div className="upload-icon">📄</div>
                <div className="upload-text">{t('Click or drop your Lab Report photo or PDF here to upload', 'ನಿಮ್ಮ ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್ ಫೋಟೋ ಅಥವಾ PDF ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ ಅಥವಾ ಡ್ರಾಪ್ ಮಾಡಿ')}</div>
                <div className="upload-hint">{t('Supported formats: JPG, PNG, PDF (Printed lab reports only)', 'ಬೆಂಬಲಿತ ಸ್ವರೂಪಗಳು: JPG, PNG, PDF (ಮುದ್ರಿತ ಲ್ಯಾಬ್ ರಿಪೋರ್ಟ್ ಮಾತ್ರ)')}</div>
              </div>
            )}

            {/* Fixtures */}
            {!labResult && !labLoading && (
              <div className="fixtures-section">
                <div className="fixtures-label">{t('Or click a verified test fixture to preview instant explanation:', 'ಅಥವಾ ತಕ್ಷಣ ವಿವರಣೆ ಪೂರ್ವವೀಕ್ಷಣೆಗಾಗಿ ಪರಿಶೀಲಿತ ಟೆಸ್ಟ್ ಫಿಕ್ಸ್‌ಚರ್ ಕ್ಲಿಕ್ ಮಾಡಿ:')}</div>
                <div className="fixtures-grid">
                  {FIXTURES.map((f) => (
                    <button
                      key={f.id}
                      className={`fixture-btn ${f.critical ? 'fixture-btn--critical' : ''}`}
                      onClick={() => analyseFixture(f.id)}
                    >
                      <StatusDot indicator={f.indicator} critical={f.critical} />
                      {lang === 'kn' ? f.labelKn : f.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Loading */}
            {labLoading && (
              <div className="state-box state-box--loading">
                <div className="spinner" />
                <p>{t('Analysing report…', 'ರಿಪೋರ್ಟ್ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ…')}</p>
              </div>
            )}

            {/* Error */}
            {labError && (
              <div className="state-box state-box--error">
                <strong>⚠️ {t('Error', 'ದೋಷ')}:</strong> {labError}
                <div style={{ marginTop: '0.75rem' }}>
                  <button className="btn-secondary" onClick={() => setLabError(null)}>
                    {t('← Back', '← ಹಿಂದೆ')}
                  </button>
                </div>
              </div>
            )}

            {/* Results */}
            {labResult && !labLoading && (
              <div className="result-panel">
                {/* Critical Alert */}
                {labResult.is_critical && labResult.critical_alert && (
                  <div className="critical-alert">
                    🚨 <strong>{t('CRITICAL ALERT', 'ತೀವ್ರ ಎಚ್ಚರಿಕೆ')}:</strong> {labResult.critical_alert}
                  </div>
                )}

                <div className="result-meta">
                  <span>📄 {labResult.document_type}</span>
                  <span>🎯 {t('Confidence', 'ನಂಬಿಕೆ')}: {Math.round((labResult.confidence_score ?? 0) * 100)}%</span>
                </div>

                <div className="params-grid">
                  {labResult.extracted_parameters.map((p) => (
                    <div key={p.test_id} className={`param-card ${p.is_critical ? 'param-card--critical' : ''}`}>
                      <div className="param-name">{lang === 'kn' && p.name_kn ? p.name_kn : p.name}</div>
                      <div className="param-value">{p.found_value} <span className="param-unit">{p.unit}</span></div>
                      <StatusBadge status={p.status} />
                      {(p.lab_printed_range.min != null || p.lab_printed_range.max != null) && (
                        <div className="param-range">
                          {t('Range', 'ಶ್ರೇಣಿ')}: {p.lab_printed_range.min ?? '—'} – {p.lab_printed_range.max ?? '—'}
                        </div>
                      )}
                      {p.is_critical && p.critical_escalation_message && (
                        <div className="param-critical-msg">🚨 {p.critical_escalation_message}</div>
                      )}
                      {lang === 'kn' && p.desc_kn && <div className="param-desc">{p.desc_kn}</div>}
                      {lang === 'en' && p.desc_en && <div className="param-desc">{p.desc_en}</div>}
                    </div>
                  ))}
                </div>

                {labResult.governance && (
                  <div className="governance-footer">
                    👨‍⚕️ {labResult.governance.reviewed_by} · {labResult.governance.reg_number}
                    <div style={{ marginTop: '0.25rem', fontSize: '0.75rem', color: '#666' }}>
                      {lang === 'kn' ? labResult.governance.disclaimer_kn : labResult.governance.disclaimer_en}
                    </div>
                  </div>
                )}

                <button className="btn-secondary" style={{ marginTop: '1rem' }} onClick={() => { setLabResult(null); setLabError(null); }}>
                  {t('← Analyse Another Report', '← ಮತ್ತೊಂದು ರಿಪೋರ್ಟ್ ವಿಶ್ಲೇಷಿಸಿ')}
                </button>
              </div>
            )}
          </div>
        )}

        {/* ════ TAB: Medicine Explainer ════ */}
        {activeTab === 'medicine' && (
          <div className="tab-content">
            <div className="med-search-row">
              <input
                className="med-search-input"
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && lookupMedicine(searchQuery)}
                placeholder={t('Enter medicine name (e.g. Glycomet, Thyronorm…)', 'ಔಷಧ ಹೆಸರು ನಮೂದಿಸಿ (ಉದಾ: Glycomet, Thyronorm…)')}
              />
              <button className="btn-primary" onClick={() => lookupMedicine(searchQuery)} disabled={medLoading}>
                {medLoading ? '…' : t('Search', 'ಹುಡುಕಿ')}
              </button>
            </div>

            {/* Quick picks */}
            <div className="quick-picks">
              {['Glycomet', 'Thyronorm', 'Amlong', 'Telma', 'Atorva'].map((q) => (
                <button key={q} className="quick-pick-btn" onClick={() => { setSearchQuery(q); lookupMedicine(q); }}>{q}</button>
              ))}
            </div>

            {medError && <div className="state-box state-box--error">⚠️ {medError}</div>}

            {medicineCard && (
              <div className="med-card">
                <div className="med-card-header">
                  <div className="med-generic">{medicineCard.generic_name}</div>
                  <div className="med-class">{medicineCard.therapeutic_class}</div>
                  <div className="med-aliases">{medicineCard.brand_aliases.join(', ')}</div>
                </div>
                <div className="med-section">
                  <div className="med-section-title">🎯 {t('Purpose', 'ಉದ್ದೇಶ')}</div>
                  <div>{lang === 'kn' ? medicineCard.purpose.kn : medicineCard.purpose.en}</div>
                </div>
                <div className="med-section">
                  <div className="med-section-title">🕐 {t('How to Take', 'ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳಬೇಕು')}</div>
                  <div>{lang === 'kn' ? medicineCard.how_to_take.kn : medicineCard.how_to_take.en}</div>
                </div>
                <div className="med-section">
                  <div className="med-section-title">⚠️ {t('Side Effects', 'ಅಡ್ಡಪರಿಣಾಮಗಳು')}</div>
                  <div>{lang === 'kn' ? medicineCard.common_side_effects.kn : medicineCard.common_side_effects.en}</div>
                </div>
                <div className="med-section">
                  <div className="med-section-title">🚨 {t('Red Flags – See Doctor Immediately', 'ಕೆಂಪು ಸಂಕೇತಗಳು – ತಕ್ಷಣ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ')}</div>
                  <ul className="med-list">
                    {(lang === 'kn' ? medicineCard.red_flags.kn : medicineCard.red_flags.en).map((f: string, i: number) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </div>
                <div className="med-section">
                  <div className="med-section-title">🛑 {t('Do Not Stop Without Doctor', 'ವೈದ್ಯರ ಸಲಹೆ ಇಲ್ಲದೆ ನಿಲ್ಲಿಸಬೇಡಿ')}</div>
                  <div>{lang === 'kn' ? medicineCard.caution_do_not_stop.kn : medicineCard.caution_do_not_stop.en}</div>
                </div>
                <div className="med-section">
                  <div className="med-section-title">❓ {t('Questions to Ask Your Doctor', 'ನಿಮ್ಮ ವೈದ್ಯರಿಗೆ ಕೇಳಬೇಕಾದ ಪ್ರಶ್ನೆಗಳು')}</div>
                  <ul className="med-list">
                    {(lang === 'kn' ? medicineCard.doctor_questions.kn : medicineCard.doctor_questions.en).map((q: string, i: number) => (
                      <li key={i}>{q}</li>
                    ))}
                  </ul>
                </div>
                <div className="med-governance">
                  👨‍⚕️ {medicineCard.governance.reviewed_by} · {medicineCard.governance.clinician_reg_no} · {medicineCard.governance.reviewed_at}
                  <div style={{ marginTop: '0.25rem', fontSize: '0.75rem', color: '#666' }}>{medicineCard.governance.disclaimer_en}</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ════ TAB: System Health ════ */}
        {activeTab === 'health' && (
          <div className="tab-content">
            <div className="health-card">
              <h2 className="health-title">⚙️ {t('System Health', 'ಸಿಸ್ಟಮ್ ಆರೋಗ್ಯ')}</h2>
              {healthLoading && <div className="state-box state-box--loading"><div className="spinner" /><p>{t('Checking backend…', 'ಬ್ಯಾಕೆಂಡ್ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ…')}</p></div>}
              {healthError && <div className="state-box state-box--error">⚠️ {healthError}</div>}
              {healthData && !healthLoading && (
                <div className="health-rows">
                  <div className="health-row">
                    <span className="health-label">{t('Service Status', 'ಸೇವಾ ಸ್ಥಿತಿ')}</span>
                    <span className={`badge ${healthData.status === 'healthy' ? 'badge--green' : 'badge--red'}`}>{healthData.status}</span>
                  </div>
                  <div className="health-row">
                    <span className="health-label">{t('Database', 'ಡೇಟಾಬೇಸ್')}</span>
                    <span className="badge badge--green">{healthData.database}</span>
                  </div>
                  <div className="health-row">
                    <span className="health-label">{t('DB Value (live read)', 'DB ಮೌಲ್ಯ (ನೇರ ಓದು)')}</span>
                    <code className="health-value">{healthData.db_value}</code>
                  </div>
                  {healthData.app_env && (
                    <div className="health-row">
                      <span className="health-label">{t('Environment', 'ಪರಿಸರ')}</span>
                      <code className="health-value">{healthData.app_env}</code>
                    </div>
                  )}
                </div>
              )}
              <button className="btn-secondary" style={{ marginTop: '1rem' }} onClick={fetchHealth}>
                {t('Refresh', 'ರಿಫ್ರೆಶ್')}
              </button>
            </div>
          </div>
        )}

      </div>

      {/* ── Footer ── */}
      <footer className="app-footer">
        {t('ReportSaathi · Educational use only · Not medical advice', 'ReportSaathi · ಶೈಕ್ಷಣಿಕ ಉದ್ದೇಶಕ್ಕಾಗಿ ಮಾತ್ರ · ವೈದ್ಯಕೀಯ ಸಲಹೆ ಅಲ್ಲ')}
      </footer>
    </div>
  );
}
