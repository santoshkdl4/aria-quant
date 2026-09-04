# ARIA QUANT Decision Log

All major architectural and business logic decisions must be recorded here to persist context for future AI agents.

## DEC-0001: Architecture & Tech Stack Selection
**Date:** 2026-09-04
**Decision:** Select FastAPI for backend, React/Vite for frontend dashboard, SQLite for transactional state, and DuckDB + Parquet for analytical market data.
**Alternatives Considered:** Streamlit/PySide6 (for UI), PostgreSQL (for database).
**Reason:** The prompt explicitly requires a premium dark web dashboard and highly portable databases (SQLite/DuckDB). Streamlit is too tightly coupled, and PostgreSQL hinders zero-config portability to a new laptop.
**Consequences:** Complete separation of concerns between backend (engine) and frontend (dashboard). The system can run headlessly.

## DEC-0002: Split Databases for State and Memory
**Date:** 2026-09-04
**Decision:** Create two separate SQLite databases (`aria_state.db` and `aria_memory.db`).
**Alternatives Considered:** Single monolithic SQLite database.
**Reason:** Memory grows unboundedly and stores historical facts, experiments, and graveyard strategies. State is transactional (active jobs, orders, agents). Splitting them improves backup strategies (e.g., daily memory backups, hourly state checkpoints).
**Consequences:** We must manage two SQLAlchemy engines and session makers. Queries spanning both databases are not possible natively in SQLite, requiring application-level joins if ever needed (rare).
