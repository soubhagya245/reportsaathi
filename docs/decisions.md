# Architecture & Implementation Decision Records (ADRs)

## ADR-001: Monorepo Foundation & Walking Skeleton Structure (TASK-01)
* **Date:** 2026-11-13
* **Status:** Accepted

### Context
To implement the plain-language medicine and lab report explainer for Karnataka citizens with clinical safety and zero defect deployments, the project requires a strict separation of concerns, deterministic contract-first data structures, automated quality gates, and a deployed walking skeleton.

### Decision
1. **Repository Layout:**
   - `shared/`: TypeScript contract interfaces for Meta WhatsApp payloads, medicine card responses, lab extraction models, DPDP erasure, and system health.
   - `backend/`: Python 3.11+ FastAPI service with Pydantic v2 data models, SQLite with Write-Ahead Logging (WAL) enabled, and `GET /api/health` reading directly from the database.
   - `frontend/`: Lightweight Vite + React + TypeScript web app (<150KB bundle) with zero heavy external UI frameworks, presenting system health and verified DB data.
2. **Quality Tooling & Deterministic Gates:**
   - Backend: `ruff` (linting & formatting), `mypy` (strict static type checking), `pytest` + `pytest-asyncio` (contract unit tests and automated smoke test).
   - Frontend: `eslint` (flat config), `tsc` (strict typecheck), `vitest` with `@testing-library/react`.
   - CI Pipeline: GitHub Actions running parallel matrix checks on every push and PR.
   - Staging: Multi-container `docker-compose.staging.yml` with health checks.
3. **Database & Data Minimization:**
   - SQLite WAL mode initialized via deterministic startup lifecycle (`lifespan`).
   - Seed table `system_metadata` created to assert live DB read capabilities over `/api/health`.

### Consequences
- Zero product features (no unvetted state machines, AI, or OCR) were built ahead of time.
- API schemas and contracts in `backend/app/schemas/` and `shared/types/` are strictly aligned with `docs/06a-api-contract.md`.
