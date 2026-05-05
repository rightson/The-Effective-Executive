# The Effective Executive

An authenticated web service that turns Peter Drucker's five effective-executive habits into structured records, weekly review actions, and dashboard signals.

The product is opinionated from first principles: effectiveness is not a personality trait, but a trainable practice. Each module exists only when it helps a knowledge worker convert scarce time, uneven strengths, and consequential judgment into observable organizational results.

## Operating loop

The five modules form one Drucker operating loop:

**Time** records actual work and forces diagnosis: should this be done at all, can it be delegated, and does it waste other people's time. The output is a time inventory, elimination list, delegation list, stop-wasting-others list, and 90-minute work-block signal.

**Contributions** defines the outward result the user is accountable for. The output is not a job description; it is an observable commitment across direct results, values and standards, or talent development.

**Strengths** maps evidence-backed strengths for self and collaborators so work can be placed where performance is possible. Ordinary weaknesses are bounded by design; trust and integrity failures are not treated as style issues.

**Priorities** concentrates attention on a few matters using Drucker's tests: future over past, opportunity over problem, own direction over pressure, and high meaning over easy wins. The output includes posteriorities: what is abandoned or deferred.

**Decisions** turns judgment into action: problem type, boundary conditions, right answer before compromise, dissent, assignee, feedback mechanism, and outcome.

**Dashboard** exposes breaks in the loop and guides the weekly review. It is a diagnostic surface, not a productivity score.

## Specification discipline

Specs and change proposals must be written from first principles. A feature is not justified because another productivity tool has it, because it is technically convenient, or because it sounds useful. It is justified only when the document makes the necessity visible.

Every spec/change should answer:

- What Drucker habit or organizational result does this serve?
- What user behavior must change for the system to create value?
- What first-principles constraint makes the feature necessary, such as scarce time, observable contribution, strengths-based placement, concentration, or decision follow-through?
- What failure mode appears if the feature does not exist?
- What concrete record, workflow, or dashboard signal proves the habit is being practiced?
- What is intentionally out of scope so the product does not become a generic task manager?

Write requirements as causal product contracts: because a user needs X outcome under Y constraint, the system shall make Z behavior easy and verifiable.

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

By default the service writes to `effective_executive.db` (SQLite) in the working directory for local development. Set `DATABASE_URL` to use Postgres:

```
docker compose up -d                                # bundled Postgres on :5432
export DATABASE_URL=postgresql+psycopg://ee:ee@localhost:5432/effective_executive
python3 manage.py db upgrade head
python3 manage.py run
```

Schema changes are managed with Alembic. `manage.py db upgrade head` brings any database to the current schema; the baseline migration is equivalent to `Base.metadata.create_all`.

To preserve an existing `effective_executive.db` under a user account, sign up first, then:

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

## Accounts / coaching view

Every domain row is scoped to `user_id`. Two users in the same Postgres see entirely separate journals.

For bounded coaching visibility, populate the `orgs` and `org_memberships` tables. A user with `role = 'manager'` in an org can:

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

Designed to be the structured journal Drucker describes, not a team productivity platform. Accounts and manager views exist only to protect habit records and expose bounded coaching signals.
