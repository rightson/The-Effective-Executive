# Design: multi-tenancy

## 1. Runtime stack

The service uses the existing FastAPI application with SQLAlchemy 2.x, Alembic migrations, password authentication, and Postgres for deployable multi-user persistence. The static SPA remains served from `/static/`.

This design keeps the Drucker domain logic in the current backend and treats multi-user support as an incremental platform change: add accounts, sessions, org memberships, user-scoped rows, and manager read-only rollups.

## 2. Multi-tenancy model

- **Tenant unit:** `user`. An `org` exists only to scope read-only manager views.
- **Isolation:** every domain row carries `user_id NOT NULL` with an index. All queries filter by `current_user.id`. No row-level security in v1; enforced in the application layer.
- **Manager view:** `org_memberships(user_id, org_id, role)` where role is one of `{member, manager}`. A manager `GET /api/dashboard?user_id=<report>` succeeds iff the target shares an org and the caller has `role=manager`.
- **Auth:** session cookie (`HttpOnly`, `Secure`, `SameSite=Lax`), argon2 password hashes, CSRF via double-submit token on state-changing requests.
- **Sessions:** server-side session table (`id, user_id, created_at, expires_at, revoked_at`) so sessions can be revoked directly.

## 3. Migration from SQLite

A one-shot script `scripts/import_sqlite.py` reads `effective_executive.db`, prompts for an account, and inserts every row under that `user_id`. It is not part of the runtime path.

## 4. Open questions

- Do we want invite links for org joining, or admin-controlled add? Default: invite links, expiring.
- Is there ever a global team time-block rollup, or strictly per-user with a manager peek? Default: per-user only in v1.
