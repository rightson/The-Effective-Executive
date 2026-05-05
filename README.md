# The Effective Executive

A local, single-user web service that turns Peter Drucker's five executive habits into structured records you can review.

The service is opinionated: each module enforces the diagnostic Drucker prescribes for that habit, rather than giving you a free-form notes app. If a field exists, the book says you should be filling it in.

## The five modules

Each maps to one of the habits in *The Effective Executive* (1967).

**Time** — log activities with duration. For every entry, answer the three diagnostic questions: is it worth doing at all, could someone else do it as well, does it waste other people's time. Analysis surfaces total minutes, breakdown by category, and how many minutes sit in **consolidated blocks** of 90+ minutes (Drucker's threshold for usable knowledge work).

**Contributions** — every planned activity records the **expected outward outcome** before it starts, classified into one of the three layers: direct results, values, or talent development. An activity without a writeable expected outcome should not be done.

**Strengths** — register strengths (your own and others') with evidence. Used to assign work to the shape of the person, not patch their weaknesses.

**Priorities** — each priority is scored on Drucker's four criteria: future-oriented, opportunity over problem, own direction, high meaning. The **would_start_today** field is the systematic-abandonment prompt: if the answer is no, mark it for abandonment.

**Decisions** — five-step decision record: problem type (generic vs. unique), boundary conditions, the right answer, the compromise, the assignee, the feedback mechanism, and a `has_dissent` flag (Drucker: a decision with no dissent is probably wrong).

A `/api/dashboard` endpoint rolls these into one view, including how many priorities are flagged for abandonment and how many decisions still have no implementer.

## Run

The fastest path uses the bundled `manage.py` helper, which provisions a venv and installs dependencies on first use:

```
python3 manage.py setup     # one-time: create .venv, install requirements
python3 manage.py run       # start on http://localhost:8000
python3 manage.py dev       # same, with auto-reload
```

Other helpers:

```
python3 manage.py db upgrade head                  # apply Alembic migrations
python3 manage.py db revision -m "msg" --autogenerate
python3 manage.py compose up -d                    # start the bundled Postgres
python3 manage.py import-sqlite path/to/old.db user@example.com
python3 manage.py shell                            # REPL inside the venv
python3 manage.py clean                            # remove the venv
```

Open http://localhost:8000 for the SPA (sign up on first visit) or http://localhost:8000/docs for the OpenAPI explorer.

## Database

By default the service writes to `effective_executive.db` (SQLite) in the working directory — fine for local single-user use. Set `DATABASE_URL` to use Postgres:

```
docker compose up -d                                # bundled Postgres on :5432
export DATABASE_URL=postgresql+psycopg://ee:ee@localhost:5432/effective_executive
python3 manage.py db upgrade head
python3 manage.py run
```

Schema changes are managed with Alembic. `manage.py db upgrade head` brings any database to the current schema; the baseline migration is equivalent to `Base.metadata.create_all`.

To migrate a legacy single-user `effective_executive.db` into a multi-user account, sign up first, then:

```
python3 manage.py import-sqlite ./effective_executive.db you@example.com
```

## Auth

Password auth (argon2) with session cookies. Sign-up is open; first user becomes the only user until you create others.

| Endpoint | Description |
|---|---|
| `POST /api/auth/signup` | Create account; returns user, sets session + CSRF cookies |
| `POST /api/auth/login` | Log in; sets session + CSRF cookies |
| `POST /api/auth/logout` | Clear session |
| `GET /api/auth/me` | Current user |

State-changing requests must echo the `ee_csrf` cookie back in the `X-CSRF-Token` header. The bundled SPA does this automatically.

## Multi-user / manager view

Every domain row is scoped to `user_id`. Two users in the same Postgres see entirely separate journals.

For team use, populate the `orgs` and `org_memberships` tables. A user with `role = 'manager'` in an org can:

- `GET /api/org/members` — list reports
- `GET /api/dashboard?user_id=<report_id>` — read-only dashboard for a report

No write endpoints accept a `user_id` override.

## API surface

| Resource | Endpoints |
|---|---|
| Auth | `POST /api/auth/signup\|login\|logout`, `GET /api/auth/me` |
| Time entries | `GET/POST/PUT/DELETE /api/time-entries`, `GET /api/time-entries/analysis` |
| Contributions | `GET/POST/PUT/DELETE /api/contributions` |
| Strengths | `GET/POST/PUT/DELETE /api/strengths` |
| Priorities | `GET/POST/PUT/DELETE /api/priorities` |
| Decisions | `GET/POST/PUT/DELETE /api/decisions` |
| Org | `GET /api/org/members` |
| Dashboard | `GET /api/dashboard[?user_id=<id>]` |

## Stack

FastAPI · SQLAlchemy 2.x · Alembic · SQLite or Postgres · argon2 · vanilla JS SPA in [static/](static/).

## Scope

Designed to be the structured journal Drucker describes — not a team productivity platform. The multi-user mode exists so a manager can see whether reports have undiagnosed time or unreviewed priorities, not to coordinate work.
