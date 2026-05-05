# Tasks

Ordered. Each item is independently shippable behind a feature flag where noted.

## 1. Infrastructure
- [x] 1.1 Add Postgres dependency (`psycopg[binary]`) to `requirements.txt`.
- [x] 1.2 Replace `DATABASE_URL` with env var; default to local Postgres, fall back to SQLite for dev.
- [x] 1.3 Add Alembic; generate baseline migration matching today's schema.
- [x] 1.4 Provide `docker-compose.yml` with Postgres 16 for local dev.

## 2. Accounts capability
- [x] 2.1 Create `users`, `sessions`, `orgs`, `org_memberships` tables (migration).
- [x] 2.2 Add `argon2-cffi` and password hashing helpers.
- [x] 2.3 `POST /api/auth/signup`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`.
- [x] 2.4 Session cookie middleware; `current_user` FastAPI dependency.
- [x] 2.5 CSRF double-submit token for state-changing routes.

## 3. Scope existing data to users
- [x] 3.1 Add `user_id` (NOT NULL, indexed) FK to `time_entries`, `contributions`, `strengths`, `priorities`, `decisions`. Migration backfills to a designated "legacy" user when a SQLite import has been run; otherwise the column is added on an empty DB.
- [x] 3.2 Update every list/get/update/delete query to filter by `current_user.id`.
- [x] 3.3 Update create endpoints to set `user_id = current_user.id`.
- [x] 3.4 Update `GET /api/dashboard` and `GET /api/time-entries/analysis` to scope.

## 4. Manager view
- [x] 4.1 `GET /api/org/members` lists members of orgs the user manages.
- [x] 4.2 `GET /api/dashboard?user_id=<id>` allowed iff caller is a manager in a shared org. Returns the same shape as the self dashboard.
- [x] 4.3 No write endpoints get a `?user_id` override.

## 5. UI
- [x] 5.1 Add `/login` and `/signup` pages to the SPA.
- [x] 5.2 Auth guard on the SPA; redirect to `/login` on 401.
- [x] 5.3 Manager picker on the dashboard (visible only when `org/members` returns >0).

## 6. Migration & docs
- [x] 6.1 `scripts/import_sqlite.py` — import an existing `effective_executive.db` under a chosen account.
- [x] 6.2 Update `README.md` to document Postgres setup and auth.
- [x] 6.3 Move spec deltas in `docs/changes/multi-user-time-management/specs/` into `docs/specs/` on accept.

## 7. Acceptance
- [x] 7.1 New user signs up, logs in, creates a time entry, sees only their own data.
- [x] 7.2 A second user in the same org cannot read user 1's entries via API.
- [x] 7.3 A manager in the same org can `GET /api/dashboard?user_id=<report>` and gets the report's rollup; a non-manager gets `403`.
- [x] 7.4 Alembic `upgrade head` from an empty database produces the same schema as `Base.metadata.create_all`.
