---
status: active
created: 2026-05-07
---

# Change: local dev defaults to Postgres with `.env` and `db init`

## Necessity

Local development currently defaults to SQLite (`sqlite:///./effective_executive.db`) while production uses Postgres. The platform spec already names Postgres as durable persistence and the repo ships a `docker-compose.yml` Postgres service, but every contributor still has to manually export `DATABASE_URL` and bootstrap a role/database.

Failure modes without this change:

- Schema and behavior drift between dev (SQLite) and prod (Postgres). Migrations or queries that pass on SQLite can fail on Postgres (different type coercion, constraint timing, JSON ops). Habit evidence is durable record per the platform spec; we cannot afford a divergent dev path.
- New contributors trip on Postgres bootstrap. Role/db creation requires a superuser connection, and that step is currently only triggered as a side-effect of `manage.py run` if `DATABASE_URL` is already set.
- Secrets and connection strings live as ad hoc shell exports — easy to lose, easy to leak into shell history.

## Behavior change

1. `.env.example` (committed) holds the default local dev `DATABASE_URL` pointing at the docker-compose Postgres (`postgresql://ee:ee@localhost:5432/effective_executive`) plus other env knobs.
2. `.env` (gitignored) is the active local config. `manage.py db init` copies `.env.example` to `.env` if missing.
3. `manage.py db init` is the canonical first-run command:
   - Loads `.env` into the process environment.
   - If `DATABASE_URL` is Postgres, tries to connect directly. If that fails because the role or database is missing, asks interactively for an admin connection URL (`postgresql://postgres@localhost:5432/postgres` or similar), creates the role and database, then retries.
   - Runs `alembic upgrade head`.
4. `manage.py run` / `dev` / `db <alembic-args>` all load `.env` first, so contributors do not need to `export DATABASE_URL` by hand.
5. Default `DATABASE_URL` (when neither env var nor `.env` is present) flips from SQLite to the Postgres URL above. SQLite remains supported only for explicitly running with `DATABASE_URL=sqlite:///...` and for the `import-sqlite` import path of legacy data.
6. The admin URL is **only used in memory** during `db init` and is not written to `.env`.

## Out of scope

- Switching the production deploy story; this change is local-dev-only.
- Removing the SQLite code path. `effective_executive.db` and `manage.py import-sqlite` continue to work because legacy data still lives in SQLite files.
- Secret management beyond `.env`. No vault, no encryption.

## Spec delta

See [specs/platform/spec.md](specs/platform/spec.md) for the delta to apply on accept.
