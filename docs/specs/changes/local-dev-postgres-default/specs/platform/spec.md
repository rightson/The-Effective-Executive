---
status: active
created: 2026-05-07
---

# Delta: platform — local dev defaults to Postgres

Apply on accept.

## MODIFIED Requirement: Durable persistence

Because habit evidence must survive review cycles and schema evolution, all environments — local development and production — SHALL use Postgres through SQLAlchemy 2.x. SQLite is retained only as a read source for `manage.py import-sqlite` to migrate legacy data.

#### Scenario: Local development start
- **WHEN** a contributor runs `python3 manage.py db init` on a fresh checkout
- **THEN** the command SHALL provision a `.env` from `.env.example` if missing, bootstrap the Postgres role and database (asking for an admin connection URL when the configured role lacks privileges), and run migrations to head.

#### Scenario: Production start
- **WHEN** `DATABASE_URL` points at Postgres
- **THEN** the service connects on startup and requires migrations to be current before accepting traffic.

## MODIFIED Technical Shape line

Replace:

> Postgres for durable persistence; SQLite for local development.

With:

> Postgres for durable persistence in all environments. SQLite is retained only as an import source for legacy data via `manage.py import-sqlite`.
