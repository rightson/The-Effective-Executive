# Design: owned habit records

## Product Necessity

The design exists to preserve three Drucker requirements:

- actual time, contribution, strengths, priorities, and decisions must be attributable to the person practicing the habit;
- each user's journal must remain private enough for honest diagnosis;
- managers may receive limited aggregate signals to coach effectiveness habits without owning another person's records.

## Runtime Shape

The service uses the existing FastAPI application with SQLAlchemy 2.x, Alembic migrations, password authentication, and Postgres for durable persistence. The static SPA remains served from `/static/`.

The design keeps Drucker domain logic primary: identity defines whose habit practice is being recorded, ownership protects raw reflection, and manager rollups expose only bounded coaching signals.

## Multi-Tenancy Model

- **Tenant unit:** `user`.
- **Domain ownership:** every time entry, contribution, strength, priority, and decision has `user_id NOT NULL` with an index.
- **Isolation:** all raw domain queries filter by `current_user.id`; cross-user raw reads return `404`.
- **Org scope:** `orgs` and `org_memberships` exist only to authorize read-only manager rollups.
- **Manager authorization:** a manager can call `GET /api/dashboard?user_id=<report>` only when caller and target share an org where the caller has `role=manager`.
- **Writes:** no write endpoint accepts a cross-user override.

## Auth Model

- Passwords are hashed with argon2id.
- Sessions are server-side rows with `created_at`, `expires_at`, and `revoked_at`.
- Cookies are `HttpOnly`, `Secure`, and `SameSite=Lax`.
- State-changing requests require a double-submit CSRF token.

## Migration Model

Schema changes use Alembic. Existing SQLite data can be moved by `scripts/import_sqlite.py`, which inserts old records under a selected account. The import script exists only to preserve prior habit evidence and is not part of normal request handling.

## Open Questions

- Should org joining use expiring invite links or admin-controlled creation?
- Should future manager views include trend summaries while still hiding raw notes?
