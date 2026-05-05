# Capability: platform (MODIFIED)

## MODIFIED Requirements

### Requirement: Postgres persistence (was: SQLite persistence)
The service SHALL persist all data in **Postgres** via SQLAlchemy 2.x. The connection string is read from `DATABASE_URL`. SQLite remains supported for local development only.

#### Scenario: Production start
- **WHEN** `DATABASE_URL` points at Postgres
- **THEN** the service connects on startup; missing migrations cause a hard fail with a clear message.

### Requirement: Alembic migrations (was: No migrations)
Schema changes SHALL ship as Alembic migrations. `alembic upgrade head` is required before the app accepts traffic. Deleting the database is no longer the upgrade path.

### Requirement: Authenticated API (was: Single user, no auth)
All `/api/*` routes except `/api/auth/*` SHALL require an authenticated session. Unauthenticated requests receive `401`.

## UNCHANGED
- Single-process FastAPI app on port 8000.
- SPA delivery from `static/`.
- OpenAPI at `/docs` (now requires login when called from a browser session, but stays public for tooling that passes a session token).
