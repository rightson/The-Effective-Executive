# Tasks

Tasks are ordered by the Drucker behavior they protect. Identity, persistence, and manager rollups are implementation mechanisms; the goal is honest diagnosis, attributable commitments, protected reflection, and bounded coaching.

## 1. Preserve habit evidence durably

- [x] 1.1 Add Postgres dependency (`psycopg[binary]`).
- [x] 1.2 Read `DATABASE_URL`; keep SQLite only as a local development fallback.
- [x] 1.3 Add Alembic and baseline migration.
- [x] 1.4 Provide local Postgres through `docker-compose.yml`.

**Acceptance evidence:** an empty database can be migrated to the current schema without losing the structure required for Drucker records.

## 2. Give every habit journal an owner

- [x] 2.1 Create `users`, `sessions`, `orgs`, and `org_memberships`.
- [x] 2.2 Add argon2id password hashing.
- [x] 2.3 Implement signup, login, logout, and current-user endpoints.
- [x] 2.4 Add session-cookie based `current_user`.
- [x] 2.5 Add CSRF protection for state-changing routes.

**Acceptance evidence:** a user can authenticate and all private routes reject unauthenticated requests.

## 3. Protect raw Drucker records by owner

- [x] 3.1 Add indexed `user_id` foreign keys to time entries, contributions, strengths, priorities, and decisions.
- [x] 3.2 Filter all raw list/read/update/delete queries by `current_user.id`.
- [x] 3.3 Set `user_id` from the authenticated user on creates.
- [x] 3.4 Scope time analysis and self dashboard to the authenticated user.

**Acceptance evidence:** user A cannot discover or mutate user B's raw records.

## 4. Enable habit coaching without surveillance

- [x] 4.1 Add `GET /api/org/members` for managers.
- [x] 4.2 Add authorized `GET /api/dashboard?user_id=<report>`.
- [x] 4.3 Keep all write endpoints self-scoped.

**Acceptance evidence:** managers can see report rollups, but cannot write into or browse raw report journals.

## 5. Make the habit flow usable

- [x] 5.1 Add login and signup screens.
- [x] 5.2 Add SPA auth guard and 401 handling.
- [x] 5.3 Add manager picker when report rollups are available.

**Acceptance evidence:** a user can complete the basic Drucker habit workflow after login without manually calling APIs.

## 6. Preserve prior habit evidence

- [x] 6.1 Add `scripts/import_sqlite.py`.
- [x] 6.2 Document Postgres setup and auth.
- [x] 6.3 Move accepted spec changes into current specs.

**Acceptance evidence:** an existing journal can be imported under a chosen account.

## 7. End-to-end acceptance

- [x] 7.1 New user signs up, logs in, creates a time entry, and sees only their own data.
- [x] 7.2 Another user cannot read the first user's records.
- [x] 7.3 A manager in a shared org can view a report dashboard.
- [x] 7.4 A non-manager gets `403` for the same dashboard.
- [x] 7.5 Alembic `upgrade head` from an empty database produces the expected schema.
